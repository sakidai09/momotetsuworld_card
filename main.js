const resultsContainer = document.getElementById("results");
const input = document.getElementById("station-input");
const clearButton = document.getElementById("clear-button");

const categoryDefinitions = [
  {
    containerId: "attack-card-buttons",
    cards: [
      "刀狩りカード",
      "豪速球カード",
      "強奪飛びカード",
      "ふういんカード",
      "坊主丸儲けカード",
      "ライトニングカード",
      "一頭地を抜くカード",
      "音速カード",
      "牛歩カード",
    ],
  },
  {
    containerId: "move-card-buttons",
    cards: [
      "☆飛びカード",
      "シンデレラカード",
      "超音速カード",
      "冬眠カード",
      "物件飛びカード",
      "キングに！カード",
      "銀河鉄道カード",
    ],
  },
  {
    containerId: "special-card-buttons",
    cards: [
      "ダビングカード",
      "指定うんち！カード",
      "ゴールドカード",
      "絶好調カード",
    ],
  },
];

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

const toHiragana = (text) => {
  if (typeof text !== "string") {
    return "";
  }

  return text.replace(/[\u30a1-\u30f6]/g, (char) =>
    String.fromCharCode(char.charCodeAt(0) - 0x60)
  );
};

const normalize = (value) => {
  if (value == null) {
    return "";
  }

  const normalized = value
    .toString()
    .normalize("NFKC")
    .trim()
    .toLowerCase();

  return toHiragana(normalized);
};

const performSearch = (query = input.value) => {
  const normalizedQuery = normalize(query);

  if (!normalizedQuery) {
    renderMessage("駅名またはカード名を入力して検索を開始してください。");
    return;
  }

  const filtered = stations.filter(({ station, cards }) => {
    const matchesStation = normalize(station).includes(normalizedQuery);
    const matchesCard = Array.isArray(cards)
      ? cards.some((card) => normalize(card).includes(normalizedQuery))
      : false;

    return matchesStation || matchesCard;
  });

  resultsContainer.innerHTML = "";

  if (!filtered.length) {
    renderMessage("該当する駅はありません。", "error-message");
    return;
  }

  filtered.forEach((stationData) => {
    resultsContainer.appendChild(createResultCard(stationData));
  });
};

const createCategoryButton = (cardName) => {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "category-button";
  button.textContent = cardName;
  button.addEventListener("click", () => {
    input.value = cardName;
    input.focus();
    performSearch(cardName);
  });

  return button;
};

const populateCategoryButtons = () => {
  categoryDefinitions.forEach(({ containerId, cards }) => {
    const container = document.getElementById(containerId);

    if (!container) {
      return;
    }

    container.innerHTML = "";
    cards.forEach((cardName) => {
      container.appendChild(createCategoryButton(cardName));
    });
  });
};

const attachEventListeners = () => {
  input.addEventListener("input", (event) => {
    performSearch(event.target.value);
  });

  clearButton.addEventListener("click", () => {
    input.value = "";
    input.focus();
    performSearch("");
  });
};

const formatStationEntry = ([station, cards]) => ({
  station,
  cards: Array.isArray(cards) ? cards : [],
});

const loadStationsFromData = (data) => {
  if (Array.isArray(data?.stations)) {
    return data.stations.map((entry) => ({
      station: entry?.station ?? "",
      cards: Array.isArray(entry?.cards) ? entry.cards : [],
    }));
  }

  if (data && typeof data === "object") {
    return Object.entries(data).map(formatStationEntry);
  }

  throw new Error("Unexpected data format");
};

const init = async () => {
  renderMessage("データを読み込み中です...", "loading-message");

  try {
    const response = await fetch("data/card_shops.json", { cache: "no-store" });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    stations = loadStationsFromData(data);
    performSearch(input.value);
  } catch (error) {
    console.error("データの読み込みに失敗しました", error);
    renderMessage(
      "データの読み込みに失敗しました。時間をおいて再度お試しください。",
      "error-message"
    );
  }
};

if (resultsContainer && input && clearButton) {
  populateCategoryButtons();
  attachEventListeners();
  init();
} else {
  console.error("検索UIの初期化に必要な要素が見つかりませんでした。");
}
