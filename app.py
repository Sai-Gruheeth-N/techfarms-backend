from flask import Flask,jsonify, request
from werkzeug.utils import secure_filename

import numpy as np
import tensorflow as tf
<<<<<<< HEAD
# import pickle
=======
>>>>>>> parent of 57622a2 (added pickle module for model loading)
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from dotenv import load_dotenv
import os

import boto3
from PIL import Image
from io import BytesIO
import requests
import random
import h5py

class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']


load_dotenv('.env')
app = Flask(__name__)
limiter_threshold = (random.randrange(0,4)*0.0314159265359)

@app.route('/')
def printHi():
    return 'Welcome To Tech-Farms'


@app.route('/upload',methods=["POST","PUT"])
def upload_image():
    if request.method == "POST":
        imageFile = request.files['image']
        content_type = request.mimetype
        s3 = boto3.client(
            's3',
            region_name = 'us-west-1',
            aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"],
        )
        filename = secure_filename(imageFile.filename)
        # imageFile.save('./uploadedImages/'+secure_filename(imageFile.filename))
        s3.put_object(
            Body = imageFile,
            Bucket = os.environ["BUCKET_NAME"],
            Key = filename,
            ContentType = content_type
        )
        print('\nImage file : ' + imageFile.filename)
        return 'Image uploaded'
        

@app.route('/predict/<fileName>',methods=["GET"])
def predict(fileName):

    # print('in pred func')
    print('\nPredict parameter : ' + fileName)

    response = requests.get('{}/{}'.format(os.environ["hostURL"],fileName))
    img = Image.open(BytesIO(response.content))
    resized_img = img.resize((256, 256), Image.ANTIALIAS)
    print('Retrieved image from S3')

    # s3 = boto3.client(
    #     's3',
    #     region_name = 'us-west-1',
    #     aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
    #     aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY"),
    # )
    # bucket = s3.Bucket(os.environ.get('BUCKET_NAME'))
    # image = bucket.Object(fileName)
    # image_data = image.get().get('Body').read()
    # sample_file = Image.open(BytesIO(image_data))
    

    sample_file = resized_img
    # sample_img = image.load_img(sample_file,target_size = (256,256,3))
    sample_img = image.img_to_array(sample_file)
    sample_img = np.expand_dims(sample_img,axis=0)

<<<<<<< HEAD

    model = load_model('fridayModel.h5')
    # file = h5py.File('C:\\Users\\gruhe\\Desktop\\backend\\capstone-backend\\fridayModel.h5','r')
    # file = h5py.File('/home/ubuntu/fridayModel.h5','r')
    # model = load_model(file,compile=False)

    # with open('model_pkl' , 'rb') as f:
    #     lr = pickle.load(f)

    prediction_arr = model.predict(sample_img)
    # f.close()
    # prediction_arr = lr.predict(sample_img)
=======
    model = load_model('fridayModel.h5')
    prediction_arr = model.predict(sample_img)
>>>>>>> parent of 57622a2 (added pickle module for model loading)
    result = {
        'Sample' : str(fileName),
        'Label' : str(class_names[prediction_arr.argmax()]),
        'Confidence' : str(prediction_arr.max() - limiter_threshold)
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)
