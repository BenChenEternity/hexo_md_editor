import tkinter as tk
from tkinter import scrolledtext, ttk

from PIL import Image, ImageTk

from settings import APP_NAME
from src.app.resources import icon_info, icon_settings
from src.core.mvc_template.view import View as BaseView

from ..utils.ui import UI
from . import _
from .constants import (
    EVENT_MAIN_MODEL_LANGUAGE_CHANGED,
    EVENT_MAIN_UI_DEPLOY_CLICKED,
    EVENT_MAIN_UI_GENERATE_CLICKED,
    EVENT_MAIN_UI_INFO_CLICKED,
    EVENT_MAIN_UI_SETTINGS_CLICKED,
)
from .model import MainModel


class MainView(BaseView):
    """
    主视图，遵循 BaseView 模板。
    """

    def __init__(self, master, model: MainModel):
        super().__init__(master, model)

    def _create_widgets(self):
        self.pack(fill="both", expand=True)
        UI.center_window(self.winfo_toplevel(), 800, 600)
        self._load_icons()

        style = ttk.Style()
        style.configure("Header.TFrame", background="#f0f0f0")
        style.configure("Header.TButton", background="#f0f0f0", borderwidth=0, focuscolor="none")
        style.map("Header.TButton", background=[("active", "#e0e0e0")])

        title_bar = ttk.Frame(self, height=self.TITLE_BAR_HEIGHT, style="Header.TFrame")
        title_bar.pack(fill="x", side="top", padx=1, pady=1)
        title_bar.pack_propagate(False)

        self.info_button = ttk.Button(title_bar, image=self.info_icon, style="Header.TButton")
        self.info_button.pack(side="right", padx=(0, 10))
        self.settings_button = ttk.Button(title_bar, image=self.settings_icon, style="Header.TButton")
        self.settings_button.pack(side="right", padx=(0, 5))
        self.title_label = ttk.Label(title_bar, text="...", font=("Segoe UI", 16, "bold"), background="#f0f0f0")
        self.title_label.pack(expand=True)

        main_content_frame = ttk.Frame(self, padding=10)
        main_content_frame.pack(fill="both", expand=True)
        self._create_command_panel(main_content_frame)

        self.update_ui_texts()
        self.title_label.config(text=APP_NAME)

    def _setup_bindings(self):
        self.settings_button.config(command=lambda: self.send_event(EVENT_MAIN_UI_SETTINGS_CLICKED))
        self.info_button.config(command=lambda: self.send_event(EVENT_MAIN_UI_INFO_CLICKED))
        self.generate_button.config(command=lambda: self.send_event(EVENT_MAIN_UI_GENERATE_CLICKED))
        self.deploy_button.config(command=lambda: self.send_event(EVENT_MAIN_UI_DEPLOY_CLICKED))
        # 假设标题栏有一个“打开项目”的按钮，或者未来菜单项会发送这个事件
        # 这里我们暂时不创建这个按钮，但保留这个逻辑

    def _setup_subscriptions(self):
        self.subscribe(EVENT_MAIN_MODEL_LANGUAGE_CHANGED, self.on_language_changed)

    def on_language_changed(self, **kwargs):
        self.update_ui_texts()

    def update_ui_texts(self):
        self.cmd_panel.config(text=_("Command Panel"))
        self.generate_button.config(text=_("Generate"))
        self.deploy_button.config(text=_("Deploy"))
        # --- 同样使用 winfo_toplevel() 来设置标题 ---
        toplevel = self.winfo_toplevel()
        toplevel.title(self.model.get_app_name())

    def _load_icons(self):
        self.TITLE_BAR_HEIGHT = 50
        icon_size = self.TITLE_BAR_HEIGHT - 18
        self.settings_icon = ImageTk.PhotoImage(
            icon_settings.resize((icon_size, icon_size), resample=Image.Resampling.LANCZOS)
        )
        self.info_icon = ImageTk.PhotoImage(icon_info.resize((icon_size, icon_size), resample=Image.Resampling.LANCZOS))

    def _create_command_panel(self, parent):
        self.cmd_panel = ttk.Labelframe(parent, text=_("Command Panel"), padding=10)
        self.cmd_panel.pack(fill="x", expand=False, pady=10)
        button_frame = ttk.Frame(self.cmd_panel)
        button_frame.pack(fill="x", pady=(0, 10))
        self.generate_button = ttk.Button(button_frame, text=_("Generate"))
        self.generate_button.pack(side="left", padx=(0, 5))
        self.deploy_button = ttk.Button(button_frame, text=_("Deploy"))
        self.deploy_button.pack(side="left")
        self.output_text = scrolledtext.ScrolledText(self.cmd_panel, height=15, wrap=tk.WORD, state="disabled")
        self.output_text.pack(fill="both", expand=True)
