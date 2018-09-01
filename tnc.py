#!/usr/bin/python

""" 
    This program was created for educational purposes only.
    Any use of it's content, for other than educational purposes, is strictly     prohibited. 
    License information provided by:
    Andrew Christiano
    Yrume Fernandez
    Brian Orwick
    Juila Sell
    
"""

# import required modules for webscraping and html parsing
import requests
from bs4 import BeautifulSoup

# The News Counter Webscraper
def tncWebscraper():
    
    # create variables
    web_page = 'https://www.foxnews.com'


    # set get request for html
    page_response = requests.get(web_page, timeout=5)
    print (page_response)

    page_content = BeautifulSoup(page_response.content, "html.parser")

    textContent = []
    i = 0
    for p in page_content.find_all("article"):
        print (i)
        paragraphs = page_content.find_all("article")[i].text
        textContent.append(paragraphs)
        print (paragraphs)
        i = i+1

def main():
    tncWebscraper()

if __name__=="__main__":
    main()
