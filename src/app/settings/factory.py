import tkinter as tk
from typing import TYPE_CHECKING

from src.app.model import MainModel
from src.app.settings.controller import SettingsController
from src.app.settings.view import SettingsView
from src.utils.ui import UI

from . import _

if TYPE_CHECKING:
    from src.app.module_manager import ModuleManager


class SettingsFactory:
    @staticmethod
    def create_module(context: dict):
        """
        组装 MVC
        """
        module_manager: "ModuleManager" = context["module_manager"]
        parent_model: "MainModel" = context["model"]
        parent_view: tk.Misc = context["view"]
        module_name: str = context["module_name"]

        # 创建一个新的Toplevel窗口来容纳设置视图
        toplevel_window = tk.Toplevel(parent_view.winfo_toplevel())
        toplevel_window.title(_("settings"))
        toplevel_window.transient(parent_view.winfo_toplevel())
        toplevel_window.grab_set()
        toplevel_window.protocol(
            "WM_DELETE_WINDOW", lambda: SettingsFactory.destroy_module(module_name, module_manager, toplevel_window)
        )

        controller = SettingsController(parent_model)
        view = SettingsView(toplevel_window, parent_model)

        # 将视图Frame放入Toplevel窗口中
        view.pack(in_=toplevel_window, fill="both", expand=True)

        # 居中显示新窗口
        UI.center_window(toplevel_window, 400, 300)

        # 返回MVC三元组，其中view现在已经被正确地展示在它自己的窗口里
        return parent_model, view, controller

    @staticmethod
    def destroy_module(module_name: str, module_manager: "ModuleManager", window: tk.Misc):
        module_manager.deactivate(module_name)
        window.destroy()
