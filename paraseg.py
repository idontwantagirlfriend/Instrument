import re
from copy import deepcopy
import seg

"""This module can do a word-level segmentation. You are supposed to use the main(path,export) method in order to input the raw text and export the formatted text (both as filepath). 
This is done in several steps:
0. Seperate paragraphs by linebreaker characters i.e. \n
0.1 Wash empty lines: only non-empty lines are counted into the paragraphs
1. Seperate a sentence when the symbol character precedes immediately the quotation mark. i.e. : ." (\W*)
2. For general space patterns like \s, detect sentences (sentence segementation) by the previous character. i.e. : (.?!) => sentence ; (others) => word
3. Detect words on the occurrence of symbol characters
4. Normally, without divisor, will add the character at the current pointer position into cache level 1
5. Finalize. Wash empty paragraphs again. 
6. Decorate the segmentated article with line markers (Lx) and sentence index numbers (x.x). Output the result in str. 
"""

def wash(string):
    """Detect redundant space markers."""
    lst=string.split(" ")
    lst2=[]
    for c in lst:
        if c:
            lst2.append(c)
    return " ".join(lst2)

def wash(list):
    temp=[]
    for c in list:
        if c :
            temp.append(c)
    return temp

def tag(rawtext):
    """(Deprecated) Main executive function that return the (not very accurate) segmentated text. """
    kami=wash(rawtext)
    kami2=""
    for c in range(len(kami)):
        #for patterns like 'I saw this man."', when the symbol character precedes immediately the quotation mark. 
        try:
            if (kami[c] in ["\"","»"]) and (kami[c-1].isalnum()==False) and (bool(re.findall("\s",kami[c-1]))==False):
                kami2+=kami[c]+"\n"
                continue
        except:
            pass
        try:
            if (kami[c] in ["\"","»"]) and (kami[c-2].isalnum()==False) and (bool(re.findall("\s",kami[c-2]))==False):
                kami2+=kami[c]+"\n"
                continue
        except:
            pass
        #for general space patterns like \s. Detect paragraph (sentence segementation) by the previous character.
        if re.findall("\s",kami[c]):
            try:
                if (kami[c-1] in [".","?","!"]):
                    kami2+="\n"
                else:
                    kami2+="\t"
                continue
            except:
                pass
        #for general symbols, add a tab character before. if the symbol requires a space before it, add no tab  character. 
        # try:
        #     if (kami[c].isalnum()==False):
        #             if kami[c] in ["-", "'","’","?","!","[","(",":",";"]:
        #                 pass
        #             elif (kami[c-1].isdigit()) and (kami[c+1].isdigit()):
        #                 pass
        #             else:
        #                 kami2+="\t"
        #             kami2+=kami[c]
        #             if kami[c] in ["\""]:
        #                 kami2+="\t"
        #             #kami2+="\t"
        #             continue
        # except:
        #     pass
        if (kami[c].isalnum()==False):
            if kami[c] in ["-", "'","’","?","!","[","(",":",";","«","»"]:
                pass
            else:
                try:
                    if(kami[c-1].isdigit()) and (kami[c+1].isdigit()):
                        pass
                    else:
                        raise Exception
                except:
                    kami2+="\t"
            kami2+=kami[c]
            if kami[c] in ["\""]:
                kami2+="\t"
            continue
            
        kami2+=kami[c]
    #remove redundant space char after seg.
    kami2=re.sub("\s*»","\t»",kami2)
    kami2=re.sub("\t\t","\t",kami2)
    kami2=re.sub("\t\n","\n",kami2)
    kami2=re.sub("\n\t","\n",kami2)
    return kami2

def clear(thingy:callable):
    if isinstance(thingy,str):
        return str()
    if isinstance(thingy,float):
        return float()
    if isinstance(thingy,int):
        return int()
    if isinstance(thingy,list):
        return list()

def segSentence(rawtext):
    """Sentence-level segmentation. Need to be paired with paragraph-level seg method. """
    kami=wash(rawtext)
    kami2="" # Cache level 1
    kami3=[] # Cache level 2
    kamiTotal=[] # Prepared result
    for c in range(len(kami)):
        # 1. For patterns like 'I saw this man."', when the symbol character precedes immediately the quotation mark. 
        try:
            if (kami[c] in ["\"","»"]) and (kami[c-1].isalnum()==False) and (bool(re.findall("\s",kami[c-1]))==False) and re.findall("\s",kami[c+1]):
            # For the following patterns: 
            # [...] safe and sound <str>." And</str> went on... [...]
            # =>
            # [[...], [[...] safe and sound."], [And went on... [...]], [...]]
                kami2+=kami[c]
                kami3.append(kami2)
                kamiTotal.append(kami3)
                kami2=clear(kami2)
                kami3=clear(kami3)
                continue
        except:
            pass
        try:
            if (kami[c] in ["\"","»"]) and (kami[c-2].isalnum()==False) and (bool(re.findall("\s",kami[c-2]))==False) and re.findall("\s",kami[c+1]):
            # For the following patterns: 
            # [...] safe and sound <str>. " And</str> went on... [...]
            # =>
            # [[...], [[...] safe and sound. "], [And went on... [...]], [...]]
                kami2+=kami[c]
                kami3.append(kami2)
                kamiTotal.append(kami3)
                kami2=clear(kami2)
                kami3=clear(kami3)
                continue
        except:
            pass
        # 2. For general space patterns like \s. Detect paragraph (sentence segementation) by the previous character. 
        if re.findall("\s",kami[c]):
            try:
                if (kami[c-1] in [".","?","!"]):
                    kami3.append(kami2)
                    kamiTotal.append(kami3)
                    kami2=clear(kami2)
                    kami3=clear(kami3)
                else:
                    kami3.append(kami2)
                    kami2=clear(kami2)
                continue
            except:
                pass
        # 3. Detect word on the occurrence of symbol characters:
        # 3.1 normally: the preceding word and the symbol characters, as two individual words.  
        # 3.1.1 symbol characters as part of the preceding word: est-ce
        # 3.1.2 numbers with digits: "7.27", "99,39"
        # 3.1.3 symbol characters preceded by space characters, i.e. \s\W
        # 3.2 normally: right after the symbol character there's no word division, as a space character immediately follows
        # 3.2.1 no space afterward: symbol characters as part of the following word, i.e. est-ce
        #3.2.2 no space afterward: the space was dropped, then start a new word, i.e. "He did not see me.But I was always there"
        
        if (kami[c].isalnum()==False):
            if c==0:
                pass
            elif re.findall("\s",kami[c-1]):
                # 3.1.3 symbol characters preceded by space characters, i.e. \s\W
                pass
            elif kami[c] in ["'","-","’"]:
                # 3.1.1 symbol characters as part of the preceding word: est-ce
                pass
            else:
                try:
                    if(kami[c-1].isdigit()) and (kami[c+1].isdigit()):
                        # 3.1.2 numbers with digits: "7.27", "99,39"
                        pass
                    else:
                        raise Exception
                except:
                    # 3.1 normally: the preceding word and the symbol characters, as two individual words.  
                    kami3.append(kami2)
                    kami2=clear(kami2)

            kami2+=kami[c]

            if (c==len(kami)-1):
                kami3.append(kami2)
                kami2=clear(kami2)
            elif (bool(re.findall("\s",kami[c+1]))==False) and (kami[c] in ["'","-","’"]):
                # 3.2.1 no space afterward: symbol characters as part of the following word, i.e. est-ce
                pass
            elif (bool(re.findall("\s",kami[c+1]))==False):
                #3.2.2 no space afterward: the space was dropped, then start a new word, i.e. "He did not see me.But I was always there"
                kami3.append(kami2)
                kami2=clear(kami2)
            else:
                # 3.2 normally: right after the symbol character there's no word division, as a space character immediately follows
                pass
            continue

        # 4. Normally, without divisor, will add character at current pointer into cache level 1
        kami2+=kami[c]

    # Finalize. Submit remaining chars in caches. Clear caches. 
    kami3.append(kami2)
    kamiTotal.append(kami3)
    kami2=clear(kami2)
    kami3=clear(kami3)
    # By this time, the segmentation should have already been done in kamiTotal:list.

    # print("Primary seg has been completed.")
    # if len(kamiTotal)>10:
    #     for _ in range(10):
    #         print(" ".join(kamiTotal[_]))
    # else:
    #     for sentence in kamiTotal:
    #         print(" ".join(sentence))

    # Remove redundant space char.
    kami4=[] # cache level 3
    for sentence in kamiTotal:
        if sentence:
            for word in sentence:
                if word:
                    kami3.append(word)
            kami4.append(kami3)
            kami3=clear(kami3)

    kamiTotal=kami4
    kami4=clear(kami4)
    # print("Removal of redundant empty elements has been completed.")
    # if len(kamiTotal)>10:
    #     for _ in range(10):
    #         print(" ".join(kamiTotal[_]))
    # else:
    #     for sentence in kamiTotal:
    #         print(" ".join(sentence))
    
    # print(kamiTotal)

    # Shrink closing quote onto the previous list (sentence).
    # Correspond to the part ' kami2=re.sub("\s*»","\t»",kami2) '.
    manualSentenceIndex=0
    manualWordIndex=0
    for sentence in kamiTotal:
        for word in sentence:
            if (word=="»") and (manualWordIndex==0):
                if manualSentenceIndex>0:
                    kami4[manualSentenceIndex-1].append(word)
                    continue
            kami3.append(word)
            manualWordIndex+=1
        kami4.append(kami3)
        manualSentenceIndex+=1

        kami3=clear(kami3)
        manualWordIndex=0

    kamiTotal=kami4
    kami4=clear(kami4)
    manualSentenceIndex=clear(manualSentenceIndex)


    # print("Hanging quotation marks have been fixed. Previewing...")
    # if len(kamiTotal)>10:
    #     for _ in range(10):
    #         print(" ".join(kamiTotal[_]))
    # else:
    #     for sentence in kamiTotal:
    #         print(" ".join(sentence))

    return kamiTotal

def divParagraph(rawtext:str):
    """divide the raw text into paragraphs. Returns a list of paragraph contents:str"""
    kami3=[paragraph.strip(" ") for paragraph in rawtext.split("\n")]
    return wash(kami3)

def segParagraph(rawtext:str):
    """To be paired with sentence-level seg method. Returns a list of fully segmentated paragraph until word-level. """
    paragraphs=divParagraph(rawtext)
    result=[]
    for paragraph in paragraphs:
        result.append(segSentence(paragraph))
    return wash(result) # A three level list: article - paragraph - sentence

def main(path,export):
    with open(path, mode="r", encoding="utf-8") as file:
        rawtext=file.read()
    result=segParagraph(rawtext)

    print("The segmentation is done. Previewing... ")
    if len(result)>3:
        for _ in range(3):
            print(result[_])
    else:
        for _ in result:
            print(_)

    # A generic boilplate, L2-L6 are left blank. 
    # lineTail="\n\tL2\n\tL3\n\tL4\n\tL5\n\tL6\n"
    with open(export, mode="a", encoding="utf-8") as exportFile:
        i=0
        j=0
        k=0
        processor=seg.matchAText()
        for paragraph in result:
            i+=1
            for sentence in paragraph:
                j+=1
                # L1: segmentated raw text
                exportFile.write(f"{i}.{j}\tL1\t")
                exportFile.write("\t".join(sentence))
                # exportFile.write(lineTail)
                # L2: morpheme-by-morpheme seg text
                exportFile.write("\n\tL2\t")
                exportFile.write("\t".join([processor.matchResult(word,"seg",) for word in sentence]))
                # L3: English glossary
                exportFile.write("\n\tL3\t")
                exportFile.write("\t".join([processor.matchResult(word,"en") for word in sentence]))
                #L4: Idiomatic English translation, left blanc
                exportFile.write("\n\tL4")
                #L5: Chinese glossary
                exportFile.write("\n\tL5\t")
                exportFile.write("\t".join([processor.matchResult(word,"zh") for word in sentence]))
                #L6: Idiomatic Chinese translation, left blanc
                exportFile.write("\n\tL6\n")
                k+=len(sentence)
            j=clear(j)
        i=clear(i)
        print("="*12)
        print(f"Word count: {k}")
        print(f"Automatic glossing percentage: {processor.hitcount/k:.2%}")
        processor.hitcount=clear(processor.hitcount)
        k=clear(k)
