from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

from i18n import setup_translations
from src.app.constants import (
    EVENT_ERROR_OCCURRED,
    EVENT_MAIN_UI_DEPLOY_CLICKED,
    EVENT_MAIN_UI_GENERATE_CLICKED,
    EVENT_MAIN_UI_INFO_CLICKED,
    EVENT_MAIN_UI_OPEN_PROJECT_CLICKED,
    EVENT_MAIN_UI_SETTINGS_CLICKED,
    MODULE_ROOT_MAIN,
    MODULE_ROOT_MAIN_SETTINGS,
)
from src.app.model import MainModel
from src.core.mvc_template.controller import Controller as BaseController

if TYPE_CHECKING:
    from src.app.module_manager import ModuleManager


class MainController(BaseController):
    """
    主控制器，遵循 BaseController 模板。
    """

    def __init__(self, model: MainModel, module_manager: "ModuleManager"):
        # 调用父类构造函数，它会自动调用 _setup_handlers
        super().__init__(model)
        self.module_manager = module_manager

    def _setup_handlers(self):
        """注册所有需要处理的事件。"""
        # UI 事件
        self.subscribe(EVENT_MAIN_UI_SETTINGS_CLICKED, self.on_settings_click)
        self.subscribe(EVENT_MAIN_UI_INFO_CLICKED, self.on_info_click)
        self.subscribe(EVENT_MAIN_UI_OPEN_PROJECT_CLICKED, self.on_open_project)
        self.subscribe(EVENT_MAIN_UI_GENERATE_CLICKED, self.on_generate_click)
        self.subscribe(EVENT_MAIN_UI_DEPLOY_CLICKED, self.on_deploy_click)

        # 全局/模型事件
        self.subscribe(EVENT_ERROR_OCCURRED, self.on_error_occurred)
        # self.subscribe(EVENT_MAIN_MODEL_LANGUAGE_CHANGED, self.on_language_changed)

    def on_settings_click(self):
        model: MainModel = self.module_manager.get(MODULE_ROOT_MAIN)["model"]
        self.module_manager.activate(MODULE_ROOT_MAIN_SETTINGS, model.to_dict())

    def on_open_project(self):
        path = filedialog.askdirectory()
        if path:
            self.model.add_project(path)

    def on_error_occurred(self, title: str, message: str):
        messagebox.showerror(title, message)

    def on_language_changed(self, new_lang: str, **kwargs):
        setup_translations(new_lang)

    def on_info_click(self):
        # 之后可以实现打开一个“关于”窗口
        print("Info button clicked")

    def on_generate_click(self):
        print("Generate button clicked")

    def on_deploy_click(self):
        print("Deploy button clicked")
