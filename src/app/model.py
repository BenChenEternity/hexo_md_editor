import logging
from typing import Any, Dict

from src.app.constants import EVENT_MAIN_MODEL_CHANGED
from src.app.enum import MainKey
from src.core.mvc_template.model import Model

logger = logging.getLogger(__name__)


class MainModel(Model):
    """
    应用程序的主数据模型。
    遵循 BaseModel 模板。
    """

    def __init__(self, data):
        super().__init__(data)

    def to_dict(self) -> Dict[str, Any]:
        return {key.value: getattr(self, key.value, None) for key in MainKey}

    def get_value(self, key: str) -> Any:
        return getattr(self, key)

    def set_value(self, key: str, value):
        if getattr(self, key) == value:
            # 没变
            return
        setattr(self, key, value)
        self.send_event(EVENT_MAIN_MODEL_CHANGED, param={key: value})

    # def add_project(self, path: str):
    #     if path in self.open_projects:
    #         logger.info(f"Project: {path} already opened.")
    #         return
    #     self.open_projects.append(path)
    #     self.send_event(EVENT_MAIN_MODEL_PROJECT_OPENED, path=path)
    #
    # def remove_project(self, path: str):
    #     if path not in self.open_projects:
    #         err_msg_title = _("Error")
    #         err_msg = f"{_('Project:')} {path} {_('not opened but closed.')}"
    #         logger.exception(err_msg)
    #         self.send_event(EVENT_ERROR_OCCURRED, title=err_msg_title, message=err_msg)
    #         return
    #     self.open_projects.remove(path)
    #     self.send_event(EVENT_MAIN_MODEL_PROJECT_CLOSED, path=path)
