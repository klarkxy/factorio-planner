"""
根据指定的路径，查找对应的数据所在的位置
"""


def match(data: dict | str, road: list, current_road: list = [], head: bool = True):
    if len(road) == 0:  # 找到了
        print(current_road)
        return
    if isinstance(data, str):
        if road[0] == data:
            print(current_road, data)
            return
        else:
            return
    elif isinstance(data, dict):
        if road[0] in data:
            match(data[road[0]], road[1:], current_road + [road[0]], False)
        elif head:  # 如果还没找到头，那就允许更深入的搜索
            for k, v in data.items():
                match(v, road, current_road + [k])


def find(road: list):
    from load_raw_data import raw_data

    match(raw_data, road)


if __name__ == "__main__":
    find(["allowed_effects"])
