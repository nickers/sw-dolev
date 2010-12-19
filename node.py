# -*- coding: utf-8 -*-
import pickle, base64
from twisted.internet import reactor, protocol

class NodeState(object):
	def __init__(self):
		self.id = -1
		self.ready = False
		self.neighbours = []
		self.registers = {}
		self.root = -1

	def send(self, proc, msg, data):
		self.com.sendLine(base64.b64encode(pickle.dumps((proc,pickle.dumps(msg),data))))

	def write(self, j, v):
		self.send(j, msg_write_reg, (self.id,v))

	def read(self, j):
		try:
			return self.registers[j]
		except:
			return None


def msg_graph_give(node, data):
	node.neighbours = data['neighbours']
	node.ready = True
	node.id = data['id']
	print "Graph:", data, node.id

def msg_write_reg(node, data):
	#    print "msg_write", data
	node.registers[data[0]] = data[1]

###################################
def msg_get_connections(node, source_id):
	"""
		Request for root node ID.
	"""
	print "Wyslano zapytanie z '%d'"%source_id
	node.send(source_id, msg_set_connections, ((node.id,node.root), node.read(node.root), node.neighbours) )

def msg_set_connections(node, data):
	"""
		Response for msg_get_connections() - writes dot-formated graph with
		neighbours connections and spanning tree.
	"""
	# TODO dodać wysyłanie odległości i rysowanie jej przy krawędziach
	if len(node.roots) == 0:
		node.output = file(node.target_filename, "wb+")
		node.output.write("digraph result{\n")
	if data[0][1] != -1:
		node.output.write("\t%d -> %d [color=red,label=\"dist:%d\"];\n"%(data[0][0],data[0][1],data[1][1]))
	node.roots[data[0][0]] = data[0][1]
	for x in data[2]:
		if x > data[0][0]:
			node.output.write("\t%d -> %d [color=grey,dir=none];\n"%(data[0][0],x))
	if len(node.roots) >= node.id:
		node.output.write("}")
		node.output.close()
