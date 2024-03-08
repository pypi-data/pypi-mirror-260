from datetime import datetime
from datetime import timedelta
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import boto3
import tomlkit
from botocore.client import BaseClient
from poetry.utils.password_manager import PasswordManager
from pytz import UTC

from appcensus.dynamic_repos.models import BasicRepoCredentials
from appcensus.dynamic_repos.models import CachedCredentialSet
from appcensus.dynamic_repos.models import Repo


class CredentialCache:
    CACHE_FILE = Path(".ac_cred_cache")

    _active_credentials: Dict[str, CachedCredentialSet] = {}

    @classmethod
    def load(cls) -> None:
        cls._active_credentials = {}
        try:
            with cls.CACHE_FILE.open("r") as fh:
                doc = tomlkit.parse(fh.read())
                if "active_credentials" in doc.unwrap().keys():
                    credentials = doc["active_credentials"].unwrap()
                    for repo_id in credentials.keys():
                        entry = CachedCredentialSet.parse_obj(credentials[repo_id])
                        if entry.expires:
                            entry.expires = entry.expires.astimezone(UTC)
                        if entry.valid():
                            cls.cache(repo_id, entry)
        except FileNotFoundError:
            pass

    @classmethod
    def entries(cls) -> List[str]:
        return list(cls._active_credentials.keys())

    @classmethod
    def get(cls, name: str) -> Union[CachedCredentialSet, None]:
        if name in cls._active_credentials.keys():
            active = cls._active_credentials[name]
            if active.valid():
                return active
            del cls._active_credentials[name]
        return None

    @classmethod
    def cache(cls, name: str, creds: CachedCredentialSet) -> None:
        cls._active_credentials[name] = creds

    @classmethod
    def remove(cls, name: str) -> None:
        if name in cls._active_credentials.keys():
            del cls._active_credentials[name]

    @classmethod
    def save(cls) -> None:
        doc = tomlkit.document()
        active_credentials = tomlkit.table()
        for key in cls._active_credentials.keys():
            entry = cls._active_credentials[key]
            active_credentials.add(key, entry.to_table())
        doc.add("active_credentials", active_credentials)
        with cls.CACHE_FILE.open("w+") as fh:
            tomlkit.dump(doc, fh)

    @classmethod
    def wipe(cls) -> None:
        cls._active_credentials = {}
        cls.save()


CredentialCache.load()


class CredentialManager:
    DEFAULT_TIMEOUT = 12 * 60 * 60  # 12 hours is the default timeout for code artifact
    MAX_RETRIES = 3

    @classmethod
    def _caclient(cls, profile: Optional[str] = None, region: Optional[str] = None) -> BaseClient:
        session = boto3.Session(profile_name=profile, region_name=region)
        return session.client("codeartifact")

    @classmethod
    def _reliably_set_http_password(
        cls, pm: PasswordManager, name: str, login: str, password: str
    ) -> None:
        last_exception: Optional[Exception] = None
        for attempt in range(cls.MAX_RETRIES):
            try:
                pm.set_http_password(name, login, password)
                return
            except FileNotFoundError as notfound:
                # It seems that if the keyring falls back to flat file (which it will in CI)
                # it doesn't create the config path.
                filepath = Path(notfound.filename)
                if filepath.name == "auth.toml":
                    filepath.parent.mkdir(mode=0o600, parents=True, exist_ok=True)
                last_exception = notfound
            except Exception as e:
                pm.delete_http_password(name)
                last_exception = e
        raise PermissionError(
            f"Failed to set credentials for <c1>{name}</> after {cls.MAX_RETRIES} attempts: {last_exception}"
        )

    @classmethod
    def set_basic_credentials(
        cls, pm: PasswordManager, repo: Repo, credentials: BasicRepoCredentials
    ) -> None:
        cls._reliably_set_http_password(pm, repo.name, credentials.username, credentials.password)
        cache_entry = CachedCredentialSet(
            authtype="codeartifact", fingerprint=credentials.fingerprint
        )
        if repo.auth.cache:
            if repo.auth.timeout:
                cache_expiry = datetime.now().astimezone(UTC) + timedelta(
                    seconds=repo.auth.timeout if repo.auth.timeout else cls.DEFAULT_TIMEOUT
                )
                cache_entry.expires = cache_expiry
        CredentialCache.cache(repo.name, cache_entry)

    @classmethod
    def verify(
        cls, pm: PasswordManager, repo: str, cached_credentials: CachedCredentialSet
    ) -> bool:
        http_auth = pm.get_http_auth(repo)
        if http_auth:
            established_credentials = BasicRepoCredentials(
                authtype="basic", username=http_auth["username"], password=http_auth["password"]
            )
            # oddly mypy doesn't seem to consider str property == str here to be bool
            if established_credentials.fingerprint == cached_credentials.fingerprint:
                return True
        return False

    @classmethod
    def authorize_code_artifact(cls, pm: PasswordManager, repo: Repo) -> None:
        client = cls._caclient(profile=repo.auth.profile, region=repo.auth.region)
        response = client.get_authorization_token(
            domain=repo.auth.domain,
            domainOwner=repo.auth.owner,
            durationSeconds=repo.auth.timeout,
        )
        status = response["ResponseMetadata"]["HTTPStatusCode"]
        if status == 200:
            creds = BasicRepoCredentials(
                authtype="codeartifact", username="aws", password=response["authorizationToken"]
            )
            cls.set_basic_credentials(pm, repo, creds)
        else:
            raise PermissionError(f"CodeArtifact responded with {status}")

    @classmethod
    def authorize(cls, pm: PasswordManager, repo: Repo) -> None:
        cache_entry = CredentialCache.get(repo.name)
        if repo.auth.cache and cache_entry and cls.verify(pm, repo.name, cache_entry):
            return

        if repo.auth.authtype == "basic":
            raise PermissionError(
                f"Repo <c1>{repo.name}</> requires basic auth, but credentials are not available. Please use <c1>repo auth set</> to configure it."
            )
        elif repo.auth.authtype == "codeartifact":
            cls.authorize_code_artifact(pm, repo)
        else:
            raise ValueError(f"Unknown auth type {repo.auth.authtype}")
