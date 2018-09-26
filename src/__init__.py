from src.back_end.DB import DB
from src.back_end.Scraper import Scraper
from src.front_end.Web import Web
from src.main import Main

Main().web.site.run(host="0.0.0.0", port=5000, debug=True)
