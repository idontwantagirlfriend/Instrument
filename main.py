from TagMappers.FrMorphemeMapper import FrMorphemeMapper
from TagMappers.FrEnMapper import FrEnMapper
from TagMappers.FrZhMapper import FrZhMapper
from ParagraphParser import ParagraphParser
from functools import reduce
from statistics import mean


def parseFile(path, exportPath):
    with open(path, mode="r", encoding="utf-8") as file:
        rawtext = file.read()

    parser = ParagraphParser()
    parser.addElement(rawtext)
    result = parser.parse()

    previewResult(result)

    exportToFile(exportPath, result)
    return True


def previewResult(result):
    print("The segmentation is done. Previewing... ")
    if len(result) > 3:
        for _ in range(3):
            print(result[_])
    else:
        for _ in result:
            print(_)


def exportToFile(exportPath, result):
    with open(exportPath, mode="a", encoding="utf-8") as exportFile:
        frMorphemeMapper = FrMorphemeMapper()
        frEnMapper = FrEnMapper()
        frZhMapper = FrZhMapper()
        for (i, paragraph) in enumerate(result):
            for (j, sentence) in enumerate(paragraph):
                # L1: segmentated raw text
                exportFile.write(f"{i}.{j}\tL1\t")
                exportFile.write("\t".join(sentence))
                # L2: morpheme-by-morpheme seg text
                exportFile.write("\n\tL2\t")
                exportFile.write("\t".join(frMorphemeMapper.map(word)
                                 for word in sentence))
                # L3: English glossary
                exportFile.write("\n\tL3\t")
                exportFile.write("\t".join(frEnMapper.map(word)
                                 for word in sentence))
                # L4: Idiomatic English translation, left blanc
                exportFile.write("\n\tL4")
                # L5: Chinese glossary
                exportFile.write("\n\tL5\t")
                exportFile.write("\t".join(frZhMapper.map(word)
                                 for word in sentence))
                # L6: Idiomatic Chinese translation, left blanc
                exportFile.write("\n\tL6\n")
        print("="*12)

        calculateHitRate(result, [frEnMapper, frZhMapper])


def calculateHitRate(result, mappers):
    tokenCount = reduce(lambda total, paragraph: total + reduce(
        lambda subtotal, sentence: subtotal + len(sentence), paragraph, 0), result, 0)
    print(f"Word count: {tokenCount}")
    avgHitRate = mean(
        mapper.hitCount/tokenCount for mapper in mappers)
    print(
        f"Automatic glossing percentage: {avgHitRate:.2%}")
