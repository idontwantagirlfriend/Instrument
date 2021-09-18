import segParagraph
import seg


def main(path, export):
    with open(path, mode="r", encoding="utf-8") as file:
        rawtext = file.read()
    result = segParagraph.segParagraph(rawtext)

    print("The segmentation is done. Previewing... ")
    if len(result) > 3:
        for _ in range(3):
            print(result[_])
    else:
        for _ in result:
            print(_)

    # A generic boilplate, L2-L6 are left blank.
    # lineTail="\n\tL2\n\tL3\n\tL4\n\tL5\n\tL6\n"
    with open(export, mode="a", encoding="utf-8") as exportFile:
        k = 0
        processor = seg.matchAText()
        for (i, paragraph) in enumerate(result):
            for (j, sentence) in enumerate(paragraph):
                # L1: segmentated raw text
                exportFile.write(f"{i}.{j}\tL1\t")
                exportFile.write("\t".join(sentence))
                # exportFile.write(lineTail)
                # L2: morpheme-by-morpheme seg text
                exportFile.write("\n\tL2\t")
                exportFile.write(
                    "\t".join([processor.matchResult(word, "seg",) for word in sentence]))
                # L3: English glossary
                exportFile.write("\n\tL3\t")
                exportFile.write(
                    "\t".join([processor.matchResult(word, "en") for word in sentence]))
                # L4: Idiomatic English translation, left blanc
                exportFile.write("\n\tL4")
                # L5: Chinese glossary
                exportFile.write("\n\tL5\t")
                exportFile.write(
                    "\t".join([processor.matchResult(word, "zh") for word in sentence]))
                # L6: Idiomatic Chinese translation, left blanc
                exportFile.write("\n\tL6\n")
                k += len(sentence)
        print("="*12)
        print(f"Word count: {k}")
        print(f"Automatic glossing percentage: {processor.hitcount/k:.2%}")


main("Number.txt", "Number_processed.txt")
