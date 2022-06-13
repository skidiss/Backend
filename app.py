import os
import json
import tensorflow as tf
import numpy as np
import tensorflow.keras as keras
import shutil
import time
import pandas as pd
import uuid
import jwt
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from  werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from google.cloud import storage

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GCP_PROJECT = os.getenv("GCP_PROJECT")
GCP_ACCOUNT = os.getenv("GCP_ACCOUNT")
  
app = Flask(__name__)
db = SQLAlchemy(app)
storage_client = storage.Client()
bucket_user = 'c22ps191b4'
bucket_model = 'c22ps191b2'

model = tf.keras.models.load_model("gs://{bucket_model}/model.h5", custom_objects={'KerasLayer':hub.KerasLayer})
  
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))
  
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Missing Token'}), 401
  
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Onvalid Token'
            }), 401
        return  f(current_user, *args, **kwargs)
  
    return decorated

@app.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'public_id': user.public_id,
            'name' : user.name,
            'email' : user.email
        })
  
    return jsonify({'users': output})

@app.route('/login', methods =['POST'])
def login():
    auth = request.form
  
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Please Login First"'}
        )
  
    user = User.query\
        .filter_by(email = auth.get('email'))\
        .first()
  
    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist"'}
        )
  
    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
  
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password"'}
    )
  
@app.route('/signup', methods =['POST'])
def signup():
    data = request.form
  
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
  
    user = User.query\
        .filter_by(email = email)\
        .first()
    if not user:
        user = User(
            public_id = str(uuid.uuid4()),
            name = name,
            email = email,
            password = generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
  
        return make_response('Successfully registered', 201)
    else:
        return make_response('Duplicate Account', 202)

# @app.route("/upload", methods=["POST"])
# def upload():
#     if request.method == 'POST':
#         shutil.rmtree('images')
#         os.makedirs('images')
#         upload_image=request.files['images']
#         cloud_bucket = 'gs://{bucket_name}/image'
#         filepath=os.path.join(cloud_bucket, image.filename)
#         upload_image.save(filepath)

# @app.route("/predict", methods=["GET"])
# def predict():
#         path = '/content/' + fn
#         img = image.load_img(path, target_size=(150, 150))
#         x = image.img_to_array(img)
#         x = x / 255
#         x = np.expand_dims(x, axis=0)
#         images = np.vstack([x])
#         classes = model.predict(images, batch_size=10)
#         print(classes[0])
#         if max(classes[0])==classes[0][0]:
#             print("Acne and Rosacea")
#             elif max(classes[0])==classes[0][1]:
#                 return("Atopic Dermatits")
#             elif max(classes[0])==classes[0][2]:
#                 return("Herpes HPV and other STD")
#             elif max(classes[0])==classes[0][3]:
#                 return("Poison Ivy and other contact diseases")
#             elif max(classes[0])==classes[0][4]:
#                 return("Psoriasis")
#             elif max(classes[0])==classes[0][5]:
#                 return("Scabies Lyme Disease and other infestations and bites")  
#         else:
#             return "Error Predicting"

if __name__ == "__main__":
    app.run()