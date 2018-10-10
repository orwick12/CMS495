import sqlite3

conn = sqlite3.connect("tnc.db")
c = conn.cursor()
table_name_metadata = "METADATA"
table_name_article = "ARTICLE"
c.execute("DROP TABLE IF EXISTS " + table_name_metadata + ";")
c.execute("DROP TABLE IF EXISTS " + table_name_article + ";")
c.execute("CREATE TABLE " + table_name_article + " (ARTICLE_ID INTEGER PRIMARY KEY AUTOINCREMENT, URL text NOT NULL, AUTHOR text NOT NULL, PUBLISH_DATE text NOT NULL, CONTENT text NOT NULL, FOREIGN KEY (ARTICLE_ID) REFERENCES ARTICLE (ARTICLE_ID));")
c.execute("CREATE TABLE " + table_name_metadata + " (METADATA_ID INTEGER PRIMARY KEY AUTOINCREMENT, ARTICLE_ID_1 INTEGER NOT NULL, ARTICLE_ID_2 INTEGER NOT NULL, PERCENT_MATCH REAL NOT NULL, FOREIGN KEY (ARTICLE_ID_1) REFERENCES ARTICLE (ARTICLE_ID_1), FOREIGN KEY (ARTICLE_ID_2) REFERENCES ARTICLE (ARTICLE_ID_2));")
conn.commit()
conn.close()