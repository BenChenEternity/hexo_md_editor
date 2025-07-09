import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk

from src.core.mvc_template.event_bus import Consumer, Producer

from .model import Model


class View(ttk.Frame, Consumer, Producer, ABC):
    """
    视图(View)组件的抽象基类模板。
    - 继承 ttk.Frame，使其成为一个可用的UI容器。
    - 继承 Consumer，用于监听模型的状态事件。
    - 继承 Producer，用于发送用户的UI操作事件。
    """

    def __init__(self, master: tk.Misc, model: Model):
        """
        构造函数。
        :param master: 父Tkinter控件。
        :param model: 与此视图关联的模型实例。
        """
        # 依次安全地调用所有父类的构造函数
        ttk.Frame.__init__(self, master)
        Consumer.__init__(self)
        Producer.__init__(self)

        self.model = model

        # 定义一个标准化的UI创建流程
        self._create_widgets()
        self._setup_bindings()
        self._setup_subscriptions()

    @abstractmethod
    def _create_widgets(self):
        """
        [子类必须实现] 创建该视图所需的所有UI控件。
        """
        pass

    @abstractmethod
    def _setup_bindings(self):
        """
        [子类必须实现] 将UI控件的动作（如点击）绑定到发送UI事件的命令上。
        例如: self.my_button.config(command=lambda: self.send_event(...))
        """
        pass

    @abstractmethod
    def _setup_subscriptions(self):
        """
        [子类必须实现] 订阅所有关心的模型状态事件。
        例如: self.subscribe(EVENT_DATA_CHANGED, self.on_data_changed)
        """
        pass

    def cleanup(self):
        """
        在模块销毁时执行清理工作。
        核心任务是取消所有事件订阅，防止内存泄漏。
        子类如果重写此方法，应调用 super().cleanup()。
        """
        self.unsubscribe_all()
