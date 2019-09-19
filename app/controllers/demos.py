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

blueprint = Blueprint('demos', __name__, url_prefix='/demos')


@blueprint.route('/super_res', methods=['GET', 'POST'])
def super_res():
    if request.method == 'GET':
        return render_template('demos/super_res.html')
    if request.method == "POST":
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
                return redirect(url_for('demos.super_res_inference', fname=fname))
            else:
                flash("An error occurred. Please try again.")
                return redirect(request.url)


@blueprint.route('/super_res_inference/<fname>')
def super_res_inference(fname):
    image_url = url_for('demos.input_images', fname=fname)
    filepath = os.path.join(UPLOAD_FOLDER, fname)
    im = preprocess(filepath)
    output = bicubic(im[0])

    save_image(fname, output)

    predictions = [0.1, 0.5, 0.3, 0.75, 0.9, 0.5, 0.1, 0.0]
    script, div = generate_barplot(predictions)
    return render_template(
        'demos/super_res_result.html',
        plot_script=script,
        plot_div=div,
        image_url=image_url,
        output_url=url_for('demos.output_images', fname=fname)
    )


@blueprint.app_errorhandler(500)
def serve_error(error):
    return render_template('500.html'), 500


@blueprint.route('/images/input/<fname>', methods=["GET"])
def input_images(fname):
    print("INPUT IS CALLED")
    return send_file(os.path.join(UPLOAD_FOLDER, fname))

@blueprint.route('/images/output/<fname>', methods=["GET"])
def output_images(fname):
    print("OUTPUT IS CALLED", OUTPUT_FOLDER, fname)
    # image = Image.fromarray(output.astype(np.uint8))
    # output_arr = io.BytesIO()
    # image.convert('RGBA').save(output_arr, format='PNG')
    # output_arr.seek(0, 0)
    # out = output_arr.getvalue()

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
