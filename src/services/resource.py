from abc import abstractmethod
from pathlib import Path

from PIL import Image

from settings import ASSETS_PATH


class ResourceLoader:
    def __init__(self, resource_path: Path):
        self.path = resource_path

    @abstractmethod
    def load(self, name):
        pass


class AssetsResourceLoader(ResourceLoader):
    def __init__(self):
        super().__init__(ASSETS_PATH)

    @abstractmethod
    def load(self, name):
        pass


class IconResourceLoader(AssetsResourceLoader):

    def load(self, name):
        icon_path = self.path / "icons" / name

        with Image.open(icon_path) as icon:
            icon.load()
            return icon
        # 图标找不到直接异常停止


icon_loader = IconResourceLoader()
