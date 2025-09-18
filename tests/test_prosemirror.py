import json
from richtextjson2typst.converter import convert


def test_prosemirror_parser():
    data_file = "tests/data/prosemirror-basic-doc.json"
    with open(data_file, "r") as f:
        data = json.load(f)
    result = convert(data, "prosemirror")
    typst_file = "tests/data/prosemirror-basic-doc.typ"
    with open(typst_file, "w") as f:
        f.write(result)
    print(result)
    assert result == ""
