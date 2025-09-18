from typing import Union

from .base import BaseParser
from .exceptions import UnsupportedFormatError
from .formats.prosemirror import ProseMirrorParser
from .formats.quill import QuillParser
from .formats.slate import SlateParser

# Registry globale
PARSERS = {
    "quill": QuillParser(),
    "slate": SlateParser(),
    "prosemirror": ProseMirrorParser(),
}


def register_parser(name: str, parser: BaseParser):
    """Register custom parser under a given name."""
    if not isinstance(parser, BaseParser):
        raise TypeError("Parser must inherit from BaseParser")
    PARSERS[name] = parser


def convert(data: dict, fmt: Union[str, BaseParser]) -> str:
    """
    Convert JSON in Typst string using specified format or parser.

    - fmt = "quill" → use native parser
    - fmt = parser instance → use custom parser directly
    """
    if isinstance(fmt, BaseParser):  # parser custom directement passé
        return fmt.parse(data)

    parser = PARSERS.get(fmt)
    if not parser:
        raise UnsupportedFormatError(f"Unsupported format: {fmt}")
    return parser.parse(data)
