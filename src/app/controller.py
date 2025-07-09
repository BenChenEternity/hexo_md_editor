from tkinter import filedialog

from i18n import setup_translations

from .model import MainModel
from .settings.app import SettingsApp
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
        settings_app = SettingsApp(self.view, self)
        # 共享 model 传进去
        settings_app.set_model(self.model)
        settings_app.run()

    def close_project(self, path: str):
        """处理关闭项目标签页的请求。"""
        self.model.remove_project(path)

    def on_open_project(self):
        path = filedialog.askdirectory()

        # 检查用户是否选择了路径，而不是取消
        if path:
            # 指示模型添加这个新项目
            self.model.add_project(path)

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
