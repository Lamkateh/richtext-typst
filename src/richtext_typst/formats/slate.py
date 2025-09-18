from ..base import BaseParser
from ..exceptions import InvalidFormatError


class SlateParser(BaseParser):
    def parse(self, data: dict) -> str:
        if "nodes" not in data:
            raise InvalidFormatError("Slate JSON must have a 'nodes' field")
        if not isinstance(data["nodes"], list):
            raise InvalidFormatError("'nodes' must be a list")

        output = []
        for node in data["nodes"]:
            text = node.get("text")
            if not isinstance(text, str):
                raise InvalidFormatError("'text' must be a string")

            attrs = node.get("attributes", {})
            if attrs.get("bold"):
                text = f"*{text}*"
            if attrs.get("italic"):
                text = f"/{text}/"
            output.append(text)

        return "".join(output)
