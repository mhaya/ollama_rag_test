from src.ingest import make_splitter


def test_splitter_respects_chunk_size_and_overlap():
    splitter = make_splitter(chunk_size=50, chunk_overlap=10)
    text = " ".join(["token"] * 80)  # ~480 characters
    chunks = splitter.split_text(text)

    assert chunks, "Splitter should return at least one chunk"
    assert all(len(chunk) <= 50 for chunk in chunks), "Chunk size exceeded"
    # Overlap implies more than one chunk for this input
    assert len(chunks) > 1
