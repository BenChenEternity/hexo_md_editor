import logging
import tkinter as tk

from constants import APP_NAME, LOG_FILE_PATH, SETTINGS_FILE_PATH
from i18n import setup_translations
from src.app.controller import MainController
from src.app.model import MainModel
from src.app.module_manager import ModuleManager
from src.app.view import MainView
from src.core.logging_manager import LoggingManager
from src.core.settings_manager import settings_manager
from src.services.persistence import PersistenceService


class Application:
    def __init__(self):
        self.logging_manager = LoggingManager(LOG_FILE_PATH)
        logging.info("Application starting up...")

        self.root = tk.Tk()
        self.root.minsize(800, 600)

        self.model = MainModel()
        # 实例化并注册模块管理器
        self.module_manager = ModuleManager(self.root, self.model)
        self.module_manager.register_modules()

        # 加载配置
        settings_manager.set_settings_path(SETTINGS_FILE_PATH)
        user_settings = settings_manager.load_settings()
        language = user_settings.get("language", "en")
        self.model.set_current_language(language)
        self.model.set_app_name(APP_NAME)

        # 启动服务
        self.persistence_service = PersistenceService()
        setup_translations(self.model.current_language)

        # --- 核心更改: 修正初始化顺序和参数 ---
        # Controller 依赖 Model 和 ModuleManager
        self.controller = MainController(self.model, self.module_manager)
        # View 依赖 Root Window 和 Model
        self.view = MainView(self.root, self.model)

        logging.info("Application UI is ready.")
        self.root.title(self.model.get_app_name())

    def run(self):
        self.root.mainloop()
        # 确保所有订阅和服务都被正确清理
        if self.persistence_service:
            self.persistence_service.unsubscribe_all()
        if self.module_manager:
            self.module_manager.cleanup_all()
        logging.info("Application shutting down.")
