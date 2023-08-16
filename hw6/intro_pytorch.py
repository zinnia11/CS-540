import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.

# torchvision.datasets.FashionMNIST()

"""
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) 
                    or the test set (if training = False)
"""
def get_data_loader(training = True):
    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    
    if (training == True):
        # use training set
        data_set=datasets.FashionMNIST('./data',
            train=True, download=True, transform=custom_transform)
    elif (training == False):
        # use test set
        data_set=datasets.FashionMNIST('./data', 
            train=False, transform=custom_transform)

    loader = torch.utils.data.DataLoader(data_set, batch_size = 64)
    return loader


"""
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
"""
def build_model():
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(28*28, 128),
        nn.ReLU(),
        nn.Linear(128, 64),
        nn.ReLU(),
        nn.Linear(64, 10),
    )

    return model


"""
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
"""
def train_model(model, train_loader, criterion, T):
    # criterion = nn.CrossEntropyLoss()
    model.train() # use training model
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    it = range(T)
    for ep in it: # T epochs
        running_loss = 0.0
        correct = 0
        total = 0
        # loop through data
        for i, data in enumerate(train_loader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            opt.zero_grad()

            # actually optimizing the model using crieterion
            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            opt.step()

            _, predicted = torch.max(outputs.data, 1) # prediction
            # add to the totals
            running_loss += loss.item()
            correct += (predicted == labels).sum()
            total += labels.size(0)

        # print out stats for each epoch run 
        print('Train Epoch: {num} Accuracy: {correct}/{total}({percent:.2f}%) Loss: {loss:.3f}'.format(
            num = ep, correct = correct, total = total, percent = 100.*correct/total, loss = running_loss/len(train_loader)))


"""
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
"""
def evaluate_model(model, test_loader, criterion, show_loss = True):
    model.eval() # evaluate mode

    running_loss = 0.0
    total = 0
    correct = 0
    with torch.no_grad(): # no gradients for evaluation
        for data, labels in test_loader:
            outputs = model(data)

            _, predicted = torch.max(outputs.data, 1) # prediction
            loss = criterion(outputs, labels) 
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            running_loss += loss.item()

    # final stats
    if (show_loss == True):
        print("Average loss: {loss:.4f}".format(loss = running_loss/len(test_loader)))
    print('Accuracy: {accurate:.2f}%'.format(accurate = 100.*correct/total))


def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    class_names = ['T-shirt/top','Trouser','Pullover','Dress','Coat','Sandal','Shirt'
                    ,'Sneaker','Bag','Ankle Boot']
    
    data = test_images[index]
    outputs = model(data)
    prob = F.softmax(outputs, dim=1)
    prob = prob.detach().numpy()[0]
    index = np.argsort(prob)[::-1]
    print('{classn}: {prob:.2f}%'.format(classn=class_names[index[0]], prob=prob[index[0]]*100))
    print('{classn}: {prob:.2f}%'.format(classn=class_names[index[1]], prob=prob[index[1]]*100))
    print('{classn}: {prob:.2f}%'.format(classn=class_names[index[2]], prob=prob[index[2]]*100))



if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    criterion = nn.CrossEntropyLoss()
    '''
    train_loader = get_data_loader()
    test_loader = get_data_loader(False)
    model = build_model()
    train_model(model, train_loader, criterion, 5)
    evaluate_model(model, test_loader, criterion, show_loss = True)
    pred_set, _ = next(iter(test_loader))
    predict_label(model, pred_set, 1)
    '''

