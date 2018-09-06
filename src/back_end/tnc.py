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
import newspaper
from newspaper import news_pool
import sqlite3

# create list containing news sites to scrape
web_list = ['http://www.foxnews.com', 'http://www.usatoday.com']

# setup newspaper to multi-thread news sources 
newsWebList = [newspaper.build(i) for i in web_list]
news_pool.set(newsWebList, threads_per_source=2)
news_pool.join()

# connect to Sqlite database and initiate / build table 
con = sqlite3.connect('tnc.db')
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS NewsArticle")
    cur.execute("CREATE TABLE NewsArticle(Id TEXT, Number INT, Name TEXT, Count INT)")

# The News Counter Webscraper
def tncWebscraper():
    # iterates through sources
    for web_page in web_list:
        # set get request for html
        i = 0
        j = 1
        for article in newsWebList[j].articles:
            #print (i)
            article.download()
            article.parse()
            paragraphs = article.title
            #print(web_page, "   ", paragraphs)
            cur.execute("INSERT INTO NewsArticle VALUES(?,?,?,?)", (web_page, i, paragraphs, 1))
            i = i+1
        j = j + 1

def dbRetrieve():
    cur.execute("SELECT * FROM NewsArticle")
    data=cur.fetchall()
    for line in data:
        print(line)

def compareArticle():
    wordcount = 0
    totalcount= 0
    for web_page in web_list:
        cur.execute("SELECT * FROM NewsArticle WHERE Id = ?;", (web_page,))
        words1=cur.fetchall()
        cur.execute("SELECT * FROM NewsArticle WHERE Id != ?;", (web_page,))
        words2=cur.fetchall()
        for line in words1:
            site, id, title, count = line
            word = title.split()
            for line2 in words2:
                site1, id1, title1, count1 = line2
                words = title1.split()
                for x in word:
                    totalcount= totalcount + 1
                    for y in words:
                        if x == y:
                            wordcount = wordcount + 1
                if wordcount / totalcount * 100 >= 70:
                    print("will be sent to database count")
                    #for testing
                    print("total: ", totalcount, "word: ", wordcount)
                    print(line)
                    print(line2)
                else:
                    print("Did not make it")
                    print("total: ", totalcount, "word: ", wordcount)
                totalcount= 0
                wordcount= 0                

def main():
    tncWebscraper()
    #dbRetrieve()
    compareArticle()

if __name__=="__main__":
    main()
