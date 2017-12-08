#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:17:21 2017

@author: jorgesaldivar
"""

import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity
from analytics.utils import tokenize_and_remove_stop_words, tokenize_and_stem,\
                  download_stop_words


class DocumentClustering:
    '''
    Cluster documents by similarity using the k-means algorithm.
    
    Parameters
    ----------
    num_clusters : int, 5 by default
        The number of clusters in which the documents will be grouped.
    
    context_words : list, empty list by default
        List of context-specific words that should notbe considered in the 
        analysis.
        
    ngram_range: tuple, (1,1) by default
        The lower and upper boundary of the range of n-values for different 
        n-grams to be extracted. All values of n such that 
        min_n <= n <= max_n will be used.
    
    min_df: float in range [0.0, 1.0] or int, default=0.1
        The minimum number of documents that any term is contained in. It 
        can either be an integer which sets the number specifically, or a 
        decimal between 0 and 1 which is interpreted as a percentage of all 
        documents.
    
    max_df: float in range [0.0, 1.0] or int, default=0.9
        The maximum number of documents that any term is contained in. It 
        can either be an integer which sets the number specifically, or a 
        decimal between 0 and 1 which is interpreted as a percentage of all 
        documents.
    
    consider_urls: boolean, False by default
        Whether URLs should be removed or not.
    
    language: string, english by default
        Language of the documents. Only the languages supported by the
        library NLTK are supported.

    algorithm: string, 'k-means' by default
        Clustering algorithm use to group documents
        Currently available: k-means and agglomerative (hierarchical)
    
    '''
    
    _reg_exp_urls = r'^https?:\/\/.*[\r\n]*'
    
    def __init__(self, num_clusters=5, context_words=[], ngram_range=(1,1), 
                 min_df=0.1, max_df=0.9, consider_urls=False, 
                 language='english', algorithm="k-means"):
        self.num_clusters = num_clusters
        self.context_words = context_words
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        self.consider_urls = consider_urls
        self.language = language
        # properties
        self._docs = None
        self._corpus = pd.DataFrame()
        self._model = None
        self._tdidf_matrix = {}
        self._features = []
        self._feature_weights = {}
        self._num_docs_per_clusters = {}
        self._clusters = []
        self._algorithm = algorithm
        # download stop words in case they weren't already downloaded
        download_stop_words()
    
    def clustering(self, docs):
        '''
        Cluster, by similarity, a collection of documents into groups.
        
        Parameters
        ----------
        docs: iterable
            An iterable which yields a list of strings
        
        Returns
        -------
        self : DocumentClustering
        '''
        
        self._docs = docs
        # clean and stem documents
        stemmed_docs = []
        for doc in self._docs:
            if not self.consider_urls:
                doc = re.sub(self._reg_exp_urls, '', doc, flags=re.MULTILINE)
            stemmed_docs.append(tokenize_and_stem(doc, self.context_words,
                                                  join_words=True,
                                                  language=self.language))
        # create td-idf matrix
        tfidf_vectorizer = TfidfVectorizer(max_df=self.max_df, 
                                           min_df=self.min_df,
                                           use_idf=True,
                                           ngram_range=self.ngram_range)
        #fit the vectorizer to ideas
        try:
            self._tfidf_matrix = tfidf_vectorizer.fit_transform(stemmed_docs)
            self._features = tfidf_vectorizer.get_feature_names()
            weights = np.asarray(self._tfidf_matrix.mean(axis=0)).ravel().tolist()
            weights_df = pd.DataFrame({'term': self._features, 'weight': weights})
            self._feature_weights = weights_df.sort_values(by='weight', 
                                                          ascending=False). \
                                                          to_dict(orient='records')
        except ValueError as error:
            raise Exception(error)
        # compute clusters
        if self._algorithm == "agglomerative":
            self._model = AgglomerativeClustering(n_clusters=self.num_clusters)
            self._model.fit(self._tfidf_matrix.toarray())
        elif self._algorithm == "k-means":
            self._model = KMeans(n_clusters=self.num_clusters)
            self._model.fit(self._tfidf_matrix)
        self._clusters = self._model.labels_.tolist()
        # create a dictionary of the docs and their clusters
        docs_clusters = {'docs': self._docs, 'cluster': self._clusters}
        docs_clusters_df = pd.DataFrame(docs_clusters, index = [self._clusters] , 
                                        columns = ['doc', 'cluster'])
        # save the number of documents per cluster
        self._num_docs_per_clusters = dict(docs_clusters_df['cluster']. \
                                           value_counts())
        return self
        
    def top_terms_per_cluster(self, num_terms_per_cluster=3):
        '''
        Compute the top 'n' terms per cluster.
        
        Parameters
        ----------
        num_terms_per_cluster: int, default=3
            The number of terms per clusters that should be returned
        
        Returns
        -------
        top_terms : Dictionary of clusters and their top 'n' terms
        '''

        if self._corpus.empty:
            cleaned_txt = []
            stemmed_txt = []
            for doc in self._docs:
                cleaned_txt.extend(tokenize_and_remove_stop_words(doc, 
                                                                  self.context_words))
                stemmed_txt.extend(tokenize_and_stem(doc, self.context_words))
            # create a panda dataframe containing the cleaned and 
            # stemmed texts
            self._corpus = pd.DataFrame({'words': cleaned_txt}, index=stemmed_txt)
        top_terms = {}
        # sort cluster centers by proximity to centroid
        order_centroids = self._model.cluster_centers_.argsort()[:, ::-1] 
        for i in range(self.num_clusters):
            str_cluster = ''
            term_counter = 0
            for idx in order_centroids[i, :num_terms_per_cluster]:
                str_cluster = str_cluster + \
                self._corpus.ix[self._features[idx].split(' ')].values. \
                tolist()[0][0]
                if term_counter < (num_terms_per_cluster-1):
                    str_cluster = str_cluster + ', '
                    term_counter += 1
            top_terms[i] = str_cluster.strip()
        return top_terms
    
    def get_coordinate_vectors(self):
        '''
        First, the function computes the cosine similarity of each document. 
        Cosine similarity is measured against the tf-idf matrix and can be used 
        to generate a measure of similarity between each document and the other 
        documents in the corpus.
        
        Then, it converts the dist matrix into a 2-dimensional array of 
        coordinate vectors.
        
        
        Returns
        -------
        coor_vecs: Dictionary that maps each document with its corresponding
        cluster and its x and y coordinate.
        '''
        
        MDS()
        dist = 1 - cosine_similarity(self._tfidf_matrix)
        mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
        pos = mds.fit_transform(dist) # shape (n_components, n_samples)
        xs, ys = pos[:, 0], pos[:, 1]
        # create a dictionary that has the result of the MDS plus the cluster 
        # numbers and documents
        coor_vecs = dict(x=xs, y=ys, label=self._clusters, docs=self._docs)
        return coor_vecs
    
    @property
    def docs(self):
        return self._docs
    
    @property
    def features(self):
        return self._features
    
    @property
    def num_docs_per_cluster(self):
        return self._num_docs_per_clusters

class IterativeDocumentClustering:
    '''
    Cluster documents using the DocumentClustering class previously
    defined. If one of the clusters is too big, it clusters it again
    and repeat the process until all clusters are small enough.
    
    Parameters
    ----------
    num_clusters : int, 5 by default
        The number of clusters in which the documents will be grouped.
        If a given cluster is too big it will be re clustered so there
        could be more clusters than num_clusters.
    
    context_words : list, empty list by default
        List of context-specific words that should notbe considered in the 
        analysis.
        
    ngram_range: tuple, (1,1) by default
        The lower and upper boundary of the range of n-values for different 
        n-grams to be extracted. All values of n such that 
        min_n <= n <= max_n will be used.
    
    min_df: float in range [0.0, 1.0] or int, default=0.1
        The minimum number of documents that any term is contained in. It 
        can either be an integer which sets the number specifically, or a 
        decimal between 0 and 1 which is interpreted as a percentage of all 
        documents.
    
    max_df: float in range [0.0, 1.0] or int, default=0.9
        The maximum number of documents that any term is contained in. It 
        can either be an integer which sets the number specifically, or a 
        decimal between 0 and 1 which is interpreted as a percentage of all 
        documents.
    
    consider_urls: boolean, False by default
        Whether URLs should be removed or not.
    
    language: string, english by default
        Language of the documents. Only the languages supported by the
        library NLTK are supported.

    threshold: float, 0.9 by default
        Percentage of the docs that defines the maximun size for a cluster.abs

    n_sub_clusters: integer, 3 by default
        Number of sub cluster on which any big cluster will be re clustered.
    
    num_temrs: integer, 3 by default
        Number of top terms per cluster
    '''
    
    def __init__(self, num_clusters=5, context_words=[], ngram_range=(1,1), 
                min_df=0.05, max_df=0.9, consider_urls=False, 
                language='english', threshold=0.6, n_sub_clusters=3,
                num_terms=3):
        self.num_clusters = num_clusters
        self.context_words = context_words
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        self.consider_urls = consider_urls
        self.language = language
        self.threshold = threshold
        self.n_sub_clusters = n_sub_clusters
        self.num_terms = num_terms
        self._clusters_data = {}

    def cluster_subset(self, docs, coords=None, num_clusters=5):
        '''
        Cluster a set of docs into num_clusters groups

        Parameters
        ----------
        docs: iterable
            An iterable which yields a list of strings
        
        coords: iterable
            An iterable which yields a list of tuple of (x,y) form where x
            and y represent bidimensional coordinates of each doc.
            If None, it uses the get_coordinate_vectors method of the
            DocumentClustering class to calculate new coordinates.

        num_clusters: int, 5 by default
            The number of clusters in which the documents will be grouped.

        Returns
        -------
        result: dictionary where keys are clusters labels and values are list
        of the form (t,x,y) where t is the text of a document, and x & y are
        the coordinates of the document.

        top_terms: dictionary where keys are clusters labels and values are
        strings that have the top termns per clusters.
        '''

        dc = DocumentClustering(num_clusters=num_clusters,
                                context_words=self.context_words,
                                ngram_range=self.ngram_range,
                                min_df=self.min_df,
                                max_df=self.max_df)
        dc.clustering(docs)
        vec = dc.get_coordinate_vectors()
        if coords != None:
            xs = [c[0] for c in coords]
            ys = [c[1] for c in coords]
        else:
            xs = vec["x"]
            ys = vec["y"]
        labels = vec["label"]
        texts = vec["docs"]
        result = {str(l): [] for l in set(labels)}
        for i in range(0, len(labels)):
            cluster = str(labels[i])
            data = (texts[i], xs[i], ys[i])
            result[cluster].append(data)

        top_terms = {str(c): tt for c,tt in dc.top_terms_per_cluster\
                                             (self.num_terms).items()}
        return result, top_terms

    def clustering(self, docs):
        '''
        Call cluster_subset method iteratively until all groups are small 
        enough.

        Parameters
        ----------
        docs: iterable
            An iterable which yields a list of strings
        '''
        top_terms = {}
        limit =  int(self.threshold*len(docs))
        #first time cluster_subset is called with the num_clusters attribute
        result, top_terms = self.cluster_subset(docs=docs,
                                                num_clusters=self.num_clusters)
        while True:
            n_docs = {c: len(l) for c,l in result.items()}
            re_cluster = [c for c,n in n_docs.items() if n > limit]
            if len(re_cluster) == 0:
                break
            # re_cluster contains the labels of groups that are over the limit
            for rc in re_cluster:
                # remove big cluster from final result
                rc_data = result.pop(rc)
                rc_docs = [t for (t,x,y) in rc_data]
                saved_coords = [(x,y) for (t,x,y) in rc_data]
                # cluster_subset is called with the n_sub_clusters attribute
                # when re-clustering
                new_res, new_terms = self.cluster_subset(docs=rc_docs, 
                                             coords=saved_coords,
                                             num_clusters=self.n_sub_clusters)
                # add new clusters to final result
                for nc,l in new_res.items():
                    result[rc+"."+nc] = l
                # remove top terms of big clusters
                top_terms.pop(rc)
                # add new clusters' top terms
                for nc,tt in new_terms.items():
                    top_terms[rc+"."+nc] = tt
        self._clusters_data = result
        self._top_terms = top_terms
    
    @property
    def clusters_data(self):
        return self._clusters_data

    @property
    def top_terms_per_cluster(self):
        return self._top_terms
    
    