from __future__ import print_function
import argparse
import torch
import math
from PIL import Image

from torchvision.transforms import ToTensor
import torchvision.transforms as transforms
import numpy as np
from srcnn_model import SRCNN

class View:
    def __call__(self, img):
        c, h, w = img.size()
        return img.view(1, c, h, w)


class Inference:
    def __init__(self, args):
        self.model = torch.load(args.model)
        if args.cuda:
            self.model = self.model.cuda()
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            View(),
        ])
        self.post_process = transforms.ToPILImage()
        self.scale = args.scale
    
    def __call__(self, input_img):
        h, w = input_img.size
        output_size = (int(h*self.scale), int(w*self.scale))
        img = input_img.resize(output_size, Image.BICUBIC)
        img = self.preprocess(img)
        img = self.model(img).cpu()[0].detach().numpy()
        img *= 255.0
        img = img.clip(0, 255)
        img = Image.fromarray(np.uint8(img), mode='YCbCr').convert("RGB")
        return img
    
    def preprocess(self, img):
        img = img.convert('YCbCr')
        # y, cb, cr = img.split()
        img = self.transform(transforms)
        return img


# Training settings
parser = argparse.ArgumentParser(description='PyTorch Super Res Example')
parser.add_argument('--input_img', type=str, required=True, help='input img to use')
parser.add_argument('--model', type=str, required=True, help='model file to use')
parser.add_argument('--output_filename', type=str, help='where to save the output img')
parser.add_argument('--scale_factor', type=float, help='factor by which super resolution needed')

parser.add_argument('--cuda', action='store_true', help='use cuda')
opt = parser.parse_args()

print(opt)
input_img = Image.open(opt.input_img)
img = Image.open(opt.input_img).convert('YCbCr')
#y, cb, cr = img.split()

#tt2 = transforms.Scale((math.floor(img.size[1]*opt.scale_factor),math.floor(img.size[0]*opt.scale_factor)),interpolation=img.CUBIC)


#img = tt2(img)

img = img.resize((int(img.size[0]*opt.scale_factor),int(img.size[1]*opt.scale_factor)), Image.BICUBIC)

model = SRCNN()
model.load_state_dict(torch.load(opt.model), strict=True)
model.eval()

input = ToTensor()(img).view(1, -1, img.size[1], img.size[0])
if opt.cuda:
    model = model.to(torch.device('cuda'))
    input = input.cuda()

out = model(input)
# out = input
out = out.cpu()[0].detach().numpy().transpose((1, 2, 0))
out *= 255.0
out = out.clip(0, 255)
out = Image.fromarray(np.uint8(out), mode='YCbCr').convert("RGB")
output_img = out

input_min_max = input_img.getextrema()
output_min_max = output_img.getextrema()
print(input_min_max, output_min_max)
print("Input SHAPE: {} - MIN: {} - MAX: {}".format(input_img.size, *(input_img.getextrema())))
print("Output SHAPE: {} - MIN: {} - MAX: {}".format(output_img.size, *(output_img.getextrema())))
input_img.show()
output_img.show()
# print ("type = ",type(out))
# tt = transforms.ToPILimg()

# img_out = tt(out.data[0])
# img_out = out
# # img_out = img_out.convert('RGB')
# print("Saving output...")
# img_out.save(opt.output_filename)

# exit()





# out_img_y = out.data[0].numpy()
# out_img_y *= 255.0
# out_img_y = out_img_y.clip(0, 255)
# out_img_y = img.fromarray(np.uint8(out_img_y[0]), mode='L')

# out_img_cb = cb.resize(out_img_y.size, img.BICUBIC)
# out_img_cr = cr.resize(out_img_y.size, img.BICUBIC)
# out_img = img.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')

# out_img.save(opt.output_filename)
# print('output img saved to ', opt.output_filename)
