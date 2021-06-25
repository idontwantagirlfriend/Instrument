def naturalJoin(kami):
    """Very naïve naturalJoin function. Join an iterable and return a string. The join method will comply to natural language rules of using space."""
    if hasattr(kami,"__iter__"):
        pass
    else:
        raise TypeError("NaturalJoin function requires an iterable parameter.")

    result=str()
    if bool(kami) is not True:
        return result

    if hasattr(kami,"__len__"):
        if len(kami)==1:
            return kami[0]
    else:
        raise TypeError("NaturalJoin requires the parameter to have \"__len__\" property.")
    
    import symbolCharSpaceParam
    # Fallback option is that every word must have a space after it. The principle is that the usage of space depends on a property of the symbol character. Some may require space before them, others don't. This latter rule prevails over the fallback rule.
    for (index,word) in enumerate(kami):
        result+=word
        if index==(len(kami)-1):
            continue
        if kami[index+1] in symbolCharSpaceParam.noSpaceBeforeChars:
            continue
        result+=" "
    return result

