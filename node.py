import pickle, base64

class NodeState(object):
    def __init__(self):
        self.id = -1
        self.ready = False
	self.neighbours = []
	self.registers = {}
	self.root = -1

    def send(self, proc, msg, data):
	self.com.sendLine(base64.b64encode(pickle.dumps((proc,msg,data))))

    def write(self, j, v):
#	print "write: ", j, v
	self.send(j, msg_write_reg, (self.id,v))

    def read(self, j):
	try:
		return self.registers[j]
	except:
	    return None


def msg_graph_give(node, data):
    node.neighbours = data['neighbours']
    node.ready = True
    node.id = data['id']
    print "Graph:",data

def msg_write_reg(node, data):
#    print "msg_write", data
    node.registers[data[0]] = data[1]
    
    
