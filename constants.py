from collections import OrderedDict
from pathlib import Path

ROOT_PATH = Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

# 设置中可选的语言
languages = OrderedDict({
    "en": "English",
    "zh-cn": "简体中文",
    "zh-tw": "繁體中文",
})
