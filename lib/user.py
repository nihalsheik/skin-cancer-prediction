import mysql.connector


class User:

    def __init__(self, mysqldb):
        self.mysqldb = mysqldb

    def save_user(self, form_data):
        name = form_data['name']
        mobile = form_data['mobile']
        email = form_data['email']
        password = form_data['password']

        error = ''

        for key in form_data:
            if not form_data[key]:
                error = 'Invalid ' + key
                break

        if error:
            return {
                'hasError': True,
                'error': error
            }

        res = self.mysqldb.fetch_one('SELECT COUNT(*) FROM tbl_user WHERE email = %s', (email,))
        count = res[0]

        print('Record count', count)

        if count > 0:
            return {
                'hasError': True,
                'error': 'User already exist'
            }

        sql = "INSERT INTO tbl_user (name, email, password, mobile) VALUES (%s, %s, %s, %s)"

        self.mysqldb.execute(sql,  (name, email, password, mobile))
        self.mysqldb.commit()

        print('Data inserted')

        return {
            'hasError': False
        }

    def check_login(self, email, password):
        if not email or not password:
            return False

        res = self.mysqldb.fetch_one('SELECT COUNT(email) FROM tbl_user WHERE email = %s && password = %s',
                                     (email, password))
        return res[0] > 0
