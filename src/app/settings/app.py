import tkinter as tk

from src.app.settings.controller import SettingsController
from src.app.settings.view import SettingsView

from . import _


class SettingsApp:
    def __init__(self, main_view, main_controller):
        self.window = None

        self.main_view = main_view
        self.master_controller = main_controller

        self.model = None
        self.view = None
        self.controller = None

    def set_model(self, model):
        self.model = model

    def run(self):
        # --- 创建并配置 Toplevel 窗口 ---
        self.window = tk.Toplevel(self.main_view)
        self.window.title(_("Settings"))
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        self.window.transient(self.main_view)  # 保持在主窗口之上
        self.window.grab_set()  # 设置为模态对话框，阻止与其他窗口交互

        # --- 放置在窗口中 ---
        self.view = SettingsView(master=self.window, model=self.model)
        self.view.pack(fill="both", expand=True)

        # --- 创建控制器 ---
        self.controller = SettingsController(self.master_controller, self.view, self.model)
        self.view.bind_callback(self.controller)

        # --- 设置窗口关闭协议 ---
        # 将窗口右上角的 "X" 按钮也绑定到安全关闭方法
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- 将窗口居中 ---
        self._center_window()

    def on_close(self):
        self.view.on_close()
        self.window.destroy()

    def _center_window(self):
        """将窗口相对于其父窗口居中显示。"""
        self.window.update_idletasks()  # 确保获取到最新的窗口尺寸
        parent_toplevel = self.main_view.winfo_toplevel()

        parent_x = parent_toplevel.winfo_x()
        parent_y = parent_toplevel.winfo_y()
        parent_width = parent_toplevel.winfo_width()
        parent_height = parent_toplevel.winfo_height()

        width = self.window.winfo_width()
        height = self.window.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        self.window.geometry(f"{width}x{height}+{x}+{y}")
