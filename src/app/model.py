import logging
from tkinter import messagebox

from src.app.constants import (
    EVENT_LANGUAGE_CHANGED,
    EVENT_PROJECT_CLOSED,
    EVENT_PROJECT_OPENED,
)
from src.core.mvc_template.event_bus import Producer

from . import _

logger = logging.getLogger(__name__)


class MainModel(Producer):
    """
    应用程序的数据模型。
    这个类是所有应用状态的“单一数据源 (Single Source of Truth)”。
    它不关心这些数据如何显示，只负责存储和管理。
    """

    def __init__(self):
        """
        初始化模型的所有属性。
        """
        super().__init__()
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
        """添加一个新项目，如果它尚未打开，并发出事件。"""
        if path in self.open_projects:
            # TODO 选择到已经打开的项目
            logger.info(f"Project: {path} already opened.")
            return

        self.open_projects.append(path)
        self.send_event(EVENT_PROJECT_OPENED, path=path)

    def remove_project(self, path: str):
        """移除一个项目并发出事件。"""
        if path not in self.open_projects:
            err_msg_title = _("error")
            err_msg = f"{_('Project:')} {path} {_('not opened but closed.')}"
            messagebox.showerror(err_msg_title, err_msg)
            logger.exception(err_msg)
            return

        self.open_projects.remove(path)
        self.send_event(EVENT_PROJECT_CLOSED, path=path)
