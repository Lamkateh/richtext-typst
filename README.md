# Rich Text JSON to Typst Converter

Convert rich text JSON documents (from editors like ProseMirror, Quill, Slate) to [Typst](https://typst.app/) markup.

## Features

- **Supports multiple formats**: Quill, Slate, ProseMirror (extensible)
- **Simple API**: One function to convert any supported format
- **Custom parser support**: Register your own parser for new formats

---

## Installation

```bash
pip install richtext-typst
```

---

## Usage

### Basic Example

```python
from richtext_typst import convert

# Example: ProseMirror JSON
prosemirror_json = {
  "type": "doc",
  "content": [
    {"type": "paragraph", "content": [
      {"type": "text", "text": "Hello", "marks": [{"type": "bold"}]}
    ]}
  ]
}
typst = convert(prosemirror_json, "prosemirror")
print(typst)  # Output: *Hello*
```

### Supported Formats

- `prosemirror`: [ProseMirror](https://prosemirror.net/) JSON
- `quill`: [Quill.js](https://quilljs.com/) Delta JSON (Soon)
- `slate`: [Slate.js](https://docs.slatejs.org/) JSON (Soon)

### API

#### `convert(data: dict, fmt: str | BaseParser) -> str`

- `data`: The rich text JSON object
- `fmt`: Format name (`"quill"`, `"slate"`, `"prosemirror"`) or a custom parser instance
- Returns: Typst markup as a string

#### Registering a Custom Parser

```python
from richtextjson2typst import register_parser, BaseParser

class MyParser(BaseParser):
		def parse(self, data: dict) -> str:
				return f"#myformat[{data['text']}]
"
register_parser("myformat", MyParser())
```

---

## Testing

Run all tests:

```bash
uv run pytest
```

---

## Project Structure

- `src/richtextjson2typst/` — Main package
  - `converter.py` — Format dispatch and API
  - `base.py` — Parser interface
  - `exceptions.py` — Error types
  - `formats/` — Built-in format parsers (Quill, Slate, ProseMirror)
- `tests/` — Unit and robustness tests

---

## License

MIT License. See [LICENSE](LICENSE).
