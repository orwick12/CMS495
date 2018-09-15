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

    def stream_template(self, template_name, **context):
        self.site.update_template_context(context)
        t = self.site.jinja_env.get_template(template_name)
        rv = t.stream(context)
        rv.enable_buffering(5)
        return rv

    def getDB(self):
        self.scraper.generate_news()

    def get_results(self):
        return self.db.db_query()

    def next_result(self):
        while True:
            result = next(self.results)
            if result is not None:
                yield result
            else:
                break

    def routes(self):
        @self.site.route("/")
        def tncPageContent():
            template = self.env.get_template("index.html")
            content = self.get_results()
            return template.render(content=content)
            # return Response(self.get_results())

        @self.site.route("/continued_results")
        def continued():
            content = next(self.get_results())
            return Response(self.stream_template('index.html', content=content))
            # return Response(self.get_results())

        @self.site.route("/js/<jscript>")
        def js(jscript):
            return send_from_directory("../js/", jscript)
