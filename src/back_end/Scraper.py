import newspaper


class Scraper(object):
    def __init__(self, websites, db):
        self.websites = websites
        self.db = db

    def generate_news(self):
        for site in self.websites:
            articles = self.get_articles(site)
            self.parse(articles)

    def get_articles(self, site):
        paper = newspaper.build(site)
        return paper.articles

    def parse(self, articles):
        for article in articles:
            url, date, content = self.download(article)
            self.db.db_insert(url=url, date=date, content=content)

    def download(self, article):
        article.download()
        article.parse()
        return article.url, article.publish_date, article.text
