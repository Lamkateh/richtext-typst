from ..base import BaseParser
from ..exceptions import InvalidFormatError


class ProseMirrorParser(BaseParser):
    def parse(self, data: dict | list, additional_attributes: dict = {}) -> str:
        if isinstance(data, list):
            return "\n".join(self.parse(item) for item in data)

        if "type" not in data:
            raise InvalidFormatError(
                "Missing 'type' field in ProseMirror data")

        if data["type"] == "doc":
            return self.__parse_doc_type(data)
        elif data["type"] == "paragraph":
            return self.__parse_paragraph_type(data)
        elif data["type"] == "heading":
            return self.__parse_heading_type(data)
        elif data["type"] == "text":
            return self.__parse_text_type(data)
        elif data["type"] == "bullet_list":
            return self.__parse_list_type(data)
        elif data["type"] == "ordered_list":
            return self.__parse_list_type(data)
        elif data["type"] == "list_item":
            return self.__parse_list_item_type(data, additional_attributes)
        elif data["type"] == "hr":
            return self.__parse_hr_type(data)
        elif data["type"] == "code_fence":
            return self.__parse_code_fence(data)
        elif data["type"] == "container_notice":
            return self.__parse_container_notice_type(data)
        elif data["type"] == "table":
            return self.__parse_table_type(data)
        else:
            return ""

    def __parse_doc_type(self, data: dict) -> str:
        if data.get("type") != "doc":
            raise InvalidFormatError("Invalid ProseMirror document type")
        return self.parse(data["content"])

    def __parse_paragraph_type(self, data: dict) -> str:
        if data.get("type") != "paragraph":
            raise InvalidFormatError("Invalid ProseMirror paragraph type")
        if "content" not in data:
            return ""
        return self.parse(data["content"])

    def __parse_heading_type(self, data: dict) -> str:
        if data.get("type") != "heading":
            raise InvalidFormatError("Invalid ProseMirror heading type")
        level = data.get("attrs", {}).get("level", 1)
        return f"{'=' * level} {self.parse(data['content'])}"

    def __parse_text_type(self, data: dict) -> str:
        if data.get("type") != "text":
            raise InvalidFormatError("Invalid ProseMirror text type")

        text_parameters = {}
        strikethrough = False
        code = False

        if "marks" in data:
            for mark in data["marks"]:
                if mark.get("type") == "strong":
                    text_parameters["weight"] = "bold"
                elif mark.get("type") == "em":
                    text_parameters["style"] = "italic"
                elif mark.get("type") == "strikethrough":
                    strikethrough = True
                elif mark.get("type") == "code_inline":
                    code = True

        if code:
            return f"#raw(\"{data.get('text', '')}\")"
        if text_parameters:
            params = ", ".join(
                f"{key}: \"{value}\"" for key, value in text_parameters.items())
            text = f"#text(\"{data.get('text', '')}\", {params})"
        else:
            text = data.get("text", "")

        if strikethrough:
            text = f"#strike(\"{text}\")"

        return text

    def __parse_list_type(self, data: dict, additional_attributes: dict = {}) -> str:
        if data.get("type") != "bullet_list" and data.get("type") != "ordered_list":
            raise InvalidFormatError("Invalid ProseMirror list type")

        if data.get("type") == "ordered_list":
            list_char = "+"
        else:
            list_char = "-"

        items = []
        for item in data.get("content", []):
            if "list_level" not in additional_attributes:
                additional_attributes["list_level"] = 1
            else:
                additional_attributes["list_level"] += 1
            items.append(self.parse(item, additional_attributes))
            additional_attributes["list_level"] -= 1
        indent = "  " * (additional_attributes.get("list_level", 1))
        items = [f"{indent}{list_char} {item.strip()}" for item in items]
        return "\n".join(items) + ""

    def __parse_list_item_type(self, data: dict, additional_attributes: dict = {}) -> str:
        if data.get("type") != "list_item":
            raise InvalidFormatError("Invalid ProseMirror list_item type")
        return self.parse(data.get("content", []), additional_attributes)

    def __parse_hr_type(self, data: dict) -> str:
        if data.get("type") != "hr":
            raise InvalidFormatError(
                "Invalid ProseMirror horizontal_rule type")
        if "attrs" in data and "markup" in data["attrs"]:
            if data["attrs"]["markup"] == "***":
                return "#pagebreak()"
            elif data["attrs"]["markup"] == "---":
                return "#line(length: 100%)"
        return ""

    def __parse_code_fence(self, data: dict) -> str:
        if data.get("type") != "code_fence":
            raise InvalidFormatError("Invalid ProseMirror code_fence type")
        language = data.get("attrs", {}).get("language", "")
        code_content = data.get("content", [])
        code_text = ""
        for item in code_content:
            if item.get("type") == "text":
                code_text += item.get("text", "")
        return f"```{language}\n{code_text}\n```"

    def __parse_container_notice_type(self, data: dict) -> str:
        if data.get("type") != "container_notice":
            raise InvalidFormatError(
                "Invalid ProseMirror container_notice type")
        content = self.parse(data.get("content", []))
        return f"#block(\"{content}\")"

    def __parse_table_type(self, data: dict) -> str:
        if data.get("type") != "table":
            raise InvalidFormatError("Invalid ProseMirror table type")
        cells = []
        for row in data.get("content", []):
            for cell in row.get("content", []):
                if cell.get("type") in ["td", "th"]:
                    print(cell.get("attrs", {}))
                    cell_content = self.parse(cell.get("content", []))
                    cell_element = f"table.cell(rowspan: {cell.get('attrs', {}).get('rowspan', 1)}, colspan: {cell.get('attrs', {}).get('colspan', 1)}, [" + \
                        cell_content + "])"
                    cells.append(cell_element)
        return "#table(align: \"center\",columns: (auto, auto, auto)," + ", ".join(cells) + ")"
