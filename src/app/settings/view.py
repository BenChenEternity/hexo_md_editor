import tkinter as tk
from tkinter import ttk

from settings import LANGUAGES
from src.app.constants import EVENT_LANGUAGE_CHANGED, SETTINGS_UI_LANGUAGE_SELECTED
from src.core.mvc_template.model import Model as BaseModel
from src.core.mvc_template.view import View as BaseView

from . import _


class SettingsView(BaseView):
    """
    设置视图 (View 组件)。
    完全遵循 BaseView 模板。
    """

    def __init__(self, master, model: BaseModel):
        super().__init__(master, model)

    def _create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.lang_frame = ttk.LabelFrame(self, text=_("Language Settings"), padding=10)
        self.lang_frame.pack(fill="x")
        self.lang_frame.grid_columnconfigure(0, minsize=120)
        self.lang_frame.grid_columnconfigure(1, weight=1)
        self.lang_label = ttk.Label(self.lang_frame, text=_("Language") + ":")
        self.lang_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        lang_display_name = LANGUAGES.get(self.model.get_current_language(), "English")
        self.lang_var = tk.StringVar(value=lang_display_name)
        self.lang_combo = ttk.Combobox(
            self.lang_frame,
            textvariable=self.lang_var,
            values=list(LANGUAGES.values()),
            state="readonly",
            justify="center",
        )
        self.lang_combo.grid(row=0, column=1, sticky="we")

    def _setup_bindings(self):
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language_selected)

    def _setup_subscriptions(self):
        self.subscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)

    def _on_language_selected(self, event):
        selected_language_name = event.widget.get()
        lang_map = {v: k for k, v in LANGUAGES.items()}
        lang_code = lang_map.get(selected_language_name)
        if lang_code:
            self.send_event(SETTINGS_UI_LANGUAGE_SELECTED, lang_code=lang_code)

    def on_language_changed(self, **kwargs):
        new_title = self.update_ui_texts()
        self.winfo_toplevel().title(new_title)

    def update_ui_texts(self):
        self.lang_frame.config(text=_("Language Settings"))
        self.lang_label.config(text=_("Language") + ":")
        lang_display_name = LANGUAGES.get(self.model.get_current_language(), "English")
        self.lang_var.set(lang_display_name)
        return _("Settings")
