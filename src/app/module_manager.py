import logging
import tkinter as tk
from typing import Any, Dict, Optional, Type

from ..core.tree import TreeNode
from ..services.factory import Factory
from .constants import MODULE_ROOT, MODULE_ROOT_MAIN, MODULE_ROOT_MAIN_SETTINGS
from .factory import MainFactory
from .settings.factory import SettingsFactory

logger = logging.getLogger(__name__)

ModuleInstanceInfo = Dict[str, Any]
ModuleNode = Dict[str, Any]  # e.g., {"instance": info, "children": {}}


class ModuleManager:
    """
    负责管理所有模块的创建、生命周期和呈现（以树状结构）。
    这是应用的核心协调器。
    """

    def __init__(self, root_window: tk.Tk):
        self._module_factories: Dict[str, Factory] = {}
        self._activate_tree = None
        self._register_modules()
        # 根节点
        self._activate_tree = TreeNode(
            MODULE_ROOT,
            ModuleManager._create_node_data(None, root_window, None),
        )

    @staticmethod
    def _create_node_data(model, view, controller):
        return {
            "model": model,
            "view": view,
            "controller": controller,
        }

    def get(self, name: str):
        """
        获取已经加载的模块 比如： MODULE_ROOT_MAIN_SETTINGS
        """
        name = name.split(".", 1)[1]
        node = self._activate_tree.get_child(name)
        if node is None:
            return None
        return node.data

    def _register_modules(self):
        """集中注册所有已知的模块及其工厂和呈现方式。"""
        self.register(MODULE_ROOT_MAIN, MainFactory)
        self.register(MODULE_ROOT_MAIN_SETTINGS, SettingsFactory)

    def register(self, name: str, factory: Type[Factory]) -> None:
        """
        注册一个模块。
        :param name: 模块的唯一名称。
        :param factory: 创建模块MVC三元组的工厂类
        """
        self._module_factories[name] = factory(name, self)

    def activate(self, name: str, model_data: dict) -> Optional[ModuleInstanceInfo]:
        """
        激活一个模块（按需加载）。
        如果模块已激活，则将其带到最前。
        :param name: 要激活的模块名
        :param model_data: 模型初始参数
        :return: 成功激活后返回模块的实例信息字典，否则返回 None。
        """
        logger.debug(f"Activating: ({name}).")
        full_name = name
        # 从root开始排除自身
        name = name.split(".", 1)[1]

        factory = self._module_factories.get(full_name, None)
        # 工厂未注册
        if factory is None:
            logger.exception(f"Module: '{full_name}' not registered.")
            return

        module_node: TreeNode = self._activate_tree.get_child(name)

        # 已激活
        if module_node is not None:
            data = module_node.data
            if not isinstance(data, dict):
                logger.exception(f"Error module info type: {type(data)}.")
                return

            # 如果是窗口，放最上面提醒
            view = data.get("view", None)
            if isinstance(view, tk.Toplevel):
                view.deiconify()
                view.lift()
            return

        # 激活模块
        module_node = self._activate_tree.add_child(name)
        parent_module = module_node.parent
        if not parent_module:
            # 1.如果是根模块不需要手动激活 2.非根模块没有父节点
            logger.exception(f"Module ('{full_name}') has no parent.")
            return

        parent_module_data = parent_module.data
        if parent_module_data is None:
            # 父节点数据缺失
            logger.exception(f"Module ('{full_name}') has no parent data.")
            return

        parent_view = parent_module_data.get("view", None)
        if parent_view is None:
            # 父模块不能没视图
            logger.exception(f"Module ('{full_name}') has no parent view.")
            return

        model, view, controller = factory.assemble(parent_view, model_data)

        # 添加到激活树
        instance_info = ModuleManager._create_node_data(model, view, controller)
        module_node.data = instance_info

        logger.debug(f"[DONE] Activated: ({full_name}).")

    def deactivate(self, name: str):
        """
        停用并清理一个模块（包括其所有子模块），采用后序遍历。
        :param name: 要停用的模块全名。
        """
        logger.debug(f"Deactivating: ({name}).")
        relative_name = name.split(".", 1)
        if len(relative_name) == 1:
            # 根节点
            relative_name = relative_name[0]
            node_to_remove = self._activate_tree
        else:
            relative_name = relative_name[1]
            node_to_remove = self._activate_tree.get_child(relative_name)

        if not node_to_remove:
            logger.warning(f"Module {name} not found in activate tree. Cannot deactivate.")
            return

        def _post_order_cleanup(node: TreeNode):
            for child in node.get_children().values():
                _post_order_cleanup(child)

            instance_info = node.data
            if not instance_info:
                return

            controller = instance_info.get("controller")
            view = instance_info.get("view")

            if controller and hasattr(controller, "cleanup"):
                controller.cleanup()

            if view and hasattr(view, "cleanup"):
                view.cleanup()

            logger.debug(f"Deactivating now -> ({node.name}).")

        # 开始后序遍历清理
        _post_order_cleanup(node_to_remove)

        # 移除节点
        self._activate_tree.remove_child(relative_name)
        logger.debug(f"[DONE] Deactivated: ({name}).")

    def cleanup_all(self):
        self.deactivate(MODULE_ROOT)
