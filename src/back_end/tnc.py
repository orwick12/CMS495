#!/usr/bin/python

""" 
    This program was created for educational purposes only.
    it required sqlite3 to be installed and path included in environment variable.
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
import sqlite3
#import sys

# Build Database
con = sqlite3.connect('tnc.db')
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS NewsArticle")
    cur.execute("CREATE TABLE NewsArticle(Id INT, Name TEXT, Count INT)")

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
        #print (i)
        paragraphs = page_content.find_all("article")[i].text
        textContent.append(paragraphs)
        #print (paragraphs)
        cur.execute("INSERT INTO NewsArticle VALUES(?,?,?)", (i, paragraphs, 1))
        i = i+1

def dbRetrieve():
    cur.execute("SELECT * FROM NewsArticle")
    data=cur.fetchall()
    for line in data:
        print(line)

def main():
    tncWebscraper()
    dbRetrieve()

if __name__=="__main__":
    main()
