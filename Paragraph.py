import re
from utils import utils


class Paragraph():

    sentenceSeperators = [".", "?", "!"]
    cliticChars = ["'", "-", "’", "%"]
    quotationMarks = ["\"", "»", "”"]
    closingQuotes = ["»", "”"]

    def __init__(self, content):
        self.content = content

    def parse(self):
        isQuotationMark, isAlNum, isSpaceChar, isClosingQuote, isSentenceSeparator, isClitic = Paragraph.isQuotationMark, Paragraph.isAlNum, Paragraph.isSpaceChar, Paragraph.isClosingQuote, Paragraph.isSentenceSeparator, Paragraph.isClitic

        currentWord = ""
        currentSentence = []
        result = []
        for index in range(len(self.content)):
            currentChar = self.content[index]

            try:
                previousChar = self.content[index-1]
                nextChar = self.content[index+1]

                if isQuotationMark(currentChar) and not(isAlNum(previousChar) and isSpaceChar(previousChar)) and isSpaceChar(nextChar):
                    if re.findall(",", previousChar):
                        currentSentence.append(currentWord)
                        currentWord = utils.flush(currentWord)

                    currentWord += currentChar
                    currentSentence.append(currentWord)

                    if re.findall(",", previousChar):
                        pass

                    else:
                        result.append(currentSentence)
                        currentSentence = utils.flush(currentSentence)

                    currentWord = utils.flush(currentWord)
                    continue
            except IndexError:
                pass

            try:
                previousChar = self.content[index-1]
                nextChar = self.content[index+1]
                beforePreviousChar = self.content[index-2]

                if (isQuotationMark(currentChar)) and not(isAlNum(beforePreviousChar) and isSpaceChar(beforePreviousChar)) and isSpaceChar(nextChar):
                    currentWord += currentChar
                    currentSentence.append(currentWord)

                    if re.findall(",", beforePreviousChar):
                        pass
                    else:
                        result.append(currentSentence)
                        currentSentence = utils.flush(currentSentence)

                    currentWord = utils.flush(currentWord)
                    continue
            except IndexError:
                pass

            if isSpaceChar(currentChar):
                currentSentence.append(currentWord)
                currentWord = utils.flush(currentWord)

                if (isSentenceSeparator(previousChar)):
                    result.append(currentSentence)
                    currentSentence = utils.flush(currentSentence)

                continue

            if not isAlNum(currentChar):
                if index == 0 or isSpaceChar(previousChar) or isClitic(currentChar) or ((previousChar.isdigit()) and (nextChar.isdigit())):
                    pass
                else:
                    currentSentence.append(currentWord)
                    currentWord = utils.flush(currentWord)

                currentWord += currentChar

                if (index == len(self.content)-1):
                    currentSentence.append(currentWord)
                    currentWord = utils.flush(currentWord)
                continue

            currentWord += currentChar

        currentSentence.append(currentWord)
        result.append(currentSentence)
        currentWord = utils.flush(currentWord)
        currentSentence = utils.flush(currentSentence)

        utils.removeNullElements(result)
        for sentence in result:
            utils.removeNullElements(sentence)

        for (sentenceIndex, currentSentence) in enumerate(result):
            for (wordIndex, currentWord) in enumerate(currentSentence):
                if sentenceIndex > 0 and isClosingQuote(currentWord) and wordIndex == 0:
                    result[sentenceIndex-1].append(currentWord)
                    currentSentence.pop(wordIndex)
                    continue

        return result

    @property
    def next(self):
        if hasattr(self, "_next"):
            return self._next

    @next.setter
    def next(self, newParagraph):
        self._next = newParagraph

    @staticmethod
    def isAlNum(char):
        return isinstance(char, str) and char.isalnum()

    @staticmethod
    def isSpaceChar(char):
        return bool(re.findall("\s", char))

    @staticmethod
    def isQuotationMark(char):
        return char in Paragraph.quotationMarks

    @staticmethod
    def isClosingQuote(char):
        return char in Paragraph.closingQuotes

    @staticmethod
    def isSentenceSeparator(char):
        return char in Paragraph.sentenceSeperators

    @staticmethod
    def isClitic(char):
        return char in Paragraph.cliticChars
