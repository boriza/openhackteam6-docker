#!flask/bin/python
import os, requests, sys
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from io import BytesIO

import pandas as pd
from sklearn import linear_model
import pickle
from PIL import Image, ImageOps

app = Flask(__name__)

def process_image(image_url):
    
    response = requests.get(image_url)
    im = Image.open(BytesIO(response.content))    
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
    
    new_im = [np.ravel(img)]

    return new_im

def process_image_file(file):
    
    img = file.read()
    img_io = BytesIO(img)
    im = Image.open(img_io)
    print('loaded image', file=sys.stderr)
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
    
    new_im = [np.ravel(img)]

    return new_im


@app.route('/isAlive')
def index():
    return "true"

@app.route('/prediction/api/v1.0/score', methods=['GET'])
def get_prediction():

    image_url = request.args.get('image_url')
    print('request.args.get', file=sys.stderr)

    loaded_model = pickle.load(open('/app/team6_challenge3_rfc.pkl', 'rb'))
    print('loaded pickle', file=sys.stderr)

    img = process_image (image_url)
    prediction = loaded_model.predict(img)

    return str(test_pred)

@app.route('/prediction/api/v1.0/test', methods=['GET'])
def get_test():

    return str("it works!")


@app.route('/prediction/api/v1.0/gear', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # try:
        # check if the post request has the file part

        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)

        file = request.files['file']

        print('url is ' + file, file=sys.stderr)

        im = process_image_file(file)

        # if user does not select file, browser also
        # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)

        #return str("It also works!")

        #if file and allowed_file(file.filename):
        loaded_model = pickle.load(open('team6_challenge3_rfc.pkl', 'rb'))
        prediction = loaded_model.predict(im)

        #last_prediction = prediction

        #except requests.exceptions.RequestException as e:
        return str(prediction)

    if request.method == 'GET':
        return last_prediction


@app.errorhandler(500)
def handle_internal_error(e):
    #return render_template('500.html', error=e), 500
    return str(e)


if __name__ == '__main__':
    if os.environ['ENVIRONMENT'] == 'production':
        app.run(port=80,host='0.0.0.0')
    if os.environ['ENVIRONMENT'] == 'local':
        app.run(port=5000,host='0.0.0.0')

