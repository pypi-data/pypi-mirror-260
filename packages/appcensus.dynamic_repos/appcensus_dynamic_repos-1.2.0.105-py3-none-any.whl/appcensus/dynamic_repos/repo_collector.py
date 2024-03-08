import logging
from abc import ABC
from abc import abstractmethod
from typing import List

from poetry.config.source import Source
from poetry.repositories.pypi_repository import PyPiRepository
from poetry.repositories.repository_pool import RepositoryPool

logger = logging.getLogger(__name__)


# Poetry has had a shifting package management API, so we have an ability to plug in different
# implementation strategies. We have retired backward compatible support for versions prior to
# 1.5, but retain the flexibility to validate the current strategy, and plug in new ones if
# necessary.
class RepoStrategy(ABC):
    def __init__(self, pool: RepositoryPool):
        self._pool = pool

    @abstractmethod
    def repositories(self) -> List[Source]:
        pass


# In 1.5, there is a proper public API for getting repository priority.
class PrioritizedRepoStrategy(RepoStrategy):
    def __init__(self, pool: RepositoryPool):
        super().__init__(pool)

    def repositories(self) -> List[Source]:
        repos = []
        logger.debug("Collecting repos from a prioritized repo:")
        for repo in self._pool.repositories:
            if type(repo) is PyPiRepository:
                continue
            prio = self._pool.get_priority(repo.name)
            repos.append(
                Source(name=repo.name, url=repo.url, priority=prio)  # type: ignore[attr-defined]
            )
        return repos


# RepoCollector is a facade that detecs and uses a strategy for mining sources from the repo pool.
class RepoCollector:
    _strategy: RepoStrategy

    def __init__(self, pool: RepositoryPool):
        if hasattr(pool, "get_priority"):
            self._strategy = PrioritizedRepoStrategy(pool)
        else:
            raise NotImplementedError(
                "Cannot find a repo strategy for a pool that does not support explicit priority retrieval"
            )
        logger.debug(f"Selected {type(self._strategy).__name__} for repo enumeration")

    def repositories(
        self,
    ) -> List[Source]:
        return self._strategy.repositories()
