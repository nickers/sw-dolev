from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import random

class NodeState(object):
    def __init__(self, n):
        self.id = n
        self.ready = False

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
	    print i, tmp, cnt
	    l = random.sample(tmp, cnt)
	    self.graph[i].extend(l)
	    for x in l:
		self.graph[x].append(i)
	for l in self.graph:
	    l.sort()

n = NodesList(5)
n.generate_graph()
for i in range(len(n.graph)):
    for l in n.graph[i]:
	print i, "--", l, ";"
		
	

class DolevProtocol(LineReceiver):

    def connectionMade(self):
        self.sendLine("Ok, I am listening.") 
	

    def lineReceived(self, line):
	if line=="":
		self.sendLine("BYE!")
		self.transport.loseConnection()
	else:
		self.sendLine("Ok, line received: %s"%line)

# Next lines are magic:
factory = Factory()
factory.protocol = DolevProtocol

# 8007 is the port you want to run under. Choose something >1024
reactor.listenTCP(8007, factory)
reactor.run()

