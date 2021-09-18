from utils import utils
from Paragraph import Paragraph

"""[summary]
    A word-level segmentation. You are supposed to use the main(path,export) method in order to input the raw text and export the formatted text (both as filepath).
    This is done in several steps:
    0. Seperate paragraphs by linebreaker characters i.e. \n
    0.1 Wash empty lines: only non-empty lines are counted into the paragraphs
    1. Seperate a sentence when the symbol character precedes immediately the quotation mark. i.e. : ." (\W*)
    2. For general space patterns like \s, detect sentences (sentence segementation) by the previous character. i.e. : (.?!) => sentence ; (others) => word
    3. Detect words on the occurrence of symbol characters
    4. Normally, without divisor, will add the character at the current pointer position into cache level 1
    5. Finalize. Wash empty paragraphs again.
    6. Decorate the segmentated article with line markers (Lx) and sentence index numbers (x.x). Output the result in str.
    See doc file for more implementation info.

    Returns:
        list
    """


def divideParagraphs(rawtext: str):
    paragraphs = [paragraph.strip(" ") for paragraph in rawtext.split("\n")]
    return utils.removeNullElements(paragraphs)


def segParagraph(rawtext: str):
    paragraphs = divideParagraphs(rawtext)
    result = []
    for paragraph in paragraphs:
        result.append(segSentence(paragraph))
    return utils.removeNullElements(result)


def segSentence(rawtext):
    """Sentence-level segmentation. Need to be paired with paragraph-level seg method. """
    return Paragraph(utils.removeRedundantSpaceChar(rawtext)).parse()
