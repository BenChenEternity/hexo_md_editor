from src.core.mvc_template.event_bus import Consumer
from src.core.settings_manager import SettingsManager


class PersistenceService(Consumer):
    """
    一个后台服务，负责将应用程序的状态持久化到磁盘。
    它通过监听事件总线上的事件来触发保存操作。
    """

    def __init__(self, settings_manager: SettingsManager):
        super().__init__()
        # 订阅关心的事件
        # self.subscribe(EVENT_MAIN_MODEL_LANGUAGE_CHANGED, self.on_language_changed)
        self.settings_manager = settings_manager

    def on_language_changed(self, new_lang: str):
        self.settings_manager.update_setting("language", new_lang)

    def close(self):
        # self.unsubscribe(EVENT_MAIN_MODEL_LANGUAGE_CHANGED, self.on_language_changed)
        pass
