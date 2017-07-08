from flask import Flask, redirect, url_for, request, render_template,json
import os
import pickle
import networkx as nx
import community


app = Flask(__name__)

@app.route('/')
def default_view():
	json_node = [
		{"id" : "1" , "group" : 1},
		{"id" : "2" , "group" : 1},
		{"id" : "3" , "group" : 1}
	]
	json_link = [
		{"target": "2", "strength": 1,"source": "1"},
    	{"source": "2", "target": "3", "strength": 8}
	]
	graph_data = info(json_node,json_link)
	return render_template('for.html',json_link = json_link,json_node =json_node, graph_data=graph_data)

@app.route('/preset',methods=['POST'])
def preset():
	text = request.form['text']
	flag = request.form['flag']
	with open('presets/'+text+'/'+flag+'detected_'+text+'_'+'nodes','rb') as f:
		json_node = pickle.load(f)
	with open('presets/'+text+'/'+flag+'detected_'+text+'_'+'links','rb') as f:
		json_link = pickle.load(f)
	graph_data = info(json_node,json_link)
	return render_template('for.html',json_link = json_link,json_node =json_node, graph_data=graph_data)


@app.route('/detect',methods=['POST'])
def detect(na=None,la=None):
	if na:
		pass
	else:
		na = json.loads(request.form['na'])
		la = json.loads(request.form['la'])
	
	nodes = []
	edges = []
	for i in na:
		nodes.append(i['id'])
	for i in la:
		edges.append((i['source']['id'],i['target']['id']))

	G = nx.Graph()
	G.add_nodes_from(nodes)
	G.add_edges_from(edges)
	partition = community.best_partition(G)

	json_node = []
	for i in partition:
		json_node.append({'id': i ,'group': partition[i]})

	json_link = []
	for i in la:
		json_link.append({'source':i['source']['id'],'target':i['target']['id'],'strength':1})

	graph_data = info(json_node,json_link)
	return render_template('for.html',json_link = json_link,json_node =json_node, graph_data=graph_data)

@app.route('/upload',methods=['POST'])
def upload():
	file = request.files['file']
	try:
		t = file.read().decode('utf-8')
		file.close()

		nodes = []

		edgelist = t.split('\n')
		for i in t.replace('\n',' ').split(' '):
			if i not in nodes:
				nodes.append(i)

		json_node = []
		json_link = []

		for i in nodes:
			json_node.append({'id':i,'group':1})

		for i in edgelist:
			s = i.split(' ')
			# edges.append({'source':{'id':s[0]},'target':{'id':s[1]}})
			json_link.append({'source':s[0],'target':s[1],'strength': 1})

		# return detect(nodes,edges)
		graph_data = info(json_node,json_link)
		return render_template('for.html',json_link = json_link,json_node =json_node, graph_data=graph_data)
	except Exception as e:
		raise e from None
		# print(e)
		return "Unsuccessful"

def info(json_node,json_link):
	nodes = []
	edges = []
	G = nx.Graph()

	for i in json_node:
		nodes.append(i['id'])

	for i in json_link:
		edges.append((i['source'],i['target']))

	G.add_nodes_from(nodes)
	G.add_edges_from(edges)
	degree_centrality = nx.degree_centrality(G)
	betweenness_centrality = nx.betweenness_centrality(G)
	clustering_coefficent = nx.clustering(G)
	return [degree_centrality,betweenness_centrality,clustering_coefficent]



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9090))
    app.run(host='0.0.0.0', port=port,debug=True)