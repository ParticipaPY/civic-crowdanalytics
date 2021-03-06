# Civic CrowdAnalytics

Data analytics tool that applies Natural Language Processing (NLP) and Machine Learning (ML), such as concept extraction, idea classification, and sentiment analysis to make sense of crowdsourced civic input. This tool automatically organizes contributions into executive summaries and compelling visualizations, which are easy to comprehend, searchable, and interrelated. Civic CrowdAnalytics (CCA) is based on the scientific publication [**Civic CrowdAnalytics: Making sense of crowdsourced civic input with big data tools**](http://dl.acm.org/citation.cfm?id=2994366).

Civic CrowdAnalytics features a simple user-interface for submitting an unstructured dataset for analysis. The user can choose, for example, to organize ideas by pre-defined categories, visualize the frequency of recurring concepts, and sort the sentiments of related comments. The tool displays the results in both tabular summaries and interactive visualizations, which users can search and manipulate. Users can also choose to export the results in various formats, such as CSV, PNG, JPEG, SVG, or PDF.

## Screenshots

![dashboard](/frontoffice/screenshoots/dashboard.png?raw=true "Dashboard")

![categorization](/frontoffice/screenshoots/categorization.png?raw=true "Category Summary")

![concept_extraction](/frontoffice/screenshoots/concept_extraction.png?raw=true "Concept Extraction")

## Motivation

Civic technologies are currently bottlenecked by a common need for more effective processing of citizen contributions. Civic CrowdAnalytics provides a solution. By using innovative NLP and ML techniques, the tool automates the analysis and synthesis of key aspects of crowdsourced civic input. This automation will dramatically accelerate and improve the standard data management features that Civic Backoffice will also provide.

## Features

In its first version the tool supports the following analytics features:

1. **Classification:** This feature organizes the data into main- and subcategories by using well-known classifiers, such as [Naive Bayes](https://en.wikipedia.org/wiki/Naive_Bayes_classifier), [Decision Tree](https://en.wikipedia.org/wiki/Decision_tree_learning), [Random Forest](https://en.wikipedia.org/wiki/Random_forest), and [Support Vector Machine](https://en.wikipedia.org/wiki/Support_vector_machine). To train the classification algorithm, the user has first to code part of the dataset by labeling main categories and subcategories and then lets one of the algorithms to categorize the rest of the data. Texts written in any language supported by the [NLTK library](http://www.nltk.org/) can be classified;
2. **Concept Extraction:** Expressions and words are extracted from the data and displayed by frequency. Concept extraction provides lists of key terms and phrases, distributed by occurrence, which can then be further analyzed using statistical and qualitative methods. The user can specify a list of domain-specific words that should not be included in the analysis. The tool supports the extraction of three-words expressions at maximum;
3. **Sentiment Analysis:** The data is analyzed in terms of positive, negative, or neutral sentiment which is assessed regarding established values of words and expressions. For example, words such as reduce, remove, and problem would show a negative sentiment, whereas increase, resolve, and good would show a positive sentiment. So far, CCA supports the analysis of sentiment of texts written in four languages: English, Spanish, Portuguese, and French. For English texts, CCA uses the [Vader](http://www.nltk.org/_modules/nltk/sentiment/vader.html) algorithm of the NLTK toolkit. In the case of Spanish, CCA has its implementation based on the algorithm [ML-SentiCon](http://timm.ujaen.es/recursos/ml-senticon/). For the rest of the languages, the feature first translates the text into English by using the python package [Googletrans](https://pypi.python.org/pypi/googletrans) and then employs the Vader algorithm;
4. **Text Similarity:** This feature clusters together texts that are similar among them. The feature tokenizes and stemms the text, then it uses [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) to transform the set of text into a [Vector Space Model](https://en.wikipedia.org/wiki/Vector_space_model), and finally applies [K-means](https://en.wikipedia.org/wiki/K-means_clustering) algorithm to group texts represented by similar TF-IDF vectors.


## Installation

### Backend Installation

1. Clone the repository `git clone https://github.com/ParticipaPY/civic-crowdanalytics.git`
2. Get into the directory civic-crowdanalytics
3. Create a virtual environment `virtualenv env`
4. Activate the virtual environment `source env/bin/activate`
5. Get into the directory backoffice
6. Execute `pip install -r requirements.txt` to install dependencies. If an error occurs during the installation, it might be because some of these reasons: a) Package python-dev is missing b) Package libmysqlclient-dev is missing c) The environment variables LC_ALL and/or LC_CTYPE are not defined or don't have a valid value
7. Create a mysql database. Make sure your database collation is set to UTF-8
8. Rename the file backoffice/backoffice/settings.py.example as backoffice/backoffice/settings.py
9. Set the configuration parameters of the database in backoffice/backoffice/settings.py
```
DATABASES = {
    ...
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    ...
}
```
10. Run `python manage.py migrate` to set up the database schema
11. Run `python manage.py loaddata data.json` to load configuration data
12. Run `python manage.py createsuperuser` to create an admin user
13. Run the Django server by running the following command `python manage.py runserver 0:8000`

### Frontend Installation

1. Install Node.js (version higher than 0.10.32) and update npm (version higher than 2.1.8). See [here](https://docs.npmjs.com/getting-started/installing-node) for an installation guide
2. Get inside civic-crowdanalytics/frontoffice
3. Install the project's dependencies by running `npm install`
4. Set the backend server url, django user and password in frontoffice/src/Backend.vue
```
baseURL: 'http://localhost:8000/api',
username: '',
password: '',
```
5. Start local server by running `npm run dev`
6. Go to the following url http://localhost:8080 to access to the tool

## Technologies

### Backend Technologies

1. [Django Framework](https://www.djangoproject.com/)
2. [Django Rest Framework](http://www.django-rest-framework.org/)
3. [MySQL](https://www.mysql.com/) database (version 5.7 or higher) and its corresponding python package

### Frontend Technologies

1. [Node.js](https://nodejs.org) and [npm](https://www.npmjs.com)
2. [Vue.js](https://vuejs.org)
3. [CoreUI](http://coreui.io)
4. [Chart.js](http://www.chartjs.org)
