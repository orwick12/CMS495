from flask import Flask, send_from_directory, request, Response, flash, stream_with_context
from jinja2 import Environment, PackageLoader, select_autoescape

# using https://gist.github.com/huiliu/46be335427605960fa84 as a reference


class Web(object):
    def __init__(self, scraper, db):
        self.site = Flask(__name__)
        self.db = db
        self.scraper = scraper
        self.env = Environment(
                loader=PackageLoader('front_end', 'templates'),
                autoescape=select_autoescape(['html', 'xml'])
        )
        self.routes()
        # self.getDB()
        # self.results = self.get_results()

    def getDB(self):
        self.scraper.generate_news()

    def get_results(self):
        return self.db.db_query()

    def routes(self):
        @self.site.route("/")
        def tncPageContent():
            content = "hello world!<br />Hi!<br />"
            # content = self.get_results()
            return Response(self.stream_template('index.html', content=content))
            # return Response(self.get_results())

        @self.site.route("/js/<jscript>")
        def js(jscript):
            return send_from_directory("js", jscript)
