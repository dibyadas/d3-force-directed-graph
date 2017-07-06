from flask import Flask, redirect, url_for, request, render_template,json
import os
import pickle
import networkx as nx
import community

UPLOAD_FOLDER = 'uploaded_files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def default_view():
	json_node = [
		{"id" : "1" , "group" : 1},
		{"id" : "2" , "group" : 1},
		{"id" : "3" , "group" : 1}
		# {id : "4" , group : 1},
		# {id : "5" , group : 1}
	]
	json_link = [
		{"target": "2", "strength": 1,"source": "1"},
    	{"source": "2", "target": "3", "strength": 8}
    	# {source: "3", target: "9", strength: 10},
   	 # 	{source: "4", target: "8", strength: 6},
    	# {source: "5", target: "7", strength: 1}
	]
	return render_template('for.html',json_link = json_link,json_node =json_node,text = '')

@app.route('/preset',methods=['POST'])
def preset():
	text = request.form['text']
	flag = request.form['flag']
	with open('presets/'+text+'/'+flag+'detected_'+text+'_'+'nodes','rb') as f:
		json_node = pickle.load(f)
	with open('presets/'+text+'/'+flag+'detected_'+text+'_'+'links','rb') as f:
		json_link = pickle.load(f)
	return render_template('for.html',json_link=json_link,json_node=json_node,text=text)


@app.route('/detect',methods=['POST'])
def detect():

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

	return render_template('for.html',json_link=json_link,json_node=json_node)

@app.route('/upload',methods=['POST'])
def upload():
	file = request.files['file']
	print(os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), file.filename))
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
	return 'file uploaded successfully'
	




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9090))
    app.run(host='localhost', port=port,debug=True)