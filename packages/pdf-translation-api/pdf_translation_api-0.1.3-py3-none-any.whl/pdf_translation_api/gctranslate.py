from __future__ import annotations

import json
import os
from pathlib import Path

from google.cloud import translate_v3beta1
from google.cloud.translate_v3beta1 import (
    TranslateDocumentRequest,
    TranslationServiceClient,
)


def translate_document(
    *,
    path: str,
    target_lang: str,
    source_lang: None | str = None,
    mime_type: str = "application/pdf",
) -> Path:
    """Translate the content of a document from source language to target language.

    ```python
    from pdf_translation_api import translate_document

    output_path = translate_document(
        path="path/to/your/document.pdf",
        target_lang="nl",
    )
    print(output_path)
    >>> /path/to/your/document.nl.pdf
    ```

    Args:
        content: Document's content represented as a stream of bytes.
        target_lang: The language to translate the document to.
        source_lang: The language of the document to be translated.
            If not specified, the API will attempt to detect the language.
        mime_type: pecifies the input document's mime_type. Supported mime types are:
        -  application/pdf
        -  application/vnd.openxmlformats-officedocument.wordprocessingml.document
        -  application/vnd.openxmlformats-officedocument.presentationml.presentation
        -  application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

    Returns:
        The path of the translated document.
        The file is saved in the same directory as the original document
        with the language code of the target language appended to the file name.
    """
    pdf_file = Path(path)

    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path is None:
        msg = "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
        raise ValueError(msg)

    service_account_file = Path(credentials_path)
    service_account_info = json.loads(service_account_file.read_text())
    project_id = service_account_info["project_id"]

    request = TranslateDocumentRequest(
        parent=f"projects/{project_id}/locations/global",
        source_language_code=source_lang,
        target_language_code=target_lang,
        document_input_config=translate_v3beta1.DocumentInputConfig(
            content=pdf_file.read_bytes(),
            mime_type=mime_type,
        ),
    )

    translate_client = TranslationServiceClient.from_service_account_info(
        service_account_info,
    )
    response = translate_client.translate_document(request)
    current_suffix = pdf_file.suffix
    output_path = pdf_file.with_suffix(f".{target_lang}{current_suffix}")
    if output_path.exists():
        msg = f"{output_path} already exists."
        raise FileExistsError(msg)
    output_path.write_bytes(response.document_translation.byte_stream_outputs[0])
    return output_path.absolute()
