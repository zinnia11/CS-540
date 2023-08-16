# python imports
import os
from tqdm import tqdm

# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms


class LeNet(nn.Module):
    def __init__(self, input_shape=(32, 32), num_classes=100):
        super(LeNet, self).__init__()
        # certain definitions
        #1
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=6, kernel_size=5, stride=1, bias=True)
        self.max_pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        #2
        self.conv2 = nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5, stride=1, bias=True)
        self.max_pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        #4
        self.fc1 = nn.Linear(16*5*5, 256)
        #5
        self.fc2 = nn.Linear(256, 128)
        #6
        self.fc3 = nn.Linear(128, num_classes)


    def forward(self, x):
        shape_dict = {}
        # certain operations
        #1
        out = self.conv1(x)
        out = nn.functional.relu(out)
        out = self.max_pool1(out)
        shape_dict.update({1: list(out.size())})
        #2
        out = self.conv2(out)
        out = nn.functional.relu(out)
        out = self.max_pool2(out)
        shape_dict.update({2: list(out.size())})
        #3
        out = torch.flatten(out, 1)
        shape_dict.update({3: list(out.size())})
        #4
        out = self.fc1(out)
        out = nn.functional.relu(out)
        shape_dict.update({4: list(out.size())})
        #5
        out = self.fc2(out)
        out = nn.functional.relu(out)
        shape_dict.update({5: list(out.size())})
        #6
        out = self.fc3(out)
        out = nn.functional.relu(out)
        shape_dict.update({6: list(out.size())})

        return out, shape_dict


def count_model_params():
    '''
    return the number of trainable parameters of LeNet.
    '''
    model = LeNet()
    model_params = 0.0
    for name, p in model.named_parameters():
        if p.requires_grad: 
            model_params += p.numel()

    # want number of model parameters in units of millions
    return model_params/1000000


def train_model(model, train_loader, optimizer, criterion, epoch):
    """
    model (torch.nn.module): The model created to train
    train_loader (pytorch data loader): Training data loader
    optimizer (optimizer.*): A instance of some sort of optimizer, usually SGD
    criterion (nn.CrossEntropyLoss) : Loss function used to train the network
    epoch (int): Current epoch number
    """
    model.train()
    train_loss = 0.0
    for input, target in tqdm(train_loader, total=len(train_loader)):
        ###################################
        # fill in the standard training loop of forward pass,
        # backward pass, loss computation and optimizer step
        ###################################

        # 1) zero the parameter gradients
        optimizer.zero_grad()
        # 2) forward + backward + optimize
        output, _ = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        # Update the train_loss variable
        # .item() detaches the node from the computational graph
        # Uncomment the below line after you fill block 1 and 2
        train_loss += loss.item()

    train_loss /= len(train_loader)
    print('[Training set] Epoch: {:d}, Average loss: {:.4f}'.format(epoch+1, train_loss))

    return train_loss


def test_model(model, test_loader, epoch):
    model.eval()
    correct = 0
    with torch.no_grad():
        for input, target in test_loader:
            output, _ = model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_acc = correct / len(test_loader.dataset)
    print('[Test set] Epoch: {:d}, Accuracy: {:.2f}%\n'.format(
        epoch+1, 100. * test_acc))

    return test_acc
