# -*- coding: utf-8 -*

"""formatter
"""
from pathlib import Path


class DataFormatter:
    """数据格式化器基类"""

    def __init__(self):
        pass

    def format(self, data) -> str:
        """格式化为字符串"""
        raise NotImplementedError

    def export(self, data, file_path: Path) -> list[Path]:
        """导出为文件"""
        raise NotImplementedError


_local_formatter_dict = {}


def add_formatter(name: str, formatter: DataFormatter):
    """get_formatter"""
    assert isinstance(formatter, DataFormatter), f"Invalid formatter: {formatter}"
    _local_formatter_dict[name] = formatter


def get_formatter(formatter: str | DataFormatter) -> DataFormatter:
    """get_formatter"""
    _formatter = formatter
    if isinstance(formatter, str):
        _formatter = _local_formatter_dict.get(formatter)
    assert isinstance(_formatter, DataFormatter), f"Invalid formatter: {formatter}"
    return _formatter
