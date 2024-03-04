"""JsonFormatter"""

from pathlib import Path
from .formatter import DataFormatter
from ..utils import write_file


class JsonFormatter(DataFormatter):
    """Json格式化器"""

    def __init__(self, indent: int = 4, depth=None, style: str = "list", with_schema: bool = False):
        super().__init__()
        self.depth = depth
        self.indent = indent
        self.style = style
        self.with_schema = with_schema

    def format(self, data) -> str:
        """格式化数据
        Args:
            data (dict): 数据
        Returns:
            str: 格式化后的字符串
        """
        if self.style == "map":
            return object_to_string(data.data_map(), 0, 2)
        if self.style == "list":
            return object_to_string(data.data_list(), 0, 1)
        if self.style == "column":
            return object_to_string(data.column_map(), 0, 2)
        raise ValueError(f"data style: {self.style} not support")

    def export(self, data, file_path: Path) -> list[Path]:
        """export"""
        # data
        _ret_list = []
        if self.style == "column":
            _columns = data.column_map()
            for key in _columns:
                _data = {"data": _columns[key]}
                _data_text = object_to_string(_data, 0, 2)
                _file_path2 = file_path.joinpath(f"{data.name}_{key}.json")
                write_file(_file_path2, _data_text)
                _ret_list.append(_file_path2)
        else:
            _data = {}
            if self.style == "map":
                _data = data.data_map()
            elif self.style == "list":
                _data = {"data": data.data_list()}
            else:
                raise ValueError(f"data style: {self.style} not support")
            if self.with_schema:
                _data["schema"] = data.schema
            _data_text = object_to_string(_data, 0, 2)
            if not file_path.name.endswith(".json"):
                file_path = file_path.joinpath(f"{data.name}.json")
            write_file(file_path, _data_text)
            _ret_list.append(file_path)
        return _ret_list


def object_to_string(obj: object, depth=0, max_depth=0, indent=4, sep_comma=", ", sep_equal=": ") -> str:
    """object_to_string

    Args:
        obj (object): _description_
        depth (int, optional): _description_. Defaults to 0.
        max_depth (int, optional): _description_. Defaults to 0.
        indent (int, optional): _description_. Defaults to 4.
        sep_comma (str, optional): _description_. Defaults to ", ".
        sep_equal (str, optional): _description_. Defaults to ": ".

    Returns:
        str: _description_
    """
    if isinstance(obj, list):
        data_list = []
        for item in obj:
            data_list.append(object_to_string(item, depth + 1, max_depth, indent, sep_comma, sep_equal))
        if len(data_list) > 0:
            comma, indent1, indent2 = _get_sep_break_indent(depth + 1, max_depth, indent, sep_comma)
            text = comma.join(data_list)
            text = f"[{indent1}{text}{indent2}]"
        else:
            text = "[]"
        return text
    if isinstance(obj, dict):
        data_list = []
        for key in obj.keys():
            value_str = object_to_string(obj[key], depth + 1, max_depth, indent, sep_comma, sep_equal)
            data_list.append(f'"{key}"{sep_equal}{value_str}')
        if len(data_list) > 0:
            comma, indent1, indent2 = _get_sep_break_indent(depth + 1, max_depth, indent, sep_comma)
            text = comma.join(data_list)
            text = f"{{{indent1}{text}{indent2}}}"
        else:
            text = "{}"
        return text
    if isinstance(obj, str):
        if obj.startswith('"') and obj.endswith('"'):
            return obj
        return f'"{obj}"'
    return str(obj)


def _get_sep_break_indent(depth, max_depth, indent, sep_comma):
    if depth <= max_depth:
        indent1 = "\n" + " " * indent * depth
        indent2 = "\n" + " " * indent * (depth - 1)
        comma_indent = "," + indent1
    else:
        indent1 = ""
        indent2 = ""
        comma_indent = ","
    return comma_indent, indent1, indent2
