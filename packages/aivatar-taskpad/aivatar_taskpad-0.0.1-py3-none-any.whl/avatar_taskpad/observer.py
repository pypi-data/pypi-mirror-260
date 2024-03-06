# -*- coding: utf-8 -*-

class Event:
    """Event class for Observer pattern."""

    def __init__(self, event_type, data):
        self.event_type = event_type
        self.data = data

class Observer():
    """Observer class for Observer pattern."""

    def on_event(self, event):
        raise NotImplementedError('Observer.on_event() must be implemented')

class Observable:
    """Observable class for Observer pattern."""

    def __init__(self):
        self._observers = []

    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            result = observer.on_event(event)
            if result is not None:
                return result
        return None
