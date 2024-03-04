# excel2x

## 转换 Config 配置工具 excel2x

`Python3` 库 `excel2x`。只需要用工具生成自己项目的配置文件，就可以按照配置文件导`Excel`表了。现在支持 `csv`、`lua`、`json` 格式，后面后继续扩展 `xml` 等格式。

支持生成数据格式 `Schema` 接口，现在支持 `Lua table`、`TypeScript interface`，后面会支持 `Java Class` 和 `C# Class`。

---

## 安装

```bash
pip install excel2x
```

## 使用方式

### 查看帮助

```bash
python3 -m excel2x -h
# or
excel2x-cli -h
```

### 创建项目配置

```bash
python3 -m excel2x --config project_path/config.json --name project_name --create
# or
excel2x-cli --config project_path/config.json --name project_name --create
```

### 命令行转换 Excel

#### 按 config.json 配置转换

```bash
python3 -m excel2x --config project_path/config.json
# or
excel2x-cli --config project_path/config.json
```
#### 转换单个文件

```
excel2x-cli -i xxx/xxx.xlsx -o project_path/xxx.json -f json
```

### 在 `Python` 脚本中使用

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*

from excel2x import convert_config
from excel2x import convert_one

if __name__ == "__main__":
    # 项目配置路径
    proj_config_path = "project_path/config.json"
    convert_config(proj_config_path)

    # 单个文件转换
    convert_one("xxx/xxx.xlsx", "project_path/xxx.json", "json")

```
