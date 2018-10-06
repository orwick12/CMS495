import sqlite3


class DB(object):
    def __init__(self):
        self.dbFile = "tnc.db"
        self.table_name_article = "ARTICLE"
        self.table_name_metadata = "METADATA"
        # self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS " + self.table_name_article + ";")
        c.execute("DROP TABLE IF EXISTS " + self.table_name_metadata + ";")
        conn.commit()
        c.execute("CREATE TABLE " + self.table_name_article + " (ARTICLE_ID INTEGER PRIMARY KEY AUTOINCREMENT, URL text NOT NULL, AUTHOR text NOT NULL, PUBLISH_DATE text NOT NULL, CONTENT text NOT NULL, FOREIGN KEY (ARTICLE_ID) REFERENCES ARTICLE (ARTICLE_ID));")
        c.execute("CREATE TABLE " + self.table_name_metadata + " (METADATA_ID INTEGER PRIMARY KEY AUTOINCREMENT, ARTICLE_ID_1 INTEGER NOT NULL, ARTICLE_ID_2 INTEGER NOT NULL, PERCENT_MATCH REAL NOT NULL, FOREIGN KEY (ARTICLE_ID_1) REFERENCES ARTICLE (ARTICLE_ID_1), FOREIGN KEY (ARTICLE_ID_2) REFERENCES ARTICLE (ARTICLE_ID_2));")
        conn.commit()
        conn.close()

    def db_insert(self, date, url, content, authors):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        if authors == " ":
            authors = "Unknown"
        if date is None:
            date = "Unknown"
        c.execute("INSERT INTO {tn} (URL, AUTHOR, PUBLISH_DATE, CONTENT) VALUES (?, ?, ?, ?)".format(tn=self.table_name_article), (url, authors, date, content))
        conn.commit()
        conn.close()

    def db_related_insert(self, ARTICLE_ID_1, ARTICLE_ID_2, PERCENT_MATCH):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("INSERT INTO {tn} (ARTICLE_ID_1, ARTICLE_ID_2, PERCENT_MATCH) VALUES (?, ?, ?)".format(tn=self.table_name_metadata), (ARTICLE_ID_1, ARTICLE_ID_2, PERCENT_MATCH))
        conn.commit()
        conn.close()

    def db_update(self, objid, qualifier, input):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("UPDATE {tn} SET {q} = ? WHERE id = ?".format(tn=self.table_name_article, q=qualifier), (input, objid))
        conn.commit()
        conn.close()

    def db_query(self):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("SELECT Count(ARTICLE_ID) FROM {t}".format(t=self.table_name_article))
        count = c.fetchone()[0]
        conn.close()
        for i in range(0, count):
            conn = sqlite3.connect(self.dbFile)
            c = conn.cursor()
            c.execute("SELECT ARTICLE_ID, CONTENT, URL FROM {t} LIMIT 1 OFFSET {k}".format(t=self.table_name_article, k=i))
            row = c.fetchone()
            conn.close()
            yield self.mass_compare(row)

    def mass_compare(self, row):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("SELECT ARTICLE_ID, CONTENT, URL FROM {t} LIMIT -1 OFFSET {k}".format(t=self.table_name_article, k=int(row[0])))
        a = row
        html = ""
        while True:
            try:
                b = c.fetchone()
                if b is None:
                    conn.close()
                    break
                p = self.compare(self.count_content(a), self.count_content(b))
                if p > .7 and p != 1.0:
                    html += "id's {c} and {d} have {v} percent word match<br/>".format(v=p*100, c=a[0], d=b[0])
                    html += "url for a is <a href='{i}'>{i}</a><br/>".format(i=a[2])
                    html += "url for b is <a href='{j}'>{j}</a><br/>".format(j=b[2])
                    # self.db_related_insert(ARTICLE_ID_1=a[0], ARTICLE_ID_2=b[0], PERCENT_MATCH=p)
                    # return html
                else:
                    html += "id's {c} and {d} do not match...<br/>".format(c=a[0], d=b[0])
                    html += "url for a is <a href='{i}'>{i}</a><br/>".format(i=a[2])
                    html += "url for b is <a href='{j}'>{j}</a><br/>".format(j=b[2])
                    # return html
            except sqlite3.Error as e:
                html += "An error occurred: {0}".format(e.args[0])
                conn.close()
        conn.close()
        return html

    def compare(self, dict1, dict2):
        counter = 0
        for key in dict1.keys():
            v2 = dict2.get(key)
            if v2 is not None:
                v1 = float(dict1.get(key))
                v2 = float(v2)
                v = v2/v1
                if v > .9:
                    counter += 1
                    # print("{i} {j}".format(i=v1/v2, j=counter))
        percent = float(counter)/float(len(dict1))
        if len(dict1) is 1:
            percent = 0.0
        return percent

    def count_content(self, row):
        content = str(row[1]).split(" ")
        return dict([i, content.count(i)] for i in content)
