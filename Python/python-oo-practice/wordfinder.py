"""Word Finder: finds random words from a dictionary."""
from random import randint


class WordFinder:
    """creates a list of words from a file you can generate random words from

    Expects:
    path: path to the local file containing a list of words
    ---------------------
    Attributes:
    random: returns random word from the list given"""

    def __init__(self, path):
        """takes a list of words and puts them in a list under the words attribute.
            prints out the amount of words that are in the list"""
        self.words = []
        self.num_words_read = self.read_and_count(path)
        self.print_num_words()

    def random(self):
        """returns a random word from the given list"""
        rand_index = randint(0, self.num_words_read)
        return self.words[rand_index]

    def read_and_count(self, path):
        """reads words list file and puts the words in to a list while counting total number of words"""
        word_count = 0
        words_file = open(path, "r")

        for word_line in words_file:
            word_count += 1
            word = word_line[0:-2]
            self.words.append(word)

        words_file.close()

        return word_count

    def print_num_words(self):
        """prints out the number of words read in the file"""
        print(f"{self.num_words_read} words read")


class SpecialWordFinder(WordFinder):
    """Deals with a list with blank lines and comments

    >>>SpecialWordFinder("spaced_words.txt")
    68 words read
    """

    def __init__(self, path):
        """sets up the words file and defines the banned characters"""
        self.BANNED_CHARACTERS = ["#", "\n"]
        super().__init__(path)

    def read_and_count(self, path):
        """reads words list file and puts the words in to a list while counting total number of words"""
        word_count = 0
        words_file = open(path, "r")

        for word_line in words_file:
            if word_line[0] not in self.BANNED_CHARACTERS:
                word_count += 1
                word = word_line[0:-2]
                self.words.append(word)

        words_file.close()

        return word_count
