from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
import numpy as np
import nltk


class NLProcessor:
    """Responsibility: Filters text data from corpus"""
    def __init__(self):
        self.stopwords = set(stopwords.words("english"))
        self.count_words = defaultdict(int)

    @staticmethod
    def tokenize_data(data):
        """Tokenize words from given numpy array"""
        token_data = []
        for np_list in data:
            token_data.append(np.array(np_list[0].split()))
        return np.array(token_data)

    @staticmethod
    def parts_of_speech_tag(processed_text):
        """Label text with parts of speech"""
        returnable_array = []
        try:
            for e in processed_text:
                tagged = nltk.pos_tag(e)
                returnable_array.append(tagged)
        except Exception as e:
            print(str(e))
        finally:
            return returnable_array

    def remove_stopwords(self, data):
        """Remove stopwords from given numpy array -- Inplace function"""
        for l in range(len(data)):
            for word in data[l]:
                if word in self.stopwords:
                    indicies_mask = np.where(data[l] == word)
                    data[l] = np.delete(data[l], indicies_mask)

    def process_list_of_text(self, textlist):
        """Return list of text without stopwords and as tokens"""
        "textlist should be from ChromeDataCollector.get_recent_search_terms function"
        returnable_array = []
        for e in textlist:
            text = word_tokenize(e[0])
            self.remove_stopwords(text)
            for w in text[0]:
                self.count_words[w] += 1
            returnable_array.append(text)
        return returnable_array


    def chunking(self, POSarray):
        """Chunk text based on parts of speech"""
        returnable_array = []
        chunkGram = r"""C: {<VB.?>*<NN.?>*}"""
        chunkParser = nltk.RegexpParser(chunkGram)
        for e in POSarray:
            returnable_array.append(chunkParser.parse(e))
        return returnable_array




