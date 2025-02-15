class Appointment:

    def __init__(self, mysqldb):
        self.mysqldb = mysqldb

    def book(self, props):
        try:
            doctor_id = props['doctor_id']
            patient_id = props['patient_id']
            fees = props['fees']
            date = props['date']
            self.mysqldb.execute('INSERT INTO tbl_appointment(doctor_id,patient_id,date,fees) VALUES(%s,%s,%s,%s)',
                                 (doctor_id, patient_id, date, fees))
            self.mysqldb.commit()
            return {
                'error': None
            }
        except RuntimeError:
            return {
                'error': 'Unknown error while booking appointment, Please try after some time'
            }
