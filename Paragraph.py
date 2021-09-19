from utils import utils
from Parser import Parser
from CharContextManager import CharContextManager


class Paragraph(Parser):
    """[summary]
    A word-level segmentation. You are supposed to use the main(path,export) method in order to input the raw text and export the formatted text (both as filepath).
    This is done in several steps:\n
    0. Seperate paragraphs by linebreaker characters i.e. \n
    0.1 Wash null paragraphs: only non-empty lines are counted into the paragraphs\n
    1. Scan every character to be a...\n
        1.1. quotation mark? Does current sentence end?\n
        1.2. space char? Ends current word. Does current sentence end?\n
        1.3. normal non-alnum symbol char? Does current sentence end?\n
        1.4. other char: only add it to current word. \n
    2. Finalize: add cached word/sentence to parsed paragraph. \n
    3. Wash null tokens. \n

    Returns:\n
        list
    """

    def __init__(self, content: str):
        super().__init__()
        self.__content = content.strip()
        self.__charContextManager = CharContextManager()

    def addElement(self, newElement):
        return super().addElement(newElement)

    def parse(self):
        content = self.__content
        manager = self.__charContextManager

        self.__resetParseResult()

        for index in range(len(content)):

            if manager.isEndOfQuote(content, index):
                manager.handleEndOfQuote(content, index)

                continue

            if manager.isStartOfQuote(content, index):
                manager.handleStartOfQuote(content, index)

                continue

            if manager.isSpaceChar(content[index]):
                manager.handleSpaceChar(content, index)

                continue

            if not manager.isAlNum(content[index]):
                manager.handleSymbol(content, index)
                continue

            manager.handleAlNumChar(content, index)

        self._elements = manager.result

        self.__removeNullTokens()

        return self._elements

    def __removeNullTokens(self):
        utils.removeFalsyElements(self._elements)
        for sentence in self._elements:
            utils.removeFalsyElements(sentence)

    def __resetParseResult(self):
        self._elements = []
