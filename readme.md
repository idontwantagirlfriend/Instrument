# How this segmentation tool works

The code was terribly messy so I do a bit clean up.
- Segmentation:
    # 1. Current char is quotation mark? For patterns like 'I saw this man."', .
        # For the following patterns:
                # [...] safe and sound <str>." And</str> went on... [...]
                # =>
                # [[...], [[...] safe and sound."], [And went on... [...]], [...]]
        # There doesn't exist any space char between "," and close quotation mark, we thus need to delimit the previous word manually.
                            # "," does not start a new sentence
                # Other char can start a new sentence, such as:
                # He picked up his bag and retorted: "I don't think so."
                # Chaque fois que mes parents commençaient: « Il faut que tu.. »
        # For the following patterns:
                # [...] safe and sound <str>. " And</str> went on... [...]
                # =>
                # [[...], [[...] safe and sound. "], [And went on... [...]], [...]]
                                # "," does not start a new sentence
                # Other char can start a new sentence, such as:
                # Chaque fois que mes parents commençaient: « Il faut que tu... »

      # 2. Current char is a space char? Detect paragraph (sentence segementation) by the previous character.

      # 3. Normal non-alnum symbol char? 
        # 3.1 normally: the preceding word and the symbol characters, as two individual words.
        # 3.1.1 symbol characters as part of the preceding word: est-ce
        # 3.1.2 numbers with digits: "7.27", "99,39"
        # 3.1.3 symbol characters preceded by space characters, i.e. \s\W
        # 3.2 normally: right after the symbol character there's no word division, as a space character immediately follows
        # 3.2.1 no space afterward: symbol characters as part of the following word, i.e. est-ce
        # 3.2.2 no space afterward: the space was dropped, then start a new word, i.e. "He did not see me.But I was always there"
      # 4. Normally, without divisor, will add character at current pointer into cache level 1
       # Finalize. Submit remaining chars in caches. Clear caches.
        # By this time, the segmentation should have already been done in kamiTotal:list.
        # Shrink closing quote onto the previous list (sentence).

- Glossing:
  - Simply map every token to a glossing tag. Done. Res in pool_*.py



