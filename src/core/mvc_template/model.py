from abc import ABC, abstractmethod

from src.core.mvc_template.event_bus import Producer


class Model(Producer, ABC):
    """
    模型(Model)组件的抽象基类模板。
    它继承自 Producer，因此所有模型都可以发送事件。
    """

    def __init__(self):
        """
        构造函数。自动调用父类 Producer 的构造函数。
        """
        super().__init__()

    @abstractmethod
    def initialize(self):
        """
        用于初始化模型数据的抽象方法。
        子类必须实现此方法来设置其初始状态。
        """
        pass

    def cleanup(self):
        """
        在模块销毁时执行清理工作（如果需要）。
        默认情况下无操作，子类可以根据需要重写。
        """
        pass
