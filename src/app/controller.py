from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

from i18n import setup_translations
from src.app.constants import (
    EVENT_ERROR_OCCURRED,
    EVENT_MAIN_SETTINGS_MODEL_APPLIED,
    EVENT_MAIN_UI_DEPLOY_CLICKED,
    EVENT_MAIN_UI_GENERATE_CLICKED,
    EVENT_MAIN_UI_INFO_CLICKED,
    EVENT_MAIN_UI_OPEN_PROJECT_CLICKED,
    EVENT_MAIN_UI_SETTINGS_CLICKED,
    MODULE_ROOT_MAIN,
    MODULE_ROOT_MAIN_SETTINGS,
)
from src.app.enum import MainKey
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
        self.subscribe(EVENT_MAIN_SETTINGS_MODEL_APPLIED, self.on_settings_applied)

    def on_settings_applied(self, settings: dict):
        """
        当设置被应用时调用。
        :param settings: 新的应用设置字典。
        """
        # 检查语言设置是否有变化
        new_lang = settings.get(MainKey.LANGUAGE.value)
        if new_lang and new_lang != self.model.get_value(MainKey.LANGUAGE.value):
            # 1. 更新主模型
            self.model.set_value(MainKey.LANGUAGE.value, new_lang)
            # 2. 切换应用的语言
            setup_translations(new_lang)
            # 3. MainModel的set_value会自动发送EVENT_MAIN_MODEL_CHANGED事件，
            #    所有订阅了此事件的视图都会更新其UI文本。

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
