import os
import yaml

from load_raw_data import raw_data

PWD = os.path.dirname(os.path.abspath(__file__))


class Recipe:
    def __init__(self, k: str, v: dict):
        self.name: str = k
        # 分析原料
        ingredients: dict[str, int] = {}
        for x in v.get("ingredients", {}):
            ingredients[x["name"]] = x["amount"]
        # 分析产物
        results: dict[str, int] = {}
        for x in v.get("results", {}):
            results[x["name"]] = x["amount"]
        self.time: float = (v.get("energy_required", 0),)
        self.ingredients = (ingredients,)
        self.results = (results,)
        self.allow_productivity: bool = (v.get("allow_productivity", False),)
        self.allow_quality: bool = (v.get("allow_quality", False),)
        self.category: str = (v.get("category", "unkonwn"),)


# 读取配方数据
def load_recipes():
    recipes = {}
    raw_recipes = raw_data["recipe"]
    # 提取出配方中的数据
    for k, v in raw_recipes.items():
        recipes[k] = Recipe(k, v)

    return recipes


recipes = load_recipes()


# 读取流体列表
def load_fluids():
    fluids = []
    raw_fluid = raw_data["fluid"]
    for k, v in raw_fluid.items():
        name = k
        fluids.append(name)
    return fluids


fluids = load_fluids()


# 读取机器数据
class Machine:
    def __init__(self, k: str, v: dict):
        self.name: str = k
        self.speed: float = v["crafting_speed"]
        self.module_slots: int = v["module_slots"]
        self.energy_usage: float = v["energy_usage"]
        self.ingredient_count: int = v["ingredient_count"]


def load_machines():
    machine_type = [
        "furnace",
        "beacon",
        "mining-drill",
        "rocket-silo",
        "assembling-machine",
        "lab",
    ]
    machines = {}
    for t in 