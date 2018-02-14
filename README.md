# Civic CrowdAnalytics

Novel data analytics tool that applies Natural Language Processing (NLP) and Machine Learning (ML), such as concept extraction, idea classification, and sentiment analysis to make sense of crowdsourced civic input. This tool automatically organizes contributions into executive summaries and compelling visualizations, which are easy to comprehend, searchable, and interrelated. Civic CrowdAnalytics is based on the scientific publication [**Civic CrowdAnalytics: Making sense of crowdsourced civic input with big data tools**](http://dl.acm.org/citation.cfm?id=2994366).

Civic CrowdAnalytics features a simple user-interface for submitting an unstructured dataset for analysis. The user can choose, for example, to organize ideas by pre-defined categories, visualize the frequency of recurring concepts, and sort the sentiments of related comments. The tool displays the results in both tabular summaries and interactive visualizations, which users can search and manipulate. Users can also choose to export the results in various formats, such as CSV, PNG, JPEG, SVG, or PDF.

## Screenshots

![dashboard](/frontoffice/screenshoots/dashboard.png?raw=true "Dashboard")

![categorization](/frontoffice/screenshoots/categorization.png?raw=true "Category Summary")

![concept_extraction](/frontoffice/screenshoots/concept_extraction.png?raw=true "Concept Extraction")

## Motivation

Civic technologies are currently bottlenecked by a common need for more effective processing of citizen contributions. Civic CrowdAnalytics provides a solution. By using innovative NLP and ML techniques, the tool automates the analysis and synthesis of key aspects of crowdsourced civic input. This automation will dramatically accelerate and improve the standard data management features that Civic Backoffice will also provide.

## Features

In its first version the tool supports the following analytics features:

1. **Categorization:**  This feature organizes the data into main- and subcategories by using a well-known concept extraction algorithm that we adapt to our purposes. To train the algorithm, the user first codes a part of the dataset by labeling main categories and subcategories, and then lets the algorithm categorize the rest of the data;
2. **Concept Occurrence:**  Expressions and words are extracted from the data and displayed by frequency. Concept extraction provides lists of key terms and phrases, distributed by occurrence, which are then further analyzed using a variety of statistical and qualitative methods;
3. **Sentiment Analysis:**  The data is analyzed in terms of positive, negative, or neutral sentiment which is assessed in terms of established values of words and expressions. For example, words such as reduce, remove, and problem would show a negative sentiment, whereas increase, resolve, and good would show a positive sentiment. Sentiment analysis is already a common feature of algorithmic filtering on social media platforms;
4. **Entity Similarity:**  This feature display associations between ideas and comments based on their content similarity, which is also a common feature of algorithmic filtering on social media platforms.

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

1. Install Node.js (version higher than 0.10.32) and update npm (version higher than 2.1.8). See [here](https://docs.npmjs.com/getting-started/installing-node) for a guide
2. Get inside civic-crowdanalytics/frontoffice
3. Install project's dependencies by running `npm install`
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
