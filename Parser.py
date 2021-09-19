from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self):
        self._elements = []

    @abstractmethod
    def addElement(self, newElement):
        self._elements.append(newElement)

    @abstractmethod
    def parse(self):
        return [element.parse() for element in self._elements]
