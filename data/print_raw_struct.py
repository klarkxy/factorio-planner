import os

import locale

"""
打印所有数据结构
"""
PWD = os.path.dirname(os.path.abspath(__file__))


def scan():
    from load_raw_data import raw_data

    ret = ""
    for k, v in raw_data.items():
        print(k)
        ret = ret + f"{k}({locale.get(k)}):\n"
        struct = {}
        for k1, v1 in v.items():
            for k2, v2 in v1.items():
                if k2 not in struct:
                    struct[k2] = type(v2)
                elif struct[k2] != type(v2):
                    if isinstance(struct[k2], list):
                        if type(v2) not in struct[k2]:
                            struct[k2].append(type(v2))
                    else:
                        struct[k2] = [struct[k2], type(v2)]
        for k1, v1 in struct.items():
            ret = ret + f"  {k1}({locale.get(k1)}): {v1}\n"
    return ret


if __name__ == "__main__":
    x = scan()
    with open(os.path.join(PWD, "data_struct.yaml"), "w", encoding="utf-8") as f:
        f.write(x)
