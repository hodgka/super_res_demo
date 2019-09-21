import torch.nn as nn


class SRCNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1_rgb = nn.Conv2d(3, 64 ,kernel_size=9, padding=4)
        self.conv1_y = nn.Conv2d(1, 64, kernel_size=9, padding=4)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(64, 32, kernel_size=1, padding=0)
        self.relu2 = nn.ReLU()
        self.conv3 = nn.Conv2d(32, 3, kernel_size=5, padding=2)
        
    def forward(self, x):
        _, c, _, _ = x.size()
        out = self.conv1_rgb(x) if c == 3 else self.conv1_y(x)
        out = self.relu1(out)
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.conv3(out)

        return out
