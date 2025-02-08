from flask import Flask, render_template, request, jsonify
# import tensorflow as tf
# from tensorflow.keras.models import load_model  # type: ignore
# from tensorflow.keras.preprocessing import image  # type: ignore
# from tensorflow.keras.metrics import AUC  # type: ignore
# import numpy as np
import lib.user as user


app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'tmp/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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

@app.route("/upload", methods=['POST'])
def get_output():
    img = request.files['image_file']
    img_path = "tmp/uploads/" + img.filename
   # img.save(img_path)
    # predict_result = predict_label(img_path)
    return render_template("upload.html")


if __name__ == '__main__':
    app.run(debug=True)
