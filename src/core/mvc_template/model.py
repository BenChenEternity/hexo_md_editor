from abc import ABC, abstractmethod
from typing import Any, Dict

from src.core.mvc_template.event_bus import Producer


class Model(Producer, ABC):
    def __init__(self, data: dict):
        super().__init__()
        for key, value in data.items():
            setattr(self, key, value)

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    def cleanup(self):
        pass
