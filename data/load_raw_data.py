import os
from lupa import LuaRuntime

PWD = os.path.dirname(os.path.abspath(__file__))
RAW_LUA = os.path.join(PWD, 'raw.lua')


lua = LuaRuntime(unpack_returned_tuples=True)

with open(RAW_LUA, "r", encoding="utf-8") as file:
    lua_code = file.read()

lua_table = lua.execute(lua_code)

def lua_table_to_dict(lua_table):
    if isinstance(lua_table, (str, int, float)):
        return lua_table
    if hasattr(lua_table, 'items'):
        x = {k: lua_table_to_dict(v) for k, v in lua_table.items()}
        is_array = True
        for k, v in x.items():
            if not isinstance(k, int):  # 存在不是整数的key，按对象处理
                is_array = False
                break
        if is_array:
            return [v for k, v in sorted(x.items())]
        return x
    if hasattr(lua_table, '__iter__'):
        return [lua_table_to_dict(v) for v in lua_table]
    return lua_table

raw_data = lua_table_to_dict(lua_table)


