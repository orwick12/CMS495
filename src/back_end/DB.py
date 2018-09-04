import sqlite3, json, pprint


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
        c.execute("CREATE TABLE " + self.table_name + " (id INTEGER PRIMARY KEY AUTOINCREMENT, published text, url text, content text);")
        conn.commit()
        conn.close()

    def db_insert(self, date, url, content):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("INSERT INTO {tn} (published, url, content) VALUES (?, ?, ?)".format(tn=self.table_name),(date, url, content))
        conn.commit()
        conn.close()

    def db_query(self):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        json_list = []
        for row in c.execute("SELECT id, published, url, content FROM {0}".format(self.table_name)):
            json_list.append(self.json_object(row))
        html = "<html>"
        html += json.dumps(json_list)
        html += "</html>"
        return html

    def json_object(self, row):
        json_object = {
            "id": row[0],
            "date": row[1],
            "url": row[2],
            "content": row[3],
            "similar_to_id": []
        }
        return json_object
