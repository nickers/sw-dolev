__author__ = 'nickers'

class Registry(object):

	def __init__(self):
		self.registry = {}

	def read(self, k):
		return self.registry[k]

	def write(self, k, v):
		self.registry[k] = v
  