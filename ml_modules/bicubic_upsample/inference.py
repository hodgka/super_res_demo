from skimage.io import imread, imsave
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np


def inference(img, scale=2):

    h, w, _ = img.shape
    output_shape = (scale*h, scale*w)
    img = resize(img, output_shape, order=3)
    return img


if __name__ == '__main__':

    img = imread('/home/alec/Documents/super_res_demo/ml_modules/test_imgs/img1.jpg')

    double = inference(img, scale=2)
    print("Input Shape: {}\nOutput Shape:{}".format(img.shape, double.shape))

    plt.imshow(img)
    plt.show()
    plt.imshow(double)
    plt.show()

    imsave('/home/alec/Documents/super_res_demo/ml_modules/test_imgs/output.jpg', img)