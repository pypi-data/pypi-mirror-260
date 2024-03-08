import logging
from pathlib import Path
from typing import cast
from typing import List
from typing import Optional
from typing import Union

import tomlkit
from cleo.helpers import argument
from cleo.ui.table_cell import TableCell
from cleo.ui.table_separator import TableSeparator
from poetry.config.source import Source
from poetry.console.commands.command import Command
from poetry.utils.password_manager import PasswordManager
from tomlkit.items import Table
from tomlkit.toml_document import TOMLDocument

from appcensus.dynamic_repos import REPO_FILE_PATH
from appcensus.dynamic_repos.auth import CredentialCache
from appcensus.dynamic_repos.auth import CredentialManager
from appcensus.dynamic_repos.models import BasicRepoCredentials
from appcensus.dynamic_repos.models import RepoManager
from appcensus.dynamic_repos.repo_collector import RepoCollector

logger = logging.getLogger(__name__)


class RepoShowCommand(Command):
    name = "acrepo show"
    description = "Show the configuration of active dynamic repos"

    # Repo prioritization has shifted between using a combination of definition order, and two flags to
    # an clearer definition of enumerated priorities. We detect what is in play and adjust accordingly.
    def _use_flags(self, repo: Source) -> bool:
        return hasattr(repo, "default") and hasattr(repo, "secondary")

    def _flags2prio(self, repo: Source) -> str:
        if repo.default:  # type: ignore[attr-defined]
            return "default"
        elif repo.secondary:  # type: ignore[attr-defined]
            return "secondary"
        return "normal"

    def handle(self) -> int:
        try:
            for repo in RepoCollector(self.poetry.pool).repositories():
                creds = CredentialCache.get(repo.name)
                table = self.table(style="compact")
                active_state = f" : <c1>{'yes' if creds and creds.valid() else 'no'}</>"
                if creds:
                    active_state += (
                        f" expires <c1>{creds.expires.isoformat() if creds.expires else 'never'}</>"
                    )
                rows: List[Union[List[Union[str, TableCell]], TableSeparator]] = [
                    [
                        "<info>name</>",
                        f" : <c1>{repo.name}</>",
                    ],
                    ["<info>priority</>", f" : {self._flags2prio(repo)}"]
                    if self._use_flags(repo)
                    else ["<info>priority</>", f" : {repo.priority.name.lower()}"],
                    ["<info>url</>", f" : {repo.url}"],
                    ["<info>active auth</info>", active_state]
                    if creds and creds.valid()
                    else ["<info>auth</info>", " : <c1>no</c1>"],
                    ["", ""],
                ]
                table.add_rows(rows)
                table.render()
            return 0
        except Exception as e:
            self.line(f"[DynamicRepos#RepoShowCommand]: <error>{e}</>")
            return -1

    @classmethod
    def create(cls) -> "RepoShowCommand":
        return RepoShowCommand()


class RepoSetEnableCommand(Command):
    arguments = [argument("name", "Repository name")]

    def _handle(self, enable: bool) -> int:
        name = self.argument("name")

        try:
            doc: Optional[TOMLDocument] = None
            file_path: Path = REPO_FILE_PATH
            if file_path.exists():
                with file_path.open("r") as fh:
                    doc = tomlkit.parse(fh.read())
                    if "repo" not in dict.keys(doc):
                        raise ValueError(f"No repos declared in {file_path}")
                    repo: Table = cast(Table, doc["repo"])
                    if name not in dict.keys(repo):
                        raise ValueError(f"Repo {name} is not in {file_path}")
                    named_repo: Table = cast(Table, repo[name])
                    named_repo["enabled"] = enable

                with file_path.open("w") as fh:
                    tomlkit.dump(doc, fh)

                self.line(f"<c1>{name}</> {'enabled' if enable else 'disabled'}")

                return 0
            else:
                self.line(f"<error><c1>{file_path}</> does not exist</>")
                return -1
        except Exception as e:
            self.line(f"[DynamicRepos#{type(self)}]: <error>{e}</>")
            return -1


class RepoEnableCommand(RepoSetEnableCommand):
    name = "acrepo enable"
    description = "Enable a dynamic repo"

    def handle(self) -> int:
        return super()._handle(True)


class RepoDisableCommand(RepoSetEnableCommand):
    name = "acrepo disable"
    description = "Disable a dynamic repo"

    def handle(self) -> int:
        return super()._handle(False)


class RepoUseCommand(Command):
    name = "acrepo use"
    description = "Enable a specific set of repositories exclusiviely"

    arguments = [argument("names", "List of repositories to enable", multiple=True)]

    def handle(self) -> int:
        names = self.argument("names")

        try:
            repo_entries = RepoManager.entries()

            for name in names:
                if name not in repo_entries:
                    self.line(f"<error><c1>{name}>/c> is not a valid repo</>")
                    return -1

            for name in repo_entries:
                entry = RepoManager.get(name)
                if name in names:
                    entry.enabled = True
                else:
                    entry.enabled = False

            RepoManager.save()

            return 0
        except Exception as e:
            self.line(f"[DynamicRepos#{type(self).name}]: <error>{e}</>")
            return -1


class RepoSetAuth(Command):
    name = "acrepo auth set"
    description = "Configure the basic authentication credential for a named repo, and setup the repo credential cache to reflect it."

    arguments = [
        argument("name", "Repository name"),
        argument("username", "The username"),
        argument("password", "The password"),
    ]

    def handle(self) -> int:
        repo_name = self.argument("name")
        username = self.argument("username")
        password = self.argument("password")

        try:
            repos = RepoManager.entries()
            for name in filter(lambda n: n == repo_name, repos):
                repo = RepoManager.get(name)
                if not repo.auth:
                    raise ValueError(f"{repo.name} does not have an auth configuration")
                if repo.auth.authtype != "basic":
                    raise ValueError(f"{repo.name} is not a basic auth repo")

                poetry = self.poetry
                pm = PasswordManager(poetry.config)
                creds = BasicRepoCredentials(authtype="basic", username=username, password=password)

                CredentialManager.set_basic_credentials(pm, repo, creds)
                CredentialCache.save()

                self.line(f"credentials configured for {name}")
                return 0
            raise ValueError(f"{name} is not a valid repo")
        except ValueError as ve:
            self.line(f"<error>{ve}</>")
            return -1
        except Exception as e:
            self.line(f"[DynamicRepos#RepoSetBasicAuth]: <error>{e}</>")
            return -1


class RepoShowCredentials(Command):
    name = "acrepo creds show"
    decription = "Show entries from the credential cache, and their status"

    arguments = [argument("name", "A specific repository to view", optional=True)]

    def handle(self) -> int:
        try:
            specific_repo = self.argument("name")
            cache_entries = CredentialCache.entries()
            if specific_repo:
                cache_entries = filter(lambda n: n == specific_repo, cache_entries)
            self.line(f"Found <c1>{len(cache_entries)}</> entries")
            pm = PasswordManager(self.poetry.config)
            for name in cache_entries:
                cache_entry = CredentialCache.get(name)
                table = self.table(style="compact")
                rows: List[Union[List[Union[str, TableCell]], TableSeparator]] = [
                    [
                        "<info>name</>",
                        f" : <c1>{name}</>",
                    ],
                    ["<info>fingerprint</>", f" : {cache_entry.fingerprint}"],
                    [
                        "<info>expires</>",
                        f" : {cache_entry.expires.isoformat() if cache_entry.expires else 'Never'}",
                    ],
                    [
                        "<info>verifies</>",
                        f" : {'yes' if CredentialManager.verify(pm, name, cache_entry) else 'no'}",
                    ],
                    ["", ""],
                ]
                table.add_rows(rows)
                table.render()
            return 0
        except Exception as e:
            self.line(f"[DynamicRepos#RepoShowCredentials]: <error>{e}</>")
            return -1


class RepoClearCredentials(Command):
    name = "acrepo creds clear"
    decription = (
        "Clear the credential cache, and clean up existing keychain entries for dynamic repos"
    )

    arguments = [argument("name", "A specific repository to clear", optional=True)]

    def handle(self) -> int:
        try:
            specific_repo = self.argument("name")
            pm = PasswordManager(self.poetry.config)

            if specific_repo:
                if (
                    specific_repo not in CredentialCache.entries()
                    and specific_repo not in RepoManager.entries()
                ):
                    raise ValueError(f"<c1>{specific_repo}</c> does not exist.")
                try:
                    pm.delete_http_password(specific_repo)
                except Exception as e:
                    self.line(f"Could not delete <c1>{specific_repo}</c> - <error>{e}</>")
                CredentialCache.remove(specific_repo)
                CredentialCache.save()
            else:
                logger.debug(f"Will clear {len(RepoManager.entries())} entries")
                for repo in RepoManager.entries():
                    try:
                        pm.delete_http_password(repo)
                    except Exception as e:
                        self.line(f"Could not delete <c1>{repo}</c> - <error>{e}</>")
                CredentialCache.CACHE_FILE.unlink(missing_ok=True)
            return 0
        except Exception as e:
            self.line(f"[DynamicRepos#RepoClearCredentials]: <error>{e}</>")
            return -1
