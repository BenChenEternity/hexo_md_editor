import tkinter as tk

from i18n import setup_translations
from src.app.controller import MainController
from src.app.model import MainModel
from src.app.view import MainView


class Application:
    """
    应用程序的主类。
    负责创建和协调MVC组件：Model, View, Controller。
    这是应用程序的“组合根 (Composition Root)”。
    """

    def __init__(self):
        """
        初始化应用程序。
        """
        # M
        self.model = MainModel()

        # i18n
        # 在创建任何UI组件之前，必须先设置好翻译
        setup_translations(self.model.current_language)

        # 主窗口
        self.root = tk.Tk()
        self.root.minsize(600, 400)

        # V
        self.view = MainView(self.root)

        # C
        self.controller = MainController(self.model, self.view)

        # 6. 将控制器设置给视图
        # 视图现在可以将其UI组件的事件 (如按钮点击) 绑定到控制器的方法上
        self.view.bind_callback(self.controller)

        # 7. 设置窗口标题
        # 在所有组件都初始化后，设置窗口的最终标题
        self.controller.on_ui_ready()
        self.root.title(self.controller.get_app_name())

    def run(self):
        """
        启动应用程序的主事件循环。
        """
        self.root.mainloop()
