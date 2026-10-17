from app.llm.schema import ExtractionModel


def test_extraction_schema_is_accepted_by_gemini_response_schema():
    # Gemini rejects JSON Schema "additionalProperties" in response_schema (400 Bad Request).
    assert "additionalProperties" not in str(ExtractionModel.model_json_schema())
