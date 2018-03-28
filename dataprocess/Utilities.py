import datetime as dt
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd


def date_to_microseconds(specified_date, days):
    """Converts the interval between dates into microseconds based on inputted day"""
    date_before = specified_date + dt.timedelta(-days) + dt.timedelta(hours=6)
    micro = (date_before - dt.datetime(1601, 1, 1, 0, 0)).total_seconds() * 1000000
    return micro


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def convert_dict_to_series_sort(dictionary):
    return pd.Series(dictionary).sort_values(ascending=False)


