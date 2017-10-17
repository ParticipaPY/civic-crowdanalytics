#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 17:07:11 2017

@author: jorgesaldivar
"""

import pandas as pd
import nltk
import re
from utils import tokenize_and_remove_stop_words


class ConceptExtractor():
    ''' 
    
    Extract the most common concepts from a collection of documents.
    
    Parameters
    ----------
    num_concepts : int, 5 by default
        The number of concepts to extract.
    
    context_words : list, empty list by default
        List of context-specific words that should notbe considered in the 
        analysis.
    
    ngram_range: tuple, (1,1) by default
        The lower and upper boundary of the range of n-values for different 
        n-grams to be extracted. All values of n such that 
        min_n <= n <= max_n will be used.
    
    pos_vec: list, only words tagged as nouns (i.e., ['NN', 'NNP']) are 
    considered by default
        List of tags related with the part-of-speech that 
        should be considered in the analysis. Please check
        http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html 
        for a complete list of tags.
    
    consider_urls: boolean, False by default
        Whether URLs should be removed or not
    
    language: string, english by default
        Language of the documents. Only the languages supported by the
        library NLTK are supported.
    '''
    _reg_exp_urls = r'^https?:\/\/.*[\r\n]*'
    
    def __init__(self, num_concepts=5, context_words=[], 
                 ngram_range=(1,1), pos_vec=['NN', 'NNP'], 
                 consider_urls=False, language='english'):
        self.num_concepts = num_concepts
        self.context_words = context_words
        self.ngram_range = ngram_range
        self.pos_vec = pos_vec
        self.consider_urls = consider_urls
        self.language = language
        # properties
        self._number_words = 0
        self._unique_words = 0
        self._common_concepts = []
    
    def extract_concepts(self, docs):
        '''
        Extract the most common concepts in the collection of 
        documents.
        
        Parameters
        ----------
        docs: iterable
            An iterable which yields a list of strings
        
        Returns
        -------
        self : ConceptExtractor
        
        '''
        
        #docs = ideas
        
        # tokenize documents
        tokenized_docs = []
        for doc in docs:
            if not self.consider_urls:
                doc = re.sub(self._reg_exp_urls, '', doc, 
                              flags=re.MULTILINE)
            tokenized_doc = tokenize_and_remove_stop_words(doc, 
                                                           self.context_words)
            tokenized_docs.append(tokenized_doc)
            
        # consider only the part-of-speech (pos) required
        tagged_senteces = [nltk.pos_tag(token) for token in tokenized_docs]
        pos_tokens = [tagged_token for tagged_sentence in tagged_senteces 
                      for tagged_token in tagged_sentence if tagged_token[1] 
                      in self.pos_vec]
        tokens = [pos_token[0] for pos_token in pos_tokens]
        
        # compute most frequent words
        fdist = nltk.FreqDist(tokens)
        common_words = fdist.most_common(self.num_concepts)
        self._unique_words = fdist.keys()
        self._number_words = sum([i[1] for i in fdist.items()])
        
        # compute most frequent n-grams
        min_n, max_n = self.ngram_range
        common_bigrams = []
        common_trigrams = []
        if min_n == 1:
            if max_n == 1:
                self._common_concepts = common_words[:self.num_concepts]
                return self
            else:
                if max_n <= 3:
                    for i in range(min_n, max_n):
                        if i==1:
                            bgs = nltk.bigrams(tokens)
                            fdist = nltk.FreqDist(bgs)
                            common_bigrams = fdist.most_common(self.num_concepts)
                        else:
                            bgs = nltk.trigrams(tokens)
                            fdist = nltk.FreqDist(bgs)
                            common_trigrams = fdist.most_common(self.num_concepts)
                else:
                    raise Exception('The max number in the n-gram range \
                                    cannot be larger than 3')
        else:
            raise Exception('The minimun number in the n-gram range \
                            must be equal to 1')
        
        # make list of common concepts considering n-grams
        least_freq_common_word = common_words[-1][1]
        ngrams_to_consider = []
        # save relevant ngrams        
        for bigram in common_bigrams:
            if bigram[1] > least_freq_common_word:
                ngrams_to_consider.append(bigram)
            else:
                break
        for trigram in common_trigrams:
            if trigram[1] > least_freq_common_word:
                ngrams_to_consider.append(trigram)
            else:
                break
        # delete word of the ngrams from the list of common words to avoid 
        # duplicates
        for ngram in ngrams_to_consider:
            idx_elements_to_remove = [i for word in ngram[0] for i in 
                                      range(len(common_words)) 
                                      if word == common_words[i][0]]
        for idx in idx_elements_to_remove:
            del common_words[idx]
        # add to list of common words the relevant ngrams
        common_words.extend(
                [
                (' '.join(ngram[0]), ngram[1]) for ngram in ngrams_to_consider
                ]
        )
        # order list
        self._common_concepts = sorted(common_words, key=lambda tup: tup[1],
                                       reverse=True)
        # select the first n concepts
        self._common_concepts = self._common_concepts[:self.num_concepts]       
        return self
    
    @property
    def total_words(self):
        return self._number_words
    
    @property
    def unique_words(self):
        return self._uniquer_words
    
    @property
    def common_concepts(self):
        return self._common_concepts
