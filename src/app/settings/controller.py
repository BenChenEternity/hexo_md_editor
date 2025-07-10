import logging

from src.app.constants import (
    EVENT_MAIN_SETTINGS_UI_APPLY_CLICKED,
    EVENT_MAIN_SETTINGS_UI_LANGUAGE_SELECTED,
)
from src.app.enum import MainKey
from src.app.settings.model import SettingsModel
from src.core.mvc_template.controller import Controller as BaseController

logger = logging.getLogger(__name__)


class SettingsController(BaseController):
    model: SettingsModel

    def __init__(self, model: SettingsModel):
        super().__init__(model)

    def _setup_handlers(self):
        self.subscribe(EVENT_MAIN_SETTINGS_UI_LANGUAGE_SELECTED, self.on_language_selected)
        self.subscribe(EVENT_MAIN_SETTINGS_UI_APPLY_CLICKED, self.on_apply_clicked)

    def on_language_selected(self, lang_code: str):
        if lang_code != self.model.get_value(MainKey.LANGUAGE.value):
            self.model.set_value(MainKey.LANGUAGE.value, lang_code)

    def on_apply_clicked(self):
        self.model.apply_changes()
