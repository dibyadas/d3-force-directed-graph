import networkx as nx
import community
import pickle

# with open('karate.edgelist.txt','r') as f:
# 	temp = f.read()
# 	edgelist = temp.split('\n')
# 	nodes = []
# 	for i in temp.replace('\n',' ').split(' '):
# 		if i not in nodes:
# 			nodes.append(i)
nodes = []

with open('node','rb') as f:
	node2 = pickle.load(f)
	for i in node2:
		nodes.append(i['id'])

edges = []

with open('link','rb') as f:
	edge2 = pickle.load(f)
	for i in edge2:
		edges.append((i['source'],i['target']))


G = nx.Graph()

# edges = [(s.split(' ')[0],s.split(' ')[1]) for s in edgelist]

G.add_nodes_from(nodes)

G.add_edges_from(edges)

partition = community.best_partition(G)

# print(partition)

comm_node = []

for i in partition:
	t = {'id':i,'group':partition[i]}
	comm_node.append(t)

with open('nodes_community_football','wb') as f:
	pickle.dump(comm_node,f)

# json_link = []
# for i in edgelist:
# 	s = i.split(' ')
# 	try:
# 		y = {'source':s[0],'target':s[1],'strength':1}
# 	except IndexError:
# 		print(s)
# 	json_link.append(y)

with open('links_community_football','wb') as f:
	pickle.dump(edge2,f)

