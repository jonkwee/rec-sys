from collections import defaultdict
import tldextract

class WebsiteListProcessor:
    """Responsibility: Website Url processor"""
    def __init__(self, web_list):
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


