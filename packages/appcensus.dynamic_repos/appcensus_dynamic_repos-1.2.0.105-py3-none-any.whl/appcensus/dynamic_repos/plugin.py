import logging
from typing import List
from typing import Type

from cleo.io.io import IO
from poetry.config.source import Source
from poetry.console.application import Application
from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from poetry.repositories.repository_pool import RepositoryPool
from poetry.utils.password_manager import PasswordManager
from poetry.utils.source import source_to_table
from tomlkit.items import AoT

from appcensus.dynamic_repos import REPO_FILE_PATH
from appcensus.dynamic_repos.auth import CredentialCache
from appcensus.dynamic_repos.auth import CredentialManager
from appcensus.dynamic_repos.commands import RepoClearCredentials
from appcensus.dynamic_repos.commands import RepoDisableCommand
from appcensus.dynamic_repos.commands import RepoEnableCommand
from appcensus.dynamic_repos.commands import RepoSetAuth
from appcensus.dynamic_repos.commands import RepoShowCommand
from appcensus.dynamic_repos.commands import RepoShowCredentials
from appcensus.dynamic_repos.commands import RepoUseCommand
from appcensus.dynamic_repos.models import Repo
from appcensus.dynamic_repos.models import RepoManager
from appcensus.dynamic_repos.repo_collector import RepoCollector
from appcensus.dynamic_repos.source_manager import SourceManager

logger = logging.getLogger(__name__)


class DynamicRepos(Plugin):
    def _new_source(self, repo: Repo) -> Source:
        if repo.priority:
            return Source(
                name=repo.name,
                url=repo.url,
                default=repo.default,
                secondary=repo.secondary,
                priority=repo.priority,
            )
        return Source(name=repo.name, url=repo.url, default=repo.default, secondary=repo.secondary)

    def _check_source(self, existing_sources: List[Source], new_source: Source) -> bool:
        if new_source.default and new_source.secondary:  # type: ignore[attr-defined]
            raise ValueError(f"Repo {new_source.name} cannot be default and secondary - pick one")

        for source in existing_sources:
            if source == new_source:
                raise ValueError(
                    f"Identical source <c1>{new_source.name}</> already exists. Perhaps you have a declaration in"
                    " pyproject.toml. You should resolve the redundancy to prevent conflict."
                )

            if source.name == new_source.name:
                raise ValueError(
                    f"Inconsistent source with name <c1>{new_source.name}</c1> already exists."
                    " Please reconile this."
                )

            if source.default and new_source.default:  # type: ignore[attr-defined]
                raise ValueError(
                    f"Source with name <c1>{source.name}</c1> is already set to default."
                    f" Only one default source can be configured at a time. <c1>{new_source.name}</c1>"
                    " will be rejected."
                )
        return True

    def _configure_sources(self, poetry: Poetry, io: IO) -> None:
        logger.debug("Configuring sources ...")

        existing_sources = RepoCollector(poetry.pool).repositories()

        logger.debug(f"Beginning with {len(existing_sources)} existing sources")
        for source in existing_sources:
            logger.debug(f"- {source}")

        new_sources = AoT([source_to_table(source) for source in existing_sources])

        for name in RepoManager.entries():
            logger.debug(f"repo {name}")
            repo = RepoManager.get(name)
            if repo.enabled:
                try:
                    new_source = self._new_source(repo)
                    if self._check_source(existing_sources, new_source):
                        if repo.auth:
                            try:
                                pm = PasswordManager(poetry.config)
                                CredentialManager.authorize(pm, repo)
                            finally:
                                CredentialCache.save()
                        logger.debug(f"Adding {new_source.name}")
                        new_sources.append(source_to_table(new_source))
                except Exception as e:
                    self._exceptional_error(io, e)
                    return

        # configure new sources
        logger.debug(f"Configuring {len(new_sources)} sources ...")
        poetry._pool = RepositoryPool()
        SourceManager().add_sources(poetry, new_sources, io)

    def _exceptional_error(self, io: IO, e: Exception) -> None:
        logger.error(e, exc_info=True)
        io.write_error_line(f"DynamicRepos: <error>{e}</error>")

    def activate(self, poetry: Poetry, io: IO) -> None:
        logger.debug("Activating appcensus.dynamic_repos")
        if not REPO_FILE_PATH.exists():
            return
        self._configure_sources(poetry, io)


class DynamicReposApplication(ApplicationPlugin):
    @property
    def commands(self) -> List[Type[Command]]:
        return [
            RepoShowCommand,
            RepoEnableCommand,
            RepoDisableCommand,
            RepoSetAuth,
            RepoShowCredentials,
            RepoClearCredentials,
            RepoUseCommand,
        ]

    def activate(self, application: Application) -> None:
        for command in self.commands:
            assert command.name
            application.command_loader.register_factory(command.name, command)
