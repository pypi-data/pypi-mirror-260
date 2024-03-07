from pdf_translation_api import translate_document


def test_translate_document():
    output_path = translate_document(
        path="pdf-translation-api/tests/dummy.pdf",
        target_lang="nl",
    )
    assert output_path.read_bytes()
    assert output_path.exists()

