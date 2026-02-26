"""POS tagging solutions for Assignment 2 (Python 3.12+)."""

import collections
import itertools
import math
import time
import nltk

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train: list[str]) -> tuple[list[list[str]], list[list[str]]]:
    """

    """
    brown_words: list[list[str]] = []
    brown_tags: list[list[str]] = []
   
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags: list[list[str]]) -> dict[tuple[str, str, str], float]:
    """
    """
    q_values: dict[tuple[str, str, str], float] = {}
    return q_values


# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values: dict[tuple[str, str, str], float], filename: str) -> None:
    """Write trigram log probabilities to a file.

    Args:
        q_values: Dict mapping trigram tuples to log probabilities.
        filename: Output file path.

    Returns:
        None.
    """
    outfile = open(filename, "w")
    for trigram in sorted(q_values.keys()):
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python set where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words: list[list[str]]) -> set[list[str]]:
    """
    """
    known_words: set[list[str]] = set([])
    
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words: list[list[str]], known_words: set[list[str]]) -> list[list[str]]:
    """
    """
    brown_words_rare: list[list[str]] = []
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare: list[list[str]], filename: str) -> None:
    """Write sentences with rare replacements to a file.

    Args:
        rare: List of word sequences with rare replacements.
        filename: Output file path.

    Returns:
        None.
    """
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(
        brown_words_rare: list[list[str]],
        brown_tags: list[list[str]]
    ) -> tuple[dict[tuple[str, str], float], set[str]]:
    """
    """
    e_values: dict[tuple[str, str], float] = {}
    tags_list: set[list[str]] = set([])

    return e_values, tags_list

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values: dict[tuple[str, str], float], filename: str) -> None:
    """Write emission log probabilities to a file.

    Args:
        e_values: Dict mapping (word, tag) to log probability.
        filename: Output file path.

    Returns:
        None.
    """
    outfile = open(filename, "w")
    for item in sorted(e_values.keys()):
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(
        brown_dev_words: list[list[str]],
        taglist: set[str],
        known_words: set[str],
        q_values: dict[tuple[str, str, str], float],
        e_values: dict[tuple[str, str], float]
    ) -> list[str]:
    """
    """
    tagged: list[str] = []

    return tagged

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged: list[str], filename: str) -> None:
    """Write Viterbi-tagged sentences to a file.

    Args:
        tagged: List of tagged sentence strings.
        filename: Output file path.

    Returns:
        None.
    """
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(
        brown_words: list[list[str]],
        brown_tags: list[list[str]],
        brown_dev_words: list[list[str]]
    ) -> list[str]:
    """
    """
    # Hint: use the following line to format data to what NLTK expects for training
    training = [list(zip(brown_words[i], brown_tags[i])) for i in range(len(brown_words))]

    # IMPLEMENT THE REST OF THE FUNCTION HERE
    tagged: list[str] = []
    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    """Write NLTK-tagged sentences to a file.

    Args:
        tagged: List of tagged sentence strings.
        filename: Output file path.

    Returns:
        None.
    """
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    """Run all steps for Part B and write outputs."""
    # start timer
    start_time = time.perf_counter()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    elapsed = time.perf_counter() - start_time
    print("Part B time: " + str(elapsed) + ' sec')

if __name__ == "__main__":
    main()
