#!/usr/bin/python

""" 
    This program was created for educational purposes only.
    it required sqlite3 to be installed and path included in environment variable.
    Any use of it's content, for other than educational purposes, is strictly prohibited. 
    Project Team:
    Andrew Christiano
    Yrume Fernandez
    Brian Orwick
    Juila Sell
    
"""

# import required modules for webscraping and html parsing
import requests
from bs4 import BeautifulSoup
import sqlite3


# connect to Sqlite database and build table 
con = sqlite3.connect('tnc.db')
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS NewsArticle")
    cur.execute("CREATE TABLE NewsArticle(Id TEXT, Number INT, Name TEXT, Count INT)")

# The News Counter Webscraper
def tncWebscraper():
    
    # create list containing news sites to scrape
    web_list = ['https://www.foxnews.com', 'https://www.usatoday.com']

    for web_page in web_list:
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
            cur.execute("INSERT INTO NewsArticle VALUES(?,?,?,?)", (web_page, i, paragraphs, 1))
            i = i+1

def dbRetrieve():
    cur.execute("SELECT * FROM NewsArticle")
    data=cur.fetchall()
    for line in data:
        print(line)

def compareArticle():
    wordcount = 0
    totalcount= 0
    cur.execute("SELECT * FROM NewsArticle WHERE Id = 'https://www.foxnews.com'")
    words1=cur.fetchall()
    cur.execute("SELECT * FROM NewsArticle WHERE Id = 'https://www.usatoday.com'")
    words2=cur.fetchall()
    for line in words1:
        site, id, title, count = line
        word = title.split()
        for x in word:
            print(x)
            totalcount= totalcount + 1
            if x in str(words2):
                wordcount = wordcount + 1
                #print("WordCount= ", wordcount)
    print(totalcount)
    print(wordcount)

def main():
    tncWebscraper()
   # dbRetrieve()
    compareArticle()

if __name__=="__main__":
    main()
