# -*- coding: utf-8 -*-
from twisted.internet import reactor, protocol
from node import *
from algo import algo
from communication_client import get_communication_client

host = "localhost"
port = 8007
STEP_TIME = 1

node = NodeState()

def algo_schedule():
	"""
		Execute algorithm step and schedule next for execution in future.
	"""
	algo(node.id, node)
	reactor.callLater(STEP_TIME, algo_schedule)

class DolevClientFactory(protocol.ClientFactory):
	"""
		Needed for twister reactor.
	"""
	#protocol = CommunicationClient
	protocol = get_communication_client(node, lambda:reactor.callLater(STEP_TIME, algo_schedule))

if __name__ == '__main__':
	f = DolevClientFactory()
	reactor.connectTCP(host, port, f)
	reactor.run()
