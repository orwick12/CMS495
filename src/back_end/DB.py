import sqlite3, json, difflib


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
        c.execute("CREATE TABLE " + self.table_name + " (id INTEGER PRIMARY KEY AUTOINCREMENT, published text, url text, content text, counted_content text);")
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
        self.bag_of_words()
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        json_list = []
        for row in c.execute("SELECT counted_content FROM {0}".format(self.table_name)):
            json_list.append(row)
        conn.close()
        html = "<html>"
        html += json.dumps(json_list)
        html += "</html>"
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
            c.execute("UPDATE {tn} SET counted_content = ? WHERE id = ?".format(tn=self.table_name), (v, k))
        conn.commit()
        conn.close()

    def count_content(self, row):
        content = str(row[1]).split(" ")
        unsorted = dict([i, content.count(i)] for i in content)
        return sorted(unsorted.items(), key=lambda x: x[1], reverse=True)