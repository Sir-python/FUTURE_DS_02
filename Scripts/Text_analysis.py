import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

def tokenize(text):
    stops = set(stopwords.words("english"))
    tokens = word_tokenize(str(text).lower())
    return [word for word in tokens if word.isalpha() and word not in stops]

def get_most_common_words(df):
    all_ticket_unigrams = Counter(w for toks in df["tokens"] for w in toks)
    all_resolution_unigrams = Counter(w for toks in df["resolution tokens"] for w in toks)
    return all_ticket_unigrams, all_resolution_unigrams

def get_most_common_bigrams(df):
    all_bigrams = Counter()
    for tokens in df["tokens"]:
        for i in range(len(tokens) - 1):
            bigram = (tokens[i], tokens[i + 1])
            all_bigrams[bigram] += 1
    return all_bigrams