# pdf-tools

Extract annotations and comments from PDF files using PyMuPDF.

## Usage

```bash
uv run python comments7.py
```

Edit the PDF path at the bottom of `comments7.py` to point to your file. The script extracts all annotations, formats newlines, and writes them to `comments.txt` with word and character counts.

## Setup

```bash
uv sync
```

## Dependencies

- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF annotation extraction
