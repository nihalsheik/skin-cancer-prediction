class Appointment:

    def __init__(self, mysqldb):
        self.mysqldb = mysqldb

    def book(self, params):
        doctor_id = params['doctor_id']
        patient_id = params['patient_id']
        amount = params['amount']
        self.mysqldb.execute('INSERT INTO tbl_appointment(doctor_id,patient_id,amount) VALUES(%s,%s,%s)',
                             (doctor_id, patient_id, amount))
        self.mysqldb.commit()
