import datetime as dt
import numpy as np


class WordListObject:

    def __init__(self):
        self.current = dt.datetime.now()
        self.wordlist = np.array([])
        self.stored_date = None

    def get_current_date(self):
        return self.current

    def set_current_date(self, date):
        self.current = date

    def get_stored_date(self):
        return self.stored_date

    def set_stored_date(self, date):
        self.stored_date = date

    def get_wordlist(self):
        return self.wordlist

    def set_wordlist(self, wordlist):
        self.wordlist = wordlist



