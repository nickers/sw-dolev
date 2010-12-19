# -*- coding: utf-8 -*-
from twisted.internet import reactor, protocol
from node import *
from communication_client import get_communication_client
import pickle, base64, sys

host = "localhost"
port = 8007
STEP_TIME = 1

DO_PROBLEMS = False

for a in sys.argv: 
	if a == "--dirty": DO_PROBLEMS = True

target_filename = './graph_clean.txt'
if DO_PROBLEMS:
	target_filename = './graph_dirty.txt'


node = NodeState()

def make_problems():
	print "Generating random problems in network."
	node.send(0, displ, "@nic takiego@")
	print "POMIDOR! :D"

def wait_full_state(node,data):
	"""
	Stops this nodes reactor when whole graph was received.
	"""
	if len(node.roots)>=node.id:
		reactor.stop()
	else:
		reactor.callLater(0, lambda:wait_full_state(node,data))

def generate_start_graph(node,data):
	return
	out = file("./graph_empty.txt", "wb+")
	out.write("digraph start{\n")
	for src in range(len(node.neighbours)):
		for dst in node.neighbours[src]:
			if dst > src:
				out.write("\t%d -> %d [color=grey,dir=none];\n"%(src,dst))
	out.write("}")
	out.close()

	
def get_state():
	"""
	Request current tree from network.
	
	Before sending request wait until node is fully initialized. 
	"""
	if node.id<0:
		reactor.callLater(0, get_state)
		return
	node.send(node.id, generate_start_graph, None)
	node.target_filename = target_filename
	node.roots = {}
	for i in range(0,node.id):
		node.send(i, msg_get_connections, node.id)
	node.send(node.id, wait_full_state, 0)

class DolevClientFactory(protocol.ClientFactory):
	"""
	Needed for twister reactor.
	"""
	#protocol = CommunicationClient
	protocol = get_communication_client(node, lambda:reactor.callLater(0, get_state))


if __name__ == '__main__':
	try:
		f = DolevClientFactory()
		reactor.connectTCP(host, port, f)
		reactor.run()
	except:
		None
