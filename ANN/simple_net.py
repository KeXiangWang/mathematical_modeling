from torch import nn, optim
import numpy as np
import torch
from torch.autograd import Variable


class simpleNet(nn.Module):
    """docstring for simpleNet"""

    def __init__(self, in_dim, n_hidden_1, n_hidden_2, out_dim):
        super(simpleNet, self).__init__()
        self.in_dim = in_dim
        self.layer1 = nn.Sequential(nn.Linear(in_dim, n_hidden_1), nn.BatchNorm1d(n_hidden_1), nn.ReLU(True))
        self.layer2 = nn.Sequential(nn.Linear(n_hidden_1, n_hidden_2), nn.BatchNorm1d(n_hidden_2), nn.ReLU(True))
        self.layer3 = nn.Linear(n_hidden_2, out_dim)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return x


if __name__ == '__main__':
    Totel_list_train_data = np.loadtxt("MultiSetzzh.csv", delimiter=",")

    train_x = np.array(Totel_list_train_data, dtype=np.float32)[:, 0:22]
    train_y = np.array(Totel_list_train_data, dtype=np.float32)[:, 22:24]

    x_train = torch.from_numpy(train_x)
    y_train = torch.from_numpy(train_y)

    if torch.cuda.is_available():
        module = simpleNet(22, 110, 110, 2).cuda()
    else:
        module = simpleNet(22, 110, 110, 2)

    criterion = nn.MSELoss()
    optimizer = optim.SGD(module.parameters(), lr=1e-3)

    num_epoch = 10000
    for epoch in range(num_epoch):
        if torch.cuda.is_available():
            input1 = Variable(x_train).cuda()
            target = Variable(y_train).cuda()
        else:
            input1 = Variable(x_train)
            target = Variable(y_train)
        out = module(input1)
        loss = criterion(out, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 is 0:
            print(loss.data.numpy())
            print("===============")

    torch.save(module.state_dict(), 'params.pkl')
