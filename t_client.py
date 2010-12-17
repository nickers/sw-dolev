from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, protocol
import pickle, base64
from node import *
from algo import algo

host = "localhost"
port = 8007
STEP_TIME = 5

node = NodeState()

def algo_schedule():
    algo(node.id, node)
    reactor.callLater(STEP_TIME, algo_schedule)

class CommunicationClient(LineReceiver):

    def __init__(self):
	node.com = self

    def lineReceived(self, line):
	m = pickle.loads(base64.b64decode(line))
	func = m[0]
	func(node, m[1])
#	reactor.callLater(1, algo_schedule)
	#algo(node.id,node)
	

    def connectionMade(self):
	reactor.callLater(STEP_TIME, algo_schedule)
	LineReceiver.connectionMade(self)
	print "Connection made..."

    def connectionLost(self, reason):
	LineReceiver.connectionLost(self, reason)
	print "Lost: ", reason
	reactor.stop()

    def set_node(self, n):
	self.node = n

class DolevClientFactory(protocol.ClientFactory):
    protocol = CommunicationClient

if __name__ == '__main__':
    f = DolevClientFactory()
    reactor.connectTCP(host, port, f)
    reactor.run()
