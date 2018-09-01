from flask import Flask


class Web(object):
    def __init__(self):
        self.site = Flask(__name__)
        self.routes()

    def routes(self):
        @self.site.route("/")
        def helloWorld():
            return "Hello world!"
