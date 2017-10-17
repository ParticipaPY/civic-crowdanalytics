#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

class SentimentAnalyzer():
    '''
    Analyzes the sentiment polarity of a collection of documents.
    It determines wether the feeling about each text is positive,
    negative or neutral

    Parameters
    ----------
    neu_inf_lim : float, -0.3 by default
        If a doc's polarity score is lower than this paramenter, 
        then the sentiment is considered negative.
        Use values greater than -1 and lower than 0.

    neu_pos_lim : float, 0.3 by default
        If a doc's polarity score is greater than this parameter,
        then the seniment is considered positive.
        Use values greater than 0 and lower than 1.

    algorithm : string, 'ntlk_vader' by default
        The algorithm used to calculate the polarity score of a text.
        Immplemented algorithms: 'ntlk_vader', 'textblob_base' 
    '''

    _sia = SentimentIntensityAnalyzer()
    _tagged_docs = []

    def __init__(self, neu_inf_lim=-0.3,
                 neu_sup_lim=0.3,
                 algorithm="nltk_vader"):
        self.neu_inf_lim = neu_inf_lim
        self.neu_sup_lim = neu_sup_lim
        self.algorithm = algorithm

    def get_polarity_score(self, text):
        '''
        Returns the polarity score for a given text.
        This score ranges from -1 to 1, were -1 is extreme negative
        and 1 means extreme positive.

        '''

        if self.algorithm == "nltk_vader":
            return self._sia.polarity_scores(text)["compound"]
        elif self.algorithm == "textblob_base":
            blob = TextBlob(text)
            return blob.sentiment.polarity

    def analyze_text(self, text):
        '''
        Analyzes a given text and returns a tuple
        (text, predicted sentiment, polarity score)
        where text is the original text;
        predicted sentiment can be 'pos', 'neu' or 'neg'
        for positive, neutral and negative sentiment respectevely;
        and polarity score is a float that ranges from -1 to 1.
        '''

        score = self.get_polarity_score(text)
        if score >= -1 and score < self.neu_inf_lim:
            predicted_sentiment = "neg"
        elif score >= self.neu_inf_lim and score < self.neu_sup_lim:
            predicted_sentiment = "neu"
        else:
            predicted_sentiment = "pos"
        return (text, predicted_sentiment, score)

    def analyze_docs(self, text_list):
        '''
        Analyzes a document collection by applying the analyze_text()
        method for each document.
        All the results are stored in the _tagged_docs attribute.
        '''

        results = []
        for text in text_list:
            results.append(self.analyze_text(text))
        self._tagged_docs = results

    @property
    def tagged_words(self):
        return self._tagged_docs