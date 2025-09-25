"""Application container orchestrating routes and startup events."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

from urllib.parse import parse_qs, urlsplit

from .exceptions import HTTPException
from .routing import APIRouter, Route, resolve_dependencies


@dataclass
class FastAPI:
    """Lightweight application mimicking FastAPI behaviour for tests."""

    title: str = "FastAPI"
    version: str = "0.1.0"
    routes: List[Route] = field(default_factory=list)
    startup_handlers: List[Callable[[], Any]] = field(default_factory=list)

    def include_router(self, router: APIRouter) -> None:
        """Register all routes from a router with the application."""

        self.routes.extend(router.routes)

    def get(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Register a GET endpoint directly on the app instance."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(path=path, methods=["GET"], endpoint=func))
            return func

        return decorator

    def post(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Register a POST endpoint directly on the app instance."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(path=path, methods=["POST"], endpoint=func))
            return func

        return decorator

    def patch(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Register a PATCH endpoint directly on the app instance."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes.append(Route(path=path, methods=["PATCH"], endpoint=func))
            return func

        return decorator

    def on_event(self, event: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
        """Register startup events (shutdown not implemented)."""

        if event != "startup":
            raise NotImplementedError("Only startup events are supported in the shim")

        def decorator(func: Callable[[], Any]) -> Callable[[], Any]:
            self.startup_handlers.append(func)
            return func

        return decorator

    def _find_route(self, method: str, path: str) -> tuple[Route, Dict[str, Any]]:
        """Return the matching route and extracted path parameters."""

        for route in self.routes:
            if method not in route.methods:
                continue
            params: Dict[str, Any] = {}
            if self._match_route(route.path, path, params):
                return route, params
        raise HTTPException(status_code=404, detail="Not Found")

    @staticmethod
    def _match_route(pattern: str, path: str, params: Dict[str, Any]) -> bool:
        """Very small path matcher supporting `{param}` syntax."""

        pattern_parts = [part for part in pattern.strip("/").split("/") if part]
        path_parts = [part for part in path.strip("/").split("/") if part]
        if len(pattern_parts) != len(path_parts):
            return False
        for pattern_part, path_part in zip(pattern_parts, path_parts):
            if pattern_part.startswith("{") and pattern_part.endswith("}"):
                params[pattern_part[1:-1]] = path_part
            elif pattern_part != path_part:
                return False
        return True


class Response:
    """Simple response wrapper used by the shim TestClient."""

    def __init__(self, status_code: int, data: Any):
        self.status_code = status_code
        self._data = data

    def json(self) -> Any:
        return self._data


class TestClient:
    """In-process test client resolving dependencies manually."""

    __test__ = False

    def __init__(self, app: FastAPI):
        self.app = app
        for handler in app.startup_handlers:
            result = handler()
            if hasattr(result, "__await__"):
                import asyncio

                asyncio.run(result)

    def _request(self, method: str, path: str, json: Any | None = None) -> Response:
        try:
            parsed = urlsplit(path)
            clean_path = parsed.path or "/"
            query_params = {key: values[0] if len(values) == 1 else values for key, values in parse_qs(parsed.query).items()}
            route, params = self.app._find_route(method, clean_path)
            dependencies = resolve_dependencies(route.endpoint, params, query_params=query_params, body=json)
            finalizers = dependencies.pop("__finalizers__", [])
            try:
                result = route.endpoint(**dependencies)
                if hasattr(result, "__await__"):
                    import asyncio

                    result = asyncio.run(result)
            except HTTPException as exc:
                for finalizer in finalizers:
                    finalizer()
                return Response(status_code=exc.status_code, data={"detail": exc.detail})
            except Exception as exc:  # pragma: no cover - unexpected errors bubble up as 500
                for finalizer in finalizers:
                    finalizer()
                return Response(status_code=500, data={"detail": str(exc)})
            else:
                for finalizer in finalizers:
                    finalizer()
                status = 200 if method == "GET" else 200
                return Response(status_code=status, data=result)
        except HTTPException as exc:
            return Response(status_code=exc.status_code, data={"detail": exc.detail})

    def get(self, path: str) -> Response:
        return self._request("GET", path)

    def post(self, path: str, json: Any | None = None) -> Response:
        return self._request("POST", path, json=json)

    def patch(self, path: str, json: Any | None = None) -> Response:
        return self._request("PATCH", path, json=json)
