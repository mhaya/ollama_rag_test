Repository: Ollama RAG Chat (Python)
====================================

English / 日本語の両方で手順を示します。  
A minimal Retrieval-Augmented Generation (RAG) chat service using FastAPI, FAISS, and local Ollama models (`llama3` for answers, `nomic-embed-text` for embeddings). Ingest local text files into a vector index, then query with grounded responses.

## Quickstart / クイックスタート
- Install deps / 依存インストール: `make deps`
- Pull models (Ollama running) / モデル取得: `ollama pull llama3` と `ollama pull nomic-embed-text`
- Ingest documents / ドキュメント取り込み: `.venv/bin/python src/ingest.py` (`data/*.txt` を読み、`vectors/` にFAISS保存)
- Serve API / サーバ起動: `make serve`（`0.0.0.0:5000`）
- Test call / 動作確認:  
  `curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message":"概要を教えて"}'`

## Project Structure / 構成
- `src/app.py`: FastAPI app; `/chat` でストリーム応答、`/health` で状態確認。
- `src/ingest.py`: `data/` を読み込み、分割・埋め込みして FAISS を `vectors/` に保存。
- `data/`: 取り込み対象の `.txt` を置く。
- `vectors/`: Ingest 後の FAISS インデックス。
- `tests/`: プロンプト生成・分割のユニットテスト。
- `.env.example`: 設定サンプル。`cp .env.example .env` で上書き設定。

## Configuration / 設定
Set in `.env` if needed / 必要に応じ `.env` に設定:
- `OLLAMA_MODEL=llama3`
- `OLLAMA_EMBED_MODEL=nomic-embed-text`
- `VECTOR_DIR=vectors`
- `DATA_DIR=data`
- `TOP_K=4`
- `CHUNK_SIZE=800`
- `CHUNK_OVERLAP=120`

## Development / 開発
- `make lint` / `make format`: `ruff check` / `ruff format`
- `make test`: unit tests
- Keep endpoints thin; retrieval/prompt logic is unit-tested. / エンドポイントは薄くし、取得/プロンプトのロジックをテスト対象に。

## API Notes / APIメモ
- `POST /chat`: body `{"message": "...", "top_k": 4?}` でプレーンテキストをストリーム返却。
- `GET /health`: モデル/設定のヘルスチェック。

## Troubleshooting / トラブルシュート
- Missing embed model: `ollama pull nomic-embed-text`
- Missing index: run ingest; ensure `vectors/` exists. / インデックス無し: ingest 実行で `vectors/` を作成。
- Bind/port: edit `make serve` or run `uvicorn src.app:app --host 0.0.0.0 --port 5000`. / ポート変更はコマンドで指定可。
