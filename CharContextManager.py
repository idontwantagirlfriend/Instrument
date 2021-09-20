import re


class CharContextManager:
    sentenceSeperators = [".", "?", "!"]
    cliticChars = ["'", "-", "’", "%"]
    quotationMarks = ["\"", "»", "“", "”", "\""]
    closingQuotes = ["»", "”"]

    def __init__(self):
        self.__wordCache = []
        self.__sentenceCache = []
        self.__result = []

    def handleEndOfQuote(self, text, position):
        self.__endOfWord()
        self.__wordCache.append(text[position])
        self.__endOfWord()

        previousChar = text[position-1]
        if not re.findall(",", previousChar):
            self.__endOfSentence()

        self.handleCache(text, position)

    def handleStartOfQuote(self, text, position):
        self.__wordCache.append(text[position])
        self.__endOfWord()

    def handleStartOfQuoteBadUsage(self, text, position):
        self.__endOfWord()
        self.handleStartOfQuote(text, position)

    def handleSpaceChar(self, text, position):
        self.__endOfWord()

        # No need for verification because content has been stripped upon initialization
        previousChar = text[position-1]
        if (CharContextManager.isSentenceSeparator(previousChar)):
            self.__endOfSentence()

    def handleSymbol(self, text, position):
        if self.isEndOfWord(text, position):
            self.__endOfWord()

        self.__wordCache.append(text[position])

        if position == 0:
            self.__endOfWord()

        self.handleCache(text, position)

    def handleAlNumChar(self, text, position):
        self.__wordCache.append(text[position])
        self.handleCache(text, position)

    def handleCache(self, text, position):
        if position == len(text)-1:
            self.__endOfWord()
            self.__endOfSentence()

    def isEndOfQuote(self, string, pos):
        result = pos > 0 and pos < len(string)-1
        if result:
            currentChar = string[pos]
            previousChar = string[pos-1]
            nextChar = string[pos+1]
            result &= self.isQuotationMark(currentChar) and not(
                self.isAlNum(previousChar) and self.isSpaceChar(previousChar)) and self.isSpaceChar(nextChar)
        return result

    def isStartOfQuote(self, string, pos):
        result = pos > 1
        if result:
            currentChar = string[pos]
            previousChar = string[pos-1]
            beforePreviousChar = string[pos-2]
            result &= (self.isQuotationMark(currentChar)) and not(self.isAlNum(
                beforePreviousChar) and self.isSpaceChar(beforePreviousChar)) and self.isSpaceChar(previousChar)
        return result

    def isStartOfQuoteBadUsage(self, string, pos):
        result = pos > 1 and pos < len(string)-1
        if result:
            currentChar = string[pos]
            previousChar = string[pos-1]
            nextChar = string[pos+1]
            result &= self.isQuotationMark(
                currentChar) and previousChar == ":" and self.isAlNum(nextChar)
        return result

    def isEndOfWord(self, string, pos):
        result = pos > 0
        if result:
            currentChar = string[pos]
            previousChar = string[pos-1]

            isDecimalSeparator = pos < len(
                string)-1 and (previousChar.isdigit()) and (string[pos+1].isdigit())
            result &= not self.isSpaceChar(previousChar) and not self.isClitic(
                currentChar) and not isDecimalSeparator
        return result

    def __endOfWord(self):
        self.__sentenceCache.append("".join(self.__wordCache))
        self.__wordCache.clear()

    def __endOfSentence(self):
        sentence = [token for token in self.__sentenceCache]
        self.__sentenceCache.clear()
        self.__result.append(sentence)

    @property
    def result(self):
        return self.__result

    @staticmethod
    def isAlNum(char):
        return isinstance(char, str) and char.isalnum()

    @staticmethod
    def isSpaceChar(char):
        return bool(re.findall("\s", char))

    @staticmethod
    def isQuotationMark(char):
        return char in CharContextManager.quotationMarks

    @staticmethod
    def isClosingQuote(char):
        return char in CharContextManager.closingQuotes

    @staticmethod
    def isSentenceSeparator(char):
        return char in CharContextManager.sentenceSeperators

    @staticmethod
    def isClitic(char):
        return char in CharContextManager.cliticChars
