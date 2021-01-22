def print_upper_words(words, letters):
    """Prints out each word entered in all caps"""
    upper_words = []
    upper_letters = []

    for word in words:
        upper_word = word.upper()
        upper_words.append(upper_word)

    for letter in letters:
        upper_letter = letter.upper()
        upper_letters.append(upper_letter)

    for word in upper_words:
        if word[0] in upper_letters or word[0].upper() in upper_letters:
            print(word.upper())
