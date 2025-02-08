from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.preprocessing import image  # type: ignore
from tensorflow.keras.metrics import AUC  # type: ignore
import numpy as np
import lib.user as user

app = Flask(__name__, template_folder='templates')
# app.config['UPLOAD_FOLDER'] = 'tmp/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/<path:path>')
def static_file(path):
    print(path)
    return render_template(path + '.html')


@app.route("/login", methods=['POST'])
def login():
    form_data = request.get_json()
    result = user.check_login(form_data['email'], form_data['password'])
    return jsonify({
        'result': result
    })

@app.route("/signup", methods=['POST'])
def signup():
    form_data = request.get_json()
    result = user.save_user(form_data)
    return jsonify(result)


print('Loading model skin.h5...')
model = load_model('model/skin.h5')

@app.route("/upload", methods=['POST'])
def get_output():
    img = request.files['image_file']
    img_path = "tmp/uploads/" + img.filename
    img.save(img_path)
    predict_result = predict(img_path)
    return render_template("upload.html", prediction=predict_result)


def predict(img_path):
    test_image = image.load_img(img_path, target_size=(28, 28))
    test_image = image.img_to_array(test_image) / 255.0
    test_image = test_image.reshape(1, 28, 28, 3)
    predict_x = model.predict(test_image)
    classes_x = np.argmax(predict_x, axis=1)
    verbose_name = {
        0: 'Actinic keratoses and intraepithelial carcinomae',
        1: 'Basal cell carcinoma',
        2: 'Benign keratosis-like lesions',
        3: 'Dermatofibroma',
        4: 'Melanocytic nevi',
        5: 'Pyogenic granulomas and hemorrhage',
        6: 'Melanoma',
    }
    return verbose_name[classes_x[0]]

if __name__ == '__main__':
    app.run(debug=True)
