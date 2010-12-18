from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from node import *
import random, base64, pickle



class NodesList(object):
	def __init__(self, n):
		self.amount = n
		self.available = [i for i in range(n)]
		self.nodes = {}
	self.graph = []

	def add_client(self, c):
		i = random.choice(self.available)
		self.available.remove(i)
		self.nodes[i] = c

	def del_client(self, c):
		for x in self.nodes:
			if self.nodes[x] == c:
				del self.nodes[x]
				self.available.append(x)
				return

	def generate_graph(self):
		n = self.amount
		self.graph = [[] for i in range(n)]
		for i in range(n):
			tmp = [x for x in range(n) if x not in self.graph[i] and x!=i]
			cnt = (n/2)+1 - len(self.graph[i])
			##print i, tmp, cnt
			l = random.sample(tmp, cnt)
			self.graph[i].extend(l)
			for x in l:
				self.graph[x].append(i)
		for l in self.graph:
			l.sort()

import sys
N = int(sys.argv[1])
nodes = NodesList(N)
nodes.generate_graph()
for i in range(len(nodes.graph)):
	for l in nodes.graph[i]:
		print i, "--", l, ";"

class CommunicationServer(object):
	def __init__(self):
		self.clients = {}
		self.queue = {}

	def add_client(self, c):
		i = 0
		while i in self.clients:
			i += 1
		self.clients[i] = c
		return i

	def del_client(self, c):
		for i in self.clients:
			if self.clients[i]==c:
				del self.clients[i]
				return

	def requeue(self, i):
		if i in self.queue:
			for m in self.queue[i]:
				print 'Requeue', m
				self.send_msg(m)
			del self.queue[i]


	def send_msg(self, m):
		m2 = pickle.loads(base64.b64decode(m))
		addr =  m2[0]
		msg = (m2[1],m2[2])
		print addr, msg
		if addr in self.clients:
			self.clients[addr].sendLine(base64.b64encode(pickle.dumps(msg)))
		else:
			if addr not in self.queue:
				self.queue[addr] = []
			self.queue[addr].append(m)

	def send_raw_msg(self, id, msg, data):
		self.clients[id].sendLine(base64.b64encode(pickle.dumps((msg,data))))


serv = CommunicationServer()

class DolevProtocol(LineReceiver):

	def __init__(self):
		self.clients = {}

	def connectionMade(self):
		# self.sendLine("client connected") 
		id = serv.add_client(self)
		data = {'id':id, 'neighbours':nodes.graph[id]}
		print "client connected:", data
		serv.send_raw_msg(id, msg_graph_give, data) 
		serv.requeue(id)

	def connectionLost(self, reason):
		print "client lost"
		serv.del_client(self)

	def lineReceived(self, line):
		serv.send_msg(line)

# Next lines are magic:
factory = Factory()
factory.protocol = DolevProtocol

# 8007 is the port you want to run under. Choose something >1024
reactor.listenTCP(8007, factory)
reactor.run()

