from src.back_end.DB import DB
from src.front_end.Web import Web


class Main(object):
    def __init__(self):
        self.web = Web()
        self.db = DB()


Main().web.site.run(host="0.0.0.0", port=5000)
