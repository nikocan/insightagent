"""Exception classes mirroring FastAPI interfaces used in the project."""


class HTTPException(Exception):
    """Minimal HTTPException capturing status code and detail message."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail
