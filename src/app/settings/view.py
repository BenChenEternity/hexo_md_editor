import tkinter as tk
from tkinter import ttk

from constants import LANGUAGES
from src.core.event_bus import Consumer

from ..constants import EVENT_LANGUAGE_CHANGED
from . import _


class SettingsView(tk.Toplevel, Consumer):
    """
    设置窗口 (View)。
    负责显示和布局所有 UI 组件，并将用户操作传递给其控制器。
    """

    def __init__(self, parent, model):
        tk.Toplevel.__init__(self, parent)
        Consumer.__init__(self)
        self.transient(parent)  # 保持在主窗口之上
        self.title(_("Settings"))
        self.model = model
        self.parent = parent

        # --- 窗口布局 ---
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()  # 模态对话框，阻止与其他窗口交互

        # --- 创建控件 ---
        self._create_widgets()

        # --- 窗口居中 ---
        self._center_window()

        # --- 订阅事件 ---
        # 语言变更
        self.subscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)

        # 事件取消

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def bind_callback(self, controller):
        self.lang_combo.bind("<<ComboboxSelected>>", controller.on_toggle_language)
        self.ok_button.config(command=self.on_close)

    def update_ui_texts(self):
        self.title(_("Settings"))
        self.lang_frame.config(text=_("Language Settings"))
        self.lang_label.config(text=_("Language") + ":")
        self.ok_button.config(text=_("close"))

    def on_close(self):
        """
        自定义的窗口关闭处理方法。
        确保我们在销毁窗口前，先注销所有事件。
        """
        # 1. 先从事件总线注销自己
        self.unsubscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)
        # 2. 再安全地销毁窗口
        self.destroy()

    def on_language_changed(self, **kwargs):
        self.update_ui_texts()

    def _center_window(self):
        """将窗口居中于父窗口。"""
        self.update_idletasks()
        toplevel_parent = self.parent.winfo_toplevel()

        # 结果 parent_x 是0，因为 parent 是铺满嵌套在另一个窗口里面的，要得到真正的父窗口
        # parent_x = self.parent.winfo_x()
        # parent_y = self.parent.winfo_y()
        # parent_width = self.parent.winfo_width()
        # parent_height = self.parent.winfo_height()
        parent_x = toplevel_parent.winfo_x()
        parent_y = toplevel_parent.winfo_y()
        parent_width = toplevel_parent.winfo_width()
        parent_height = toplevel_parent.winfo_height()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        """创建窗口中的所有UI组件。"""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # --- 国际化/语言设置 ---
        self.lang_frame = ttk.LabelFrame(main_frame, text=_("Language Settings"), padding=10)
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
        # Place the combobox in column 1 and make it fill the available space
        self.lang_combo.grid(row=0, column=1, sticky="we")

        # --- 底部按钮 ---
        button_frame = ttk.Frame(main_frame, padding=(0, 20, 0, 0))
        button_frame.pack(fill="x", side="bottom")

        self.ok_button = ttk.Button(button_frame, text=_("close"), command=self.destroy)
        self.ok_button.pack(side="right")
