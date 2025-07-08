from collections import defaultdict
from typing import Any, Callable, List, Tuple


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def register(self, event_name: str, callback: Callable[..., Any]):
        """消费者注册事件处理器"""
        if callback not in self._subscribers[event_name]:
            self._subscribers[event_name].append(callback)

    def unregister(self, event_name: str, callback: Callable[..., Any]):
        """取消注册事件处理器"""
        # 使用 try-except 避免在回调不存在时出错
        try:
            self._subscribers[event_name].remove(callback)
        except ValueError:
            # 可以选择在此处记录一个警告，说明尝试取消一个未注册的回调
            pass

    def emit(self, event_name: str, *args, **kwargs):
        """生产者触发事件"""
        # 遍历列表的副本，以允许在回调中取消订阅
        for callback in self._subscribers.get(event_name, []):
            callback(*args, **kwargs)


bus = EventBus()


class Producer:
    def __init__(self):
        self.bus = bus

    def send_event(self, event_name: str, *args, **kwargs):
        self.bus.emit(event_name, *args, **kwargs)


class Consumer:
    """
    事件消费者基类。
    优化点：自动跟踪订阅，并提供一键取消所有订阅的功能。
    """

    def __init__(self):
        self.bus = bus
        self._subscriptions: List[Tuple[str, Callable]] = []

    def subscribe(self, event_name: str, handler: Callable[..., Any]):
        """订阅一个事件，并记录下来。"""
        self.bus.register(event_name, handler)
        self._subscriptions.append((event_name, handler))

    def unsubscribe(self, event_name: str, handler: Callable[..., Any]):
        """取消单个订阅，并从记录中移除。"""
        self.bus.unregister(event_name, handler)
        try:
            self._subscriptions.remove((event_name, handler))
        except ValueError:
            pass

    def unsubscribe_all(self):
        """
        --- 新增核心方法 ---
        取消此消费者实例的所有订阅。
        在组件销毁时调用此方法，以防止内存泄漏。
        """
        for event_name, handler in self._subscriptions:
            self.bus.unregister(event_name, handler)
        self._subscriptions.clear()
