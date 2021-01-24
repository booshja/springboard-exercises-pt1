def vowel_count(phrase):
    """Return frequency map of vowels, case-insensitive.

        >>> vowel_count('rithm school')
        {'i': 1, 'o': 2}

        >>> vowel_count('HOW ARE YOU? i am great!')
        {'o': 2, 'a': 3, 'e': 2, 'u': 1, 'i': 1}
    """

    VOWELS_LOWER = 'aeiou'
    phrase_lower = phrase.lower()
    frequency = {}

    for char in phrase_lower:
        if char in VOWELS_LOWER:
            if frequency.get(char) == None:
                frequency[char] = 1
            else:
                frequency[char] = frequency[char] + 1

    return frequency
