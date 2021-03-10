### PDF Decryptor

This repository contains a simple PDF decryptor.

To run it first install the required dependencies with `pip install -r requirements.txt` and run `python decrypt.py` specifying the following arguments:

- `--input`: path to the encrypted PDF file
- `--output`: path where the output PDF will be saved
- `--ocr-language`: which [language](https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc#languages) should be used for the OCR?
- `--copy-pdf-id`: whether the original PDF ID should be preserved (`y/n`, default `y`)

If it's not bundled with your system you may also have to install [Tesseract](https://github.com/tesseract-ocr/tesseract)

### How does this work?

This script rasterizes the input PDF to a set of images using `pdftoppm`, which are then rebuilt into a PDF via `tesseract` and finally the OCR is applied via [ocrmypdf](https://ocrmypdf.readthedocs.io/en/latest/)