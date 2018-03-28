from nltk.corpus import stopwords
import numpy as np


class NLProcessor:

    def __init__(self):
        self.stopwords = set(stopwords.words("english"))

    @staticmethod
    def tokenize_data(data):
        """Tokenize words from given numpy array"""
        token_data = []
        for np_list in data:
            token_data.append(np.array(np_list[0].split()))
        return np.array(token_data)

    def remove_stopwords(self, data):
        """Remove stopwords from given numpy array -- Inplace function"""
        for l in range(len(data)):
            for word in data[l]:
                if word in self.stopwords:
                    indicies_mask = np.where(data[l] == word)
                    data[l] = np.delete(data[l], indicies_mask)








