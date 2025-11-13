const resultsContainer = document.getElementById("results");
const input = document.getElementById("station-input");
const clearButton = document.getElementById("clear-button");

let stations = [];

const renderMessage = (message, className = "result-placeholder") => {
  resultsContainer.innerHTML = "";
  const wrapper = document.createElement("div");
  wrapper.className = className;
  wrapper.textContent = message;
  resultsContainer.appendChild(wrapper);
};

const createResultCard = ({ station, cards }) => {
  const article = document.createElement("article");
  article.className = "result-card";

  const heading = document.createElement("h2");
  heading.textContent = station;
  article.appendChild(heading);

  const list = document.createElement("ul");
  list.className = "card-list";

  cards.forEach((card) => {
    const item = document.createElement("li");
    item.textContent = card;
    list.appendChild(item);
  });

  article.appendChild(list);
  return article;
};

const normalize = (text) =>
  text
    .toString()
    .normalize("NFKC")
    .trim()
    .toLowerCase();

const renderResults = (query) => {
  const normalizedQuery = normalize(query);

  if (!normalizedQuery) {
    renderMessage("駅名を入力して検索を開始してください。");
    return;
  }

  const filtered = stations.filter(({ station }) =>
    normalize(station).includes(normalizedQuery)
  );

  resultsContainer.innerHTML = "";

  if (!filtered.length) {
    renderMessage(
      `「${query}」に一致する駅は見つかりませんでした。`,
      "error-message"
    );
    return;
  }

  filtered.forEach((stationData) => {
    const card = createResultCard(stationData);
    resultsContainer.appendChild(card);
  });
};

const attachEventListeners = () => {
  input.addEventListener("input", (event) => {
    renderResults(event.target.value);
  });

  clearButton.addEventListener("click", () => {
    input.value = "";
    input.focus();
    renderResults("");
  });
};

const init = async () => {
  renderMessage("データを読み込み中です...", "loading-message");

  try {
    const response = await fetch("data/card_shops.json", { cache: "no-store" });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    if (!Array.isArray(data?.stations)) {
      throw new Error("Unexpected data format");
    }

    stations = data.stations;
    renderResults(input.value);
  } catch (error) {
    console.error("データの読み込みに失敗しました", error);
    renderMessage(
      "データの読み込みに失敗しました。時間をおいて再度お試しください。",
      "error-message"
    );
  }
};

if (resultsContainer && input && clearButton) {
  attachEventListeners();
  init();
} else {
  console.error("検索UIの初期化に必要な要素が見つかりませんでした。");
}
