from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, protocol

host = "localhost"
port = 8007

class CommunicationClient(LineReceiver):
    def __init__(self):
	None

    def lineReceived(self, line):
	print "Line: [", line, "]"


    def connectionMade(self):
	LineReceiver.connectionMade(self)
	print "Connection made..."

    def connectionLost(self, reason):
	LineReceiver.connectionLost(self, reason)
	print "Lost: ", reason

class DolevClientFactory(protocol.ClientFactory):
    protocol = CommunicationClient
    

if __name__ == '__main__':
    f = DolevClientFactory()
    reactor.connectTCP(host, port, f)
    reactor.run()
