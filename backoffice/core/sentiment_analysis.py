import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

sia = SentimentIntensityAnalyzer()

def get_sentiment_value(text, algorithm = "nltk_vader"):
    if algorithm == "nltk_vader":
        return sia.polarity_scores(text)["compound"]
    elif algorithm == "textblob_base":
        blob = TextBlob(text)
        return blob.sentiment.polarity


def analyze_text_sentiment(text, inf_limit = -0.3, sup_limit = 0.9):
    sentiment_value = get_sentiment_value(text)
    if sentiment_value >= -1 and sentiment_value < inf_limit:
        predicted_sentiment = "neg"
    elif sentiment_value >= inf_limit and sentiment_value < sup_limit:
        predicted_sentiment = "neu"
    else:
        predicted_sentiment = "pos"
    return (text, predicted_sentiment, sentiment_value)


def analyze_list_sentiment(text_list, inf_limit = -0.3, sup_limit = 0.9):
    results = []
    for text in text_list:
        results.append(analyze_text_sentiment(text))
    return results
