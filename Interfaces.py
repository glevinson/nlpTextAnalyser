import abc

class ISentimentAdapter(abc.ABC) :
    @abc.abstractclassmethod
    def calculateSentiment(self, text) :
        """Calculates the sentiment score of a given body of text.
        Args:
            text (String): A body of text to be analyzed.
        Returns:
            dict: keys = ["neg", "neu", "pos", "compound"] 
                Please ensure naming convention to interface 
                with the SentimentAnalyzer class.
        """
        pass



class ISentimentGraphAdapter(abc.ABCMeta):
    def __init__(self):
        raise NotImplementedError()
    @abc.abstractclassmethod
    def plotSentimentHistory(self):
        raise NotImplementedError()
    @abc.abstractmethod
    def testFunction(self):
        raise NotImplementedError()
