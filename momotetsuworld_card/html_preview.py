"""Static HTML preview generator for Momotetsu World card data."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from .data import CardShop, DEFAULT_DATA_PATH, load_card_shops

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"ja\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>桃太郎電鉄ワールド カード販売駅一覧</title>
  <style>
    :root {
      color-scheme: light dark;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
    }
    body {
      margin: 0;
      padding: 2rem clamp(1rem, 5vw, 3rem);
      background: canvas;
      color: canvastext;
    }
    h1 {
      margin-top: 0;
      font-size: clamp(1.75rem, 4vw, 2.5rem);
    }
    p {
      line-height: 1.6;
    }
    .search-panels {
      display: grid;
      gap: 1.5rem;
      margin-block: 2rem;
    }
    .panel {
      padding: 1.25rem;
      border-radius: 0.75rem;
      background: color-mix(in srgb, canvas 85%, canvastext 15%);
      box-shadow: 0 0.25rem 1rem color-mix(in srgb, canvastext 25%, transparent);
    }
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 600;
    }
    input[type=\"search\"], input[type=\"text\"] {
      width: 100%;
      padding: 0.65rem 0.75rem;
      border-radius: 0.5rem;
      border: 1px solid color-mix(in srgb, canvastext 30%, transparent);
      font-size: 1rem;
    }
    button {
      margin-top: 0.75rem;
      padding: 0.5rem 0.85rem;
      border-radius: 999px;
      border: none;
      background: #f05133;
      color: white;
      font-weight: 600;
      cursor: pointer;
    }
    button:hover, button:focus {
      background: #c63b25;
    }
    .results {
      display: grid;
      gap: 0.75rem;
      margin-top: 1.5rem;
    }
    .result-card {
      padding: 1rem 1.25rem;
      border-radius: 0.75rem;
      background: color-mix(in srgb, canvas 92%, canvastext 8%);
    }
    .result-card h2 {
      margin: 0 0 0.5rem;
      font-size: 1.25rem;
    }
    .result-card ul {
      margin: 0;
      padding-left: 1.25rem;
    }
    .empty-state {
      padding: 1rem 1.25rem;
      border-radius: 0.75rem;
      background: color-mix(in srgb, canvas 92%, canvastext 8%);
    }
    footer {
      margin-top: 3rem;
      font-size: 0.85rem;
      color: color-mix(in srgb, canvastext 60%, transparent);
    }
    @media (min-width: 768px) {
      .search-panels {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }
  </style>
</head>
<body>
  <h1>桃太郎電鉄ワールド カード販売駅リスト</h1>
  <p>桃太郎電鉄ワールドの各駅で購入できるカードを調べることができます。駅名またはカード名を入力して検索してください。</p>
  <div class=\"search-panels\">
    <section class=\"panel\" aria-labelledby=\"station-search-heading\">
      <h2 id=\"station-search-heading\">駅名で探す</h2>
      <label for=\"station-search\">駅名</label>
      <input id=\"station-search\" type=\"search\" placeholder=\"例: サンプル駅\" />
      <button type=\"button\" data-action=\"search-station\">検索</button>
      <div class=\"results\" data-results=\"station\"></div>
    </section>
    <section class=\"panel\" aria-labelledby=\"card-search-heading\">
      <h2 id=\"card-search-heading\">カード名で探す</h2>
      <label for=\"card-search\">カード名</label>
      <input id=\"card-search\" type=\"search\" placeholder=\"例: サンプルカード\" />
      <button type=\"button\" data-action=\"search-card\">検索</button>
      <div class=\"results\" data-results=\"card\"></div>
    </section>
  </div>
  <section class=\"panel\">
    <h2>登録済みのカードショップ一覧</h2>
    <div data-results=\"preview\"></div>
  </section>
  <script id=\"card-data\" type=\"application/json\">__DATA__</script>
  <script>
    const cardData = JSON.parse(document.getElementById("card-data").textContent || "[]");

    const stationIndex = new Map(cardData.map((shop) => [shop.station.toLocaleLowerCase(), shop]));
    const cardIndex = new Map();
    for (const shop of cardData) {
      for (const card of shop.cards) {
        const key = card.toLocaleLowerCase();
        if (!cardIndex.has(key)) {
          cardIndex.set(key, new Set());
        }
        cardIndex.get(key).add(shop.station);
      }
    }

    function renderStationResult(container, query) {
      container.innerHTML = "";
      if (!query) {
        container.innerHTML = `<p class="empty-state">駅名を入力してください。</p>`;
        return;
      }
      const key = query.toLocaleLowerCase();
      const shop = stationIndex.get(key);
      if (!shop) {
        container.innerHTML = `<p class="empty-state">該当する駅が見つかりませんでした。</p>`;
        return;
      }

      const listItems = shop.cards.length
        ? shop.cards.map((card) => `<li>${card}</li>`).join("")
        : `<li>登録されているカード情報がありません。</li>`;
      container.innerHTML = `
        <article class="result-card">
          <h2>${shop.station}</h2>
          <ul>${listItems}</ul>
        </article>
      `;
    }

    function renderCardResult(container, query) {
      container.innerHTML = "";
      if (!query) {
        container.innerHTML = `<p class="empty-state">カード名を入力してください。</p>`;
        return;
      }
      const key = query.toLocaleLowerCase();
      const stations = cardIndex.get(key);
      if (!stations || stations.size === 0) {
        container.innerHTML = `<p class="empty-state">取り扱い駅が見つかりませんでした。</p>`;
        return;
      }

      const listItems = Array.from(stations)
        .map((station) => `<li>${station}</li>`)
        .join("");
      container.innerHTML = `
        <article class="result-card">
          <h2>${query}</h2>
          <ul>${listItems}</ul>
        </article>
      `;
    }

    function renderPreview(container) {
      container.innerHTML = "";
      if (cardData.length === 0) {
        container.innerHTML = `<p class="empty-state">登録されているカードショップ情報がありません。</p>`;
        return;
      }
      const cards = cardData
        .map((shop) => {
          const listItems = shop.cards.length
            ? shop.cards.map((card) => `<li>${card}</li>`).join("")
            : `<li>登録されているカード情報がありません。</li>`;
          return `
            <article class="result-card">
              <h2>${shop.station}</h2>
              <ul>${listItems}</ul>
            </article>
          `;
        })
        .join("");
      container.innerHTML = cards;
    }

    const stationContainer = document.querySelector('[data-results="station"]');
    const cardContainer = document.querySelector('[data-results="card"]');
    const previewContainer = document.querySelector('[data-results="preview"]');
    const stationInput = document.getElementById("station-search");
    const cardInput = document.getElementById("card-search");

    document.querySelector('[data-action="search-station"]').addEventListener('click', () => {
      renderStationResult(stationContainer, stationInput.value.trim());
    });
    document.querySelector('[data-action="search-card"]').addEventListener('click', () => {
      renderCardResult(cardContainer, cardInput.value.trim());
    });
    stationInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        renderStationResult(stationContainer, stationInput.value.trim());
      }
    });
    cardInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        renderCardResult(cardContainer, cardInput.value.trim());
      }
    });

    renderPreview(previewContainer);
  </script>
  <footer>
    <p>このページはオフラインでも利用できます。データを更新した場合は、<code>momotetsuworld_card.html_preview</code> モジュールで HTML を再生成してください。</p>
  </footer>
</body>
</html>
"""


def _serialize(card_shops: Iterable[CardShop]) -> str:
    payload = [
        {
            "station": shop.station,
            "cards": shop.cards,
        }
        for shop in card_shops
    ]
    return json.dumps(payload, ensure_ascii=False)


def render_html(card_shops: Iterable[CardShop]) -> str:
    """Return an HTML page that embeds ``card_shops`` for offline preview."""

    data_json = _serialize(card_shops)
    return HTML_TEMPLATE.replace("__DATA__", data_json)


def export_html(
    output: Path | str,
    data_path: Path | str = DEFAULT_DATA_PATH,
) -> Path:
    """Export ``card_shops`` data to a static HTML file."""

    card_shops = load_card_shops(data_path)
    output_path = Path(output)
    output_path.write_text(render_html(card_shops), encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="カードショップ一覧の静的 HTML を生成します")
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="カードショップ情報を含む JSON ファイルへのパス",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/index.html"),
        help="出力する HTML ファイルのパス",
    )
    args = parser.parse_args(argv)

    export_html(args.output, data_path=args.data)
    print(f"HTML を生成しました: {args.output}")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
