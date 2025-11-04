"""Data loading helpers for Momotetsu World card shop listings."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "card_shops.json"


@dataclass(frozen=True)
class CardShop:
    """A station and the cards sold there."""

    station: str
    cards: List[str]


def load_card_shops(path: Path | str = DEFAULT_DATA_PATH) -> list[CardShop]:
    """Load card shop data from ``path``.

    Parameters
    ----------
    path:
        A JSON file containing a ``stations`` list. Each item must be a mapping with
        ``station`` and ``cards`` keys.

    Returns
    -------
    list[CardShop]
        Parsed card shop entries.
    """

    path = Path(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    stations: Iterable[dict[str, object]] = raw.get("stations", [])

    card_shops: list[CardShop] = []
    for entry in stations:
        station_name = str(entry.get("station", "")).strip()
        cards = [str(card).strip() for card in entry.get("cards", []) if str(card).strip()]
        if not station_name:
            continue
        card_shops.append(CardShop(station=station_name, cards=cards))

    return card_shops
