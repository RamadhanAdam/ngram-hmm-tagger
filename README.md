# Language Modeling and POS Tagging

## Part A - Language Models

### Q1 - N-gram Probabilities
Computed unigram, bigram and trigram log base 2 probabilities from Brown_train.txt.
Each sentence was padded with two start symbols (*) and one stop symbol (STOP).

### Q2 - Scoring
Scored every sentence in the training corpus using each model.
Any sentence containing an unseen n-gram was assigned a score of -1000.

| Model    | Perplexity  |
|----------|-------------|
| Unigram  | 1052.49     |
| Bigram   | 57.49       |
| Trigram  | 5.71        |

### Q3 - Linear Interpolation
Blended all three models using equal weights (lambda = 1/3 each).

| Model         | Perplexity  |
|---------------|-------------|
| Interpolated  | 12.71       |

### Q5 - Sample Comparison

| File     | Perplexity   |
|----------|--------------|
| Sample1  | 11.29        |
| Sample2  | 1.15e+173    |

Sample1 comes from the Brown dataset. The model was trained on Brown corpus data and 
assigns Sample1 a low perplexity of 11.29, meaning it recognizes the vocabulary and 
sentence structure. Sample2 has an extremely high perplexity, meaning most of its 
n-grams were never seen during training, which indicates it comes from a different source.

## Part B - POS Tagging

### Q2 - Tag Trigram Probabilities
Computed log2 trigram transition probabilities from Brown_tagged_train.txt.

### Q3 - Rare Word Replacement
Words appearing 5 times or fewer replaced with _RARE_ symbol.

### Q4 - Emission Probabilities
Computed log2 emission probabilities P(word|tag) for all word-tag pairs.

### Q5 - Viterbi
Implemented HMM decoding using Viterbi algorithm.
| Model    | Accuracy |
|----------|----------|
| Viterbi  | 93.3%    |

### Q6 - NLTK Tagger
Trigram tagger with bigram and default backoff.
| Model        | Accuracy |
|--------------|----------|
| NLTK Trigram | 100%     |