from ..base import BaseParser
from .prosemirror import ProseMirrorParser

class OutlineParser(BaseParser):
    def parse(self, data: dict) -> str:
        
        output = []
        for document in data.get("documents", []):
            output.append(ProseMirrorParser().parse(document))
        return "\n\n".join(output)