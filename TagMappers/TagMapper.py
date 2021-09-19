from abc import ABC, abstractmethod


class TagMapper(ABC):
    def __init__(self):
        self._hitCount = 0

    @property
    @abstractmethod
    def _tagLibrary(self):
        pass

    def doMap(self, token):
        result = ""
        for _ in self._tagLibrary:
            if token.lower() == _.lower():
                self.__incrementHitCount()
                result = self._tagLibrary[_]
                break

        return [token, result]

    def map(self, token):
        match = self.doMap(token)

        if match[1]:
            match = self.AutoCapFirstLetter(match)

        return match[1]

    def AutoCapFirstLetter(self, match: list):
        token, result = match[0], match[1]

        def isCapital(char: str):
            return char.isalpha() and char.lower() != char

        if result[0].isalpha() and isCapital(token[0]):
            result = result.capitalize()

        return [token, result]

    def resetHitCount(self):
        self._hitCount = 0

    def __incrementHitCount(self):
        self._hitCount += 1

    @property
    def hitCount(self):
        return self._hitCount
