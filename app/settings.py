"""Settings configuration - Configuration for environment variables can go in here."""

import os
from keras.models import load_model
import tensorflow as tf
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('FLASK_ENV', default='production')
DEBUG = ENV == 'development'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY', default='octocat')
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', default='/home/alec/Documents/super_res_demo/uploads')
ALLOWED_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpeg', 'gif'])
CHAR_SET = list(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
IMAGE_LABELS = ['Headphone', 'Mouse', 'Camera', 'Smartphone', 'Glasses', 'Shoes', 'Watch', 'Laptop']
MODEL_PATH=os.getenv('MODEL_PATH', default="/home/alec/Documents/super_res_demo/ml_modules/tutorial/SouqNet128v2_gpu.h5")
MODEL = load_model(MODEL_PATH)
global graph
graph = tf.get_default_graph()