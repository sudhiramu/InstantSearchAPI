from flask import Flask, Response, render_template, request, jsonify
import json
import csv
from wtforms import TextField, Form
app = Flask(__name__)
# change file path here
f = open("data.csv",encoding='utf-8')
reader = csv.reader(f)
res=[]
for line in reader:
	for item in line:
		res.append(' '.join(line))
result=list(set(res))

class SearchForm(Form):
	autocomp = TextField('Insert Name', id='name_autocomplete')


@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
	return Response(json.dumps(result), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def index():
	form = SearchForm(request.form)
	return render_template("search.html", form=form)

@app.route("/api/search/<string:name>")
def flight_api(name):
	"""Return details about a single flight."""
	names=[]
	for item in result:
		size=len(item.split())
		if name in item:
			dict={}
			dict["name"]=item.split()[0]
			if(size>2):
				dict["middle name"]=item.split()[1]
				dict["surname"]=item.split()[2]
			elif(size>1):
				dict["middle name"]=item.split()[1]
				dict["surname"]=""
			else:
				dict["middle name"]=""
				dict["surname"]=""
			names.append(dict)
			
	# Make sure flight exists.
	return jsonify(names)

if __name__ == '__main__':
	app.run(debug=True)
