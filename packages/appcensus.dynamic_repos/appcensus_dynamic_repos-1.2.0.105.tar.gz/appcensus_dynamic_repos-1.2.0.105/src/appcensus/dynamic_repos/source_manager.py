import logging
from typing import List
from typing import Protocol

from cleo.io.io import IO
from poetry.config.source import Source
from poetry.factory import Factory
from poetry.poetry import Poetry

logger = logging.getLogger(__name__)


# Poetry has had a shifting package management API, so we have an ability to plug in different
# implementation strategies. We have retired backward compatible support for versions prior to
# 1.5, but retain the flexibility to validate the current strategy, and plug in new ones if
# necessary.
class SourceCreationStrategy(Protocol):
    def add_sources(self, poetry: Poetry, new_sources: List[Source], io: IO) -> None:
        pass


# Supports the 1.4+ interface for sources.
class FactoryCreatesPool(SourceCreationStrategy):
    def add_sources(self, poetry: Poetry, new_sources: List[Source], io: IO) -> None:
        # tmw: I can only assume that mypy is somewhat confused by multiple inheritance on tomlkit.items.Table,
        #      because it most certainly does have an unwrap via its AbstractTable parent.
        pool = Factory.create_pool(poetry.config, [s.unwrap() for s in new_sources], io)  # type: ignore[attr-defined]
        poetry.set_pool(pool)


# RepoManager is a facade that detects and uses a strategy for mining sources from the repo pool.
class SourceManager:
    _strategy: SourceCreationStrategy

    def __init__(self) -> None:
        if hasattr(Factory, "create_pool"):
            self._strategy = FactoryCreatesPool()
        else:
            raise NotImplementedError(
                "Cannot find a repo management strategy for the current Factory implementation"
            )
        logger.debug(f"Selected {type(self._strategy).__name__} for repo management")

    def add_sources(self, poetry: Poetry, new_sources: List[Source], io: IO) -> None:
        return self._strategy.add_sources(poetry, new_sources, io)
