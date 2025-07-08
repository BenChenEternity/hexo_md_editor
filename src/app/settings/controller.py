import logging

from constants import LANGUAGES

logger = logging.getLogger(__name__)


class SettingsController:
    def __init__(self, main_controller, settings_view, main_model):
        self.main_controller = main_controller
        self.settings_view = settings_view
        self.main_model = main_model

    def on_toggle_language(self, event):
        """
        当用户在下拉框中选择了新的语言
        """
        selected_language_name = event.widget.get()

        lang_map = {v: k for k, v in LANGUAGES.items()}
        selected_language = lang_map.get(selected_language_name)

        if not selected_language:
            # 将翻译后的信息和调试上下文一起记录到日志中
            logger.error(
                f"Error: No such language. Invalid value received: '{selected_language_name}'. Defaulting to 'en'."
            )
            selected_language = "en"

        self.main_controller.change_language(selected_language)
