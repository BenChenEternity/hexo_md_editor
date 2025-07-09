from abc import ABC, abstractmethod

from src.core.mvc_template.event_bus import Consumer

from .model import Model


class Controller(Consumer, ABC):
    """
    控制器(Controller)组件的抽象基类模板。
    它继承自 Consumer，用于监听视图发出的UI事件。
    """

    def __init__(self, model: Model):
        """
        构造函数。
        :param model: 与此控制器关联的模型实例。
        """
        super().__init__()
        self.model = model
        self._setup_handlers()

    @abstractmethod
    def _setup_handlers(self):
        """
        [子类必须实现] 注册所有需要处理的UI事件。
        例如: self.subscribe(UI_BUTTON_CLICKED, self.on_button_click)
        """
        pass

    def cleanup(self):
        """
        在模块销毁时执行清理工作。
        核心任务是取消所有事件注册，防止内存泄漏。
        子类如果重写此方法，应调用 super().cleanup()。
        """
        self.unsubscribe_all()
