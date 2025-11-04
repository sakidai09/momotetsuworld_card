# momotetsuworld_card

「桃太郎電鉄ワールド 〜地球は希望でまわってる！〜」に登場するカードショップ情報を管理するリポジトリです。データは `data/card_shops.json` に格納され、駅名と取り扱いカード名の両方から検索できるシンプルな CLI を提供します。

## データ構造

`data/card_shops.json` では、次のような構造でカードショップ情報を保持します。

```json
{
  "stations": [
    {
      "station": "サンプル駅",
      "cards": ["サンプルカードA", "サンプルカードB"]
    }
  ]
}
```

ゲーム内で確認できた駅とカードの組み合わせをこのリストに追加してください。現在のリポジトリには、攻略サイトで確認できた代表的な駅のカードショップ情報をあらかじめ登録しています。

## 使い方

### 事前準備

Python 3.10 以上を前提としています。

### 駅名で検索する

```bash
python -m momotetsuworld_card.search --station "サンプル駅"
```

### カード名で検索する

```bash
python -m momotetsuworld_card.search --card "サンプルカードA"
```

### 登録済みデータをプレビューする

```bash
python -m momotetsuworld_card.search --preview
```

### ブラウザでプレビューする（ターミナル不要）

リポジトリ直下の `docs/index.html` をブラウザで開くと、駅名・カード名の検索および登録済みデータの一覧を GUI で確認できます。インターネット接続は不要で、ファイルをダブルクリックするだけで利用できます。

データを更新した場合は、次のコマンドで HTML を再生成すると最新の内容が反映されます。

```bash
python -m momotetsuworld_card.html_preview --output docs/index.html
```

### データファイルを切り替える

別の JSON ファイルを指定したい場合は `--data` 引数を利用してください。

```bash
python -m momotetsuworld_card.search --data other_file.json --station "サンプル駅"
```

## データの更新について

カードショップ情報を収集できた際には、確認した内容を `stations` 配列に追記し、あわせてコミットしてください。
