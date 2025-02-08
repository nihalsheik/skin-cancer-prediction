import mysql.connector


def connect_mysql():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="skin_cancer_detection"
    )
    return db


def save_user(form_data):

    name = form_data['name']
    phone = form_data['phone']
    email = form_data['email']
    password = form_data['password']

    mydb = connect_mysql()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT COUNT(*) FROM tbl_user WHERE email = %s', (email,))

    count = mycursor.fetchone()[0]

    print('Record count', count)

    if count > 0:
        return {
            'hasError': True,
            'error': 'User already exist'
        }

    sql = "INSERT INTO tbl_user (name, email, password, mobile) VALUES (%s, %s, %s, %s)"
    value = (name, email, password, phone)
    mycursor.execute(sql, value)
    mydb.commit()
    print('Data inserted')
    return {
        'hasError': False
    }

def check_login(email, password):
    
    # Step1 - get mysql connection
    mydb = connect_mysql()

    # Step2 - get cursor
    mycursor = mydb.cursor()

    # Step3 - Create Sql
    # Step4 - execute cursor
    mycursor.execute('SELECT COUNT(email) FROM tbl_user WHERE email = %s && password = %s',(email, password))

    tuple = mycursor.fetchone()
    count = tuple[0]

    # Step5 - Check the count 
    # Step6 - return True if 0 otherwise False
    # if count == 0:
    #     return False
    # else:
    #     return True

    return True if count > 0 else False