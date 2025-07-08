import json
from pathlib import Path
from typing import Dict, Any


class SettingsManager:
    """
    负责以 JSON 格式加载和保存应用程序的设置。
    """

    def __init__(self):
        self.settings_path = None

    def set_settings_path(self, settings_path: Path):
        self.settings_path = settings_path

    def load_settings(self) -> Dict[str, Any]:
        if not self.settings_path.exists():
            return {}
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}. Starting with default settings.")
            return {}

    def save_settings(self, settings: Dict[str, Any]):
        try:
            # 新增：在写入文件前，确保其所在的目录存在。
            # exist_ok=True 表示如果目录已存在，则不抛出异常。
            # parents=True 表示如果父目录不存在，也一并创建。
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving settings: {e}")

    def update_setting(self, key: str, value: Any) -> None:
        current_settings = self.load_settings()
        current_settings[key] = value
        self.save_settings(current_settings)


settings_manager = SettingsManager()
