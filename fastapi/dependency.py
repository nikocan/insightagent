"""Dependency helper replicating FastAPI's Depends and Query signatures."""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Dependency:
    """Stores a callable dependency for manual resolution."""

    dependency: Callable[..., Any]


def Depends(dependency: Callable[..., Any]) -> Dependency:
    """Return a dependency descriptor understood by the shim router."""

    return Dependency(dependency=dependency)


def Query(default: Any = None, **_: Any) -> Any:
    """Return default value for query parameters (validation omitted)."""

    return default
