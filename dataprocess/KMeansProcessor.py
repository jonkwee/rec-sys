import PageContentProcessor as PCP
import numpy as np
import os
import datetime as dt
import pickle
import dataobject.WordListObject
from sklearn.feature_extraction.text import TfidfVectorizer


class KNNProcessor:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(min_df=1)  # minimum document frequency
        self.PCP = PCP.PageContentProcessor()
        self.url_list = None
        self.word_list_object = self.load_word_list_object()

    @staticmethod
    def load_word_list_object():
        """Pickle word list object to current directory"""
        if os.path.isfile('./wordlistobject.pickle'):
            with open(r"wordlistobject.pickle", "rb") as input_file:
                print("Log: Unpickling word list object.")
                return pickle.load(input_file)
        else:
            return dataobject.WordListObject.WordListObject()

    @staticmethod
    def save_word_list_object(word_list_object):
        """Load word list object from current directory"""
        with open(r"wordlistobject.pickle", "wb") as output_file:
            pickle.dump(word_list_object, output_file)

    def __create_document_wordlist(self):
        """Create list of words from the contents of given url list."""
        print("Log: Previous pickled date:", self.word_list_object.get_stored_date())
        word_list = self.word_list_object.get_wordlist()
        previous_word_list_length = len(word_list)
        for url in self.url_list:
            print(url)
            self.PCP.change_url(url)
            word_list = np.append(word_list, self.PCP.get_list_of_words())
        print("Log: Done with content of websites.")
        # save process in word list object
        if len(word_list) != previous_word_list_length:
            self.word_list_object.set_wordlist(word_list)
            self.word_list_object.set_stored_date(dt.datetime.now())
            self.save_word_list_object(self.word_list_object)
            print("Log: Stored pickled date:", dt.datetime.now())
            print("Log: Done with pickling")
        return word_list

    def fit_transform(self):
        """Fit data into vectorizer"""
        return self.vectorizer.fit_transform(self.__create_document_wordlist())

    def set_url_list(self, url_list):
        """Sets given url list to KNNProcessor object"""
        self.url_list = url_list

    def get_word_list_object(self):
        return self.word_list_object
