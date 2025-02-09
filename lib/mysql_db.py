import mysql.connector


class MySqlDB:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="skin_cancer_detection"
        )
        self.cursor = self.conn.cursor()

    def get_conn(self):
        return self.conn

    def commit(self):
        return self.conn.commit

    def get_cursor(self):
        return self.cursor

    def execute(self, sql, params):
        return self.cursor.execute(sql, params or ())

    def fetch_all(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def fetch_one(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchone()

    # noinspection PyMethodMayBeStatic
    def parse(self, result, cols=None):
        plist = []
        for row in result:
            k = {}
            i = 0
            for col in cols:
                k[col] = row[i]
                i = i + 1
            plist.append(k)
        return plist
