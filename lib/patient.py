class Patient:

    def __init__(self, mysqldb):
        self.mysqldb = mysqldb

    def get_list(self):
        res = self.mysqldb.fetch_all('select name,dob,mobile,address from tbl_patient')
        return self.mysqldb.parse(res, ('name', 'dob', 'mobile', 'address'))

    def get(self, mobile):
        rows = self.mysqldb.fetch_all('select id,name,dob,mobile,address from tbl_patient where mobile = %s', (mobile,))
        res = self.mysqldb.parse(rows, ('id','name', 'dob', 'mobile', 'address'))
        return res[0] if len(res) else None

    def register(self, form_data):

        name = form_data['name']
        dob = form_data['dob']
        mobile = form_data['mobile']
        address = form_data['address']

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

        res = self.mysqldb.fetch_one('SELECT COUNT(*) FROM tbl_patient WHERE mobile = %s', (mobile,))
        count = res[0]

        print('Record count', count)

        if count > 0:
            return {
                'hasError': True,
                'error': 'Patient already exist'
            }

        sql = "INSERT INTO tbl_patient (name, dob, mobile, address) VALUES (%s, %s, %s, %s)"

        self.mysqldb.execute(sql, (name, dob, mobile, address))
        self.mysqldb.commit()

        print('Data inserted')

        return {
            'hasError': False
        }
