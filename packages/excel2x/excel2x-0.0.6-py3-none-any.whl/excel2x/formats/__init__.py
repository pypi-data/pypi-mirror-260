# 初始化 formatter
from .formatter import DataFormatter
from .formatter import add_formatter
from .formatter import get_formatter
from .json_fmt import JsonFormatter
from .lua_fmt import LuaFormatter

# 注册 json
add_formatter("json", JsonFormatter(style="list"))
add_formatter("json-list", JsonFormatter(style="list"))
add_formatter("json-map", JsonFormatter(style="map"))
add_formatter("json-column", JsonFormatter(style="column"))

# 注册 lua
add_formatter("lua", LuaFormatter(style="list", with_schema=True))
add_formatter("lua-list", LuaFormatter(style="list", with_schema=True))
add_formatter("lua-map", LuaFormatter(style="map", with_schema=True))
add_formatter("lua-column", LuaFormatter(style="column", with_schema=False))
