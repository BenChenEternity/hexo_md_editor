import tkinter as tk

from src.app.model import MainModel
from src.app.settings.controller import SettingsController
from src.app.settings.view import SettingsView


def create_module(master: tk.Misc, main_model: MainModel):
    """
    设置模块的工厂函数。
    负责创建并返回该模块的 MVC 实例。
    :param master: 视图(View)将要依附的父控件。
    :param main_model: 共享的主数据模型。
    :return: (model, view, controller) 元组。
    """
    # 注意：这里的 model 是共享的 main_model，所以我们直接使用它。
    # 控制器只需要模型。
    controller = SettingsController(main_model)
    # 视图需要父控件和模型。
    view = SettingsView(master, main_model)

    return main_model, view, controller
