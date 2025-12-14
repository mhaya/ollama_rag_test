Repository Guidelines / 開発ガイド
=====================

This repository is a lightweight Ollama-based RAG chat scaffold. Use these guidelines to keep contributions consistent and easy to review.  
本リポジトリは Ollama を用いた軽量な RAG チャット基盤です。貢献時の指針として参照してください。

## Project Structure & Module Organization / 構成
- `src/`: Core application (FastAPI app, ingest pipeline).
- `data/`: ローカルドキュメント置き場（大容量・秘匿データはコミット禁止）。
- `vectors/`: `make ingest` で生成される FAISS インデックス。
- `tests/`: `src/` に対応するユニットテスト。
- `.env.example`: 実行時設定サンプル。必要に応じて `.env` を作成。

## Build, Test, and Development Commands / コマンド
- `make deps`: venv 作成と依存インストール。
- `make ingest`: `data/` を分割・埋め込みし `vectors/` に保存（Ollama + embed モデル起動・取得済み必須）。
- `make serve`: FastAPI/Uvicorn を `0.0.0.0:5000` で起動。
- `make test`: ユニットテスト実行。
- `make lint` / `make format`: `ruff check` / `ruff format`。

## Coding Style & Naming Conventions / コーディング規約
- Python: PEP 8, 4-space indent, public 関数に型ヒント。`ruff format` + `ruff check` で統一。
- ファイル/モジュール: snake_case、クラス: PascalCase、定数: UPPER_SNAKE。
- エンドポイントは薄く保ち、処理ロジックはヘルパーへ分離しテスト可能に。

## Testing Guidelines / テスト指針
- Framework: `pytest`。分割、プロンプト生成、検索ヘルパーを重点的に。
- テスト命名: 対応モジュールに合わせる（例 `test_prompt.py`）。
- ユニットテストは高速・決定的に。Ollama 依存はモックまたはスキップし、ネットワークを避ける。

## Commit & Pull Request Guidelines / コミット・PR
- Commits: 命令形サマリ（例 `Add retriever batching`）、論理的な単位で分割。
- PRs: 概要、関連 Issue、`make test` の結果、UI変更はスクショ/GIF。大きな変更はリスクとロールバック方針を記載。

## Security & Configuration Tips / セキュリティと設定
- APIキーや認証情報をコミットしない。`.env` などで管理。
- ユーザー入力は埋め込み前にバリデーション/サニタイズ。
- 依存更新時はライセンスと supply-chain リスクを確認し、`requirements.txt` 等でバージョン管理。
