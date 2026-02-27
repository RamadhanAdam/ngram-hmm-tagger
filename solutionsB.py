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
    Split tagged sentences into separate word tag lists.
    Each token "WORD/TAG" is split on the last '/' to handle words like "1/2/NUM".
    Each sentence is padded with two start symbols and one stop symbol.
    
    Args:
        brown_train: List of tagged sentences e.g. "He/PRON had/VERB\n"
    
    Returns:
        brown_words: [['*', '*', 'He', 'had', 'STOP'], ...]
        brown_tags:  [['*', '*', 'PRON', 'VERB', 'STOP'], ...]
    """
    brown_words: list[list[str]] = []
    brown_tags: list[list[str]] = []

    for sentence in brown_train:
        words = [START_SYMBOL, START_SYMBOL]
        tags = [START_SYMBOL, START_SYMBOL]
        for token in sentence.split():
            word, tag = token.rsplit("/",1)
            words.append(word)
            tags.append(tag)
        
        words.append(STOP_SYMBOL)
        tags.append(STOP_SYMBOL)

        brown_words.append(words)
        brown_tags.append(tags)
            
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags: list[list[str]]) -> dict[tuple[str, str, str], float]:
    """
    Compute log2 trigram probabilities for tag sequences.
    
    Args:
        brown_tags: List of tag sequences e.g. [['*', '*', 'PRON', 'VERB', 'STOP'], ...]
    
    Returns:
        Dict mapping tag trigram tuples to log2 probabilities e.g. {('*', '*', 'PRON'): -2.3, ...}
    """
    q_values: dict[tuple[str, str, str], float] = {}
    bigram_count = collections.defaultdict(float)
    trigram_count = collections.defaultdict(float)

    for tags in brown_tags:
        for tg in nltk.bigrams(tags):
            bigram_count[tg] += 1

    for tags in brown_tags:
        for tg in nltk.trigrams(tags):
            trigram_count[tg] += 1
    q_values = {tg: math.log(count/bigram_count[tg[:2]], 2) for tg, count in trigram_count.items()}
    
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
def calc_known(brown_words: list[list[str]]) -> set[str]:
    """
    Return a set of words that appear more than 5 times in the training data.
    Words appearing 5 times or fewer are considered rare.
    
    Args:
        brown_words: List of word sequences from training data.
    
    Returns:
        Set of known words with frequency greater than RARE_WORD_MAX_FREQ.
    """

    known_words: set[str] = set()
    word_counts = collections.Counter(word for sentence in brown_words for word in sentence)
    known_words = {word for word, count in word_counts.items() if count > RARE_WORD_MAX_FREQ}
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# First, ensure you add proper docstrings to this function, and then implement it.
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words: list[list[str]], known_words: set[list[str]]) -> list[list[str]]:
    """
    Replace words appearing 5 times or fewer with the _RARE_ symbol.
    Start and stop symbols are preserved.
    
    Args:
        brown_words: List of word sequences from training data.
        known_words: Set of words that appear more than 5 times.
    
    Returns:
        Same structure as brown_words but with rare words replaced by '_RARE_'.
    """
    brown_words_rare: list[list[str]] = []

    for sentence in brown_words:
        new_sentence = [ word if word in known_words or word == START_SYMBOL or word== STOP_SYMBOL else RARE_SYMBOL for word in sentence]
        brown_words_rare.append(new_sentence)
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
       Compute log2 emission probabilities P(word|tag) for all word-tag pairs.
    
    Args:
        brown_words_rare: Word sequences with rare words replaced by '_RARE_'.
        brown_tags: Corresponding tag sequences.
    
    Returns:
        e_values: Dict mapping (word, tag) tuples to log2 probabilities.
        tags_list: Set of all unique tags seen in training data.
    """
    e_values: dict[tuple[str, str], float] = {}
    tags_list: set[str] = set()

    word_tag_count = collections.defaultdict(int)
    tag_count = collections.defaultdict(int)

    for words, tags in zip(brown_words_rare, brown_tags):
        for word, tag in zip(words, tags):
            word_tag_count[(word, tag)] += 1
            tag_count[tag] += 1
            tags_list.add(tag)

    e_values = {(word, tag): math.log(count/tag_count[tag], 2) for (word, tag), count in word_tag_count.items() }
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
    Tag sentences using the Viterbi algorithm for HMM decoding.
    
    For each sentence, finds the most likely tag sequence using dynamic programming.
    Unknown words are replaced with '_RARE_' for probability lookup but original
    words are used in the output.
    
    Args:
        brown_dev_words: List of word sequences to tag.
        taglist: Set of all possible tags.
        known_words: Set of known words from training data.
        q_values: Dict mapping tag trigrams to log2 transition probabilities.
        e_values: Dict mapping (word, tag) to log2 emission probabilities.
    
    Returns:
        List of tagged sentences in "WORD/TAG" format with terminal newline.
    """
    tagged: list[str] = []
    
    for sentence in brown_dev_words:
        T = len(sentence)
        words = [w if w in known_words else RARE_SYMBOL for w in sentence]

        lattice = [{} for _ in range(T)]
        backpointer = [{} for _ in range(T)]

        # initialization
        for tag in taglist:
            if (words[0], tag) in e_values:
                lattice[0][tag] = q_values.get((START_SYMBOL, START_SYMBOL, tag), LOG_PROB_OF_ZERO) + e_values[(words[0], tag)]
                backpointer[0][tag] = (START_SYMBOL, START_SYMBOL)

        # recursion
        for t in range(1, T):
            for tag in taglist:
                if (words[t], tag) not in e_values:
                    continue
                best_prob = float('-inf')
                best_prev = None
                for prev_tag in lattice[t-1]:
                    prev_prev_tag = backpointer[t-1][prev_tag][1]
                    trans = q_values.get((prev_prev_tag, prev_tag, tag), LOG_PROB_OF_ZERO)
                    prob = lattice[t-1][prev_tag] + trans + e_values[(words[t], tag)]
                    if prob > best_prob:
                        best_prob = prob
                        best_prev = (prev_prev_tag, prev_tag)
                if best_prev is not None:
                    lattice[t][tag] = best_prob
                    backpointer[t][tag] = best_prev

        # termination
        if not lattice[T-1]:
            tagged.append(' '.join(w + '/NOUN' for w in sentence) + '\n')
            continue

        best_last_tag = max(lattice[T-1], key=lambda tag: lattice[T-1][tag])

        # backtrace
        tags_seq = [best_last_tag]
        for t in range(T-1, 0, -1):
            tags_seq.append(backpointer[t][tags_seq[-1]][1])
        tags_seq.reverse()

        # format output
        tagged.append(' '.join(sentence[i] + '/' + tags_seq[i] for i in range(T)) + '\n')

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
    Tag sentences using NLTK's trigram tagger with bigram and default backoff.
    
    Args:
        brown_words: Word sequences from training data.
        brown_tags: Tag sequences from training data.
        brown_dev_words: Word sequences to tag.
    
    Returns:
        List of tagged sentences in "WORD/TAG" format, one sentence per string.
    """
    # Hint: use the following line to format data to what NLTK expects for training
    training = [list(zip(brown_words[i], brown_tags[i])) for i in range(len(brown_words))]

    # IMPLEMENT THE REST OF THE FUNCTION HERE
    default_tagger = nltk.DefaultTagger("NOUN")
    bigram_tagger = nltk.BigramTagger(training, backoff = default_tagger)
    trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)

    tagged: list[str] = []

    for sentence in brown_dev_words:
        tagged_sent = trigram_tagger.tag(sentence)
        tagged.append(' '.join(word + '/' + tag for word, tag in tagged_sent) + '\n')
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
