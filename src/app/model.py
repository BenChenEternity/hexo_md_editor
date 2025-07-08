from src.app.constants import EVENT_LANGUAGE_CHANGED
from src.core.event_bus import Producer


class MainModel(Producer):
    """
    应用程序的数据模型。
    这个类是所有应用状态的“单一数据源 (Single Source of Truth)”。
    它不关心这些数据如何显示，只负责存储和管理。
    """

    def __init__(self):
        """
        初始化模型的所有属性。
        """
        super().__init__()
        self.app_name = "Hexo Helper"
        self.current_language = 'en'
        self.command_output = ""

    def get_current_language(self):
        return self.current_language

    def set_current_language(self, language_code):
        if self.current_language != language_code:
            self.current_language = language_code
            self.send_event(EVENT_LANGUAGE_CHANGED, new_lang=language_code)

    def get_app_name(self):
        return self.app_name
