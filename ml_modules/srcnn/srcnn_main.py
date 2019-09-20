from __future__ import print_function
import argparse
from math import log10
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from srcnn_data import get_training_set, get_test_set
from srcnn_model import SRCNN

parser = argparse.ArgumentParser(description='PyTorch Super Res Example')
parser.add_argument('--upscale_factor', type=int, default=2, help="super resolution upscale factor")
parser.add_argument('--batch_size', type=int, default=64, help='training batch size')
parser.add_argument('--test_batch_size', type=int, default=10, help='testing batch size')
parser.add_argument('--epochs', type=int, default=150, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=0.01, help='Learning Rate. Default=0.01')
parser.add_argument('--cuda', action='store_true', help='use cuda?')
parser.add_argument('--threads', type=int, default=4, help='number of threads for data loader to use')
parser.add_argument('--seed', type=int, default=123, help='random seed to use. Default=123')
parser.add_argument('--no_cuda', action='store_true', default=False, help='disables CUDA training')
parser.add_argument('--gpu_ids', type=str, default='0',
                        help='use which gpu to train, must be a \
                        comma-separated list of integers only (default=0)')
args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()
device = torch.device('cuda' if args.cuda else 'cpu')
if args.cuda:
    try:
        args.gpu_ids = [int(s) for s in args.gpu_ids.split(',')]
    except ValueError:
        raise ValueError('Argument --gpu_ids must be a comma-separated list of integers only')
    torch.cuda.manual_seed(args.seed)
torch.manual_seed(args.seed)
print(args)

train_set = get_training_set(args.upscale_factor)
test_set = get_test_set(args.upscale_factor)
training_data_loader = DataLoader(dataset=train_set, num_workers=args.threads, batch_size=args.batch_size, shuffle=True)
testing_data_loader = DataLoader(dataset=test_set, num_workers=args.threads, batch_size=args.test_batch_size, shuffle=False)

srcnn = SRCNN()
criterion = nn.MSELoss()

if args.cuda:
    srcnn = nn.DataParallel(srcnn, device_ids=args.gpu_ids)
srcnn = srcnn.to(device)
criterion = criterion.to(device)

optimizer = optim.Adam(srcnn.parameters(),lr=args.lr)


def train(epoch):
    epoch_loss = 0
    for iteration, batch in enumerate(training_data_loader, 1):
        input, target = batch[0], batch[1]
        if args.cuda:
            input = input.to(device)
            target = target.to(device)

        optimizer.zero_grad()
        # print ("input shape = " , input.shape)
        # print ("target shape = ", target.shape)
        model_out = srcnn(input)
        #print ("model_out shape =" , model_out.shape)
        loss = criterion(model_out, target)
        epoch_loss += loss.item()
        loss.backward()
        optimizer.step()

        print("===> Epoch[{}]({}/{}): Loss: {:.4f}".format(epoch, iteration, len(training_data_loader), loss.item()))

    print("===> Epoch {} Complete: Avg. Loss: {:.4f}".format(epoch, epoch_loss / len(training_data_loader)))



def test():
    avg_psnr = 0
    for batch in testing_data_loader:
        input, target = batch[0], batch[1]
        if args.cuda:
            input = input.to(device)
            target = target.to(device)

        prediction = srcnn(input)
        mse = criterion(prediction, target)
        psnr = 10 * log10(1 / mse.item())
        avg_psnr += psnr
    print("===> Avg. PSNR: {:.4f} dB".format(avg_psnr / len(testing_data_loader)))


def checkpoint(model, epoch):
    save_filename = 'model_{}_scale_{}_epoch.pth'.format(args.upscale_factor, epoch)
    save_path = os.path.join('models', save_filename)
    if isinstance(model, nn.DataParallel) or isinstance(model, DistributedDataParallel):
        model = model.module
    state_dict = model.state_dict()
    for key, param in state_dict.items():
        state_dict[key] = param.cpu()
    torch.save(state_dict, save_path)
    # model_out_path = "model_epoch_{}.pth".format(epoch)
    # torch.save(srcnn, model_out_path)
    print("Checkpoint saved to {}".format(save_path))

for epoch in range(1, args.epochs + 1):
    train(epoch)
    test()
    if(epoch%10==0):
        checkpoint(srcnn, epoch)

