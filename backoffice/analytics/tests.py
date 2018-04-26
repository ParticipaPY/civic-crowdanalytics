import pandas as pd
from django.test import TestCase
from concept_extraction import ConceptExtractor
from clustering import DocumentClustering

class AnalyticsTestCase(TestCase):
    def setUp(self):
        # Importing the data
        dataset = pd.read_csv('../test_data/ideas-vallejo.tsv', delimiter = '\t', 
                              quoting=3)  # ignore double quotes
        # Select interested columns
        dataset = dataset[['title', 'text']]
        # Drop NA rows
        dataset = dataset.dropna()
        # Put ideas into a list
        self.ideas = dataset['text'].tolist()
        # Set context-specific words (e.g., proper names) that shouldn't be 
        # taken into consideration
        self.context_words = ['vallejo']

    def test_concept_extractor(self):
        # Extract Concepts
        ce = ConceptExtractor(num_concepts=15, 
                              context_words=self.context_words, 
                              ngram_range=(1,2))
        ce.extract_concepts(self.ideas)
        common_words = ce.common_concepts
        self.assertEqual('city', common_words[0][0])
        self.assertEqual('school', common_words[1][0])
        self.assertEqual('community', common_words[2][0])
        self.assertEqual('place', common_words[3][0])
        self.assertEqual('area', common_words[4][0])
        self.assertEqual('program', common_words[5][0])
        self.assertEqual('help', common_words[6][0])
        self.assertEqual('money', common_words[7][0])
        self.assertEqual('center', common_words[8][0])
        self.assertEqual('food', common_words[9][0])
        self.assertEqual('mare island', common_words[10][0])
    
    def test_document_clustering(self):
        dc = DocumentClustering(num_clusters=5, 
                                context_words=self.context_words, 
                                ngram_range=(1,3), min_df=0.1, max_df=0.9)
        dc.clustering(self.ideas)
        features = dc.features
        self.assertEqual('citi', features[0])
        self.assertEqual('communiti', features[1])
        self.assertEqual('help', features[2])
        self.assertEqual('kid', features[3])
        self.assertEqual('make', features[4])
        self.assertEqual('need', features[5])
        self.assertEqual('peopl', features[6])
        self.assertEqual('school', features[7])
        self.assertEqual('would', features[8])
        doc_clusters = dc.num_docs_per_cluster
        self.assertEqual(94, doc_clusters[0])
        self.assertEqual(487, doc_clusters[1])
        self.assertEqual(78, doc_clusters[2])
        self.assertEqual(84, doc_clusters[3])
        self.assertEqual(79, doc_clusters[4])
        terms_clusters = dc.top_terms_per_cluster()
        self.assertEqual('people, make, community', terms_clusters[0])
        self.assertEqual('city, would, people', terms_clusters[1])
        self.assertEqual('need, people, help', terms_clusters[2])
        self.assertEqual('school, would, help', terms_clusters[3])
        self.assertEqual('kids, school, help', terms_clusters[4])
        