import os
import sqlite3
import numpy as np
import datetime as dt
from itertools import chain

import database.SQLStatements as SQLStatements
import dataprocess.Utilities as Util


class ChromeDataConnector:
    """Responsibility: Connects and Queries from Database"""

    path_to_db = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\history"

    @staticmethod
    def connect_to_db():
        """Opens connection to Chrome Database"""
        connect = sqlite3.connect(ChromeDataConnector.path_to_db)
        return connect.cursor()

    @staticmethod
    def close_db_connection(cursor):
        """Close connection to Chrome Database. Use in conjunction with connect_to_db"""
        cursor.close()

    def __generic_database_wrapper(self, query_type, additional_params=None):
        """Generic wrapper method for database extraction"""
        cursor = self.connect_to_db()
        if additional_params is None:
            cursor.execute(query_type)
        else:
            cursor.execute(query_type, additional_params)
        results = cursor.fetchall()
        self.close_db_connection(cursor)
        return np.array(results)

    def get_site_visit_counts(self):
        """Get all website's URL and visit counts existing in Database"""
        return self.__generic_database_wrapper(SQLStatements.VISIT_QUERY)

    def get_search_terms(self):
        """Get search terms used in Google Chrome"""
        return self.__generic_database_wrapper(SQLStatements.SEARCH_TERMS_QUERY)

    def get_recent_search_terms(self, days):
        """Get all recently search terms within specified days"""
        microseconds = Util.date_to_microseconds(dt.datetime.now(), days)
        return self.__generic_database_wrapper(SQLStatements.RECENT_SEARCH_TERMS_QUERY, (microseconds,))

    def get_all_visited_url(self):
        """Get all visited urls using Chrome"""
        database_url_list = self.__generic_database_wrapper(SQLStatements.URL_QUERY)
        return list(chain.from_iterable(database_url_list))  # flatten url efficiently

    def get_visited_url_interval(self, start_date, end_date):
        """Get all visited urls between specified start and end dates"""
        start_microseconds = Util.date_to_microseconds(start_date, 0)
        end_microseconds = Util.date_to_microseconds(end_date, 0)
        url_interval_list = self.__generic_database_wrapper(SQLStatements.URL_INTERVAL_QUERY,
                                                            (start_microseconds, end_microseconds))
        return list(chain.from_iterable(url_interval_list))










