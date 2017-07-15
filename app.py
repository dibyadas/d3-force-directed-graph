from flask import Flask, redirect, url_for, request, render_template, send_from_directory
import json
import os
import pickle
import networkx as nx
import community
import re


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
	return render_template('for.html',json_link = json_link,json_node =json_node, graph_data=graph_data,detected='false')

@app.route('/preset',methods=['POST'])
def preset():
	text = request.form['text']
	flag = request.form['flag']
	with open('presets/'+text+'/'+flag+'detected_'+text+'_'+'nodes','rb') as f:
		json_node = pickle.load(f)
	with open('presets/'+text+'/'+flag+'detected_'+text+'_'+'links','rb') as f:
		json_link = pickle.load(f)
	graph_data = info(json_node,json_link)
	return render_template('for.html',json_link = json_link,json_node =json_node, graph_data=graph_data,detected='false')


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
		edges.append((i['source'],i['target']))

	G = nx.Graph()
	G.add_nodes_from(nodes)
	G.add_edges_from(edges)
	partition = community.best_partition(G)

	json_node = []
	for i in partition:
		json_node.append({'id': i ,'group': partition[i]})

	json_link = []
	for i in la:
		# json_link.append({'source':i['source']['id'],'target':i['target']['id'],'strength':1})
		json_link.append({'source':i['source'],'target':i['target'],'strength':1})
	graph_data = info(json_node,json_link)
	return render_template('for.html',json_link = json_link,json_node =json_node, graph_data=graph_data,detected='true')

@app.route('/upload',methods=['POST'])
def upload():
	file = request.files['file']
	try:
		t = file.read().decode('utf-8')
		file.close()

		nodes = []

		t = re.split(r"\n+",t)
		edges = []

		for i in t:
			try:
				s = re.sub(r"\t",' ',i)
				s = re.search(r"\d+[ \t]\d+",s)
				s = s.group().split(' ')
				edges.append((s[0],s[1]))
			except Exception as e:
				pass				

		for i in edges:
			for j in i:
				if j not in nodes:
					nodes.append(j)

		json_node = []
		json_link = []

		for i in nodes:
			json_node.append({'id':i,'group':1})

		for i in edges:
			try:
				json_link.append({'source':i[0],'target':i[1],'strength': 1})
			except Exception:
				pass
		

		# return detect(nodes,edges)
		graph_data = info(json_node,json_link)
		return render_template('for.html',json_link = json_link,json_node =json_node, graph_data=graph_data,detected='false')
	except Exception as e:
		# raise e from None
		# print(e)
		return "Unsuccessful"

@app.route('/download',methods=['POST'])
def download():
	na = json.loads(request.form['nodes'])
	
	groups = []
	for i in na:
		if i['group'] not in groups:
			groups.append(i['group'])

	no_of_groups = len(groups)

	template = "Number of community clusters found in the graph:- {} \n".format(no_of_groups)

	na.sort(key=lambda x:x['group'])

	with open('tmp/nodelist.txt','w') as f:
		f.write(template)
		f.write("\n")
		f.write("Node -- Group\n")
		f.write("-------------\n")
		for i in na:
			f.write(i['id']+"  --  "+str(i['group']))
			f.write("\n")
	return send_from_directory(directory="tmp", filename="nodelist.txt", as_attachment=True)

def info(json_node,json_link):
	nodes = []
	edges = []
	G = nx.Graph()

	for i in json_node:
		if i is "":
			print(i)
			raise Exception("here");
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