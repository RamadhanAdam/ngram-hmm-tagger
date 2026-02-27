"""Language modeling solutions for Assignment 2 (Python 3.12+)."""

import math
import collections
import nltk
import time

# Constants you need when filling the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus: list[str]) -> tuple[dict, dict, dict]:
    """
    Compute log base 2 probabilities for unigram, bigram, and trigram models.
    
    Pads each sentence with two start symbols (*) and one stop symbol (STOP)
    before counting. Probabilities are computed using maximum likelihood estimation.
    
    Args:
        training_corpus: List of sentences as space-separated strings.
    
    Returns:
        Three dictionaries (unigram_p, bigram_p, trigram_p) mapping n-gram 
        tuples to their log base 2 probabilities.
    """
    unigram_p = collections.defaultdict(float)
    bigram_p = collections.defaultdict(float)
    trigram_p = collections.defaultdict(float)
    
    new_list = []
    for sentence in training_corpus:
        sentence = [START_SYMBOL] * 2 + sentence.split() + [STOP_SYMBOL]
        new_list.append(sentence)
    
    unigram_c = collections.defaultdict(float)
    bigram_c = collections.defaultdict(float)
    trigram_c = collections.defaultdict(float)

    for sent in new_list:
        for token in sent:
            unigram_c[token] += 1
    total = sum(count for word, count in unigram_c.items()
                if word != START_SYMBOL )
    
    unigram_p = { (word, ) : math.log(count/total, 2)for word, count in unigram_c.items()}

    for sent in new_list:
        for bg in nltk.bigrams(sent):
            bigram_c[bg] += 1
    bigram_p = {bg: math.log(count/unigram_c[bg[0]], 2) for bg, count in bigram_c.items()}

    for sent in new_list:
        for tg in nltk.trigrams(sent):
            trigram_c[tg] += 1
    total = sum(trigram_c.values())
    trigram_p = {tg: math.log(count/bigram_c[tg[:2]], 2) for tg, count in trigram_c.items()}

    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(
        unigrams: dict[tuple[str], float],
        bigrams: dict[tuple[str, str], float],
        trigrams: dict[tuple[str, str, str], float],
        filename: str
    ) -> None:
    """ Write n-gram log probabilities to a file.
        Args:
            unigrams (dict[tuple[str], float]): Dict mapping unigram tuples to log probabilities.
            bigrams (dict[tuple[str, str], float]): Dict mapping bigram tuples to log probabilities.
            trigrams (dict[tuple[str, str, str], float]): Dict mapping trigram tuples to log probabilities.
            filename (str): Output file path.
        Returns:
            None.
    """
    # output probabilities
    outfile = open(filename, 'w')

    for unigram in sorted(unigrams.keys()):
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    for bigram in sorted(bigrams.keys()):
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    for trigram in sorted(trigrams.keys()):
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()

def score(ngram_p: dict, n: int, corpus: list[str]) -> list[float]:
    """
    Compute the log probability score of each sentence using an n-gram model.
    
    Sums the log probabilities of all n-grams in each sentence. If any n-gram
    is not found in the model, the entire sentence is assigned a score of -1000.
    
    Args:
        ngram_p: Dictionary mapping n-gram tuples to log base 2 probabilities.
        n: Size of the n-gram (1 for unigram, 2 for bigram, 3 for trigram).
        corpus: List of sentences as space-separated strings.
    
    Returns:
        List of log probability scores, one per sentence.
    """
    scores: list[float] = []
    for sentence in corpus:
        words = [START_SYMBOL] * 2 + sentence.split() + [STOP_SYMBOL]

        # extracting n-grams based on
        if n == 1:
            ngrams = [(w,) for w in words if w != START_SYMBOL]
        elif n == 2:
            ngrams = list(nltk.bigrams(words))
        else:
            ngrams = list(nltk.trigrams(words))

        # sum of log probabilities
        sentence_score = 0
        for ng in ngrams:
            if ng not in  ngram_p:
                sentence_score = MINUS_INFINITY_SENTENCE_LOG_PROB
                break
            sentence_score += ngram_p[ng]  

        scores.append(sentence_score)
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores: list[float], filename: str) -> None:
    """Write sentence scores to a file.

    Args:
        scores: List of numeric scores.
        filename: Output file path.

    Returns:
        None.
    """
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# # Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# # Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# # Like score(), this function returns a python list of scores
def linearscore(
        unigrams: dict[tuple[str], float],
        bigrams: dict[tuple[str, str], float],
        trigrams: dict[tuple[str, str, str], float],
        corpus: list[str]
    ) -> list[float]:
    """
    Score each sentence using linear interpolation of three n-gram models.
    
    Blends unigram, bigram, and trigram probabilities using equal weights (lambda = 1/3).
    Converts log probabilities to real probabilities before blending, then converts back.
    Unseen n-grams are treated as probability 0.
    
    Args:
        unigrams: Dictionary mapping unigram tuples to log base 2 probabilities.
        bigrams: Dictionary mapping bigram tuples to log base 2 probabilities.
        trigrams: Dictionary mapping trigram tuples to log base 2 probabilities.
        corpus: List of sentences as space-separated strings.
    
    Returns:
        List of interpolated log probability scores, one per sentence.
    """
    
    scores: list[float] = []
    for sentence in corpus:
        sentence_score = 0.0 
        words = [START_SYMBOL] * 2  + sentence.split() + [STOP_SYMBOL]
        tri_list= list(nltk.trigrams(words))
        for token in tri_list:
            uni = unigrams.get((token[2],), MINUS_INFINITY_SENTENCE_LOG_PROB)
            bi = bigrams.get((token[1], token[2]), MINUS_INFINITY_SENTENCE_LOG_PROB)
            tri = trigrams.get((token[0],token[1], token[2]), MINUS_INFINITY_SENTENCE_LOG_PROB)

            prob = (math.pow(2, uni) + math.pow(2, bi) + math.pow(2, tri)) / 3
            sentence_score += math.log(prob, 2)
        scores.append(sentence_score)
    
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    """Run all steps for Part A and write outputs."""
    # start timer
    start_time = time.perf_counter()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    elapsed = time.perf_counter() - start_time
    print("Part A time: " + str(elapsed) + ' sec')

if __name__ == "__main__":
    main()
