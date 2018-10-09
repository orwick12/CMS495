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
from front_end.Web import Web

class TNC(object):
    def __init__(self):

        # create list containing news sites to scrape
        self.web_list = ['http://www.foxnews.com','http://www.usatoday.com']

        # setup newspaper to multi-thread news sources 
        self.newsWebList = [newspaper.build(i, memoize_articles=True, fetch_images=False) for i in self.web_list]
        news_pool.set(self.newsWebList, threads_per_source=10)
        news_pool.join()
        self.connectDB()
        self.compareArticle()

    def connectDB(self):
        # connect to Sqlite database and initiate / build table 
        self.con = sqlite3.connect('tnc.db')
        with self.con:
            cur = self.con.cursor()
            #cur.execute("DROP TABLE IF EXISTS NewsArticle")
            cur.execute("CREATE TABLE IF NOT EXISTS NewsArticle(Source TEXT, Number INT, Title TEXT, Author TEXT, Content TEXT, Url TEXT, Count INT)")
        self.con.commit()
        #self.con.close()

    def insertDB(self, web_page, i, title, author, content, url, num):
        self.con = sqlite3.connect('tnc.db')
        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO NewsArticle VALUES(?,?,?,?,?,?,?)", (web_page, i, title, author, content, url, num))
        self.con.commit()
        self.con.close()

    def updateDB(self, source, i, count):
        self.con = sqlite3.connect('tnc.db')
        with self.con:
            cur = self.con.cursor()
            cur.execute("UPDATE NewsArticle WHERE Source = source AND Number = i SET num = count")
        self.con.commit()
        self.con.close()

    # The News Counter Webscraper
    def tncWebscraper(self):
        # iterates through sources
        j = 0
        for web_page in self.web_list:
            # set get request for html
            i = 0
            for article in self.newsWebList[j].articles:
                print ("Downloading Article Number: " + str(i) + " for " + web_page)
                article.download()
                article.parse()
                title = article.title
                author = str(article.authors)
                content = article.text
                url = article.url
                self.insertDB(web_page, i, title, author, content, url, 1)
                i = i+1
            j = j + 1

    def dbRetrieve(self, web_page):
        self.con = sqlite3.connect('tnc.db')
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM NewsArticle WHERE Source = ?;", (web_page,))
            data=cur.fetchall()
        self.con.close()
        return data

    def dbRetrieveOther(self, web_page):
        self.con = sqlite3.connect('tnc.db')
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM NewsArticle WHERE Source != ?;", (web_page,))
            data=cur.fetchall()
        self.con.close()
        return data

    def htmlRetreiveAll(self):
        html=""
        self.con = sqlite3.connect('tnc.db')
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT Title, Author, url FROM NewsArticle ORDER BY Count")
            data=cur.fetchall()
        self.con.close()
        for i in range(0,100):
            for line in data:
                html += "<p>"+str(data)+"</p>" 
        return html

    def compareArticle(self):
        wordcount = 0
        totalcount= 0
        count = 0
        html=""
        for web_page in self.web_list:
            words1=self.dbRetrieve(web_page)
            words2=self.dbRetrieveOther(web_page)
            for line in words1:
                site, id, title, author, content, url, count = line
                word = content.split()
                for line2 in words2:
                    site1, id1, title1, author1, content1, url1, count1 = line2
                    words = content1.split()
                    for x in word:
                        totalcount= totalcount + 1
                        for y in words:
                            if x == y:
                                wordcount = wordcount + 1
                                totalcount = totalcount + 1
                    totalwordcount = totalcount / 2
                    percent= wordcount / totalwordcount * 100
                    if percent >= 75:
                        count = count + 1
                        count1 = count1 + 1
                        print("will be sent to database")
                        #for testing
                        print("total: ", count, "word: ", wordcount)
                        self.updateDB(site, id, count)
                        self.updateDB(site1, id1, count1) 
                        #print(line)
                        #print(line2)
                        #html += "<p>Articles %s from %s and %s from %s have %s percent word match</p>" % (id, site, id1, site1, percent)
                        #html += "You can find this article at <link> %s </link> or at %s </br>" % (url, url1)
                    else:
                        html += "Articles %s and %s do not match </br>" % (id, id1)
                    totalcount= 0
                    wordcount= 0                
        #return html

#    def main():
#        tncWebscraper()
#        #dbRetrieve()
#        compareArticle()

#    if __name__=="__main__":
 #       main()
