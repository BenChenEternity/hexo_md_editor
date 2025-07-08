from src.app.constants import EVENT_LANGUAGE_CHANGED
from src.core.settings_manager import settings_manager
from src.core.event_bus import Consumer


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
        """
        当语言设置发生变化时，此方法被调用。
        """
        print(f"Language changed to '{new_lang}', saving setting...")
        settings_manager.update_setting('language', new_lang)

    def close(self):
        """
        在应用关闭时，取消所有订阅。
        """
        self.unsubscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)
