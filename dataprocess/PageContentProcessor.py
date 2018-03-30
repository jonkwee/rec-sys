from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment
import numpy as np
import requests
import tldextract

## Categories: Informational
## Also re.compile("^(/wiki/)((?!:).)*$")) will get all links that starts with wiki


def tag_visible(element):
    # Code from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    # Code from https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


class PageContentProcessor:

    def __init__(self):
        self.url = None
        self.soup = None
        self.content = None

    def change_url(self, url):
        "Change URL and changes Soup accordingly"
        self.url = url
        self.change_soup()

    def change_soup(self):
        """Change Beautiful Soup Object"""
        self.soup = self.extract_content()

    def get_domain_from_url(self):
        """Get Domain portion from self.url"""
        tldextract_data = tldextract.extract(self.url)
        return tldextract_data.domain

    def extract_content(self):
        """Returns Beautiful Soup object with url content"""
        headers = {'User-agent': 'Mozilla/5.0'}
        webpage = requests.get(self.url, headers)
        self.content = webpage.content
        soup = BeautifulSoup(self.content, "html.parser")
        return soup

    def extract_all_links(self):
        """Returns all the links contained in the webpage"""
        self.soup.parse_only = SoupStrainer('a', href=True)
        return [t.get('href') for t in self.soup.find_all('a')
                if t.get('href') is not None and t.get('href').startswith('http')]
        # For some reason, last element is NoneType

    def get_number_of_internal_links(self):
        """Return number of links that refer back to main site"""
        counter = 0
        domain = self.get_domain_from_url()
        for url in self.extract_all_links():
            data = tldextract.extract(url)
            if data.domain == domain:
                counter += 1
        return counter

    def get_list_of_words(self):
        """Return list of words from website"""
        return np.array(" ".join([w for w in text_from_html(self.content).split() if w.isalpha()]))









