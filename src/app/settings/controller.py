import logging

from src.app.constants import EVENT_MAIN_SETTINGS_UI_LANGUAGE_SELECTED
from src.core.mvc_template.controller import Controller as BaseController
from src.core.mvc_template.model import Model

logger = logging.getLogger(__name__)


class SettingsController(BaseController):
    """
    设置控制器。
    完全遵循 BaseController 模板。
    """

    def __init__(self, model: Model):
        super().__init__(model)

    def _setup_handlers(self):
        self.subscribe(EVENT_MAIN_SETTINGS_UI_LANGUAGE_SELECTED, self.on_language_selected)

    def on_language_selected(self, lang_code: str):
        if lang_code != self.model.get_current_language():
            self.model.set_current_language(lang_code)
