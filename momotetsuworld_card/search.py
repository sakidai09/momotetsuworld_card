"""Search utilities for Momotetsu World card shop data."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List

from .data import CardShop, DEFAULT_DATA_PATH, load_card_shops


def normalize(text: str) -> str:
    """Return a case-folded representation for matching."""

    return text.casefold()


def build_indexes(card_shops: Iterable[CardShop]) -> tuple[Dict[str, CardShop], Dict[str, List[str]]]:
    """Build lookup tables for station and card searches."""

    station_index: Dict[str, CardShop] = {}
    card_index: Dict[str, List[str]] = defaultdict(list)

    for shop in card_shops:
        station_key = normalize(shop.station)
        station_index[station_key] = shop
        for card in shop.cards:
            card_key = normalize(card)
            if shop.station not in card_index[card_key]:
                card_index[card_key].append(shop.station)

    return station_index, card_index


def search_by_station(station_name: str, station_index: Dict[str, CardShop]) -> CardShop | None:
    """Return the ``CardShop`` entry for ``station_name`` if present."""

    return station_index.get(normalize(station_name))


def search_by_card(card_name: str, card_index: Dict[str, List[str]]) -> List[str]:
    """Return all stations that sell ``card_name``."""

    return card_index.get(normalize(card_name), [])


def _format_station_result(shop: CardShop | None) -> str:
    if shop is None:
        return "該当する駅が見つかりませんでした。"
    if not shop.cards:
        return f"{shop.station}: 登録されているカード情報がありません。"
    cards = "、".join(shop.cards)
    return f"{shop.station}: {cards}"


def _format_card_result(card_name: str, stations: List[str]) -> str:
    if not stations:
        return f"{card_name}: 取り扱い駅が見つかりませんでした。"
    joined = "、".join(stations)
    return f"{card_name}: {joined}"


def _format_preview(card_shops: Iterable[CardShop]) -> str:
    shops = list(card_shops)
    if not shops:
        return "登録されているカードショップ情報がありません。"

    lines: List[str] = []
    for shop in shops:
        if shop.cards:
            cards = "、".join(shop.cards)
            lines.append(f"{shop.station}: {cards}")
        else:
            lines.append(f"{shop.station}: 登録されているカード情報がありません。")

    return "\n".join(lines)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Momotetsu World のカード販売駅検索ツール"
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="カードショップ情報を含む JSON ファイルへのパス (省略時は同梱データを使用)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--station", help="駅名で検索します")
    group.add_argument("--card", help="カード名で検索します")
    group.add_argument(
        "--preview",
        action="store_true",
        help="登録済みのカードショップ情報を一覧表示します",
    )

    return parser


def run_cli(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    card_shops = load_card_shops(args.data)

    if args.preview:
        result = _format_preview(card_shops)
    else:
        station_index, card_index = build_indexes(card_shops)

        if args.station:
            result = _format_station_result(search_by_station(args.station, station_index))
        else:
            result = _format_card_result(args.card, search_by_card(args.card, card_index))

    print(result)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(run_cli())
