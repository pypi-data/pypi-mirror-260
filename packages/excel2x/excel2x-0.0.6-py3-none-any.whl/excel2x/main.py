#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""Convert Excel config to X
"""
import os
import json
import shutil
import argparse
from pathlib import Path
from ._version import __version__
from .utils import set_log_level
from .utils import get_log_level
from .utils import log_debug
from .utils import log_info
from .utils import log_error
from .utils import print_line
from .utils import read_file
from .utils import write_file
from .core import DataBook

# pylint:disable=W0718


def read_config(config_path: str) -> dict:
    """读取项目配置

    Args:
        config_path (str): 项目配置 json 路径

    Returns:
        dict: 项目配置 json dict 对象
    """
    config_path = Path(str(config_path))
    if config_path.exists() and config_path.suffix == ".json":
        config_text = read_file(config_path)
        proj_config = json.loads(config_text)
        is_check_ok = True
        for key in ["name", "root_dir", "config_dir", "output_dir", "copy_dir", "groups", "option_template"]:
            if key not in proj_config:
                log_error(f"config 缺少配置: {key}")
                is_check_ok = False
        if is_check_ok:
            return proj_config

    log_error(f"config 路径不存在或不是 json 格式：{config_path.resolve()}")

    cur_path = Path(__file__).absolute().parent
    temp_config_path = cur_path.joinpath("config_template.json")
    log_error("请参考 config 模板:")
    log_info("config_path", read_file(temp_config_path))
    raise ValueError("config 异常")


def create_proj_config(proj_config_path: str | Path, proj_name: str):
    """根据模板 config_template.json 选择创建标准项目配置

    Args:
        proj_dir (str | Path): 项目路径/config.json
        proj_name (str): 项目名称

    Raises:
        FileNotFoundError: 找不到项目路径，请先创建项目
    """
    proj_config_path = str(proj_config_path)
    if not proj_config_path.endswith(".json"):
        # 配置文件需要是 json 文件
        raise ValueError("配置文件需要是 json 文件, 例如：项目路径/config.json")

    if not Path(proj_config_path).parent.exists():
        # 项目路径不存在
        raise FileNotFoundError("project_dir not found! Please create a project first!")

    temp_config_path = Path(__file__).with_name("config_template.json")
    config_text = read_file(temp_config_path).replace("{project_name}", str(proj_name))
    write_file(proj_config_path, config_text)
    if Path(proj_config_path).exists():
        log_info(f"Create {proj_config_path} successful!")
    else:
        log_error(f"Create {proj_config_path} Failed!")


def is_data_file(file_name: str) -> bool:
    """判断文件名是否 Excel 或 csv 文件

    Args:
        file_name (str): Excel 文件名

    Returns:
        bool: 是否是 Excel 文件
    """
    if not file_name.startswith("~") and not file_name.startswith(".") and (file_name.endswith(".csv") or file_name.endswith(".xlsx")):
        return True
    return False


def convert_config(config_path: str, include_groups="", include_names="", is_copy=False, log_level="info"):
    """开始转换 Excel to X

    Args:
        config_path (str): 项目配置路径 xxx.json
        group (str, optional): 筛选分组，默认全部.
        include (str, optional): 筛选文件名，默认全部.
        is_copy (bool, optional): 是否复制到 copy_dir 路径一份副本. Defaults to False.
    """
    try:
        set_log_level(log_level)
        print_line("convert_config")
        log_info("config".ljust(8), ":", config_path)
        log_info("groups".ljust(8), ":", include_groups)
        log_info("includes".ljust(8), ":", include_names)
        log_info("copy".ljust(8), ":", is_copy)
        log_info("LogLevel".ljust(8), ":", get_log_level())
        proj_config = read_config(config_path)
        target_name = proj_config["name"]
        root_dir = Path(config_path).parent.joinpath(proj_config["root_dir"]).resolve()
        os.chdir(root_dir)
        print_line("Project")
        log_info("name".ljust(8), ":", target_name)
        log_info("root".ljust(8), ":", root_dir)
        print_line()
        select_group_dict = {name.lower(): True for name in (include_groups or "").split(",") if len(name) > 0}
        select_name_dict = {name.lower(): True for name in (include_names or "").split(",") if len(name) > 0}

        config_dir = root_dir.joinpath(proj_config["config_dir"]).resolve()
        output_dir = root_dir.joinpath(proj_config["output_dir"]).resolve()
        copy_dir = root_dir.joinpath(proj_config["copy_dir"]).resolve()
        groups = proj_config["groups"]
        option_template: dict = proj_config["option_template"]
        for option in option_template.values():
            if "copy_dir" in option and len(option["copy_dir"]) > 0:
                option["copy_dir"] = root_dir.joinpath(option["copy_dir"]).resolve()
            else:
                option["copy_dir"] = copy_dir.resolve()
            if "output_dir" in option and len(option["output_dir"]) > 0:
                option["output_dir"] = root_dir.joinpath(option["output_dir"]).resolve()
            else:
                option["output_dir"] = output_dir.resolve()

        group_iterdir = sorted([x for x in config_dir.iterdir() if x.is_dir()])
        for item in group_iterdir:
            # group 名称
            group_name = item.stem
            array = group_name.split("_")
            # group 基本名
            group_base = array[0]
            # group 变体名
            # group_variant = array[1] if len(array) > 1 else ""
            if group_base not in groups:
                # 找不到 group: {group_base} 配置!
                continue
            if len(select_group_dict) > 0 and group_name.lower() not in select_group_dict:
                # 未选中 group
                continue
            print_line("Convert group: " + group_name)
            option_list = groups[group_base]
            file_iterdir = sorted([x for x in item.iterdir() if is_data_file(x.name) and (len(select_name_dict) == 0 or x.stem.lower() in select_name_dict)])
            for excel_file in file_iterdir:
                log_info(f">> Convert: {excel_file.relative_to(root_dir)}")
                data_book = DataBook().load_book(excel_file)
                for option in option_list:
                    if isinstance(option, str):
                        option: dict = option_template[option]
                    assert isinstance(option, dict), f"找不到配置模板: {option}, 请先在 option_template 中添加!"
                    log_debug("-- style:", option["style"])
                    _output_path = option["output_dir"].joinpath(group_name, excel_file.stem).with_suffix(option["suffix"])
                    log_debug("-- target:", _output_path)
                    _out_files = data_book.export_file(option["style"], _output_path)
                    for item in _out_files:
                        log_debug("---- output:", item)
                        if is_copy:
                            copy_to = Path(option["copy_dir"].joinpath(group_base, item.name)).resolve()
                            copy_to.parent.mkdir(parents=True, exist_ok=True)
                            log_info(f"-- Copy to: {copy_to}")
                            shutil.copy(item, copy_to)
            print_line()
            log_info("")
    except Exception as e:
        log_error(e)
    finally:
        log_info("Have a nice day!")


def convert_one(input_path, output_path, formatter) -> list[str]:
    """convert_one"""
    data_book = DataBook()
    data_book.load_book(input_path)
    return data_book.export_file(formatter, output_path)


def main():
    """命令行执行"""
    print(f"Welcome to excel2x: v{__version__}")
    print(">>")
    parser = argparse.ArgumentParser(description="转换 Excel 配置表")
    parser.add_argument("-V", "--version", action="version", version=__version__, help="Display version")
    parser.add_argument("--log", dest="log", default="info", choices=["debug", "info", "warn", "error"], type=str.lower, help="log 信息级别")
    # 转换 Excel by config
    group = parser.add_argument_group("convert by config")
    group.add_argument("--config", dest="config", help="目标项目 config.json 配置文件")
    # 转换 Excel by file
    group = parser.add_argument_group("convert one Excel")
    group.add_argument("-i", "--input", dest="input", help="输入 Excel 文件路径")
    group.add_argument("-o", "--output", dest="output", help="输出目录或文件路径")
    group.add_argument("-f", "--format", dest="json", help="格式转换器. json / lua")
    # 生成项目配置参数
    group = parser.add_argument_group("create project config")
    group.add_argument("--create", action="store_true", help="创建项目配置")
    group.add_argument("--name", dest="name", default="project_name", help="项目名称")

    # 解析参数
    args = parser.parse_args()
    print("args: ", args.__dict__)
    if args.create is True:
        # 创建项目配置
        create_proj_config(args.config, args.name)
    elif args.config is not None:
        # config
        convert_config(args.config, log_level=args.log)
    elif args.input is not None:
        # 单文件
        convert_one(args.input, args.output, args.format)


if __name__ == "__main__":
    main()
