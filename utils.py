class utils:
    @staticmethod
    def removeSpaceChar(string):
        words = string.split(" ")
        return " ".join(utils.removeFalsyElements(words))

    @staticmethod
    def removeFalsyElements(list):
        for (index, element) in enumerate(list):
            if not element:
                list.pop(index)
        return list
