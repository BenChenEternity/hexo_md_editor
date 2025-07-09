import logging

from src.app.constants import (
    EVENT_ERROR_OCCURRED,
    EVENT_LANGUAGE_CHANGED,
    EVENT_PROJECT_CLOSED,
    EVENT_PROJECT_OPENED,
)
from src.core.mvc_template.model import Model as BaseModel

from . import _

logger = logging.getLogger(__name__)


class MainModel(BaseModel):
    """
    应用程序的主数据模型。
    遵循 BaseModel 模板。
    """

    def __init__(self):
        super().__init__()
        # 调用模板定义的初始化方法
        self.initialize()

    def initialize(self):
        """初始化模型的所有属性。"""
        self.app_name = ""
        self.current_language = "en"
        self.command_output = ""
        self.open_projects = []

    def get_current_language(self):
        return self.current_language

    def set_current_language(self, language_code):
        if self.current_language != language_code:
            self.current_language = language_code
            self.send_event(EVENT_LANGUAGE_CHANGED, new_lang=language_code)

    def get_app_name(self):
        return self.app_name

    def set_app_name(self, app_name):
        self.app_name = app_name

    def add_project(self, path: str):
        if path in self.open_projects:
            logger.info(f"Project: {path} already opened.")
            return
        self.open_projects.append(path)
        self.send_event(EVENT_PROJECT_OPENED, path=path)

    def remove_project(self, path: str):
        if path not in self.open_projects:
            err_msg_title = _("Error")
            err_msg = f"{_('Project:')} {path} {_('not opened but closed.')}"
            logger.exception(err_msg)
            # --- 核心更改: 不再调用messagebox，而是发送错误事件 ---
            self.send_event(EVENT_ERROR_OCCURRED, title=err_msg_title, message=err_msg)
            return
        self.open_projects.remove(path)
        self.send_event(EVENT_PROJECT_CLOSED, path=path)
