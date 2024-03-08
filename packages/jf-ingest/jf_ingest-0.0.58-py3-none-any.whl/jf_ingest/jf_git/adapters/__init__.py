import fnmatch
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

import pytz

from jf_ingest import diagnostics, logging_helper
from jf_ingest.config import GitConfig, GitProvider
from jf_ingest.jf_git.clients.github import GithubClient
from jf_ingest.jf_git.exceptions import GitProviderUnavailable
from jf_ingest.utils import retry_session

logger = logging.getLogger(__name__)

'''

    Constants

'''
# NOTE: ONLY GITHUB IS CURRENTLY SUPPORTED!!!!
BBS_PROVIDER = 'bitbucket_server'
BBC_PROVIDER = 'bitbucket_cloud'
GH_PROVIDER = 'github'
GL_PROVIDER = 'gitlab'
PROVIDERS = [GL_PROVIDER, GH_PROVIDER, BBS_PROVIDER, BBC_PROVIDER]

'''

    Standardized Structure

'''


@dataclass
class StandardizedUser:
    id: str
    name: str
    login: str
    email: str = None
    url: str = None
    account_id: str = None


@dataclass
class StandardizedBranch:
    name: str
    sha: str


@dataclass
class StandardizedOrganization:
    id: str
    name: str
    login: str
    url: str


@dataclass
class StandardizedShortRepository:
    id: int
    name: str
    url: str


@dataclass
class StandardizedRepository:
    id: int
    name: str
    full_name: str
    url: str
    is_fork: bool
    default_branch_name: str
    organization: StandardizedOrganization
    branches: List[StandardizedBranch]

    def short(self):
        # return the short form of Standardized Repository
        return StandardizedShortRepository(id=self.id, name=self.name, url=self.url)


@dataclass
class StandardizedCommit:
    hash: str
    url: str
    message: str
    commit_date: str
    author_date: str
    author: StandardizedUser
    repo: StandardizedShortRepository
    is_merge: bool
    branch_name: str = None


@dataclass
class StandardizedPullRequestComment:
    user: StandardizedUser
    body: str
    created_at: str
    system_generated: bool = None


@dataclass
class StandardizedPullRequestReview:
    user: StandardizedUser
    foreign_id: int
    review_state: str


@dataclass
class StandardizedPullRequest:
    id: any
    additions: int
    deletions: int
    changed_files: int
    is_closed: bool
    is_merged: bool
    created_at: str
    updated_at: str
    merge_date: str
    closed_date: str
    title: str
    body: str
    url: str
    base_branch: str
    head_branch: str
    author: StandardizedUser
    merged_by: StandardizedUser
    commits: List[StandardizedCommit]
    merge_commit: StandardizedCommit
    comments: List[StandardizedPullRequestComment]
    approvals: List[StandardizedPullRequestReview]
    base_repo: StandardizedShortRepository
    head_repo: StandardizedShortRepository


class GitAdapter(ABC):
    @staticmethod
    def get_git_adapter(config: GitConfig, hide_progress_bar: bool = False):
        """Static function for generating a GitAdapter from a provided GitConfig object

        Args:
            config (GitConfig): A git configuration data object. The specific GitAdapter
                is returned based on the git_provider field in this object
            hide_progress_bar (bool, optional): If provided, TQDM progress bars will be disabled.
                This is useful for our validation use case in the Agent, which requires a pretty clean output console. Defaults to False.

        Raises:
            GitProviderUnavailable: If the supplied git config has an unknown git provider, this error will be thrown

        Returns:
            GitAdapter: A specific subclass of the GitAdapter, based on what git_provider we need
        """
        from jf_ingest.jf_git.adapters.github import GithubAdapter

        if config.git_provider == GitProvider.GITHUB:
            return GithubAdapter(config, hide_progress_bar=hide_progress_bar)
        else:
            raise GitProviderUnavailable(
                f'Git provider {config.git_provider} is not currently supported'
            )

    @abstractmethod
    def get_api_scopes(self) -> str:
        """Return the list of API Scopes. This is useful for Validation

        Returns:
            str: A string of API scopes we have, given the adapters credentials
        """
        pass

    @abstractmethod
    def get_organizations(self) -> List[StandardizedOrganization]:
        """Get the list of organizations the adapter has access to

        Returns:
            List[StandardizedOrganization]: A list of standardized organizations within this Git Instance
        """
        pass

    @abstractmethod
    def get_users(self, standardized_org: StandardizedOrganization) -> List[StandardizedUser]:
        """Get the list of users in a given Git Organization

        Args:
            standardized_org (StandardizedOrganization): A standardized Git Organization Object

        Returns:
            List[StandardizedUser]: A standardized User Object
        """
        pass

    @abstractmethod
    def get_repos(self, standardized_org: StandardizedOrganization) -> List[StandardizedRepository]:
        """Get a list of standardized repositories within a given organization

        Args:
            standardized_org (StandardizedOrganization): A standardized organization

        Returns:
            List[StandardizedRepository]: A list of standardized Repositories
        """
        pass

    @abstractmethod
    def get_commits_for_included_branches(
        self,
        standardized_repo: StandardizedRepository,
    ) -> List[StandardizedCommit]:
        """For a given repo, get all the commits that are on the included branches.
        Included branches are found by crawling across the branches pulled/available
        from get_branches_for_standardized_repo

        Args:
            standardized_repo (StandardizedRepository): A standard Repository object

        Returns:
            List[StandardizedCommit]: A list of standardized commits
        """
        pass

    @abstractmethod
    def get_commits_for_default_branch(
        self,
        standardized_repo: StandardizedRepository,
    ) -> List[StandardizedCommit]:
        """Get a list of commits for the default branch

        Args:
            standardized_repo (StandardizedRepository): A standardized repository object

        Returns:
            List[StandardizedCommit]: A list of standardized commits
        """
        pass

    @abstractmethod
    def get_prs(
        self, standardized_repo: StandardizedRepository, limit: int = None
    ) -> List[StandardizedPullRequest]:
        """Get the list of standardized Pull Requests for a Standardized Repository.

        Args:
            standardized_repo (StandardizedRepository): A standardized repository
            limit (int, optional): When provided, the number of repos returned is limited.
                Useful for the validation use case, where we want to just verify we can pull PRs.
                Defaults to None.

        Returns:
            List[StandardizedPullRequest]: A list of standardized PRs
        """
        pass

    def get_branches_for_standardized_repo(self, repo: StandardizedRepository) -> set[str]:
        """Return branches for which we should pull commits, specified by customer in git config.
            The repo's default branch will always be included in the returned list.

        Args:
            repo (StandardizedRepository): A standardized repository

        Returns:
            set[str]: A set of branch names (as strings)
        """

        # Helper function
        def get_matching_branches(
            included_branch_patterns: List[str], repo_branch_names: List[str]
        ) -> List[str]:
            # Given a list of patterns, either literal branch names or names with wildcards (*) meant to match a set of branches in a repo,
            # return the list of branches from repo_branches that match any of the branch name patterns.
            # fnmatch is used over regex to support wildcards but avoid complicating the requirements on branch naming in a user's config.
            matching_branches = []
            for repo_branch_name in repo_branch_names:
                if any(
                    fnmatch.fnmatch(repo_branch_name, pattern)
                    for pattern in included_branch_patterns
                ):
                    matching_branches.append(repo_branch_name)
            return matching_branches

        branches_to_process = [repo.default_branch_name] if repo.default_branch_name else []
        additional_branches_for_repo = self.config.included_branches_by_repo.get(repo.name)
        if additional_branches_for_repo:
            repo_branch_names = [b.name for b in repo.branches if b]
            branches_to_process.extend(
                get_matching_branches(additional_branches_for_repo, repo_branch_names)
            )
        return set(branches_to_process)

    def load_and_dump_git(self):
        # TODO: write this shared function for all git adapters
        pass
