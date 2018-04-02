import sqlite3
import os
import database.SQLStatements as SQLStatements
import controller.test
import numpy as np


class HtmlDatabase:

    path_to_db = os.path.join(os.path.dirname(os.path.realpath(__file__))[:-8], 'resources', 'htmldb.sqlite')

    @staticmethod
    def connect_to_db():
        """Opens connection to Chrome Database"""
        connect = sqlite3.connect(HtmlDatabase.path_to_db)
        return connect.cursor()

    @staticmethod
    def connect_to_db_with_connection():
        """Opens connection to Chrome Database"""
        connect = sqlite3.connect(HtmlDatabase.path_to_db)
        return connect, connect.cursor()

    @staticmethod
    def close_db_connection(cursor):
        """Close connection to Chrome Database. Use in conjunction with connect_to_db"""
        cursor.close()

    def open_db(self):
        """Open html database; creates if does not exist"""
        cursor = self.connect_to_db()
        cursor.execute(SQLStatements.CREATE_TABLE)
        self.close_db_connection(cursor)

    def insert_content(self, content):
        """Insert html content as blob into database"""
        connect, cursor = self.connect_to_db_with_connection()
        cursor.execute(SQLStatements.INSERT_CONTENT, (content,))
        connect.commit()
        self.close_db_connection(cursor)

    def select_all_content(self):
        """Select all html content into a numpy array where each element is a site's content"""
        cursor = self.connect_to_db()
        cursor.execute(SQLStatements.SEARCH_ALL_CONTENT)
        all_content = cursor.fetchall()
        result = np.array([])
        for c in all_content:
            print(c)
            result = np.append(result, c)
        self.close_db_connection(cursor)
        return result



