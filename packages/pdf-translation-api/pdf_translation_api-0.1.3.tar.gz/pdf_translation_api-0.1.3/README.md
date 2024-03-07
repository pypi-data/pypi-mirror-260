# PDF Translation API

Easily translate PDF documents using the Google Cloud Translation API.

[![PyPI - Version](https://img.shields.io/pypi/v/pdf-translation-api.svg)](https://pypi.org/project/pdf-translation-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pdf-translation-api.svg)](https://pypi.org/project/pdf-translation-api)

---

## Installation and Usage

```console
pip install pdf-translation-api
```

Make sure to set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
to the path of your service account key file.
Check the [Google Cloud Translation API documentation](https://cloud.google.com/translate/docs/setup) for more information.

```python
from pdf_translation_api import translate_document

output_path = translate_document(
    path="path/to/your/document.pdf",
    target_lang="nl",
)
print(output_path)
>>> path/to/your/document.nl.pdf
```

> [!WARNING]  
> Google Cloud Translation API charges for usage. Make sure to check the [pricing](https://cloud.google.com/translate/pricing) before using this library.

## Upcoming Features

- [ ] Support for files with more than 20 pages

## License

`pdf-translation-api` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
