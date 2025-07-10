import logging
import tkinter as tk

from settings import APP_NAME, LOG_FILE_PATH, SETTINGS_FILE_PATH
from src.app.constants import MODULE_ROOT_MAIN
from src.app.enum import MainKey
from src.app.module_manager import ModuleManager
from src.core.logging_manager import LoggingManager
from src.core.settings_manager import SettingsManager
from src.services.persistence import PersistenceService


class Application:
    def __init__(self):
        self.logging_manager = LoggingManager(LOG_FILE_PATH)
        logging.info("Application starting up...")

        self.root = tk.Tk()
        self.root.minsize(800, 600)
        self.root.title(APP_NAME)

        # 配置加载
        settings = {
            MainKey.APP_NAME.value: APP_NAME,
        }
        settings_manager = SettingsManager(SETTINGS_FILE_PATH)
        user_settings = settings_manager.load_settings()
        settings.update(user_settings)
        # 启动持久化服务
        self.persistence_service = PersistenceService(settings_manager)

        # 注册
        self.module_manager = ModuleManager(self.root)

        # 激活主模块 "main"
        self.module_manager.activate(MODULE_ROOT_MAIN, settings)

        # 从主模块的模型中加载并应用配置

        # main_model.set_current_language(language)
        # main_model.set_app_name(APP_NAME)
        # setup_translations(main_model.get_current_language())

        logging.info("Application UI is ready.")

    def run(self):
        if not self.root.winfo_exists():
            return

        self.root.mainloop()

        # 清理工作保持不变
        if self.persistence_service:
            self.persistence_service.unsubscribe_all()

        if self.module_manager:
            self.module_manager.cleanup_all()

        logging.info("Application shutting down.")
