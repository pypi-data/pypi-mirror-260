from __future__ import annotations

import logging
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
from functools import cached_property
from pathlib import Path
from typing import Any
from typing import Literal
from typing import OrderedDict

import tomli
import tomlkit
from cryptography.hazmat.primitives.hashes import Hash
from cryptography.hazmat.primitives.hashes import SHA256
from poetry.repositories.repository_pool import Priority
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator
from pydantic_core.core_schema import ValidationInfo
from pytz import UTC
from tomlkit.items import KeyType
from tomlkit.items import SingleKey
from tomlkit.items import Table

from appcensus.dynamic_repos import REPO_FILE_PATH

logger = logging.getLogger(__name__)


class Auth(BaseModel):
    authtype: str
    cache: bool = False
    timeout: int | None = None

    def to_table(self) -> Table:
        table = tomlkit.table(is_super_table=True)
        table.add("authtype", self.authtype)
        table.add("cache", self.cache)
        if self.timeout:
            table.add("timeout", self.timeout)
        return table


class BasicAuth(Auth):
    authtype: Literal["basic"] = "basic"
    cache: bool = True


class CodeArtifactAuth(Auth):
    authtype: Literal["codeartifact"] = "codeartifact"
    domain: str
    owner: str
    region: str | None = None
    profile: str | None = None

    def to_table(self) -> Table:
        table = super().to_table()
        table.add("domain", self.domain)
        table.add("owner", self.owner)
        if self.region:
            table.add("region", self.region)
        if self.profile:
            table.add("profile", self.profile)
        return table


class RepoCredentials(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        ignored_types = (cached_property,)

    authtype: str

    @cached_property
    @abstractmethod
    def fingerprint(self) -> str:
        raise NotImplementedError()


class BasicRepoCredentials(RepoCredentials):
    username: str
    password: str

    def valid(self) -> bool:
        return True

    @cached_property
    def fingerprint(self) -> str:
        if not self.username or not self.password:
            raise ValueError("Cannot fingerprint empty credentials")
        digest = Hash(SHA256())
        digest.update(bytes(f"{self.username}:{self.password}".encode()))
        return digest.finalize().hex()


class CachedCredentialSet(BaseModel):
    VALID_WINDOW: int = 30

    authtype: str
    expires: datetime | None = None
    fingerprint: str

    def valid(self) -> bool:
        """Ensures that a set of credentials is valid for at least VALID_WINDOW seconds"""
        if not self.expires:
            return True
        return (datetime.now() + timedelta(seconds=self.VALID_WINDOW)).astimezone(
            UTC
        ) < self.expires.astimezone(UTC)

    def to_table(self) -> tomlkit.items.Item:
        table = tomlkit.table(is_super_table=True)
        table.append("authtype", self.authtype)
        table.append("fingerprint", self.fingerprint)
        if self.expires:
            table.append("expires", self.expires)
        return table


class Repo(BaseModel):
    name: str
    url: str | None = None
    auth: None | CodeArtifactAuth | BasicAuth = Field(None, discriminator="authtype")
    enabled: bool
    default: bool | None = None
    secondary: bool | None = None
    priority: Priority | None = None

    @field_validator("*", mode="before")
    def coerce_priority(cls, v: Any, info: ValidationInfo) -> Any:
        if info.field_name == "priority":
            if isinstance(v, Priority):
                return v
            else:
                try:
                    return Priority[v.upper()]
                except TypeError:
                    raise ValueError("value is not convertible to a PurePosixPath")
        else:
            return v

    @model_validator(mode="before")
    def ensure_priority(cls, d: dict[Any, Any]) -> dict[Any, Any]:
        if "priority" not in d.keys() and (
            "secondary" not in d.keys() or "default" not in d.keys()
        ):
            raise ValueError(
                "Either priority (1.4+) or default + secondary properties must be set on all declared repos"
            )
        return d

    def to_table(self) -> Table:
        table = tomlkit.table(is_super_table=True)
        table.append("enabled", self.enabled)
        if self.url:
            table.append("url", self.url)
        if self.auth:
            auth_table = self.auth.to_table()
            for key in dict.keys(auth_table):
                table.append(SingleKey(f"auth.{key}", KeyType.Bare), auth_table.get(key))
        if self.default:
            table.append("default", self.default)
        if self.secondary:
            table.append("secondary", self.secondary)
        if self.priority:
            table.append("priority", self.priority.name.lower())
        return table


class RepoManager:
    _repos: OrderedDict[str, Repo] = OrderedDict()

    @classmethod
    def entries(cls) -> list[str]:
        return list(cls._repos.keys())

    @classmethod
    def get(cls, name: str) -> Repo | None:
        if name in cls._repos.keys():
            return cls._repos[name]
        return None

    @classmethod
    def load(self, file_path: Path = REPO_FILE_PATH) -> None:
        logger.debug(f"Loading repositories from {file_path} ({file_path.exists()})")
        self._repos = OrderedDict()
        if file_path.exists():
            with file_path.open("r") as fh:
                doc = tomli.loads(fh.read())
                if "repo" not in doc.keys():
                    raise ValueError(f"No repos declared in {file_path}")
                for repo_id, repo_attrs in doc["repo"].items():
                    repo_attrs["name"] = repo_id
                    repo = Repo(**repo_attrs)
                    self._repos[repo.name] = repo
                    logger.debug(f"Loaded {repo}")

    @classmethod
    def save(cls, file_path: Path = REPO_FILE_PATH) -> None:
        doc = tomlkit.document()

        repos = tomlkit.table(is_super_table=True)
        for key in cls._repos.keys():
            entry = cls._repos[key]
            repos.add(key, entry.to_table())
        doc.add("repo", repos)

        with file_path.open("w+") as fh:
            tomlkit.dump(doc, fh, sort_keys=False)


RepoManager.load()
