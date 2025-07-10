import tkinter as tk
from tkinter import ttk

from settings import LANGUAGES
from src.app.constants import (  # EVENT_MAIN_SETTINGS_MODEL_WORKING_STATE_CHANGED,
    EVENT_MAIN_SETTINGS_MODEL_FIELD_DIRTY,
    EVENT_MAIN_SETTINGS_MODEL_FIELD_DIRTY_CANCELLED,
    EVENT_MAIN_SETTINGS_UI_APPLY_CLICKED,
    EVENT_MAIN_SETTINGS_UI_LANGUAGE_SELECTED,
)
from src.core.mvc_template.view import View

from ..enum import MainKey
from . import _
from .model import SettingsModel


class SettingsView(View):
    model: SettingsModel

    def __init__(self, master, model: SettingsModel):
        # 用于存储字段的各个UI组件，方便更新
        self.field_labels = {}
        super().__init__(master, model)

    def _create_widgets(self):
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # --- 语言设置 ---
        self.lang_frame = ttk.LabelFrame(self, text=_("Language Settings"), padding=10)
        self.lang_frame.pack(fill="x")
        self.lang_frame.grid_columnconfigure(0, minsize=120)
        self.lang_frame.grid_columnconfigure(1, weight=1)

        lang_label_frame = ttk.Frame(self.lang_frame)
        lang_label_frame.grid(row=0, column=0, sticky="w", padx=(0, 10))

        lang_label_text = ttk.Label(lang_label_frame, text=_("Language") + ":")
        lang_label_text.pack(side="left")
        lang_label_star = ttk.Label(lang_label_frame, text="", foreground="red")
        lang_label_star.pack(side="left")

        # 存储 label
        self.field_labels[MainKey.LANGUAGE.value] = {
            MainKey.LANGUAGE.value: lang_label_text,
            SettingsView._label_star_key(MainKey.LANGUAGE.value): lang_label_star,
        }

        lang_display_name = LANGUAGES.get(self.model.get_value(MainKey.LANGUAGE.value), "English")
        self.lang_var = tk.StringVar(value=lang_display_name)
        self.lang_combo = ttk.Combobox(
            self.lang_frame,
            textvariable=self.lang_var,
            values=list(LANGUAGES.values()),
            state="readonly",
            justify="center",
        )
        self.lang_combo.grid(row=0, column=1, sticky="we")

        # --- 添加应用按钮 ---
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", side="bottom", pady=(10, 0))
        self.apply_button = ttk.Button(button_frame, text=_("Apply"), command=self._on_apply_clicked)
        self.apply_button.pack(side="right")
        # 初始状态为禁用，因为没有更改
        self.apply_button.config(state="disabled")

    @staticmethod
    def _label_star_key(label_key):
        return f"{label_key}_star"

    def _setup_bindings(self):
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_language_selected)

    def _setup_subscriptions(self):
        # 订阅字段变脏和取消变脏的事件
        self.subscribe(EVENT_MAIN_SETTINGS_MODEL_FIELD_DIRTY, self._on_field_dirty)
        self.subscribe(EVENT_MAIN_SETTINGS_MODEL_FIELD_DIRTY_CANCELLED, self._on_field_dirty_cancelled)
        # self.subscribe(EVENT_MAIN_SETTINGS_MODEL_APPLIED, self.on_settings_applied)

    def _on_apply_clicked(self):
        self.send_event(EVENT_MAIN_SETTINGS_UI_APPLY_CLICKED)

    def _on_settings_applied(self):
        pass

    def _on_language_selected(self, event):
        selected_language_name = event.widget.get()
        lang_map = {v: k for k, v in LANGUAGES.items()}
        lang_code = lang_map.get(selected_language_name)
        if lang_code:
            self.send_event(EVENT_MAIN_SETTINGS_UI_LANGUAGE_SELECTED, lang_code=lang_code)

    def _update_label_visuals(self, key: str, dirty: bool):
        """根据字段的脏状态更新其星号标签的可见性"""
        labels = self.field_labels.get(key)
        if not labels:
            return

        star_label = labels.get(SettingsView._label_star_key(key))
        if not star_label:
            return

        star_label.config(text=" *" if dirty else "")

    def _on_field_dirty(self, key: str):
        self._on_field_state_changed(key, True)

    def _on_field_dirty_cancelled(self, key: str):
        self._on_field_state_changed(key, False)

    def _on_field_state_changed(self, key: str, dirty: bool):
        """当任何字段的脏状态改变时调用"""
        # 1. 更新对应标签的星号
        self._update_label_visuals(key, dirty)
        # 2. 根据模型整体是否变脏来更新“应用”按钮的状态
        new_state = "normal" if self.model.is_dirty() else "disabled"
        self.apply_button.config(state=new_state)

    # def on_settings_applied(self):
    #     """当更改被应用后调用"""
    #     # 1. 禁用“应用”按钮
    #     self.apply_button.config(state="disabled")
    #     # 2. 移除所有标签的星号
    #     for key in self.field_labels:
    #         self._update_label_visuals(key, False)

    def on_language_changed(self, **kwargs):
        new_title = self.update_ui_texts()
        self.winfo_toplevel().title(new_title)

    def update_ui_texts(self):
        self.lang_frame.config(text=_("Language Settings"))

        # Update the text part of the composite label
        lang_labels = self.field_labels.get(MainKey.LANGUAGE.value)
        if lang_labels and lang_labels.get("text"):
            lang_labels["text"].config(text=_("Language") + ":")

        lang_display_name = LANGUAGES.get(self.model.get_value(MainKey.LANGUAGE.value), "English")
        self.lang_var.set(lang_display_name)
        self.apply_button.config(text=_("Apply"))
        return _("Settings")
