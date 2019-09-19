import os
from flask import Flask, Response, request, abort, render_template_string, send_from_directory
from PIL import Image
import io

app = Flask(__name__)

WIDTH = 640
HEIGHT = 360

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title></title>
<meta charset="utf-8" />
<style>
body {
margin: 0;
background-color: #333;
}
.image {
display: inline-block;
margin: 3em 14px;
background-color: #444;
box-shadow: 0 0 10px rgba(0,0,0,0.3);
}
img {
display: block;
}
</style>

{% for image in images %}
    <a class="image" href="{{ image.src }}" style="width: {{ image.width }}px; height: {{ image.height }}px">
        <img src="{{ image.src }}" width="{{ image.width }}" height="{{ image.height }}" />
    </a>
{% endfor %}
</body>
'''

@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = io.StringIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory('.', filename)

@app.route('/')
def index():
    images = []
    for root, dirs, files in os.walk('.'):
        files.sort()
        for filename in [os.path.join(root, name) for name in files]:
            # get rid of non png and jpg
            if not (filename.endswith('.png') or filename.endswith('jpg')):
                continue
            # open and scale 
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height * aspect
            # add to list of files
            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename
            })
            print(filename)

    return render_template_string(TEMPLATE, **{
        'images': images
    })

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="3000")

