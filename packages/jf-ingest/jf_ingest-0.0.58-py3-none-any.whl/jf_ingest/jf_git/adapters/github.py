import logging
import traceback
from datetime import datetime, timezone
from typing import Generator, List

from dateutil import parser
from tqdm import tqdm

from jf_ingest import diagnostics, logging_helper
from jf_ingest.config import GitConfig
from jf_ingest.jf_git.adapters import (
    GitAdapter,
    StandardizedBranch,
    StandardizedCommit,
    StandardizedOrganization,
    StandardizedPullRequest,
    StandardizedPullRequestComment,
    StandardizedPullRequestReview,
    StandardizedRepository,
    StandardizedShortRepository,
    StandardizedUser,
)
from jf_ingest.jf_git.clients.github import GithubClient
from jf_ingest.name_redactor import NameRedactor, sanitize_text

logger = logging.getLogger(__name__)

'''

    Data Fetching

'''

_branch_redactor = NameRedactor(preserve_names=['master', 'develop'])
_organization_redactor = NameRedactor()
_repo_redactor = NameRedactor()


class GithubAdapter(GitAdapter):
    def __init__(self, config: GitConfig, hide_progress_bar: bool = False):
        self.config = config
        self.client = GithubClient(config.git_auth_config)

        self.repo_id_to_name_lookup: dict = {}
        self.repo_to_branch_is_quiescent_lookups: dict = {}
        self.repo_has_quiescent_prs_lookup: dict = {}

        # Optionally hide TQDM progress bar (useful during validation)
        self.hide_progress_bar = hide_progress_bar

    def get_api_scopes(self):
        return self.client.get_scopes_of_api_token()

    @diagnostics.capture_timing()
    @logging_helper.log_entry_exit(logger)
    def get_organizations(self) -> List[StandardizedOrganization]:
        logger.debug('downloading github organizations...')
        organizations = []

        # NOTE: For github, organization equates to a Github organization here!
        for organization_id in self.config.git_organizations:
            organization = self.client.get_organization_by_login(organization_id)

            if organization is None:  # skip organizations that errored out when fetching data
                continue

            organizations.append(
                _standardize_organization(
                    organization,
                    self.config.git_redact_names_and_urls,
                )
            )
        logger.debug('Done downloading organizations!')

        if not organizations:
            raise ValueError(
                'No organizations found.  Make sure your token has appropriate access to Github.'
            )
        return organizations

    @diagnostics.capture_timing()
    @logging_helper.log_entry_exit(logger)
    def get_users(
        self, standardized_organization: StandardizedOrganization
    ) -> List[StandardizedUser]:
        logger.debug('downloading github users... ')
        users = [
            _standardize_user(user)
            for user in self.client.get_users(standardized_organization.login)
        ]
        logger.debug('Done downloading users!')
        return users

    @diagnostics.capture_timing()
    @logging_helper.log_entry_exit(logger)
    def get_repos(
        self,
        standardized_organization: StandardizedOrganization,
    ) -> List[StandardizedRepository]:
        logger.debug('downloading github repos...')

        standardized_repos: List[StandardizedRepository] = []

        filters = []
        if self.config.excluded_repos:
            filters.append(
                lambda r: r['name'].lower() in set([r.lower() for r in self.config.included_repos])
            )
        if self.config.excluded_repos:
            filters.append(
                lambda r: r['name'].lower()
                not in set([r.lower() for r in self.config.excluded_repos])
            )

        for api_repo in tqdm(
            self.client.get_repos(standardized_organization.login, repo_filters=filters),
            desc=f'downloading repos for {standardized_organization.login}',
            unit='repos',
            disable=self.hide_progress_bar,
        ):
            # Enter the repo to the ID to Name look up, incase the repo name gets
            # scrubbed by our git_redact_names_and_urls logic
            repo_id = api_repo['id']
            self.repo_id_to_name_lookup[repo_id] = api_repo['name']

            # Mark if the default branch in this repo is quiescent, to save on API calls later
            # Initiate branch lookup table
            self.repo_to_branch_is_quiescent_lookups[repo_id] = {}
            default_branch = api_repo.get('defaultBranch')
            if default_branch:
                commits = (default_branch['target']['mostRecentCommits'] or {}).get('commits', [])
                if commits:
                    # Translate data from API
                    most_recent_commit = commits[0]
                    most_recent_commit_date: datetime = GithubClient.github_gql_format_to_datetime(
                        most_recent_commit['committedDate']
                    )
                    # Get our internal 'pull_from' value
                    pull_since_for_commits = self.config.get_pull_from_for_commits(
                        org_login=standardized_organization.login, repo_id=repo_id
                    )

                    # Mark if we can skip pulling this branch or not
                    self.repo_to_branch_is_quiescent_lookups[repo_id][default_branch['name']] = (
                        pull_since_for_commits >= most_recent_commit_date
                    )
                else:
                    # If there are no commits, there is nothing to pull
                    # Mark as quiescent
                    self.repo_to_branch_is_quiescent_lookups[repo_id][default_branch['name']] = True

            # Mark the latest date for PRs in this repo, to save on API calls later
            prs = api_repo['prQuery'].get('prs', [])
            if prs:
                # Translate latest PR detected from API
                latest_pr_update = GithubClient.github_gql_format_to_datetime(prs[0]['updatedAt'])
                # Get our own pull since value
                pull_since_for_prs = self.config.get_pull_from_for_prs(
                    org_login=standardized_organization.login, repo_id=repo_id
                )

                # Mark if we can skip this PR or not
                self.repo_has_quiescent_prs_lookup[repo_id] = pull_since_for_prs >= latest_pr_update
            else:
                self.repo_has_quiescent_prs_lookup[repo_id] = True

            standardized_repos.append(
                _standardize_repo(
                    api_repo, standardized_organization, self.config.git_redact_names_and_urls
                )
            )

        logger.debug('Done downloading repos!')
        if not standardized_repos:
            raise ValueError(
                'No repos found. Make sure your token has appropriate access to Github and check your configuration of repos to pull.'
            )
        return standardized_repos

    @diagnostics.capture_timing()
    @logging_helper.log_entry_exit(logger)
    def get_commits_for_included_branches(
        self,
        standardized_repo: StandardizedRepository,
    ) -> Generator[StandardizedCommit, None, None]:
        logger.debug('downloading github commits on included branches...')
        with logging_helper.log_loop_iters('repo for branch commits', i, 1):
            pull_since = self.config.get_pull_from_for_commits(
                org_login=standardized_repo.organization.login, repo_id=standardized_repo.id
            )

            for branch_name in self.get_branches_for_standardized_repo(standardized_repo):
                if self.repo_to_branch_is_quiescent_lookups[standardized_repo.id].get(
                    branch_name, False
                ):
                    continue
                try:
                    for j, api_commit in enumerate(
                        tqdm(
                            self.client.get_commits(
                                login=standardized_repo.organization.login,
                                repo_name=self.repo_id_to_name_lookup[standardized_repo.id],
                                branch_name=branch_name,
                                since=pull_since,
                            ),
                            desc=f'downloading commits for branch {branch_name} in repo {standardized_repo.name} ({standardized_repo.organization.login})',
                            unit='commits',
                            disable=self.hide_progress_bar,
                        ),
                        start=1,
                    ):
                        with logging_helper.log_loop_iters('branch commit inside repo', j, 100):
                            yield _standardize_commit(
                                api_commit,
                                standardized_repo,
                                branch_name,
                                self.config.git_strip_text_content,
                                self.config.git_redact_names_and_urls,
                            )

                except Exception as e:
                    logger.debug(traceback.format_exc())
                    logger.warning(
                        f':WARN: Got exception for branch {branch_name}: {e}. Skipping...'
                    )
        logger.debug('Done downloading commits for included branches!')

    def get_commits_for_default_branch(
        self, standardized_repo: StandardizedRepository, limit: int = None
    ) -> Generator[StandardizedCommit, None, None]:
        try:
            pull_since = self.config.get_pull_from_for_commits(
                org_login=standardized_repo.organization.login, repo_id=standardized_repo.id
            )
            for j, api_commit in enumerate(
                tqdm(
                    self.client.get_commits(
                        login=standardized_repo.organization.login,
                        repo_name=self.repo_id_to_name_lookup[standardized_repo.id],
                        branch_name=standardized_repo.default_branch_name,
                        since=pull_since,
                    ),
                    desc=f'downloading commits for branch {standardized_repo.default_branch_name} in repo {standardized_repo.name} ({standardized_repo.organization.login})',
                    unit='commits',
                    disable=self.hide_progress_bar,
                ),
                start=1,
            ):
                with logging_helper.log_loop_iters('branch commit inside repo', j, 100):
                    yield _standardize_commit(
                        api_commit,
                        standardized_repo,
                        standardized_repo.default_branch_name,
                        self.config.git_strip_text_content,
                        self.config.git_redact_names_and_urls,
                    )
                    if limit and j > limit:
                        return

        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.warning(
                f':WARN: Got exception for branch {standardized_repo.default_branch_name}: {e}. Skipping...'
            )

    @diagnostics.capture_timing()
    @logging_helper.log_entry_exit(logger)
    def get_prs(
        self, standardized_repo: StandardizedRepository, limit: int = None
    ) -> List[StandardizedPullRequest]:
        logger.debug('downloading github prs...')

        standardized_prs = []
        try:
            # Check if we flagged this repo as quiescent
            if self.repo_has_quiescent_prs_lookup[standardized_repo.id]:
                return []

            pull_since = self.config.get_pull_from_for_prs(
                standardized_repo.organization.login, standardized_repo.id
            )

            api_prs = self.client.get_prs(
                login=standardized_repo.organization.login,
                repo_name=self.repo_id_to_name_lookup[standardized_repo.id],
                include_top_level_comments=self.config.jf_options.get(
                    'get_all_issue_comments', False
                ),
            )

            for j, api_pr in enumerate(
                tqdm(
                    api_prs,
                    desc=f'processing prs for {standardized_repo.name} ({standardized_repo.id})',
                    unit='prs',
                    disable=self.hide_progress_bar,
                ),
                start=1,
            ):
                with logging_helper.log_loop_iters('pr inside repo', j, 10):
                    try:
                        updated_at = parser.parse(api_pr['updatedAt'])

                        # PRs are ordered newest to oldest
                        # if this is too old, we're done with this repo.
                        # This is an INCLUSIVE check, to stop us from grabbing
                        # the last PR that is our marker for pull_since!
                        if pull_since and pull_since >= updated_at:
                            break

                        standardized_prs.append(
                            _standardize_pr(
                                api_pr,
                                standardized_repo,
                                self.config.git_strip_text_content,
                                self.config.git_redact_names_and_urls,
                            )
                        )
                        if limit and j > limit:
                            return standardized_prs
                    except Exception as e:
                        # if something goes wrong with normalizing one of the prs - don't stop pulling. try
                        # the next one.
                        pr_id = f' {api_pr["id"]}' if api_pr else ''
                        logger.warning(
                            f'normalizing PR {pr_id} from repo {standardized_repo.name} ({standardized_repo.id}). Skipping...'
                        )
                        logger.debug(traceback.format_exc())

        except Exception as e:
            # if something happens when pulling PRs for a repo, just keep going.
            logger.warning(
                f'normalizing PR {pr_id} from repo {standardized_repo.name} ({standardized_repo.id}). Skipping...'
            )
            logger.debug(traceback.format_exc())

        logger.debug('Done downloading github PRs!')
        return standardized_prs


'''

    Massage Functions

'''


def _standardize_user(api_user) -> StandardizedUser:
    if not api_user:
        return None

    id = api_user.get('id')
    name = api_user.get('name')
    login = api_user.get('login')
    email = api_user.get('email')
    # raw user, just have email (e.g. from a commit)
    if not id:
        return StandardizedUser(
            id=email,
            login=email,
            name=name,
            email=email,
        )

    # API user, where github matched to a known account
    return StandardizedUser(id=id, login=login, name=name, email=email)


def _standardize_organization(
    api_org: dict, redact_names_and_urls: bool
) -> StandardizedOrganization:
    return StandardizedOrganization(
        id=api_org['id'],
        login=api_org['login'],
        name=api_org.get('name')
        if not redact_names_and_urls
        else _organization_redactor.redact_name(api_org.get('name')),
        url=api_org['url'] if not redact_names_and_urls else None,
    )


def _standardize_branch(api_branch, redact_names_and_urls: bool) -> StandardizedBranch:
    return StandardizedBranch(
        name=api_branch['name']
        if not redact_names_and_urls
        else _branch_redactor.redact_name(api_branch['name']),
        sha=api_branch['target']['sha'],
    )


def _standardize_repo(
    api_repo,
    standardized_organization: StandardizedOrganization,
    redact_names_and_urls: bool,
) -> StandardizedRepository:
    repo_name = (
        api_repo['name']
        if not redact_names_and_urls
        else _repo_redactor.redact_name(api_repo['name'])
    )
    url = api_repo['url'] if not redact_names_and_urls else None

    standardized_branches = [
        _standardize_branch(branch, redact_names_and_urls) for branch in api_repo['branches']
    ]

    # If a repsotiroy is completely empty, than there will be no default branch
    # this can mess with our ingestion due to the 'name' field being nested
    # on a None object
    default_branch_name = api_repo['defaultBranch']['name'] if api_repo['defaultBranch'] else None
    return StandardizedRepository(
        id=api_repo['id'],
        name=repo_name,
        full_name=repo_name,
        url=url,
        default_branch_name=default_branch_name,
        is_fork=api_repo['isFork'],
        branches=standardized_branches,
        organization=standardized_organization,
    )


def _standardize_short_form_repo(
    api_repo: dict, redact_names_and_urls: dict
) -> StandardizedShortRepository:
    repo_name = (
        api_repo['name']
        if not redact_names_and_urls
        else _repo_redactor.redact_name(api_repo['name'])
    )
    url = api_repo['url'] if not redact_names_and_urls else None

    return StandardizedShortRepository(id=api_repo['id'], name=repo_name, url=url)


def _standardize_commit(
    api_commit: dict,
    standardized_repo: StandardizedRepository,
    branch_name: str,
    strip_text_content: bool,
    redact_names_and_urls: bool,
):
    author = _standardize_user(api_commit['author'])
    commit_url = api_commit['url'] if not redact_names_and_urls else None
    return StandardizedCommit(
        hash=api_commit['sha'],
        author=author,
        url=commit_url,
        commit_date=api_commit['committedDate'],
        author_date=api_commit['authoredDate'],
        message=sanitize_text(api_commit['message'], strip_text_content),
        is_merge=api_commit['parents']['totalCount'] > 1,
        repo=standardized_repo.short(),  # use short form of repo
        branch_name=branch_name
        if not redact_names_and_urls
        else _branch_redactor.redact_name(branch_name),
    )


def _get_standardized_pr_comments(
    api_comments: list[dict], strip_text_content
) -> List[StandardizedPullRequestComment]:
    return [
        StandardizedPullRequestComment(
            user=_standardize_user(api_comment['author']),
            body=sanitize_text(api_comment['body'], strip_text_content),
            created_at=api_comment['createdAt'],
        )
        for api_comment in api_comments
    ]


def _get_standardized_reviews(api_reviews: list[dict]):
    return [
        StandardizedPullRequestReview(
            user=_standardize_user(api_review['author']),
            foreign_id=api_review['id'],
            review_state=api_review['state'],
        )
        for api_review in api_reviews
    ]


def _standardize_pr(
    api_pr,
    standardized_repo: StandardizedRepository,
    strip_text_content: bool,
    redact_names_and_urls: bool,
):
    base_branch_name = api_pr['baseRefName']
    head_branch_name = api_pr['headRefName']
    standardized_merge_commit = (
        _standardize_commit(
            api_pr['mergeCommit'],
            standardized_repo=standardized_repo,
            branch_name=base_branch_name,
            strip_text_content=strip_text_content,
            redact_names_and_urls=redact_names_and_urls,
        )
        if api_pr['mergeCommit']
        else None
    )
    return StandardizedPullRequest(
        id=api_pr['id'],
        additions=api_pr['additions'],
        deletions=api_pr['deletions'],
        changed_files=api_pr['changedFiles'],
        created_at=api_pr['createdAt'],
        updated_at=api_pr['updatedAt'],
        merge_date=api_pr['mergedAt'],
        closed_date=api_pr['closedAt'],
        is_closed=api_pr['state'].lower() == 'closed',
        is_merged=api_pr['merged'],
        # redacted fields
        url=api_pr['url'] if not redact_names_and_urls else None,
        base_branch=(
            base_branch_name
            if not redact_names_and_urls
            else _branch_redactor.redact_name(base_branch_name)
        ),
        head_branch=(
            head_branch_name
            if not redact_names_and_urls
            else _branch_redactor.redact_name(head_branch_name)
        ),
        # sanitized fields
        title=sanitize_text(api_pr['title'], strip_text_content),
        body=sanitize_text(api_pr['body'], strip_text_content),
        # standardized fields
        commits=[
            _standardize_commit(
                api_commit=commit,
                standardized_repo=standardized_repo,
                branch_name=base_branch_name,
                strip_text_content=strip_text_content,
                redact_names_and_urls=redact_names_and_urls,
            )
            for commit in api_pr['commits']
        ],
        merge_commit=standardized_merge_commit,
        author=_standardize_user(api_user=api_pr['author']),
        merged_by=_standardize_user(api_user=api_pr['mergedBy']),
        approvals=_get_standardized_reviews(api_pr['reviews']),
        comments=_get_standardized_pr_comments(api_pr['comments'], strip_text_content),
        base_repo=_standardize_short_form_repo(api_pr['baseRepository'], redact_names_and_urls),
        head_repo=_standardize_short_form_repo(api_pr['baseRepository'], redact_names_and_urls),
    )
