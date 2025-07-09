import tkinter as tk
from typing import Any, Callable, Dict, Tuple

from src.app.model import MainModel

from .settings import factory as settings_factory

# (未来可以导入更多模块的工厂)
# from .project_manager import factory as pm_factory


class ModuleManager:
    """
    负责管理所有模块的创建、生命周期和呈现。
    """

    def __init__(self, root_window: tk.Tk, main_model: MainModel):
        self.root_window = root_window
        self.main_model = main_model

        # 用于存储模块的工厂函数和呈现方式
        self._modules: Dict[str, Dict[str, Any]] = {}
        # 用于跟踪当前活动的模块实例，以便管理生命周期
        self._active_instances: Dict[str, Tuple] = {}

    def register_modules(self):
        """集中注册所有已知的模块。"""
        self.register("settings", settings_factory.create_module, presentation="window")
        # self.register("project_manager", pm_factory.create_module, presentation="tab")

    def register(self, name: str, factory: Callable, presentation: str):
        self._modules[name] = {"factory": factory, "presentation": presentation}

    def activate(self, name: str):
        """激活一个模块（按需加载）。"""
        if name in self._active_instances:
            # 如果模块已激活（例如，窗口已打开），则将其带到最前
            instance_info = self._active_instances[name]
            if "window" in instance_info:
                instance_info["window"].deiconify()
                instance_info["window"].lift()
            return

        if name not in self._modules:
            print(f"Error: Module '{name}' not registered.")
            return

        module_info = self._modules[name]
        factory = module_info["factory"]
        presentation = module_info["presentation"]

        if presentation == "window":
            self._activate_in_window(name, factory)
        elif presentation == "tab":
            # self._activate_in_tab(name, factory) # 未来可以实现
            pass

    def _activate_in_window(self, name: str, factory: Callable):
        """在新窗口中激活模块的通用逻辑。"""
        window = tk.Toplevel(self.root_window)

        # 调用工厂创建MVC实例，并将新窗口作为视图的父控件
        model, view, controller = factory(window, self.main_model)

        # 统一处理窗口关闭时的清理工作
        def on_close():
            view.cleanup()
            controller.cleanup()
            # 从活动实例中移除
            del self._active_instances[name]
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", on_close)

        # 将实例信息保存起来
        self._active_instances[name] = {"model": model, "view": view, "controller": controller, "window": window}

    def cleanup_all(self):
        """在应用退出时，清理所有活动的模块实例。"""
        # 遍历副本以安全地修改字典
        for name, instance_info in list(self._active_instances.items()):
            if "window" in instance_info:
                # 调用 on_close 来执行完整的清理流程
                instance_info["window"].destroy()
