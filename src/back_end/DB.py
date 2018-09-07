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
        c.execute("CREATE TABLE " + self.table_name + " (id INTEGER PRIMARY KEY AUTOINCREMENT, published text, url text, content text, json text);")
        conn.commit()
        conn.close()

    def db_insert(self, date, url, content):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("INSERT INTO {tn} (published, url, content) VALUES (?, ?, ?)".format(tn=self.table_name), (date, url, content))
        conn.commit()
        conn.close()

    def db_update(self, objid, json_data):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        c.execute("UPDATE {tn} SET json = ? WHERE id = ?".format(tn=self.table_name), (objid, json_data))
        #conn.commit()
        conn.close()

    def db_query(self):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        json_list = []
        self.mass_update()
        for row in c.execute("SELECT json FROM {0}".format(self.table_name)):
            json_list.append(json.loads(row))
        conn.close()
        html = "<html>"
        html += json.dumps(json_list)
        html += "</html>"
        return html

    def mass_update(self):
        conn = sqlite3.connect(self.dbFile)
        c = conn.cursor()
        list_of_ids = []
        for row in c.execute("SELECT id FROM {0}".format(self.table_name)):
            #self.filler(row, json.dumps(self.json_object(row)))
            list_of_ids.append(row[0])
        conn.close()
        for i in list_of_ids:
            conn = sqlite3.connect(self.dbFile)
            c = conn.cursor()
            for row in c.execute("SELECT id, published, url, content FROM {tn} WHERE id = {i}".format(tn=self.table_name)):

        conn.commit()


    def filler(self, row, json_data):
        self.db_update(row[0], json_data)

    def json_object(self, row):
        json_object = {
            "id": row[0],
            "date": row[1],
            "url": row[2],
            "content": row[3],
            "similar_to_id": []
        }
        return json_object
