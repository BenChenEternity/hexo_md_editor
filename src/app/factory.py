from src.app.controller import MainController
from src.app.model import MainModel
from src.app.view import MainView
from src.services.factory import Factory


class MainFactory(Factory):
    def assemble(self, parent_view, model_data):
        model = MainModel(model_data)
        controller = MainController(model, self.module_manager)
        view = MainView(parent_view, model)

        return model, view, controller
