import json
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from app import app, rank_chunks, split_chunks, source_reference, _normalize_model_data, call_model


def test_chunks_cover_text_with_overlap():
    text = " ".join(f"word{i}" for i in range(2400))
    chunks = split_chunks(text, words_per_chunk=500, overlap=80)
    assert len(chunks) >= 5
    assert chunks[0]["start"] == 0
    assert chunks[-1]["end"] == len(text)
    assert all(c["text"] for c in chunks)


def test_retrieval_ranks_relevant_clause():
    chunks = [
        {"index": 1, "start": 0, "end": 40, "text": "The supplier will provide delivery dates."},
        {"index": 2, "start": 41, "end": 100, "text": "Either party may terminate the agreement with thirty days notice."},
    ]
    assert rank_chunks("termination notice period", chunks)[0]["index"] == 2


def test_retrieval_preserves_legal_negations():
    chunks = [
        {"index": 1, "start": 0, "end": 50, "text": "The customer may cancel with written notice."},
        {"index": 2, "start": 51, "end": 110, "text": "The customer may not cancel without written notice except for fraud."},
    ]
    assert rank_chunks("may not cancel without notice except fraud", chunks)[0]["index"] == 2


def test_all_chunks_has_no_30_section_cap():
    chunks = [{"index": i, "start": i, "end": i + 1, "text": f"clause {i} cancellation"} for i in range(1, 76)]
    assert len(rank_chunks("cancellation", chunks, limit=None)) == 75
    assert len(rank_chunks("cancellation", chunks, limit=0)) == 75


def test_source_reference_comes_from_document():
    source = "[Page 1]\nOpening terms\n\n[Page 2]\nTermination clause"
    assert source_reference(source, source.index("Termination")) == "Page 2"


def test_model_json_must_be_object():
    with pytest.raises(RuntimeError, match="not a JSON object"):
        _normalize_model_data(["valid", "json", "not object"])


def test_quote_reference_and_risk_evidence_are_verified():
    source = "[Page 4]\nThe buyer may terminate with 30 days written notice."
    chunk = {"index": 1, "start": 0, "end": len(source), "text": source, "retrieval_score": 0.7}
    payload = {"message": {"content": json.dumps({
        "plain_english_answer": "Notice is required.",
        "relevant_quotes": [{"verbatim": "30 days written notice", "reference": "Invented Section 99", "relevance": "Notice period"}],
        "potential_loopholes": [
            {"title": "Notice", "supporting_quote": "The buyer may terminate with 30 days written notice."},
            {"title": "Unsupported", "supporting_quote": "Immediate termination is permitted."}
        ],
        "what_to_verify": [], "caveats": ""
    })}}
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = payload
    with patch("app.requests.post", return_value=response):
        result = call_model("termination", "sample.txt", chunk, 1, 1, "ollama", "", "llama3.2", source)
    assert result["relevant_quotes"][0]["reference"] == "Page 4"
    assert "Invented" not in result["relevant_quotes"][0]["reference"]
    assert result["potential_loopholes"][0]["evidence_verified"] is True
    assert result["potential_loopholes"][1]["evidence_verified"] is False


def test_malformed_pdf_returns_client_error_not_500():
    client = TestClient(app)
    response = client.post("/api/analyze", data={"question": "termination", "provider": "ollama", "max_sections": "1"},
                           files={"file": ("broken.pdf", b"not a pdf", "application/pdf")})
    assert response.status_code in (413, 422, 503)
    assert response.status_code != 500
