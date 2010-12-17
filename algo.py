from node import NodeState

def algo(n, node):
    if n==0:
	for n in node.neighbours:
	    node.write(n, (0,0))
    else:
	new_root = -1
	l = {}
	for m in node.neighbours:
	    x = node.read(m) 
	    if x!=None: l[m] = x

	found = False
	dist = min(l,key=lambda i:l[i][1])
	dist = l[dist][1]+1

	for m in node.neighbours:
	    if (not found) and (m in l) and (l[m][1] == dist-1):
		node.write(m, (1,dist))
		found = True
		new_root = m
	    else:
		node.write(m, (0,dist))
	if found and new_root!=node.root:
	    print "#%d has new root: %d"%(node.id, new_root)
	    node.root = new_root

