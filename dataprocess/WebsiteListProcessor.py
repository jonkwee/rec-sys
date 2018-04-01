from collections import defaultdict
import tldextract

class WebsiteListProcessor:
    """Responsibility: Website Url processor"""
    def __init__(self, web_list):
        self.blacklisted_domain = ['google', 'youtube', 'office365', 'gmail', 'github', 'taxslayer',
                                   'office', 'microsoftonline']
        self.web_list = web_list

    @staticmethod
    def get_base_url(url):
        """Get base url from provided url"""
        tldextract_data = tldextract.extract(url)
        return tldextract_data.domain

    def base_to_extension(self):
        """Creates dictionary with base url as keys and extension of base url as values"""
        return_dict = defaultdict(list)
        for url in self.web_list:
            return_dict[self.get_base_url(url)].append(url)
        return return_dict

    def filter_web_list(self):
        self.web_list = [url for url in self.web_list if self.get_base_url(url) not in self.blacklisted_domain]

    def get_web_list(self):
        return self.web_list
