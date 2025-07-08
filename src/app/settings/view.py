import tkinter as tk
from tkinter import ttk

from constants import LANGUAGES
from src.core.mvc_template.event_bus import Consumer

from ..constants import EVENT_LANGUAGE_CHANGED
from . import _


class SettingsView(ttk.Frame, Consumer):
    """
    设置视图 (View 组件)。
    这是一个可复用的 UI 组件，负责创建设置相关的控件。
    它继承自 ttk.Frame，并可以被放置在任何容器中（如 Toplevel 或其他 Frame）。
    """

    def __init__(self, master, model):
        # 初始化 Frame 自身
        ttk.Frame.__init__(self, master, padding=20)

        # 初始化事件消费者
        Consumer.__init__(self)

        self.model = model

        # --- 创建控件 ---
        self._create_widgets()

        # --- 订阅事件 ---
        # 视图只订阅那些会改变其自身内容的事件。
        self.subscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)

    def bind_callback(self, controller):
        """将控件的动作绑定到控制器的方法。"""
        self.lang_combo.bind("<<ComboboxSelected>>", controller.on_toggle_language)

    def update_ui_texts(self):
        """更新此框架内控件的文本，并返回新的窗口标题。"""
        self.lang_frame.config(text=_("Language Settings"))
        self.lang_label.config(text=_("Language") + ":")
        # 返回新的标题文本，以便父窗口可以设置它
        return _("Settings")

    def on_language_changed(self, **kwargs):
        """当语言更改时，用于更新UI文本的事件处理程序。"""
        new_title = self.update_ui_texts()
        # 视图更新自己的控件，而 App 层负责更新窗口标题。
        # 此处直接更新顶层窗口标题作为一种简便实现。
        self.winfo_toplevel().title(new_title)

    def _create_widgets(self):
        """在此框架内创建所有的UI组件。"""
        # --- 国际化/语言设置 ---
        self.lang_frame = ttk.LabelFrame(self, text=_("Language Settings"), padding=10)
        self.lang_frame.pack(fill="x")

        self.lang_frame.grid_columnconfigure(0, minsize=120)
        self.lang_frame.grid_columnconfigure(1, weight=1)

        self.lang_label = ttk.Label(self.lang_frame, text=_("Language") + ":")
        self.lang_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        lan_id = LANGUAGES.get(self.model.get_current_language(), "en")
        self.lang_var = tk.StringVar(value=lan_id)
        self.lang_combo = ttk.Combobox(
            self.lang_frame,
            textvariable=self.lang_var,
            values=list(LANGUAGES.values()),
            state="readonly",
            justify="center",
        )
        self.lang_combo.grid(row=0, column=1, sticky="we")

        # --- 底部按钮 ---
        button_frame = ttk.Frame(self, padding=(0, 20, 0, 0))
        button_frame.pack(fill="x", side="bottom")

    def on_close(self):
        self.unsubscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)
