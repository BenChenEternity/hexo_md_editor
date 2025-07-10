import copy
import logging
from typing import Any

from src.app.constants import (
    EVENT_MAIN_SETTINGS_MODEL_APPLIED,
    EVENT_MAIN_SETTINGS_MODEL_WORKING_STATE_CHANGED,
)
from src.core.mvc_template.model import Model

logger = logging.getLogger(__name__)


class SettingsModel(Model):
    """
    设置模块的数据模型。
    使用一个Set来高效地跟踪“脏”字段，并提供一个通用的setter方法。
    """

    def __init__(self, model_data: dict):
        super().__init__(model_data)
        self.dirty_fields = set()
        self.original_settings = copy.deepcopy(model_data)
        self.working_settings = copy.deepcopy(model_data)

    def get_value(self, key: str) -> Any:
        return self.working_settings.get(key, None)

    def set_value(self, key: str, value):
        if key not in self.working_settings:
            logger.exception(f"Settings key error: {key}")
            return

        # 仅当工作值发生变化时才继续
        if self.working_settings[key] == value:
            return
        self.working_settings[key] = value
        # 将新工作值与原始值比较，更新脏状态
        if self.working_settings[key] != self.original_settings[key]:
            self.dirty_fields.add(key)
        else:
            self.dirty_fields.discard(key)  # 如果改回原样，则移除脏标记

        # 更新UI脏*显示
        self.send_event(EVENT_MAIN_SETTINGS_MODEL_WORKING_STATE_CHANGED, changed_key=key)

    def to_dict(self):
        return self.working_settings

    def is_dirty(self) -> bool:
        """通过检查Set是否为空来高效判断脏状态"""
        return len(self.dirty_fields) > 0

    def get_dirty_fields(self) -> set:
        """直接返回脏字段集合"""
        return self.dirty_fields

    def apply_changes(self):
        """应用变更"""
        if not self.is_dirty():
            return

        self.original_settings = copy.deepcopy(self.working_settings)
        self.dirty_fields.clear()

        self.send_event(EVENT_MAIN_SETTINGS_MODEL_APPLIED, settings=self.original_settings)
        self.send_event(EVENT_MAIN_SETTINGS_MODEL_WORKING_STATE_CHANGED)
