from src.back_end.DB import DB
from src.back_end.Scraper import Scraper
from src.front_end.Web import Web


class Main(object):
    def __init__(self):
        self.db = DB()
        self.scraper = Scraper("https://www.washingtonpost.com/", self.db)
        self.web = Web(self.scraper, self.db)


Main().web.site.run(host="0.0.0.0", port=5000, debug=True)
