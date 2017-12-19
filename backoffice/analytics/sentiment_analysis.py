#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from analytics.utils import tokenize_and_remove_stop_words, tokenize_and_stem, \
                  clean_emojis, translate_docs


class SentimentAnalyzer():
    '''
    Analyzes the sentiment polarity of a collection of documents.
    It determines wether the feeling about each doc is positive,
    negative or neutral

    Parameters
    ----------
    neu_inf_lim : float, -0.3 by default
        If a doc's polarity score is lower than this paramenter,
        then the sentiment is considered negative.
        Use values greater than -1 and lower than 0.

    neu_sup_lim : float, 0.3 by default
        If a doc's polarity score is greater than this parameter,
        then the seniment is considered positive.
        Use values greater than 0 and lower than 1.

    algorithm : string, 'ntlk_vader' by default
        The algorithm used to calculate the polarity score of a doc.
        Immplemented algorithms: 'ntlk_vader', 'textblob_base'

    language: string, 'english'; by default
        Language on which documents are written
        Implemented languages: 'spanish'
    '''

    _sia = SentimentIntensityAnalyzer()
    _tagged_docs = []

    def __init__(self, neu_inf_lim=-0.3,
                 neu_sup_lim=0.3,
                 algorithm="nltk_vader", 
                 language="english"):
        self.neu_inf_lim = neu_inf_lim
        self.neu_sup_lim = neu_sup_lim
        self.algorithm = algorithm
        self.language=language

    def get_polarity_score(self, doc):
        '''
        Returns the polarity score for a given doc.
        This score ranges from -1 to 1, were -1 is extreme negative
        and 1 means extreme positive.

        '''

        if self.algorithm == "nltk_vader":
            return self._sia.polarity_scores(doc)["compound"]
        elif self.algorithm == "textblob_base":
            blob = TextBlob(doc)
            return blob.sentiment.polarity

    def analyze_doc(self, doc):
        '''
        Analyzes a given doc and returns a tuple
        (doc, predicted sentiment, polarity score)
        where doc is the original doc;
        predicted sentiment can be 'pos', 'neu' or 'neg'
        for positive, neutral and negative sentiment respectevely;
        and polarity score is a float that ranges from -1 to 1.
        '''
        
        pp_doc = tokenize_and_remove_stop_words(text=doc, join_words=True)
        score = self.get_polarity_score(pp_doc)
        if score >= -1 and score < self.neu_inf_lim:
            predicted_sentiment = "neg"
        elif score >= self.neu_inf_lim and score < self.neu_sup_lim:
            predicted_sentiment = "neu"
        else:
            predicted_sentiment = "pos"
        return (doc, predicted_sentiment, score)

    def analyze_docs(self, docs):
        '''
        Analyzes a document collection by applying the analyze_doc()
        method for each document.
        All the results are stored in the _tagged_docs attribute.
        Emojis are removed from docs.
        If the docs' language is not english, they are translated to
        english to use the english sentiment lexicon of the analyzer.
        If the docs' language is not english, after analyze sentiment
        '''

        results = []
        docs = clean_emojis(docs)
        if (self.language != "english"):
            if (self.language == "spanish"):
                src = "es"
            translations = translate_docs(docs, src=src, dest="en")
            originals = [o for (o,t) in translations]
            translated = [t for (o,t) in translations]
        else:
            translated = docs
        for doc in translated:
            results.append(self.analyze_doc(doc))
        
        if (self.language != "english"):
        # translation might change docs order
        # original non translated text must be re inserted in the results
            results = [(originals[i], results[i][1], results[i][2]) for i in range(len(results))]
        self._tagged_docs = results

    @property
    def tagged_docs(self):
        return self._tagged_docs
