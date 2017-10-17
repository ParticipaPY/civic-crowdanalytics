import pandas as pd
from django.test import TestCase
from concept_extraction import ConceptExtractor

class ConceptExtractorTestCase(TestCase):
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

    def test_animals_can_speak(self):
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