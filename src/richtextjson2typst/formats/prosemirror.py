from ..base import BaseParser
from ..exceptions import InvalidFormatError


class ProseMirrorParser(BaseParser):
    def parse(self, data: dict) -> str:
        if "ops" not in data:
            raise InvalidFormatError("ProseMirror JSON must have an 'ops' field")
        if not isinstance(data["ops"], list):
            raise InvalidFormatError("'ops' must be a list")

        output = []
        for op in data["ops"]:
            insert = op.get("insert")
            if not isinstance(insert, str):
                raise InvalidFormatError("'insert' must be a string")

            attrs = op.get("attributes", {})
            if attrs.get("bold"):
                insert = f"*{insert}*"
            if attrs.get("italic"):
                insert = f"/{insert}/"
            output.append(insert)

        return "".join(output)
