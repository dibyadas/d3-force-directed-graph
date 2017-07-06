from flask import Flask, redirect, url_for, request, render_template,json
import os
import pickle

app = Flask(__name__)


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
	# with open('karate.edgelist.txt','r') as f:
	# 	temp = f.read()
	# 	edgelist = temp.split('\n')
	# 	nodes = []
	# 	for i in temp.replace('\n',' ').split(' '):
	# 		if i not in nodes:
	# 			nodes.append(i)

	# 	json_node = []
	# 	for i in nodes:
	# 		t = {'id' : i, 'group' : 1}
	# 		json_node.append(t)

	# 	json_link = []
	# 	for i in edgelist:
	# 		s = i.split(' ')
	# 		# y = {"source":"1","target":"2","strength":1}
	# 		try:
	# 			y = {'source':s[0],'target':s[1],'strength':1}
	# 		except IndexError:
	# 			print(s)
	# 		json_link.append(y)
	# with open('undetected_karate_links','wb') as f:
	# 	pickle.dump(json_link,f)
	# with open('undetected_karate_nodes','wb') as f:
	# 	pickle.dump(json_node,f)
	text = request.form['text']
	flag = request.form['flag']
	with open('presets/'+text+'/'+flag+'detected_'+text+'_'+'nodes','rb') as f:
		json_node = pickle.load(f)
	with open('presets/'+text+'/'+flag+'detected_'+text+'_'+'links','rb') as f:
		json_link = pickle.load(f)
	return render_template('for.html',json_link=json_link,json_node=json_node,text=text)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9090))
    app.run(host='localhost', port=port,debug=True)