#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""Convert Excel config to X
"""
from pathlib import Path

from .excel_reader import read_book_values
from .excel_reader import convert_value

from .formats.formatter import get_formatter


class DataBook:
    def __init__(self, name="", titles: list[str] = None, types: list[str] = None, keys: list[str] = None, values: list[list] = None):
        self._name = name
        self._keys = keys or []
        self._titles = titles or []
        self._types = types or []
        self._values = values or []

    def __str__(self) -> str:
        _temp = []
        if len(self._keys) > 0:
            _temp.append(self._titles)
            _temp.append(self._types)
            _temp.append(self._keys)
            for _v in self._values:
                _temp.append(_v)
        return str(_temp)

    @property
    def name(self):
        """name"""
        return self._name

    @property
    def values(self):
        """values"""
        return self._values

    @property
    def titles(self):
        """titles"""
        return list(self._titles)

    @property
    def keys(self):
        """keys"""
        return list(self._keys)

    @property
    def types(self):
        """types"""
        return list(self._types)

    @property
    def schema(self):
        """schema"""
        return {self._keys[i]: {"type": self._types[i], "title": self._titles[i]} for i in range(len(self._keys))}

    def dict(self) -> dict:
        """dict"""
        return {"schema": self.schema, "data": self._values}

    def data_list(self):
        """data_list"""
        return [dict(zip(self._keys, row)) for row in self._values]

    def data_map(self, primary_key=None):
        """data_map"""
        if primary_key is None:
            # 如果没有设置主键，就从 titles 描述里面找有没有设置 主键 或 primary
            _primary_arr = [i for i, x in enumerate(self._titles) if ("主键" in x or "primary" in x)]
            if len(_primary_arr) > 0:
                primary_key = self._keys[_primary_arr[0]]
        if primary_key in self._keys:
            _data_map = {}
            for row in self._values:
                _data = dict(zip(self._keys, row))
                _data_map[_data[primary_key]] = _data
            return _data_map
        raise ValueError(f"{self.name} 没有主键 {primary_key}")

    def column_map(self):
        """column_map"""
        _data_split = {}
        for i, key in enumerate(self._keys):
            _temp_list = []
            for row in self.values:
                _temp_list.append(row[i])
            _data_split[key] = _temp_list
        return _data_split

    def load_book(self, file_path: str | Path, sheet_index=0, title_line=0, type_line=1, key_line=2):
        """从 Excel 加载工作簿数据

        Args:
            file_path (str | Path): 输入 Excel 文件路径
            sheet_index (int, optional): 工作薄 index, 默认 0.
            title_line (int, optional): 字段描述行号(从 0 开始)，默认 0.
            type_line (int, optional): 字段类型行号(从 0 开始)，默认 1.
            key_line (int, optional): 字段名行号(从 0 开始)，默认 2.

        Returns:
            DataBook: 返回自身
        """
        _input_file = Path(file_path)
        value_line = max(title_line, type_line, key_line) + 1
        self._name = _input_file.stem
        # 读取 Excel
        _all_values = read_book_values(_input_file, sheet_index)
        # 需要忽略的列
        _del_cols = [i for i, key in enumerate(_all_values[key_line]) if key.startswith("ignore_")]
        # 倒叙遍历 _del_cols
        for i in _del_cols[::-1]:
            for row in _all_values:
                del row[i]
        # 属性名
        self._keys = _all_values[key_line]
        # 标题描述
        self._titles = _all_values[title_line]
        # 类型定义
        self._types = _all_values[type_line]
        # 值列表
        self._values = _all_values[value_line:]
        # 处理重复 key

        _keys_map = {}
        for i, key in enumerate(self._keys):
            if key in _keys_map:
                _key2 = f"{key}2"
                self._keys[i] = _key2
                print("\033[1;31m" + f"[ValueError] {self._name} 属性名重复！key: {key} 自动重命名为 {_key2}\033[0m")
                key = _key2
            _keys_map[key] = True
        _keys_map.clear()
        _keys_map = None
        # 处理转换 value 类型
        for i, row in enumerate(self._values):
            for j, value in enumerate(row):
                row[j] = convert_value(value, self._types[j], self._keys[j], value_line + i)
        return self

    def export_str(self, formatter) -> str:
        """导出数据字符串

        Args:
            formatter (str | DataFormatter): 格式器

        Returns:
            str: 格式器转换后字符串
        """
        _formatter = get_formatter(formatter)
        return _formatter.format(self)

    def export_file(self, formatter, file_path: str | Path, *args) -> list[Path]:
        """导出数据文件

        Args:
            file_path (str): 文件路径
            formatter (str | DataFormatter): 格式器
        """
        _formatter = get_formatter(formatter)
        return _formatter.export(self, Path(file_path), *args)
