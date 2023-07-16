サバイバルTypeScriptの質問チャットボット

## 概要
サバイバルTypeScriptのドキュメントについてチャット形式で質問ができるチャットボットです。
現状は最小限のサンプル実装な状態です。
`docs`

## 開発環境
- パッケージ管理ツール: poetry

## 開発環境のセットアップ

### パッケージのインストール
```sh
$ poetry install
```

### OPENAI_API_KEYの設定
`.env`ファイルを作成して`OPENAI_API_KEY`を設定してください。

```sh
$ cp .env.example .env
```

## スクリプトの実行
```sh
$ poetry run python bot.py
```
