__author__ = 'nickers'
from communication import Registry
import sys, random


if len(sys.argv)!=2:
	print "Usage: %s <nodes_count>"%(sys.argv[0])
	exit(1)

def gen_graph(N):
	graph = [[] for i in range(N)]
	d = N/2 + 1
	for p in range(N):
		nodes = [i for i in range(N)]
		while len(graph[p])<d:
			c = random.choice(nodes)
			nodes.remove(c)
			if (c not in graph[p]) and (c!=p):
				graph[p].append(c)
				graph[c].append(p)

	return graph


N = int(sys.argv[1])
#reg = Registry()

# rysuj graf
g = gen_graph(N)

for src in range(N):
	for dst in g[src]:
		if dst>src:
			print src, '->', dst, '[color=grey,dir=none];'
			# dorysuj krawedz drzewa (pogrubione)
			if random.randint(0,1)==1:
				print src, '->', dst, '[color=red, style=bold, weight=100];'


while True:
	for i in g[0]:
		reg.write(i, (0,0))