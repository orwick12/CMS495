from src.back_end.DB import DB
from src.back_end.Scraper import Scraper
from src.front_end.Web import Web


class Main(object):
    def __init__(self):
        self.db = DB()
        self.scraper = Scraper(["https://cnn.com/","https://foxnews.com/","https://usatoday.com/"], self.db)
        self.web = Web(self.scraper, self.db)



