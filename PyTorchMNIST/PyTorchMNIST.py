import torchvision.datasets
import torchvision.transforms
import torch.utils.data                     #类分批处理
import matplotlib.pyplot as plt
import torch.nn
import torch.optim
import torch

train_dataset = torchvision.datasets.MNIST(root='./data/mnist',
       train=True,transform=torchvision.transforms.ToTensor(),download=True)     #下载训练集

test_dataset = torchvision.datasets.MNIST(root='./data/mnist',
       train=False,transform=torchvision.transforms.ToTensor(),download=True)    #下载测试集

batch_size = 100                       #每批次读取100条数据

train_loader = torch.utils.data.DataLoader(
    dataset= train_dataset,batch_size=batch_size)
print('len(train_loader)={}'.format(len(train_loader)))

test_loader = torch.utils.data.DataLoader(
    dataset=test_dataset,batch_size=batch_size)
print('len(test_loader)={}'.format(len(test_loader)))

for images,labels in train_loader:
    print('image.size()={}'.format(images.size()))
    print('labels.size()={}'.format(labels.size()))
    break

#plt.imshow(images[0,0],cmap='gray')
#plt.title('label={}'.format(labels[0]))

#训练线性判决器
fc = torch.nn.Linear(28*28,10)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(fc.parameters())

num_epochs = 5
for epoch in range(num_epochs):
    for idx,(images,labels) in enumerate(train_loader):
        x = images.reshape(-1,28*28)

        optimizer.zero_grad()
        preds = fc(x)
        loss = criterion(preds,labels)
        loss.backward()
        optimizer.step()

        if idx % 100 == 0:
            print('第{}趟第{}批：loss={:g}'.format(epoch,idx,loss))

#对训练好的线性判决器进行测试
correct = 0
total = 0

for images,labels in test_loader:
    x = images.reshape(-1,28*28)
    preds = fc(x)
    predicted = torch.argmax(preds,1)
    total += labels.size(0)
    correct += (predicted == labels).sum().item()

accuracy = correct / total
print('测试集上的准确率:{:.1%}'.format(accuracy))


