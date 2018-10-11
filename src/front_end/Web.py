from flask import Flask, send_from_directory, request, Response, flash, stream_with_context, jsonify
from jinja2 import Environment, PackageLoader, select_autoescape
import json

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

    def routes(self):
        @self.site.route("/")
        def tncPageContent():
            content = self.get_results()  # content = json.dumps(json_obj)
            return Response(stream_with_context(self.stream_template('index.html', content=content)))
            # return Response(stream_with_context(self.db.db_query()))

        @self.site.route("/js/<jscript>")
        def js(jscript):
            return send_from_directory("js", jscript)
