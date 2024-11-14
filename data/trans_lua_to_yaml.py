import os
import yaml

from load_raw_data import raw_data
import data.locale as locale

PWD = os.path.dirname(os.path.abspath(__file__))

# 生成原始yaml文件
RAW_YAML = os.path.join(PWD, 'raw.yaml')
with open(RAW_YAML, "w", encoding="utf-8") as f:
    yaml.dump(raw_data, f, allow_unicode=True)

raw_recipes = raw_data['recipe']

# 生成配方yaml
RAW_REPICES_FILE = os.path.join(PWD, 'raw_recipes.yaml')
with open(RAW_REPICES_FILE, "w", encoding="utf-8") as f:
    yaml.dump(raw_recipes, f, allow_unicode=True)

recipes = {}
recipes_zh = {}

locale.load()

# 输出配方yaml
RECIPES_FILE = os.path.join(PWD, 'recipes.yaml')
with open(RECIPES_FILE, "w", encoding="utf-8") as f:
    yaml.dump(recipes, f, allow_unicode=True)
    
# 输出中文配方表
RECIPES_ZH_FILE = os.path.join(PWD, 'recipes_zh.yaml')
with open(RECIPES_ZH_FILE, "w", encoding="utf-8") as f:
    yaml.dump(recipes_zh, f, allow_unicode=True)

## 找到所有物品
# 液体
fluid = []
raw_fluid = raw_data['fluid']
for k, v in raw_fluid.items():
    name = k
    fluid.append(name)

FLUID_FILE = os.path.join(PWD, 'fluid.yaml')
with open(FLUID_FILE, "w", encoding="utf-8") as f:
    yaml.dump({'fluid': fluid}, f, allow_unicode=True)



locale.save()