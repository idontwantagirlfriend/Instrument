class utils:
    @staticmethod
    def flush(object: any):
        if isinstance(object, str):
            return str()
        if isinstance(object, float):
            return float()
        if isinstance(object, int):
            return int()
        if isinstance(object, list):
            return list()

    @staticmethod
    def removeRedundantSpaceChar(string):
        words = string.split(" ")
        return " ".join(utils.removeNullElements(words))

    @staticmethod
    def removeNullElements(list):
        for (index, element) in enumerate(list):
            if not element:
                list.pop(index)
        return list
