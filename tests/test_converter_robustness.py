import pytest
from richtextjson2typst.converter import convert
from richtextjson2typst.exceptions import InvalidFormatError


# --- Cas Quill JSON invalide ---
def test_quill_missing_ops():
    """Un JSON Quill sans 'ops' doit lever une erreur explicite."""
    data = {"foo": "bar"}
    with pytest.raises(InvalidFormatError):
        convert(data, "quill")


def test_quill_ops_not_list():
    """'ops' doit être une liste, sinon erreur."""
    data = {"ops": "not_a_list"}
    with pytest.raises(InvalidFormatError):
        convert(data, "quill")


def test_quill_invalid_insert_type():
    """Chaque 'insert' doit être une string."""
    data = {"ops": [{"insert": 1234}]}
    with pytest.raises(InvalidFormatError):
        convert(data, "quill")


def test_quill_empty_ops():
    """Un JSON Quill vide doit donner une chaîne vide."""
    data = {"ops": []}
    result = convert(data, "quill")
    assert result == ""


# --- Cas Slate JSON invalide ---
def test_slate_missing_nodes():
    """Un JSON Slate sans 'nodes' doit lever une erreur explicite."""
    data = {"foo": "bar"}
    with pytest.raises(InvalidFormatError):
        convert(data, "slate")


# --- Cas ProseMirror JSON invalide ---
def test_prosemirror_missing_type():
    """Un JSON ProseMirror sans 'type' doit lever une erreur explicite."""
    data = {"content": [{"text": "Hello"}]}
    with pytest.raises(InvalidFormatError):
        convert(data, "prosemirror")
