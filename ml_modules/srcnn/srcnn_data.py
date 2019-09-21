from os.path import exists, join, basename
from os import makedirs, remove
from six.moves import urllib
import tarfile
# from torchvision.transforms import Compose, CenterCrop, ToTensor, Resize
import torch
from torchvision import transforms

from srcnn_data_utils import DatasetFromFolder


def download_bsd300(dest="dataset"):
    output_image_dir = join(dest, "BSDS300/images")

    if not exists(output_image_dir):
        makedirs(dest)
        url = "http://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300-images.tgz"
        print("downloading url ", url)

        data = urllib.request.urlopen(url)

        file_path = join(dest, basename(url))
        with open(file_path, 'wb') as f:
            f.write(data.read())

        print("Extracting data")
        with tarfile.open(file_path) as tar:
            for item in tar:
                tar.extract(item, dest)

        remove(file_path)

    return output_image_dir


def calculate_valid_crop_size(crop_size, upscale_factor):
    return crop_size - (crop_size % upscale_factor)


def input_transform(crop_size, upscale_factor):
    return transforms.Compose([
        transforms.TenCrop(crop_size),
        transforms.Lambda(lambda crops: torch.stack([transforms.ToTensor()(crop) for crop in crops])),
        # CenterCrop(crop_size),
        # Resize(crop_size),
        #Resize(crop_size // upscale_factor),
        # transforms.ToTensor(),
    ])


def target_transform(crop_size):
    return transforms.Compose([
        transforms.CenterCrop(crop_size),
        transforms.ToTensor(),
    ])


def get_training_set(upscale_factor):

    root_dir = download_bsd300()
    # root_dir = '/media/alec/wd1/datasets/FLICKR30K'    
    train_dir = join(root_dir, "train")
    crop_size = calculate_valid_crop_size(256, upscale_factor)

    return DatasetFromFolder(train_dir,
                             input_transform=input_transform(crop_size, upscale_factor),
                             target_transform=target_transform(crop_size))


def get_test_set(upscale_factor):
    root_dir = download_bsd300()
    # root_dir = '/media/alec/wd1/datasets/FLICKR30K'
    test_dir = join(root_dir, "test")
    crop_size = calculate_valid_crop_size(256, upscale_factor)

    return DatasetFromFolder(test_dir,
                             input_transform=input_transform(crop_size, upscale_factor),
                             target_transform=target_transform(crop_size))


if __name__ == '__main__':
    tr = get_training_set(2)
    for i in range(5):
        image, target = tr[i]
        print(image.size(), target.size())