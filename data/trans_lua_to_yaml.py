import os
import copy
import yaml
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


python_dict = lua_table_to_dict(lua_table)

# 生成原始yaml文件
RAW_YAML = os.path.join(PWD, 'raw.yaml')
with open(RAW_YAML, "w", encoding="utf-8") as f:
    yaml.dump(python_dict, f, allow_unicode=True)

raw_recipes = python_dict['recipe']

# 生成配方yaml
RAW_REPICES_FILE = os.path.join(PWD, 'raw_recipes.yaml')
with open(RAW_REPICES_FILE, "w", encoding="utf-8") as f:
    yaml.dump(raw_recipes, f, allow_unicode=True)

recipes = {}
recipes_zh = {}

# 读取locale文件 - 中文翻译
LOCALE_FILE = os.path.join(PWD, 'locale.yaml')
if os.path.exists(LOCALE_FILE):
    with open(LOCALE_FILE, "r", encoding="utf-8") as f:
        locale = yaml.load(f.read(), Loader=yaml.FullLoader)
else:
    locale = {}

def get_locale(k : str) -> str:
    if k not in locale:
        kk = k
        locale[k] = kk
    if isinstance(locale[k], list):
        return locale[k][0]
    return locale[k]

# 提取出配方中的数据
for k, v in raw_recipes.items():
    name = k
    name_zh = get_locale(name)
    time = v.get('energy_required', 0)

    # 分析原料
    ingredients = {}
    ingredients_zh = {}
    for x in v.get('ingredients', {}):
        ingredients[x['name']] = x['amount']
        ingredients_zh[get_locale(x['name'])] = x['amount']
    # 分析产物
    results = {}
    results_zh = {}
    for x in v.get('results', {}):
        results[x['name']] = x['amount']
        results_zh[get_locale(x['name'])] = x['amount']
    recipes[name] = {
        'time': time,
        'ingredients': ingredients,
        'results': results,
    }
    recipes_zh[name_zh] = {
        '用时': time,
        '原料': ingredients_zh,
        '产品': results_zh,
    }

# 输出配方yaml
RECIPES_FILE = os.path.join(PWD, 'recipes.yaml')
with open(RECIPES_FILE, "w", encoding="utf-8") as f:
    yaml.dump(recipes, f, allow_unicode=True)
    
# 输出中文配方表
RECIPES_ZH_FILE = os.path.join(PWD, 'recipes_zh.yaml')
with open(RECIPES_ZH_FILE, "w", encoding="utf-8") as f:
    yaml.dump(recipes_zh, f, allow_unicode=True)

# 覆写locale文件，用于手动添加汉化
with open(LOCALE_FILE, "w", encoding="utf-8") as f:
    yaml.dump(locale, f, allow_unicode=True)