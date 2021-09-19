from Parser import Parser
from Paragraph import Paragraph
from CharContextManager import CharContextManager
from utils import utils


class ParagraphParser(Parser):
    def __init__(self):
        super().__init__()

    isClosingQuote = CharContextManager.isClosingQuote

    def addElement(self, passage):
        paragraphs = [Paragraph(paragraph)
                      for paragraph in self.__divideParagraphs(passage)]
        self._elements.extend(paragraphs)

    def parse(self):
        result = super().parse()
        return self.__shrinkHangingParagraphs(result)

    def __divideParagraphs(self, passage: str):
        paragraphs = [paragraph.strip(" ")
                      for paragraph in passage.split("\n")]
        return utils.removeFalsyElements(paragraphs)

    def __shrinkHangingParagraphs(self, result):
        for (sentenceIndex, currentSentence) in enumerate(result):
            for (wordIndex, currentWord) in enumerate(currentSentence):
                if sentenceIndex > 0 and ParagraphParser.isClosingQuote(currentWord) and wordIndex == 0:
                    result[sentenceIndex-1].append(currentWord)
                    currentSentence.pop(wordIndex)
                    continue
        return result
