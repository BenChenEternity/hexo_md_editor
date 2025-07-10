from abc import abstractmethod


class Factory:
    def __init__(self, module_name, module_manager):
        self.module_name = module_name
        self.module_manager = module_manager

    @abstractmethod
    def assemble(self, parent_view, model_data):
        """
        返回 MVC 三元组
        """
        pass
