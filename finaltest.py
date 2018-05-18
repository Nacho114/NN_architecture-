from torch import Tensor
import torch
import math
from linear import Linear
from torch import Tensor
from network import Network
from MSE import MSE
import matplotlib
import matplotlib.pyplot as plt
from activation import Relu, Tanh

def generate_disc_set(nb):
    input = Tensor(nb, 2).uniform_(0, 1)
    modified_input = input - 0.5
    #print(modified_input.pow(2).sum(1).sub(1/ (2*math.pi)).sign().mul(-1))
    #print("Modified inputs are ", modified_input)
    target = modified_input.pow(2).sum(dim=1).sub(1/ (2*math.pi)).sign().mul(-1).add(1).div(2).long()
    return input, target

def conv_to_one_hot(labels):
	one_hot = torch.Tensor(labels.shape[0], labels.max()+1).zero_()
	one_hot.scatter_(1, labels.view(-1, 1), 1.0)
	return one_hot

def compute_nb_errors(pred, tgt):
	return (pred!=tgt).long().sum()

train_input, train_target = generate_disc_set(1000)
test_input, test_target = generate_disc_set(1000)

train_target_hot = conv_to_one_hot(train_target)

num_hidden = 3
weight_init ='uniform_pos_neg'
bias_init='uniform_pos_neg'
layers = []
linear = Linear(2, 25, weight_init=weight_init, bias_init=bias_init)
layers.append(linear)
layers.append(Tanh())
for i in range(num_hidden-1):
	layers.append(Linear(25, 25, weight_init=weight_init, bias_init=bias_init))
	layers.append(Tanh())
layers.append(Linear(25, 2, weight_init=weight_init, bias_init=bias_init))


net_2layer = Network(layers, train_input.shape[0])

mse = MSE()


lr = 1e-3
num_iter = 1000

timesteps = []
loss_at_timesteps = []

for it in range(num_iter):
	
	net_2layer.zero_grad()
	'''
	for layer in net_2layer.layers:
		print([par.size() for par in layer.param()])
	'''
	pred_2layer = net_2layer.forward(train_input.view(-1, train_input.shape[0]))
	
	
	#print("shape of pred layer", pred_2layer.shape)
	loss = mse.forward(pred_2layer, train_target_hot.t())
	print("At iteration ", str(it), " the loss is ", loss)
	loss_grad = mse.backward()
	net_2layer.backward(loss_grad)
	net_2layer.grad_step(lr=lr)
	timesteps.append(it)
	loss_at_timesteps.append(loss)


final_pred_train = net_2layer.forward(train_input.view(-1, train_input.shape[0]))
print('Number of training errors:')
print(compute_nb_errors(final_pred_train.max(0)[1], train_target))

final_pred_test = net_2layer.forward(test_input.view(-1, test_input.shape[0]))
print('Number of test errors:')
print(compute_nb_errors(final_pred_test.max(0)[1], test_target))


fig, ax = plt.subplots()
ax.plot(timesteps, loss_at_timesteps)

ax.set(xlabel='iteration (s)', ylabel='Training Loss',
	title='The Loss curve')
ax.grid()

fig.savefig("test.png")
plt.show()
