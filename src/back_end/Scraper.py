import newspaper


class Scraper(object):
    def __init__(self, website, db):
        self.website = website
        self.db = db

    def generate_news(self):
        articles = self.get_articles()
        if articles.__len__() == 0:
            self.generate_news()
        self.parse(articles)

    def get_articles(self):
        paper = newspaper.Source(self.website)
        paper.download()
        paper.parse()
        paper.set_categories()
        paper.download_categories()
        paper.parse_categories()
        paper.set_feeds()
        paper.download_feeds()
        paper.generate_articles()
        return paper.articles

    def parse(self, articles):
        for article in articles:
            url, date, content = self.download(article)
            self.db.db_insert(url=url, date=date, content=content)

    def download(self, article):
        article.download()
        article.parse()
        return article.url, article.publish_date, article.text
