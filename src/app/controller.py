from i18n import setup_translations

from .model import MainModel
from .settings.controller import SettingsController
from .settings.view import SettingsView
from .view import MainView


class MainController:
    def __init__(self, model: MainModel, view: MainView):
        self.model = model
        self.view = view

    def get_app_name(self) -> str:
        """从模型获取应用名称，提供给视图。"""
        return self.model.get_app_name()

    def change_language(self, new_lang_code: str):
        """
        封装了改变整个应用语言的完整流程。
        这是一个高级别的业务方法。
        """
        if new_lang_code == self.model.get_current_language():
            return

        setup_translations(new_lang_code)
        self.model.set_current_language(new_lang_code)

    def on_settings_click(self):
        """
        处理设置按钮的点击事件。
        这个方法会创建并运行 SettingsController。
        """
        # V
        settings_view = SettingsView(self.view, self.model)
        # C
        settings_controller = SettingsController(self, settings_view, self.model)
        settings_view.bind_callback(settings_controller)

    def on_ui_ready(self):
        """
        在UI准备就绪后调用。
        负责从模型获取初始数据并填充到视图中。
        """
        # 1. 从 Model 获取数据
        app_name = self.model.get_app_name()
        # 2. 调用 View 的方法更新UI
        self.view.set_app_title(app_name)

    def on_info_click(self):
        pass

    def on_generate_click(self):
        """处理“生成”按钮的点击事件。"""
        pass

    def on_deploy_click(self):
        """处理“部署”按钮的点击事件。"""
        pass

    def _run_command_in_thread(self, command: list):
        pass

    def _execute_command(self, command: list):
        pass
