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
            try:
                url, date, content, authors = self.download(article)
                self.db.db_insert(url=url, date=date, content=content, authors=authors)
            except Exception as e:
                print(e)

    def download(self, article):
        article.download()
        article.parse()
        authors = " ".join(str(x) for x in article.authors)
        return article.url, article.publish_date, article.text, authors
