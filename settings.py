import logging
from collections import OrderedDict
from pathlib import Path

import platformdirs

# --- 基本信息 ---
APP_NAME = "Hexo Helper"

# --- 路径定义 ---
ROOT_PATH = Path(__file__).parent.resolve()
ASSETS_PATH = ROOT_PATH / "assets"
LOCALE_DIR = ROOT_PATH / "locale"

# --- 用户数据路径 (持久化) ---
# 使用 platformdirs 手动构建，确保路径唯一性
BASE_DATA_DIR = Path(platformdirs.user_data_dir())
APP_DATA_DIR = BASE_DATA_DIR / APP_NAME
SETTINGS_FILE_PATH = APP_DATA_DIR / "settings.json"
LOG_FILE_PATH = APP_DATA_DIR / "app.log"

# --- 默认配置 ---
DEFAULT_SETTINGS = {
    "language": "en",
}

# --- i18n ---
DOMAINS = ["_", "settings", "content", "file", "deploy"]
# 设置中可选的语言
LANGUAGES = OrderedDict(
    {
        "en": "English",
        "zh-cn": "简体中文",
        "zh-tw": "繁體中文",
    }
)

LOGGER_LEVEL = logging.INFO

try:
    from local_settings import *  # noqa
except ImportError:
    pass
