import pool_en
import pool_zh
import pool_seg


def capDetection(mRRaw: list):
    """Capture the result of tagging.match method and detect capitalization.
    Raw result must start with alphabetic character."""
    if mRRaw[0][0].lower() == mRRaw[0][0]:
        return mRRaw[1]
    else:
        return mRRaw[1].capitalize()


class matchAText:
    def __init__(self):
        self.hitcount = 0
        self.switchPool = {
            "seg": pool_seg.matching,
            "en": pool_en.matching,
            "zh": pool_zh.matching
        }

    def matchings(self, langCode):
        return self.switchPool[langCode]

    def match(self, kami, matchings):
        """Iterate over the match pool key and attempt to find a tag, return matchRawResult (mRRaw) used later in this package."""
    # Not sure if the input is a string instance or void or sth else.
        try:
            for _ in matchings:
                if kami.lower() == _.lower():
                    return [kami, matchings[_]]
        except:
            pass
        return str()

    def matchResult(self, kami, langCode):
        """Controller of match raw result re-formatting."""
        """Must indicate matching language: en for fr->en match, zh for fr->zh match."""
        mRRaw = self.match(kami, self.matchings(langCode))
        if mRRaw:
            if langCode == "seg":
                self.hitcount += 1
            if mRRaw[0][0].isalpha() and mRRaw[1][0].isalpha():
                return capDetection(mRRaw)
            else:
                return mRRaw[1]
        return mRRaw

# def leftMostAlphaChar(token:str):
#     i=-1
#     for _ in token:
#         i+=1
#         if _.isalpha():
#             return i
