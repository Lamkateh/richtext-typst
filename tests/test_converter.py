import pytest
from richtextjson2typst.converter import convert, register_parser
from richtextjson2typst.base import BaseParser
from richtextjson2typst.exceptions import UnsupportedFormatError


# --- 1. Tests avec formats natifs ---
def test_quill_bold():
    data = {"ops": [{"insert": "Hello", "attributes": {"bold": True}}]}
    result = convert(data, "quill")
    assert result == "*Hello*"


def test_quill_plain_text():
    data = {"ops": [{"insert": "Hello"}]}
    result = convert(data, "quill")
    assert result == "Hello"


# --- 2. Tests avec parser custom directement ---
class MyParser(BaseParser):
    def parse(self, data: dict) -> str:
        return f"#myformat[{data['text']}]"


def test_custom_parser_direct():
    data = {"text": "Hello world"}
    parser = MyParser()
    result = convert(data, parser)
    assert result == "#myformat[Hello world]"


# --- 3. Tests avec parser enregistré globalement ---
class PortableTextParser(BaseParser):
    def parse(self, data: dict) -> str:
        return f"#portable[{data['children'][0]['text']}]"


def test_register_parser():
    register_parser("portable", PortableTextParser())
    data = {"children": [{"text": "Bonjour"}]}
    result = convert(data, "portable")
    assert result == "#portable[Bonjour]"


# --- 4. Tests erreurs ---
def test_unsupported_format():
    data = {"text": "oops"}
    with pytest.raises(UnsupportedFormatError):
        convert(data, "unknownformat")


def test_invalid_parser_type():
    with pytest.raises(TypeError):
        register_parser("bad", object())  # pas un BaseParser
