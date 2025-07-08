from collections import defaultdict
from typing import Callable, Any


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def register(self, event_name: str, callback: Callable[..., Any]):
        """消费者注册事件处理器"""
        if callback not in self._subscribers[event_name]:
            self._subscribers[event_name].append(callback)

    def unregister(self, event_name: str, callback: Callable[..., Any]):
        """取消注册事件处理器"""
        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def emit(self, event_name: str, *args, **kwargs):
        """生产者触发事件"""
        for callback in self._subscribers.get(event_name, []):
            callback(*args, **kwargs)


bus = EventBus()


class Producer:
    def __init__(self):
        self.bus = bus

    def send_event(self, event_name: str, *args, **kwargs):
        self.bus.emit(event_name, *args, **kwargs)


class Consumer:
    def __init__(self):
        self.bus = bus

    def subscribe(self, event_name: str, handler: Callable[..., Any]):
        self.bus.register(event_name, handler)

    def unsubscribe(self, event_name: str, handler: Callable[..., Any]):
        self.bus.unregister(event_name, handler)
