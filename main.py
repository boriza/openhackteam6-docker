#!flask/bin/python
import os, requests, sys
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

import pandas as pd
import pickle
from PIL import ImageOps

import base64
import numpy as np
import io
from PIL import Image
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array


app = Flask(__name__)

def get_model():
    global model
    model = pickle.load(open('/app/team6_challenge3_rfc.pkl', 'rb'))
    print("Model loaded!", file=sys.stderr)




def process_image_file(im):
    print("Processing image file...", file=sys.stderr)
    desired_size = 128
    old_size = im.size
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    im = im.resize(new_size, Image.ANTIALIAS)
    new_im = Image.new("RGB", (desired_size, desired_size), (255,255,255))
    new_im.paste(im, ((desired_size-new_size[0])//2,
                    (desired_size-new_size[1])//2))
    
    #new_im = ImageOps.autocontrast(new_im, cutoff=0)
    new_im = ImageOps.equalize(new_im)
    new_im = [np.ravel(new_im)]

    print("Processing image file completed", file=sys.stderr)

    return new_im

print("Loading sci-kit learn model...", file=sys.stderr)
get_model()



@app.route('/test', methods=['GET'])
def get_test():
    return str("it works!")


@app.route('/testpost', methods=['POST'])
def get_testpost():

    return str("POST works too!")


@app.route('/predict', methods=['POST'])
def upload_file():
    print("Processing json request...", file=sys.stderr)
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    im = process_image_file(image)
    print("Processing json request completed", file=sys.stderr)

    print("Predicting image class...", file=sys.stderr)        
    prediction = model.predict(im)
    print("Predicting image class completed", file=sys.stderr)

    return str(prediction)


@app.errorhandler(500)
def handle_internal_error(e):
    #return render_template('500.html', error=e), 500
    return str(e)


if __name__ == '__main__':
    if os.environ['ENVIRONMENT'] == 'production':
        app.run(port=80,host='0.0.0.0')
    if os.environ['ENVIRONMENT'] == 'local':
        app.run(port=5000,host='0.0.0.0')

