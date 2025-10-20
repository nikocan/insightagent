"""Lightweight FastAPI-compatible shim for offline execution and testing."""

from .application import FastAPI
from .routing import APIRouter
from .dependency import Depends, Query
from .exceptions import HTTPException

__all__ = ["FastAPI", "APIRouter", "Depends", "HTTPException", "Query"]
