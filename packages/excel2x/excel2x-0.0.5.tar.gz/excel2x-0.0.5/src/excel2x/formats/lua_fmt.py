"""JsonFormatter"""

from pathlib import Path

from .formatter import DataFormatter
from ..utils import write_file

# 符号
_sep_equal = " = "
_sep_comma = ", "


class LuaFormatter(DataFormatter):
    def __init__(self, indent: int = 4, style: str = "list", with_schema: bool = False):
        """LuaFormatter

        Args:
            indent (int, optional): 格式化缩进. Defaults to 4.
            style (str, optional): 格式样式 [ list / map ]. Defaults to list.
            with_schema (bool, optional): 导出文件时是否包含schema. Defaults to False.
        """
        super().__init__()
        self.indent = indent or 4
        self.style = style or "list"
        self.with_schema = with_schema is True

    def format(self, data) -> str:
        """format"""
        if self.style == "map":
            return object_to_string(data.data_map(), 0, 2)
        if self.style == "list":
            return object_to_string(data.data_list(), 0, 1)
        if self.style == "column":
            return object_to_string(data.column_map(), 0, 2)
        raise ValueError(f"lua style: {self.style} not support")

    def export(self, data, file_path: Path) -> list[Path]:
        """export"""
        # data
        _ret_list = []
        _suffix = ".lua.txt" if file_path.name.endswith(".lua.txt") else ".lua"
        if self.style == "column":
            _columns = data.column_map()
            if file_path.name.endswith(_suffix):
                file_path = file_path.parent
            for key in _columns:
                _file_path2 = file_path.joinpath(f"{data.name}_{key}").with_suffix(_suffix)
                _data_text = object_to_string(_columns[key], 0, 1)
                _ret_text = f"local {data.name}_{key} = {_data_text}\nreturn {data.name}_{key}\n"
                write_file(_file_path2, _ret_text)
                _ret_list.append(_file_path2)
        else:
            _ret_text = ""
            if self.with_schema:
                # schema
                _schema_text = self.format_schema(data)
                _ret_text += f"local {data.name}_type = {_schema_text}\n\n"
            _data_text = self.format(data)
            _ret_text += f"local {data.name} = {_data_text}\nreturn {data.name}\n"
            if not file_path.name.endswith(_suffix):
                file_path = file_path.joinpath(f"{data.name}.lua")
            write_file(file_path, _ret_text)
            _ret_list.append(file_path)
        return _ret_list

    def format_schema(self, data):
        """format_schema"""
        _temp_list = []
        _schema = data.schema
        for key in data.keys:
            _opt = _schema[key]
            _temp_list.append(f'-- [{_opt["type"]}] {_opt["title"]}\n    {key} = nil')
        _text = ",\n    ".join(_temp_list)
        return f"{{\n    {_text},\n}}"


def object_to_string(obj: object, depth=0, max_depth=0, indent=4, sep_comma=", ", sep_equal=" = ") -> str:
    """Python 对象转换成 Lua table 文本

    Args:
        obj : Python 对象
        depth (str): 格式化 lua 当前层级
        max_depth (str): 格式化 lua 最大深度
        indent (int, optional): 格式化 lua 缩进字符数. Defaults to 4.
        separators (tuple, optional): 格式化 lua 分割符号，逗号和等号. Defaults to (", ", " = ").

    Returns:
        str: Lua table 文本
    """
    if isinstance(obj, list):
        data_list = []
        for item in obj:
            data_list.append(object_to_string(item, depth + 1, max_depth, indent, sep_comma, sep_equal))
        if len(data_list) > 0:
            comma, indent1, indent2 = _get_sep_break_indent(depth + 1, max_depth, indent, sep_comma)
            text = comma.join(data_list)
            if indent > 0 and 0 <= depth < max_depth:
                text = text + ","
            text = f"{{{indent1}{text}{indent2}}}"
            return text
        return "{}"
    if isinstance(obj, dict):
        data_list = []
        for key in obj.keys():
            value_str = object_to_string(obj[key], depth + 1, max_depth, indent, sep_comma, sep_equal)
            data_list.append(f'["{key}"]{sep_equal}{value_str}')
        if len(data_list) > 0:
            comma, indent1, indent2 = _get_sep_break_indent(depth + 1, max_depth, indent, sep_comma)
            text = comma.join(data_list)
            if indent > 0 and 0 <= depth < max_depth:
                text = text + ","
            text = f"{{{indent1}{text}{indent2}}}"
            return text
        return "{}"
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
        comma_indent = ", "
    return comma_indent, indent1, indent2
