from collections import OrderedDict
from pathlib import Path

import platformdirs

ROOT_PATH = Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

APP_DATA_DIR = Path(platformdirs.user_data_dir()) / "HexoHelper"
SETTINGS_FILE_PATH = APP_DATA_DIR / "settings.json"

# 设置中可选的语言
languages = OrderedDict({
    "en": "English",
    "zh-cn": "简体中文",
    "zh-tw": "繁體中文",
})

DEFAULT_SETTINGS = {
    "language": "en",
}
