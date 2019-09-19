# -*- coding: utf-8 -*-
import os
import random

from flask import redirect, render_template, request, send_file
from flask import g, Blueprint, flash, url_for, session
from werkzeug.utils import secure_filename

from numpy import pi, squeeze
from keras import backend as K
from skimage.io import imread, imsave
from skimage.transform import resize
from bokeh.plotting import figure
from bokeh.embed import components

from app.settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, CHAR_SET, IMAGE_LABELS, MODEL, graph
# from app.services.github import GitHub
from app.controllers.utils import *

blueprint = Blueprint('tutorial', __name__, url_prefix='/tutorial')





@blueprint.route('/img_classification', methods=['GET', 'POST'])
def img_classification():
    print("IMG CLASSIFICATION HIT")
    if request.method == 'GET':
        return render_template('tutorial/base.html')
    if request.method=="POST":
        #     return render_template('tutorial/predict.html')
        # return render_template('tutorial/predict.html')
        print("IMG POST HIT")
        if 'image' not in request.files:
            print("NO FILE")
            flash("No file was uploaded.")
            return redirect(request.url)
        
        img_file = request.files['image']

        if img_file.filename == '':
            print("EMPTY FILENAME")
            flash("Image filename empty.")
            return redirect(request.url)
        if img_file and is_allowed(img_file.filename):
            print("IMG HIT")
            passed=False
            try:
                # fname = img_file.filename
                fname = generate_random_name(img_file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, fname)
                img_file.save(filepath)
                passed=make_thumbnail(filepath)
            except Exception as e:
                # flash(e)
                print(e)
                pass
            
            if passed:
                print("PASSED")
                return redirect(url_for('tutorial.predict', fname=fname))
            else:
                print("FAILED")
                flash("An error occurred. Please try again.")
                return redirect(request.url)



@blueprint.route('/predict/<fname>')
def predict(fname):
    image_url = url_for('tutorial.images', fname=fname)
    filepath = os.path.join(UPLOAD_FOLDER, fname)
    im = preprocess(filepath)
    with graph.as_default():
        predictions = MODEL.predict_proba(im).squeeze()
    # predictions = [0.1, 0.5, 0.3, 0.75, 0.9, 0.5, 0.1, 0.0]
    script, div = generate_barplot(predictions)
    return render_template(
        'tutorial/predict.html',
        plot_script=script,
        plot_div=div,
        image_url=image_url
    )

@blueprint.app_errorhandler(500)
def serve_error(error):
    return render_template('500.html'), 500


@blueprint.route('/images/<fname>', methods=["GET"])
def images(fname):
    print(UPLOAD_FOLDER)
    return send_file(os.path.join(UPLOAD_FOLDER, fname))
