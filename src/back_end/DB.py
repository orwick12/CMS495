import sqlite3
import json


class DB(object):
    def __init__(self):
        self.version = 1
        self.dbFile = "tnc.db"
        self.table_name = "ARTICLE"
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS " + self.table_name + ";")
        conn.commit()
        c.execute("CREATE TABLE " + self.table_name + " (id INTEGER PRIMARY KEY AUTOINCREMENT, published text, url text, content text, counted_content text, num_uniq_words INTEGER);")
        conn.commit()
        conn.close()

    def db_insert(self, date, url, content):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("INSERT INTO {tn} (published, url, content) VALUES (?, ?, ?)".format(tn=self.table_name), (date, url, content))
        conn.commit()
        conn.close()

    def db_update(self, objid, qualifier, input):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("UPDATE {tn} SET {q} = ? WHERE id = ?".format(tn=self.table_name, q=qualifier), (input, objid))
        conn.commit()
        conn.close()

    def db_query(self):
        html = ""
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("SELECT id, content, url FROM {t} LIMIT 1".format(t=self.table_name))
        row = c.fetchone()
        conn.close()
        html += self.mass_compare(row)
        html = self.mass(row, html)
        return html

    def bag_of_words(self):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        key_pair = {}
        for row in c.execute("SELECT id, content FROM {0}".format(self.table_name)):
            key_pair[row[0]] = str(self.count_content(row))
        conn.commit()
        conn.close()
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        for k, v in key_pair.items():
            c.execute("UPDATE {tn} SET counted_content = ?, num_uniq_words = ? WHERE id = ?".format(tn=self.table_name), (v, len(json.dumps(v)), k))
        conn.commit()
        conn.close()

    def mass(self, row, html):
        conn = sqlite3.connect(self.dbFile)
        try:
            print(row[0])
            c = conn.cursor()
            c.execute("SELECT id, content, url FROM {t} LIMIT 1 OFFSET {k}".format(t=self.table_name, k=int(row[0])))
            row = c.fetchone()
            if row is None:
                conn.close()
                return html
            conn.close()
            html += self.mass_compare(row)
            html = self.mass(row, html)
            return html
        except sqlite3.Error as e:
            html = "An error occurred: {0}".format(e.args[0])
            conn.close()
            return html

    def mass_compare(self, row):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("SELECT id, content, url FROM {t} LIMIT -1 OFFSET {k}".format(t=self.table_name, k=int(row[0])))
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
                # else:
                #    html += "id's {c} and {d} do not match...<br/>".format(c=a[0], d=b[0])
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
        return percent

    def count_content(self, row):
        content = str(row[1]).split(" ")
        return dict([i, content.count(i)] for i in content)
