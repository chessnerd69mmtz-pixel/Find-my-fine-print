from app import split_chunks, rank_chunks


def test_chunks_cover_text_with_overlap():
    text = " ".join(f"word{i}" for i in range(2400))
    chunks = split_chunks(text, words_per_chunk=500, overlap=80)
    assert len(chunks) >= 5
    assert chunks[0]["start"] == 0
    assert chunks[-1]["end"] == len(text)
    assert all(c["text"] for c in chunks)


def test_tfidf_ranks_relevant_clause():
    chunks = [
        {"index": 1, "start": 0, "end": 40, "text": "The supplier will provide delivery dates."},
        {"index": 2, "start": 41, "end": 90, "text": "Either party may terminate the agreement with thirty days notice."},
    ]
    ranked = rank_chunks("termination notice period", chunks)
    assert ranked[0]["index"] == 2
