"""
REQ - Quebec Business Register API Client

A Python client for the Quebec Business Register (Registre des entreprises du Québec) API.
"""

from .req import REQ
from .typess import (
    ListeEntreprises,
    REQSearchResponse,
    REQRequest,
    REQRequestOptions,
    SearchOptions,
)

__all__ = [
    "REQ",
    "ListeEntreprises",
    "REQSearchResponse",
    "REQRequest",
    "REQRequestOptions",
    "SearchOptions",
]

__version__ = "1.0.0"
