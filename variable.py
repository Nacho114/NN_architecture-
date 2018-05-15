from torch import Tensor

class Variable():

	def __init__(self, x):
		super(Variable, self).__init__()
		self.data = x
		self.grad = Tensor(x.shape)
		self.requires_grad = True
		self.shape = x.shape

	def __repr__(self):
		return "nnlib Variable containing \n" + self.data.__repr__()
	
	def __str__(self):
		return "nnlib Variable containing \n" + self.data.__str__()

if __name__ == '__main__':
	x = Tensor([1, 2, 3])
	var = Variable(x)
	print(var)
	print(var.data.shape)
	print(var.shape)
	print(var.grad)
