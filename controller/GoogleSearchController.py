from google import google
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import json, requests, re
import dataprocess.Utilities as Utilities
from database.ChromeDataCollector import ChromeDataConnector as ChromeDataConnector

from dataprocess.NaturalLanguageProcessor import NLProcessor as NLProcessor


class GoogleSearchController:
    def __init__(self, nlp, cdc):
        self.processed_text = cdc.get_recent_search_terms(2)  # Default is 2 days
        self.natural_language_processor = nlp #LanguageProcessingController(processed_text)
        self.tokenized_content = self.natural_language_processor.process_list_of_text(self.processed_text)
        self.top_used_words = Utilities.convert_dict_to_series_sort(
            self.natural_language_processor.count_words).head(10)

    @staticmethod
    def get_chunks(l):
        list_of_chunk = []
        for st in l:
            for t in st:
                if not isinstance(t, tuple):
                    list_of_chunk.append((re.sub('[\/\(\)A-Z]', '', t.pformat())))
        return list_of_chunk

    def filter_chunk_by_top_used_words(self):
        filtered = []
        for word in self.top_used_words.keys():
            if re.match(r'[^\W]', word):
                for chunk in self.get_chunks(self.natural_language_processor.chunking(
                        self.natural_language_processor.parts_of_speech_tag(self.processed_text))):
                    if word in chunk:
                        filtered.append(chunk)
        return np.unique(filtered)

    def calculate_similarity(self):
        ar = []
        l = self.filter_chunk_by_top_used_words()
        tfidf = TfidfVectorizer()
        for i in range(len(l) - 1):
            d = (l[i], l[i + 1])
            tfidf_matrix = tfidf.fit_transform(d).toarray()
            if np.sum(tfidf_matrix[0]) + np.sum(tfidf_matrix[1]) < 0.5 * (
                len(tfidf_matrix[0]) - (len(tfidf_matrix[0]) * 0.3)) * 2:
                ar.append(l[i + 1])
        return ar

    @staticmethod
    def get_autosuggest_terms(term):
        URL = "http://suggestqueries.google.com/complete/search?client=firefox&q=" + term
        headers = {'User-agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers)
        result = json.loads(response.content.decode('utf-8'))
        return result[1]

    @staticmethod
    def google_search(term):
        """Returns list of links of google search item from given term"""
        returnable_list = []
        result = google.search(term, 1)
        for entry in result:
            returnable_list.append(entry.link)
        return returnable_list
            #print("URL:", entry.link)
            #print("Name:", entry.name)
            # print("Desc:", entry.description)
            #print()


    def get_list_of_google_sites(self):
        """Returns a list of urls from google autosuggest feature"""
        total_list_urls = []
        similarity = self.calculate_similarity()
        for p in similarity:
            autosuggest = self.get_autosuggest_terms(p)
            count = 0
            for suggestion in autosuggest:
                total_list_urls += self.google_search(suggestion)
                count += 1
                if count > 3:
                    break
        return total_list_urls

#   Testing Google Search
# nlp = NLProcessor()
# cdc = ChromeDataConnector()
# gsc = GoogleSearchController(nlp, cdc)
# print(gsc.get_list_of_google_sites())

