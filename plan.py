import math
import data

Items = dict[tuple[str, int], float]  # (名字， 品质) = 数量


class Triplet:
    def __init__(
        self, speed: float = 0, productivity: float = 0, quality: float = 0
    ) -> None:
        self.speed = speed
        self.productivity = productivity
        self.quality = quality

    def __add__(self, other):
        return Triplet(
            self.speed + other.speed,
            self.productivity + other.productivity,
            self.quality + other.quality,
        )

    def __mul__(self, amount: float):
        return Triplet(
            self.speed * amount, self.productivity * amount, self.quality * amount
        )


class Module:
    # 各种插件效果计算
    def __init__(self, name: str, triplet: Triplet):
        self.name = name
        self.triplet = triplet

    def calc(self, count: int = 1) -> Triplet:
        return self.triplet * count


speed_module = Module("speed-module-3", Triplet(speed=0.5, quality=-0.025))
productivity_module = Module(
    "productivity-module-3", Triplet(speed=-0.15, productivity=0.1)
)
quality_module = Module("quality-module-3", Triplet(speed=-0.05, quality=0.025))


class Tower:
    # 插件塔，只能插2个速度
    def __init__(self, count: int = 1) -> None:
        self.count = count
        self.module = speed_module

    def calc(self) -> Triplet:
        proportion = math.sqrt(self.count)
        return self.module.calc(2) * proportion


class Step:
    def __init__(
        self, r: data.Recipe, m: data.Machine, a: int, module: Module, tower: Tower
    ):
        self.recipe = r
        self.machine = m
        self.amount = a
        self.module = module
        self.tower = tower

    def do(self, items: Items):
        t = self.tower.calc() + self.module.calc(self.machine.module_slots)
        # 计算时间: 做完一次配方需要的实际时间
        time = self.recipe.time / (1 + t.speed) / self.machine.speed
        # 计算产量：做完一次配方实际的产量
        results = {
            k: v * (1 + t.productivity)  # 产量 = 配方产量 * (1 + 生产插件效果)
            for k, v in self.recipe.results.items()
        }
        # 获取原料：做完一次实际消耗的原料
        ingredients = self.recipe.ingredients
        # 计算每秒实际产量
        results_pre_second = {k: v / time for k, v in results.items()}
        # 计算每秒实际消耗
        ingredients_pre_second = {
            k: v / time for k, v in ingredients.items() if k in items
        }
        # 更新到items中
        for k, v in results_pre_second.items():
            # 找到对应物品，看看品质
            q = 1  # 默认白品
            if k not in data.fluids:  # 流体只有白品，不用考虑
                for kk in items.keys():
                    if kk[0] == k:
                        q = kk[1]
                        break
            # 去掉产物
            items[(k, q)] = items.get((k, q), 0) - v * self.amount
            # 增加原料
            if q > 1 and t.quality > 0:  # 存在升品的情况
                q -= 1  # 原料降1品
                # 根据品质计算原料需求
                ingredients_pre_second = {
                    k: v / t.quality for k, v in ingredients_pre_second.items()
                }
            for k, v in ingredients_pre_second.items():
                items[(k, q)] = items.get((k, q), 0) + v * self.amount


class Plan:

    def __init__(self):
        self.items: Items = {}  # 原料列表 (名字， 品质) = 数量
        self.road: list[Step] = []  # 配方路径[步骤]

    def do(self, step: Step):
        step.do(self.items)
        self.road.append(step)

    def is_repeated(self, other):
        # 判断当前方案是否重复
        # 具体体现在物品和品质相同，但是另一个方案的数量比当前方案的数量大
        # 返回-1表示当前方案比另一个方案更少，判定为对方重复
        # 返回1表示当前方案比另一个方案更多，判定为当前方案重复
        # 返回0表示两个方案不相上下，不判定为重复
        p = 0
        n = 0
        for k, v in other.items():
            x = self.items.get(k, 0) - v
            if x > 0:
                p += 1  # 当前比对方多
            else:
                n += 1  # 当前比对方少
        if n == 0:  # 当前方案比对方少
            return -1
        elif p == 0:  # 当前方案比对方多
            return 1
        else:
            return 0
