"""Utilities for working with Momotetsu World card shop data."""

from __future__ import annotations

from .data import DEFAULT_DATA_PATH, load_card_shops

__all__ = [
    "DEFAULT_DATA_PATH",
    "load_card_shops",
    "search_by_station",
    "search_by_card",
    "build_indexes",
    "render_html",
    "export_html",
]


def search_by_station(*args, **kwargs):
    from .search import search_by_station as _search_by_station

    return _search_by_station(*args, **kwargs)


def search_by_card(*args, **kwargs):
    from .search import search_by_card as _search_by_card

    return _search_by_card(*args, **kwargs)


def build_indexes(*args, **kwargs):
    from .search import build_indexes as _build_indexes

    return _build_indexes(*args, **kwargs)


def render_html(*args, **kwargs):
    from .html_preview import render_html as _render_html

    return _render_html(*args, **kwargs)


def export_html(*args, **kwargs):
    from .html_preview import export_html as _export_html

    return _export_html(*args, **kwargs)
