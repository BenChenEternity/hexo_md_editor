import logging
import tkinter as tk

from constants import APP_NAME, LOG_FILE_PATH, SETTINGS_FILE_PATH
from i18n import setup_translations
from src.app.controller import MainController
from src.app.model import MainModel
from src.app.view import MainView
from src.core.logging_manager import LoggingManager
from src.core.settings_manager import settings_manager
from src.services.persistence import PersistenceService


class Application:
    def __init__(self):
        """
        初始化应用程序。
        """
        # --- 核心服务初始化 ---
        self.logging_manager = LoggingManager(LOG_FILE_PATH)
        logging.info("Application starting up...")

        # M 初始化
        self.model = MainModel()

        # --- 加载配置 ---
        settings_manager.set_settings_path(SETTINGS_FILE_PATH)
        user_settings = settings_manager.load_settings()

        # 决定语言 (从配置加载，否则用默认)
        language = user_settings.get("language", "en")

        self.model.set_current_language(language)
        self.model.set_app_name(APP_NAME)

        # 启动后台持久化服务
        self.persistence_service = PersistenceService()

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

        # 将控制器设置给视图
        # 视图现在可以将其UI组件的事件 (如按钮点击) 绑定到控制器的方法上
        self.view.bind_callback(self.controller)

        # 在所有组件都初始化后，设置窗口的最终标题
        self.controller.on_ui_ready()
        self.root.title(self.controller.get_app_name())
        logging.info("Application UI is ready.")

    def run(self):
        """
        启动应用程序的主事件循环。
        """
        self.root.mainloop()
        # 关闭持久化服务
        self.persistence_service.close()
        logging.info("Application shutting down.")
