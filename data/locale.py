import os
import traceback
import yaml
import atexit

PWD = os.path.dirname(os.path.abspath(__file__))
LOCALE_FILE = os.path.join(PWD, "locale.yaml")
if os.path.exists(LOCALE_FILE):
    with open(LOCALE_FILE, "r", encoding="utf-8") as f:
        locale = yaml.load(f.read(), Loader=yaml.FullLoader)
else:
    locale = {}


def save():
    with open(LOCALE_FILE, "w", encoding="utf-8") as f:
        yaml.dump(locale, f, allow_unicode=True)


atexit.register(save)


def do_translate(s: str):
    from translate import Translator

    translater = Translator(to_lang="chinese")
    out = translater.translate(s)
    return out


def get(k: str) -> str:
    if k not in locale:
        try:
            v = do_translate(k)
        except Exception as e:
            # traceback.print_exc()
            v = k
        locale[k] = v
    if isinstance(locale[k], list):
        return locale[k][0]
    return locale[k]


def alias(k: str, v: str, front: bool = False):
    if k not in locale:
        locale[k] = v
        return
    if isinstance(locale[k], list):
        if front:
            locale[k].insert(0, v)
        else:
            locale[k].append(v)
    else:
        if front:
            locale[k] = [v, locale[k]]
        else:
            locale[k] = [locale[k], v]
