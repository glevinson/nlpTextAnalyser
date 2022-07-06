from nltk.sentiment.vader import SentimentIntensityAnalyzer
from Interfaces import ISentimentAdapter
import pandas as pd

class VaderSentimentAdapter(ISentimentAdapter):
    @staticmethod
    def calculateSentiment(text):
        """Calculates the sentiment score of a given body of text
        based on the Vader lexicon.
        Note: inaccurate when word count is too low. E.g. "no"
        returns the maximum negative sentiment value of 1.
        Args:
            text (String): A body of text to be analyzed.
        Returns:
            dict: keys = ["neg", "neu", "pos", "compound"] 
                Please ensure naming convention.
        """
        a = SentimentIntensityAnalyzer()
        result = pd.DataFrame()
        result = a.polarity_scores(text)
        return result