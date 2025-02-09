class Patient:

    def __init__(self, mysqldb):
        self.mysqldb = mysqldb

    def get_list(self):
        res = self.mysqldb.fetch_all('select name,dob,age,mobile from tbl_patient')
        return self.mysqldb.parse(res, ('name', 'dob', 'age', 'mobile'))
