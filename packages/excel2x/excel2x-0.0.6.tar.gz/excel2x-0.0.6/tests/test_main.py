#!/usr/bin/env python3
# -*- coding: utf-8 -*

import os
import sys
import pathlib

root_dir = pathlib.Path(__file__).absolute().parent.parent
sys.path.insert(0, str(root_dir.joinpath("src")))


from excel2x import __version__ as x_version
from excel2x import DataBook
from excel2x import DataFormatter
from excel2x import JsonFormatter
from excel2x import convert_config


# using pytest
def main():
    print("__version__:", x_version)

    test_export_excel("lua", "shop")
    test_export_excel("json", "shop")
    test_export_excel("lua", "klondike_seed_3")
    test_export_excel("json-list", "klondike_seed_3")
    test_export_excel("json-map", "Language_Game")
    test_export_excel("json-column", "Language_Game")


def test_export_excel(formatter, name):
    print("test_export_excel", formatter, name)
    data_book = DataBook()
    data_book.load_book(f"tests/{name}.xlsx")
    data_book.export_file(formatter, "tests/temp")


def test_convert_config():
    _config = pathlib.Path(__file__).absolute().parent.joinpath("config.json")
    convert_config(_config, is_output=True, log_level="info")


if __name__ == "__main__":
    print(os.getcwd(), ":", x_version)
    # main()
    # test_x()
    test_convert_config()
