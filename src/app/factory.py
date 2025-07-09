from src.app.controller import MainController
from src.app.model import MainModel
from src.app.view import MainView


class MainFactory:
    @staticmethod
    def create_module(context: dict):
        """
        设置模块的工厂函数。
        :param context:
            {
                "model": model,
                "view": view,
                "controller": controller,
                "module_manager": module_manager,
                "module_name": module_name,
             }
        :return: (model, view, controller) 元组
        """
        parent_view = context["view"]
        module_manager = context["module_manager"]

        # Main模块是根，它创建并拥有唯一的 MainModel
        model = MainModel()

        # Controller 和 View 依赖 Model
        # Controller 还需要 ModuleManager 来激活其他模块
        controller = MainController(model, module_manager)
        view = MainView(parent_view, model)

        return model, view, controller
