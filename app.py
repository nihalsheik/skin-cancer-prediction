from flask import Flask, render_template, request, jsonify, session

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# --------- Tensorflow Imports
import tensorflow as tf
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.preprocessing import image  # type: ignore
from tensorflow.keras.metrics import AUC  # type: ignore
import numpy as np
# --------- Tensorflow Imports

from lib.mysql_db import MySqlDB
from lib.user import User
from lib.patient import Patient

app = Flask(__name__, template_folder='templates')
app.secret_key = 'BAD_SECRET_KEY'

mysqldb = MySqlDB()
user = User(mysqldb)
patient = Patient(mysqldb)


# app.config['UPLOAD_FOLDER'] = 'tmp/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<path:path>')
def static_file(path):
    if not path.endswith('.html'):
        path += '.html'
    return render_template(path)


@app.route('/api/patients')
def patients():
    return jsonify(patient.get_list())


@app.route("/login", methods=['POST'])
def login():
    form_data = request.get_json()
    result = user.check_login(form_data['email'], form_data['password'])

    if result:
        session['user'] = form_data['email']

    return jsonify({
        'result': result
    })


@app.route("/signup", methods=['POST'])
def signup():
    form_data = request.get_json()
    result = user.save_user(form_data)
    return jsonify(result)


@app.route("/patient/register", methods=['POST'])
def register_patient():
    form_data = request.get_json()
    result = patient.register(form_data)
    return jsonify(result)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user", None)
    return jsonify({'result': 1})


print('Loading model skin.h5...')
model = load_model('model/skin.h5')


@app.route("/diagnose", methods=['POST'])
def diagnose():
    img = request.files['image_file']
    img_path = "tmp/uploads/" + img.filename
    img.save(img_path)
    diagnose_result = predict(img_path)
    return render_template("diagnose-result.html", diagnose_name=diagnose_result[1], diagnose_desc=diagnose_result[2])


def predict(img_path):
    test_image = image.load_img(img_path, target_size=(28, 28))
    test_image = image.img_to_array(test_image) / 255.0
    test_image = test_image.reshape(1, 28, 28, 3)
    predict_x = model.predict(test_image)
    classes_x = np.argmax(predict_x, axis=1)
    print(classes_x)
    print('Disease type ', classes_x[0])
    res = mysqldb.fetch_one('SELECT type,name,description FROM tbl_disease WHERE type = %s', (str(classes_x[0]),))
    return res


if __name__ == '__main__':
    app.run(debug=True)
