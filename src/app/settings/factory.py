import tkinter as tk

from src.app.settings.controller import SettingsController
from src.app.settings.view import SettingsView
from src.services.factory import Factory
from src.utils.ui import UI

from . import _
from .model import SettingsModel


class SettingsFactory(Factory):
    def assemble(self, parent_view, model_data):
        # 创建一个新的Toplevel窗口来容纳设置视图
        toplevel_window = tk.Toplevel(parent_view.winfo_toplevel())
        toplevel_window.title(_("settings"))
        toplevel_window.transient(parent_view.winfo_toplevel())
        toplevel_window.grab_set()
        toplevel_window.protocol("WM_DELETE_WINDOW", lambda: SettingsFactory.destroy_module(self, toplevel_window))

        model = SettingsModel(model_data)
        view = SettingsView(toplevel_window, model)
        controller = SettingsController(model)

        # 组合，居中显示
        view.pack(in_=toplevel_window, fill="both", expand=True)
        UI.center_window(toplevel_window, 400, 300)

        # 返回MVC三元组，其中view现在已经被正确地展示在它自己的窗口里
        return model, view, controller

    def destroy_module(self, window: tk.Misc):
        self.module_manager.deactivate(self.module_name)
        window.destroy()
