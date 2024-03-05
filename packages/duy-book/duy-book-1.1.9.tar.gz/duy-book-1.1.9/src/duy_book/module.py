import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.optim.lr_scheduler as sched
from torchsummary import summary
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
from .colab import ColabOutput
from .tqdn import tqdn

class Scheduler:
    def __init__(self, scheduler, optimizer, T_max):
        self.scheduler = scheduler
        self.optimizer = optimizer
        self.T_max = T_max
    def init(self, epochs):
        if self.T_max == -1: self.T_max = epochs
        if self.scheduler: self.scheduler = self.scheduler(self.optimizer, self.T_max)
    def step(self):
        if self.scheduler: self.scheduler.step()

class Module(nn.Module):
    def forward(self, input):
        return self.module(input)

    def init(self, optimizer=optim.Adam, lr=1e-3, scheduler=sched.CosineAnnealingLR, T_max=-1):
        self.optimizer = optimizer(self.module.parameters(), lr)
        self.scheduler = Scheduler(scheduler, self.optimizer, T_max)
        return self.cuda()

    def summary(self, *input_size):
        return summary(self.module.cuda(), (input_size))

    def test(self, loader):
        self.eval()
        accuracy = 0
        with torch.no_grad():
            for bar, (images, labels) in tqdn(loader, desc='Testing\t'):
                predict = self(images).argmax(1)
                accuracy += (predict == labels).sum().item()
                bar.set_postfix_str('Accuracy is {:%}'.format(accuracy / len(loader.dataset)))

    def fit(self, epochs:int, loaders:list, losser=F.cross_entropy):
        colab = ColabOutput()
        losses = [[], [], []]
        self.scheduler.init(epochs)
        for bar, epoch in tqdn(range(epochs), desc='Training'):
            for param_group in self.optimizer.param_groups:
                bar.set_postfix_str(f'lr:{param_group["lr"]}')
                break

            self.train()
            for loss in losses: loss.append(0)
            for images, labels in loaders[0]:
                self.optimizer.zero_grad()
                loss = losser(self(images), labels)
                loss.backward(), self.optimizer.step()
                losses[0][-1] += loss.item()
            self.scheduler.step()
            losses[0][-1] /= len(loaders[0])

            if len(loaders) < 2: continue
            else: self.eval()
            with torch.no_grad():
                for images, labels in loaders[1]:
                    output = self(images)
                    losses[1][-1] += losser(output, labels).item()
                    losses[2][-1] += (output.argmax(1) == labels).sum().item()
            losses[1][-1] /= len(loaders[1])
            losses[2][-1] /= len(loaders[1].dataset)

            with colab:
                plt.plot(losses[0], label='Training')
                plt.plot(losses[1], label='Validation')
                plt.plot(losses[2], label='Accuracy')
                plt.legend()
        return self
