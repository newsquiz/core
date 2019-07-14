from .base import Crawler
from .voa_crawler import VOACrawler

class UniversalCrawler(Crawler):
    
    def __init__(self):
        super(UniversalCrawler, self).__init__()

    def get_text(self, url):
        crawler = self._get_crawler(url)
        return crawler.get_text(url) 

    def _get_crawler(self, url):
        if url.startswith('https://learningenglish.voanews.com'):
            return VOACrawler 
        else:
            #raise ValueError('Unknow crawler for the url: ' + url)
            return VOACrawler
