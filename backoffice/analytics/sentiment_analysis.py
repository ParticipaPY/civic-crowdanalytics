#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from analytics.utils import tokenize_and_remove_stop_words, tokenize_and_stem, \
                  clean_emojis, translate_doc

class SentimentAnalyzer:
    """
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

    language: string, 'english'; by default
        Language on which documents are written
        There are 2 languages supported natively:
        1 - 'english': through the ntlk_vader algorithms
        2 - 'spanish': through the ML_SentiCon algorithm
        If you use another language, the module will first translate each 
        document to english (using Google Translate AJAX API), so it can later
        re-use ntlk_vader algorithm for english docs.
    """

    _sia = SentimentIntensityAnalyzer()
    _tagged_docs = []

    def __init__(self, neu_inf_lim=-0.3,
                 neu_sup_lim=0.3,
                 language="english"):
        self.neu_inf_lim = neu_inf_lim
        self.neu_sup_lim = neu_sup_lim
        self.language=language
        self.translate = False
        self.need_normalization = False
        self.mlsent = {}
        self.spa_lemmas = []
        self.min_score = 100
        self.max_score = -100
        if language == "spanish":
            self.load_spa_resources()
            self.algorithm = "ML-Senticon"
            self.need_normalization = True
        elif language == "english":
            self.algorithm = "nltk_vader"
        else:
            self.algorithm = "nltk_vader"
            self.translate = True
            if self.language == "french":
                self.src_lang = "fr"
            elif self.language == "portuguese":
                self.src_lang = "pt"


    def load_spa_resources(self):
        """
        Load lexicons required when analyzing text in spanish.
        - Michal Boleslav Měchura's Spanish lemmatization dictionary.
        - ML SentiCon: Cruz, Fermín L., José A. Troyano, Beatriz Pontes, 
          F. Javier Ortega. Building layered, multilingual sentiment 
          lexicons at synset and lemma levels, 
          Expert Systems with Applications, 2014.
        
        """
        dir = os.path.dirname(os.path.realpath(__file__)) + "/lexicon_lib"
        fl = open(dir+"/lemmatization-es.txt")
        lines = fl.readlines()
        self.spa_lemmas = [(l.split()[0], l.split()[1]) for l in lines]
        fl.close()
        fmd = open(dir+"/MLsenticon.es.xml",  encoding='utf-8')
        for l in fmd.readlines():
            sl = l.split()
            if len(sl) == 6:
                word = sl[4].replace("_", " ")
                pol = float(sl[2].split('"')[1])
                self.mlsent[word] = pol
        fmd.close()

       

    def lemmatize_spa(self, spa_word):
        """
        Return spanish lemma for a given word

        Parameters
        ----------
        spa_word : string
            Spanish word to lemmatize
        """
        # spa_word is a word form
        res1 = [i[0] for i in self.spa_lemmas if i[1]==spa_word]
        if len(res1)==1:
            return res1[0]
        # spa_word is already a lemma
        res2 = [i[0] for i in self.spa_lemmas if i[0]==spa_word]
        if len(res2)>0:
            return res2[0]
        return ""


    def spa_polarity_score(self, doc):
        """
        Calculate a polarity score for a given doc usin ML-Senticon

        Parameters
        ----------
        doc : string
            Text to score

        Returns
        -------
        mlsscore : float
            Polarity score for the input doc (not normalized)
        """
        mlsscore = 0
        for word in doc.split():
            lem_word = self.lemmatize_spa(word)
            if word in self.mlsent.keys():
                mlsscore = mlsscore + self.mlsent[word]
            elif lem_word in self.mlsent.keys():
                mlsscore = mlsscore + self.mlsent[lem_word]
        if mlsscore > self.max_score:
            self.max_score = mlsscore
        if mlsscore < self.min_score:
            self.min_score = mlsscore
        return mlsscore


    def normalize_scores(self, results):
        """
        Normalice polarity scores into the range [-1,1] and 
        recalculates predicted sentiment label according to
        the normalized score.
        """
        normalized = []
        max = self.max_score
        min = self.min_score

        #no need to normalize. All docs are neutral
        if max == 0 and min == 0:
            return results    
        for (doc, sentiment, score) in results:
            n_score = -1 + ((score-min)*2)/(max-min)
            if n_score < self.neu_inf_lim:
                n_sentiment = "neg"
            elif n_score < self.neu_sup_lim:
                n_sentiment = "neu"
            else:
                n_sentiment = "pos"
            normalized.append((doc, n_score, n_sentiment))
        return normalized

        
    def get_polarity_score(self, doc):
        """
        Returns the polarity score for a given doc.
        This score ranges from -1 to 1, were -1 is extreme negative
        and 1 means extreme positive.

        """

        if self.algorithm == "nltk_vader":
            return self._sia.polarity_scores(doc)["compound"]
        elif self.algorithm == "ML-Senticon":
            return self.spa_polarity_score(doc)

    def analyze_doc(self, doc):
        """
        Analyzes a given doc and returns a tuple
        (doc, predicted sentiment, polarity score)
        where doc is the original doc;
        predicted sentiment can be 'pos', 'neu' or 'neg'
        for positive, neutral and negative sentiment respectevely;
        and polarity score is a float that ranges from -1 to 1.
        """
        # pre processing stage
        pp_doc = clean_emojis(doc)
        if self.translate:
            pp_doc = translate_doc(doc, src=self.src_lang, dest="en")
        pp_doc = tokenize_and_remove_stop_words(text=pp_doc, join_words=True,
                                                language=self.language)
        # get polarity score from pre processed doc
        score = self.get_polarity_score(pp_doc)
        # determine polarity from score and thresholds
        if score < self.neu_inf_lim:
            predicted_sentiment = "neg"
        elif score < self.neu_sup_lim:
            predicted_sentiment = "neu"
        else:
            predicted_sentiment = "pos"
        return (doc, predicted_sentiment, score)

    def analyze_docs(self, docs):
        """
        Analyzes a document collection by applying the analyze_doc() method
        for each document.
        All the results are stored in the _tagged_docs attribute.
        Normalize the results if needed.
        """
        results = []
        for doc in docs:
            results.append(self.analyze_doc(doc))
        if self.need_normalization:
            results = self.normalize_scores(results)
        self._tagged_docs = results


    @property
    def tagged_docs(self):
        return self._tagged_docs