__author__ = 'nickers'

import sys, socket

HOST = ''
PORT = 2206

if len(sys.argv)!=2:
	print "Usage: %s <nodes_amount>"%sys.argv[0]
	exit(1)


try:
	N = int(sys.argv[1])
	if (N<=0):
		raise ValueError()
except ValueError:
	print "Error: Invalid nodes amount. Please give valid integer number >0."
	exit(2)

print "Avaiting clients at port %d"%PORT
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(N)

