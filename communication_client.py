# -*- coding: utf-8 -*-
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
import pickle, base64


def get_communication_client(node, on_connection):
	"""
		Return class but with given params.
	"""

	class CommunicationClient(LineReceiver):
		"""
			Class for communication between clients.
		"""
	
		def __init__(self):
			self.__set_node(node)
	
		def lineReceived(self, line):
			m = pickle.loads(base64.b64decode(line))
			func = pickle.loads(m[0])
			reactor.callLater(1, lambda: func(node, m[1]))
			#func = m[0]
			#func(node, m[1])
	
		def connectionMade(self):
			""" Initialize connection """
			LineReceiver.connectionMade(self)
			#reactor.callLater(0, algo_schedule)
			on_connection()
			print "Connection made..."
	
		def connectionLost(self, reason):
			""" ups... stop reactor """
			LineReceiver.connectionLost(self, reason)
			print "Connection lost: ", reason.getErrorMessage()
			try:
				reactor.stop()
			except ReactorNotRunning:
				print " - reactor not running, so we are not stopping it" 
	
		def __set_node(self, n):
			"""
			Sets node data for use with functions retrieved by 
			network (packed in messages). 
			"""
			self.node = n
			self.node.com = self

	return CommunicationClient