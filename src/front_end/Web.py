from flask import Flask
from newspaper import Article

class Web(object):
    def __init__(self):
        self.site = Flask(__name__)
        self.routes()

    def getPage(self):
        url = "https://www.apnews.com/eadc2597c27e449c8952e5bedb6406c7/Amsterdam:-'Terrorist-motive'-alleged-in-attack-on-Americans"
        article = Article(url)
        article.download()
        article.parse()
        return article.text

    def routes(self):
        @self.site.route("/")
        def samplePageContent():
            return self.getPage()
