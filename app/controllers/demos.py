# -*- coding: utf-8 -*-
import os
import random
import io
from PIL import Image
# import cv2
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   send_file, session, url_for, send_from_directory)

from app.controllers.utils import *
from app.settings import (ALLOWED_EXTENSIONS, CHAR_SET, IMAGE_LABELS, MODEL,
                          UPLOAD_FOLDER, graph, OUTPUT_FOLDER)
from ml_modules import bicubic, bilinear, nearest_neighbor

SR_METHODS = {
    'bicubic': bicubic,
    'bilinear': bilinear,
    'nearest_neighbor': nearest_neighbor,
    'srcnn': bilinear} 

blueprint = Blueprint('demos', __name__, url_prefix='/demos')


@blueprint.route('/super_res', methods=['GET', 'POST'])
def super_res():
    if request.method == 'GET':
        return render_template('demos/super_res.html')
    if request.method == "POST":
        sr_method = request.form['sr_models']
        if 'image' not in request.files:
            flash("No file was uploaded.")
            return redirect(request.url)

        img_file = request.files['image']

        if img_file.filename == '':
            flash("Image filename empty.")
            return redirect(request.url)
        if img_file and is_allowed(img_file.filename):
            passed = False
            try:
                fname = generate_random_name(img_file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, fname)
                img_file.save(filepath)
                passed = make_thumbnail(filepath)
            except Exception as e:
                # flash(e)
                print(e)
                pass

            if passed:
                return redirect(url_for('demos.super_res_inference', sr_method=sr_method, fname=fname))
            else:
                flash("An error occurred. Please try again.")
                return redirect(request.url)


@blueprint.route('/super_res_inference/<sr_method>/<fname>')
def super_res_inference(sr_method, fname):
    image_url = url_for('demos.input_images', fname=fname)
    filepath = os.path.join(UPLOAD_FOLDER, fname)
    im = preprocess(filepath)

    # TODO need to fix this to use module properly instead of hacky dict at top
    sr_model = SR_METHODS.get(sr_method.lower())
    output = sr_model(im)

    save_image(fname, output)

    return render_template(
        'demos/super_res_result.html',
        image_url=image_url,
        output_url=url_for('demos.output_images', fname=fname)
    )


@blueprint.app_errorhandler(500)
def serve_error(error):
    return render_template('500.html'), 500


@blueprint.route('/images/input/<fname>', methods=["GET"])
def input_images(fname):
    return send_file(os.path.join(UPLOAD_FOLDER, fname))

@blueprint.route('/images/output/<fname>', methods=["GET"])
def output_images(fname):
    return send_from_directory(OUTPUT_FOLDER, fname, as_attachment=True)



@blueprint.route('/pokegan')
def pokegan():

    fnames = ["https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(117).jpg",
              "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(98).jpg",
              "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(131).jpg",
              "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(123).jpg",
              "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(118).jpg",
              "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(128).jpg",
              "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(132).jpg",
              "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(115).jpg",
              "https://mdbootstrap.com/img/Photos/Horizontal/Nature/12-col/img%20(133).jpg",
              ]

    return render_template('demos/pokegan.html',
                           items=fnames
                           )


@blueprint.route('/pixel_recursive_super_res')
def pixel_recursive_super_res():
    items = ['PIXELS', "GO", "HERE"]
    return render_template('demos/pixel_recursive_super_res.html', items=fnames)
