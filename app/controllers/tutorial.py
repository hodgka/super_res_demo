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

blueprint = Blueprint('tutorial', __name__, url_prefix='/tutorial')


def is_allowed(fname):
    allowed_ext = fname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return '.' in fname and allowed_ext


def generate_random_name(fname):
    ext = fname.split('.')[-1]
    rns = [random.randint(0, len(CHAR_SET)-1) for _ in range(6)]
    chars = ''.join(CHAR_SET[rn] for rn in rns)
    new_name = "{}.{}".format(chars, ext)
    new_name = secure_filename(new_name)
    return new_name


def generate_barplot(predictions):
    plot = figure(x_range=IMAGE_LABELS, plot_height=300, plot_width=400)
    plot.vbar(x=IMAGE_LABELS, top=predictions, width=0.8)
    plot.xaxis.major_label_orientation = pi/3.
    return components(plot)


def preprocess(fname):
    im = imread(fname)[:, :, :3] / 255.
    im = resize(im, (128, 128))
    im = im.reshape((-1, 128, 128, 3))
    return im


def make_thumbnail(filepath):
    """ Converts input image to 128px by 128px thumbnail if not that size
    and save it back to the source file """
    # img = Image.open(filepath)
    img = imread(filepath)
    thumb = None
    w, h, _ = img.shape

    # if it is exactly 128x128, do nothing
    if w == 128 and h == 128:
        return True

    # if the width and height are equal, scale down
    if w == h:
        thumb = resize(img, (128, 128), order=3)
        # thumb = img.resize((128, 128), Image.BICUBIC)
        imsave(filepath, thumb)
        return True

    # when the image's width is smaller than the height
    if w < h:
        # scale so that the width is 128px
        ratio = w / 128.
        w_new, h_new = 128, int(h // ratio)
        thumb = resize(img, (w_new, h_new), order=3)

        # crop the excess
        top, bottom = 0, 0
        margin = h_new - 128
        top, bottom = margin // 2, 128 + margin // 2
        box = (0, top, 128, bottom)
        # cropped = thumb.crop(box)
        cropped = thumb[0:128, top:bottom]
        # cropped.save(filepath)
        imsave(filepath, cropped)
        return True

    # when the image's height is smaller than the width
    if h < w:
        # scale so that the height is 128px
        ratio = h / 128.
        w_new, h_new = int(w // ratio), 128
        # thumb = img.resize((w_new, h_new), Image.BICUBIC)
        thumb = resize(img, (w_new, h_new), order=3)

        # crop the excess
        left, right = 0, 0
        margin = w_new - 128
        left, right = margin // 2, 128 + margin // 2
        box = (left, 0, right, 128)
        # cropped = thumb.crop(box)
        # cropped.save(filepath)
        cropped = thumb[left:right, 0:128]
        imsave(filepath, cropped)
        return True
    return False


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
