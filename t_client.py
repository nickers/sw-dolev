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
		None

	def lineReceived(self, line):
		m = pickle.loads(base64.b64decode(line))
		func = m[0]
		func(node, m[1])
		#reactor.callLater(1, algo_schedule)
		#algo(node.id,node)

	def connectionMade(self):
		""" Initialize connection """
		LineReceiver.connectionMade(self)
		reactor.callLater(STEP_TIME, algo_schedule)
		print "Connection made..."

	def connectionLost(self, reason):
		""" ups... stop reactor """
		LineReceiver.connectionLost(self, reason)
		print "Connection lost: ", reason
		reactor.stop()

	def set_node(self, n):
		"""
		Sets node data for use with functions retrieved by 
		network (packed in messages). 
		"""
		self.node = n
		self.node.com = self

class DolevClientFactory(protocol.ClientFactory):
	protocol = CommunicationClient

if __name__ == '__main__':
	f = DolevClientFactory()
	reactor.connectTCP(host, port, f)
	reactor.run()
