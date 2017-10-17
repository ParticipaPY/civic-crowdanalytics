"""
@author: jorgesaldivar
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def download_stop_words():
    # Downloading English stopwords
    nltk.download('stopwords')
    nltk.download('punkt')


'''
Based on http://brandonrose.org/clustering
'''

def tokenize_and_remove_stop_words(text, specific_words_to_delete=[], 
                                   join_words=False, language='english'):
    # define stop words
    stop_words = nltk.corpus.stopwords.words(language) + ['.', ',', '--', 
                                        '\'s', '?', ')', '(', ':', '\'', 
                                        '\'re', '"', '-', '}', '{', u'—']
    # first tokenize by sentence, then by word to ensure that punctuation 
    # is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in 
              nltk.word_tokenize(sent)]
    # removing stop words
    cleaned_tokens = [word for word in tokens if word not in 
                      set(stop_words)]
    # keep only letter
    alpha_tokens = [re.sub('[^A-Za-z]', ' ', token) for token in cleaned_tokens]
    filtered_tokens = []
    for token in alpha_tokens:
        if token not in specific_words_to_delete:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token.strip())
    if join_words:
        return ' '.join(filtered_tokens)
    else:
        return filtered_tokens


def tokenize_and_stem(text, specific_words_to_delete=[], 
                      join_words=False, language='english'):
    # define stop words
    stop_words = nltk.corpus.stopwords.words(language) + [ '.', ',', '--', 
                                        '\'s', '?', ')', '(', ':', '\'', 
                                        '\'re', '"', '-', '}', '{', u'—', ]
    # first tokenize by sentence, then by word to ensure that punctuation 
    # is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in 
              nltk.word_tokenize(sent)]
    # removing stop words
    cleaned_tokens = [word for word in tokens if word not in 
                      set(stop_words)]
    # keep only letter
    alpha_tokens = [re.sub('[^A-Za-z]', ' ', token) for token in cleaned_tokens]
    filtered_tokens = []
    for token in alpha_tokens:
        if token not in specific_words_to_delete:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token.strip())
    # stemming
    stemmer = SnowballStemmer(language)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    if join_words:
        return ' '.join(stems)
    else:
        return stems