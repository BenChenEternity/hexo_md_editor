from constants import languages
from . import _


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
        selected_language = None
        for key, value in languages.items():
            if value == selected_language_name:
                selected_language = key
                break
        if not selected_language:
            print(_("Error: No such language"))
            selected_language = "en"

        self.main_controller.change_language(selected_language)
