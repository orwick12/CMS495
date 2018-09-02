from flask import Flask


class Web(object):
    def __init__(self, scraper, db):
        self.site = Flask(__name__)
        self.db = db
        self.scraper = scraper
        self.routes()

    def getDB(self):
        self.scraper.generate_news()
        return self.db.db_query()

    def routes(self):
        @self.site.route("/")
        def samplePageContent():
            return self.getDB()
