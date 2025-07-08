from abc import abstractmethod
from pathlib import Path


class Resource:
    def __init__(self, resource_path: Path):
        self.path = resource_path

    @abstractmethod
    def load(self, name):
        pass
