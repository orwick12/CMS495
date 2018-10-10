from front_end.Web import Web
from back_end.TNC import TNC
from threading import Timer
import datetime as dt


class Main(object):
    def __init__(self):
        #nextDay = dt.datetime.now() + dt.timedelta(days=1)
        #dateString = nextDay.strftime('%d-%m-%Y') + " 01-00-00"
        #newDate = nextDay.strptime(dateString, '%d-%m-%Y %H-%M-%S')
        #delay = (newDate - dt.datetime.now()).total_seconds()
        self.tnc = TNC()
        self.db = self.tnc.connectDB()
        self.tnc.tncWebscraper()
        self.web = Web(self.tnc, self.db )
        #Timer(delay, self.tnc.tncWebscraper, ()).start()



