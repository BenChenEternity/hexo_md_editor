from abc import abstractmethod
from pathlib import Path

from PIL import Image

from constants import ASSETS_PATH
from src.core.resource import Resource


class AssetsResource(Resource):
    def __init__(self):
        super().__init__(ASSETS_PATH)

    @abstractmethod
    def load(self, name):
        pass


class IconResource(AssetsResource):

    def load(self, name):
        icon_path = self.path / "icons" / name

        with Image.open(icon_path) as icon:
            icon.load()
            return icon
        # 图标找不到直接异常停止
