class RichTextError(Exception):
    """Package generic error."""


class UnsupportedFormatError(RichTextError):
    """Unknown or unimplemented format."""


class InvalidFormatError(RichTextError):
    """The provided JSON is invalid for this format."""
