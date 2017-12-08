import collections
from nltk import NaiveBayesClassifier, DecisionTreeClassifier
from nltk.metrics import precision, recall, f_measure
from nltk.classify import apply_features, accuracy
from nltk.classify.scikitlearn import SklearnClassifier
from analytics.utils import clean_html_tags, shuffled
from concept_extraction import ConceptExtractor
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer


class DocumentClassifier():
    '''
    Train a classifier with labeled documents and classify new documents 
    into one of the labeled clases.
    We call 'dev docs' to the documents set provided for training the 
    classifier. These 'dev docs' are splitted into two sub sets: 'train docs' 
    and 'test docs' that would be used to train and test the machine learning
    model respectively.

    Parameters
    ----------
    train_p : float, 0.8 by default
        The proportion of the 'dev docs' used as 'train docs'
        Use values greater than 0 and lower than 1.
        The remaining docs will be using as 'test docs'
    
    eq_label_num : boolean, True by default
        If true, 'train docs' will have equal number of documents for each
        class. This number will be the lowest label count.
    
    complete_p : boolean, True by default
        Used when eq_label_num is True, but the lowest label count is not
        enough for getting the train_p proportion of 'train docs'. If this 
        attribute is True, more documents from 'test docs' will be moved
        to 'train docs' until we get train_p
    
    vocab_size : integer, 500 by default
        This is the size of the vocabulary set that will be used for extracting
        features out of the docs

    t_classifier : string, 'NB' by default
        This is the type of classifier model used. Available types are 'NB' 
        (Naive Bayes), 'DT' (decision tree), 'RF' (Random Forest), and 'SVM'
        (Support Vector Machine)
    '''

    def __init__(self, train_p=0.8, eq_label_num=True,  
                 complete_p=True, vocab_size=250, 
                 t_classifier="NB"):
        self._train_p = train_p
        self._eq_label_num = eq_label_num
        self._complete_p = complete_p
        self._vocab_size = vocab_size
        self._t_classifier = t_classifier
        self._vocab = []
        self._classified_docs = []
        self._classifier = None
        self._accuracy = 0
        self._precision = {}
        self._recall = {}
        self._f_measure = {}
        self._train_docs = []
        self._test_docs = []

    def split_train_and_test(self, docs):
        '''
        Split the 'dev docs' set into the 'train docs' and 'test docs' subsets

        Parameters
        ----------
        docs: iterable
            An iterable which yields a list of strings

        '''

        categories_count = self.count_categories(docs)
        label_limit = min([c for (k,c) in categories_count.items()])
        labeled_docs = {}
        train_docs = []
        test_docs = []
        # Split docs by label
        for (cat,count) in categories_count.items():
            labeled_docs[cat] = shuffled([t for (t,k) in docs if k == cat])
        if self._eq_label_num:
            # Select the same number of doc for all labels
            for cat, cat_docs in labeled_docs.items():
                cat_limit = label_limit
                cat_train_docs = cat_docs[:cat_limit]
                cat_test_docs = cat_docs[cat_limit:]
                train_docs += [(doc, cat) for doc in cat_train_docs]
                test_docs += [(doc, cat) for doc in cat_test_docs]
            l_train = len(train_docs)
            l_docs = len(docs)
            l_test = len(test_docs)
            actual_p = l_train / l_docs
            # If the training proportion is not 
            if self._complete_p == True and actual_p < self._train_p:
                shuffled_extra = shuffled(test_docs)
                extra_i = 0
                while(actual_p < self._train_p and extra_i < l_test):
                    aux_l_train = l_train + extra_i
                    actual_p = aux_l_train / l_docs
                    extra_i += 1
                train_docs += shuffled_extra[:extra_i]
                test_docs = shuffled_extra[extra_i:]
        else:
            label_limit = int(self._train_p * len(docs))
            shuffled_docs = shuffled(docs)
            train_docs = shuffled_docs[:label_limit]
            test_docs = shuffled_docs[label_limit:]
        self._train_docs = train_docs
        self._test_docs = test_docs
    
    def count_categories(self, docs):
        '''
        Count how many documents of each class are in the 'dev docs' set
        
        Parameters
        ----------
        docs: iterable
            An iterable which yields a list of strings

        Returns
        -------
        counters: dictionary
            A dictiionary where each item is the number of docs for a class
        '''

        categories = set([c for (t,c) in docs])
        counters = {}
        for cat in categories:
            counters[cat] = 0
        for (text, cat) in docs:
            counters[cat] += 1
        self._categories = sorted(categories)
        return counters

    def get_doc_features(self, doc):
        '''
        Extract features of a document, checking the presence of the words
        in the vocabulary

        Parameters
        ----------
        doc: string
            The doc from which features will be extracted

        Returns
        -------
        features: dictionary
            A dictionary where each item indicates the presence of a
            word from the vocabulary in the input doc
        '''

        features = {}
        for word in self._vocab:
            features['contains({})'.format(word)] = (word in doc)
        return features


    def train_classifier(self, dev_docs):
        '''
        Create the features vocabulary from 'dev docs', 
        Split 'dev docs', train the classifier with 'train docs',
        Evaluate accuracy with 'test docs'

        Parameters
        ----------
        dev_docs: iterable
            An iterable which yields a list of strings
        '''
        # create vocabulary for feature extraction
        ce = ConceptExtractor(num_concepts=self._vocab_size)
        ce.extract_concepts([t for (t,c) in dev_docs])
        self._vocab = set([c for (c,f) in ce.common_concepts])
        # split dev docs and create traning and test set
        self.split_train_and_test(dev_docs)
        train_set = apply_features(self.get_doc_features, self._train_docs)
        # create and train the classification model according to t_classifier
        if self._t_classifier == "NB":
            self._classifier = NaiveBayesClassifier.train(train_set)
        elif self._t_classifier == "DT":
            self._classifier = DecisionTreeClassifier.train(train_set)
        elif self._t_classifier == "RF":
            self._classifier = SklearnClassifier(RandomForestClassifier()).train(train_set)
        elif self._t_classifier == "SVM":
            self._classifier = SklearnClassifier(LinearSVC(), sparse=False).train(train_set)


    def eval_classifier(self):
        '''
        Test the model and calculates the metrics of accuracy, precision,
        recall and f-measure
        '''
        test_set = apply_features(self.get_doc_features, self._test_docs, True)
        self._accuracy = accuracy(self._classifier, test_set)
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        
        for i, (feats, label) in enumerate(test_set):
            refsets[label].add(i)
            observed = self._classifier.classify(feats)
            testsets[observed].add(i)

        for cat in self._categories:
            self._precision[cat] = precision(refsets[cat], testsets[cat])
            self._recall[cat] = recall(refsets[cat], testsets[cat])
            self._f_measure[cat] = f_measure(refsets[cat], testsets[cat])


    def classify_docs(self, docs):
        '''
        First train the classifier with the labeled data.
        Then classifies the unlabeled data.

        Parameters
        ----------
        docs: iterable
            An iterable which yields a list of strings
        '''

        dev_docs = [(t, c) for (t, c) in docs if c!=""]
        unlabeled_docs = [t for (t, c) in docs if c==""]
        self.train_classifier(dev_docs)
        self.eval_classifier()
        results = []
        for doc in unlabeled_docs:
            doc_feats = self.get_doc_features(doc)
            result = self._classifier.classify(doc_feats)
            results.append((doc, result))
        self._classified_docs = results
        self._final_cat_count = self.count_categories(dev_docs+results)
    
    @property
    def classified_docs(self):
        return self._classified_docs

    @property    
    def accuracy(self):
        return self._accuracy
    
    @property
    def precision(self):
        return self._precision

    @property
    def recall(self):
        return self._recall

    @property
    def f_measure(self):
        return self._f_measure

    @property
    def category_count(self):
        return self._final_cat_count
