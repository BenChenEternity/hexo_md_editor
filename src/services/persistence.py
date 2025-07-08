from src.app.constants import EVENT_LANGUAGE_CHANGED
from src.core.event_bus import Consumer
from src.core.settings_manager import settings_manager


class PersistenceService(Consumer):
    """
    一个后台服务，负责将应用程序的状态持久化到磁盘。
    它通过监听事件总线上的事件来触发保存操作。
    """

    def __init__(self):
        super().__init__()
        # 订阅关心的事件
        self.subscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)

    def on_language_changed(self, new_lang: str):
        settings_manager.update_setting("language", new_lang)

    def close(self):
        self.unsubscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)
