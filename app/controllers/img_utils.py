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

