from collections import OrderedDict
from pathlib import Path

import platformdirs

from src.core.settings_manager import settings_manager

# 基本信息
APP_NAME = "Hexo Helper"
# 路径
ROOT_PATH = Path(__file__).parent.resolve()
ASSETS_PATH = ROOT_PATH / "assets"

# 配置
DEFAULT_SETTINGS = {
    "language": "en",
}
APP_DATA_DIR = Path(platformdirs.user_data_dir()) / APP_NAME
SETTINGS_FILE_PATH = APP_DATA_DIR / "settings.json"
settings_manager.set_settings_path(SETTINGS_FILE_PATH)
config = settings_manager.load_settings()
if not config:
    config = DEFAULT_SETTINGS
    settings_manager.save_settings(config)

# i18n
LOCALE_DIR = ROOT_PATH / "locale"
DOMAINS = ["_", "settings", "content", "file", "deploy"]  # "_" 代表直属目录下的文件

LANGUAGE = config.get("language", "en")
# 设置中可选的语言
languages = OrderedDict(
    {
        "en": "English",
        "zh-cn": "简体中文",
        "zh-tw": "繁體中文",
    }
)
