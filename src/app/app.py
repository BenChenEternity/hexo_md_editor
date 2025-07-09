import logging
import tkinter as tk

from constants import APP_NAME, LOG_FILE_PATH, SETTINGS_FILE_PATH
from i18n import setup_translations
from src.app.constants import MODULE_ROOT_MAIN
from src.app.module_manager import ModuleManager
from src.core.logging_manager import LoggingManager
from src.core.settings_manager import settings_manager
from src.services.persistence import PersistenceService


class Application:
    def __init__(self):
        self.logging_manager = LoggingManager(LOG_FILE_PATH)
        logging.info("Application starting up...")

        self.root = tk.Tk()
        self.root.minsize(800, 600)
        self.root.title(APP_NAME)  # 可以先设置一个默认标题

        # 注册
        self.module_manager = ModuleManager(self.root)

        # 启动后台服务
        self.persistence_service = PersistenceService()

        # 激活主模块 "main"，这将创建 MainModel, MainView, MainController
        main_module_instance = self.module_manager.activate(MODULE_ROOT_MAIN)

        # 如果激活失败，应用无法启动
        if not main_module_instance:
            logging.critical("Failed to activate main module. Application cannot start.")
            self.root.destroy()
            return

        # 从主模块的模型中加载并应用配置
        main_model = main_module_instance["model"]
        settings_manager.set_settings_path(SETTINGS_FILE_PATH)
        user_settings = settings_manager.load_settings()
        language = user_settings.get("language", "en")

        main_model.set_current_language(language)
        main_model.set_app_name(APP_NAME)
        setup_translations(main_model.get_current_language())

        logging.info("Application UI is ready.")

    def run(self):
        if not self.root.winfo_exists():
            return

        self.root.mainloop()

        # 清理工作保持不变
        if self.persistence_service:
            self.persistence_service.unsubscribe_all()
        # if module_manager:
        #     module_manager.cleanup_all()
        logging.info("Application shutting down.")
