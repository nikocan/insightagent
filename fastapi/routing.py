"""Minimal routing primitives to register GET endpoints."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .dependency import Dependency


@dataclass
class Route:
    """Stores metadata for a registered route."""

    path: str
    methods: List[str]
    endpoint: Callable[..., Any]
    response_model: Optional[Any] = None


@dataclass
class APIRouter:
    """Collects endpoints under a shared prefix and tag set."""

    prefix: str = ""
    tags: Optional[List[str]] = None
    routes: List[Route] = field(default_factory=list)

    def get(self, path: str, response_model: Optional[Any] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Register a GET endpoint on the router."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(path=self.prefix + path, methods=["GET"], endpoint=func, response_model=response_model))
            return func

        return decorator

    def post(self, path: str, response_model: Optional[Any] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Register a POST endpoint on the router."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(path=self.prefix + path, methods=["POST"], endpoint=func, response_model=response_model))
            return func

        return decorator

    def patch(self, path: str, response_model: Optional[Any] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Register a PATCH endpoint on the router."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(path=self.prefix + path, methods=["PATCH"], endpoint=func, response_model=response_model))
            return func

        return decorator


def resolve_dependencies(
    func: Callable[..., Any],
    path_params: Dict[str, Any],
    query_params: Optional[Dict[str, Any]] = None,
    body: Optional[Any] = None,
) -> Dict[str, Any]:
    """Resolve dependency defaults defined using Depends."""

    import inspect

    resolved: Dict[str, Any] = {}
    for name, parameter in inspect.signature(func).parameters.items():
        default = parameter.default
        if isinstance(default, Dependency):
            dependency_callable = default.dependency
            resource = dependency_callable()
            if hasattr(resource, "__enter__") and hasattr(resource, "__exit__"):
                value = resource.__enter__()

                def finalizer(res=resource) -> None:
                    res.__exit__(None, None, None)

                resolved["__finalizers__"] = resolved.get("__finalizers__", []) + [finalizer]
            else:
                import inspect

                if inspect.isgenerator(resource):
                    generator = resource
                    value = next(generator)

                    def finalizer(gen=generator) -> None:
                        gen.close()

                    resolved["__finalizers__"] = resolved.get("__finalizers__", []) + [finalizer]
                else:
                    value = resource
            resolved[name] = value
        elif name in path_params:
            value = path_params[name]
            annotation = parameter.annotation
            if annotation is int:
                value = int(value)
            resolved[name] = value
        elif query_params and name in query_params:
            value = query_params[name]
            annotation = parameter.annotation
            if annotation is int:
                value = int(value)
            resolved[name] = value
        elif body is not None and name not in resolved:
            resolved[name] = body
    return resolved
