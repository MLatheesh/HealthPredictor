from werkzeug.utils import secure_filename
from flask import Flask, request, render_template
import numpy as np
import os
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf

global graph
graph = tf.compat.v1.get_default_graph()

app = Flask(__name__, template_folder='template')
model1 = load_model("Malaria_Model.h5")
model2 = load_model("models\Pneumonia_Prediction_model.h5")
model3 = load_model("models\Breast_model.h5")
model4 = load_model("models\Brain_Tumor_VGG_model.h5")
model5 = load_model("models\TB_model.h5")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/malaria', methods=['GET', 'POST'])
def malaria():
    return render_template('malaria.html')


@app.route('/predict_malaria', methods=['GET', 'POST'])
def predict_malaria():
    if request.method == 'POST':
        f = request.files['image']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        filepath = os.path.join(basepath, f.filename)
        print("filepath is ", filepath)
        f.save(filepath)
        img = image.load_img(filepath, target_size=(50, 50, 3))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        output = model1.predict(x)
        print("prediction", output)
        per = output[0][0] if output[0][0] > output[0][1] else output[0][1]
        res_val = "INFECTED" if output[0][1] == 0 else "UNINFECTED"

        return render_template('malaria.html', imgfile='img.png', prediction_text='Result : {} {}%'.format(res_val, per*100))
    return None


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
