from flask import Flask
from flask import render_template
app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
@app.route('/index')
def hello():
	model = {
		'title' : 'Home'
	}
	return render_template('index.html', model = model)

@app.route("/datasets")
def files():
	model = {
		'title' : 'Datasets'
	}
	return render_template('datasets.html', model = model)

@app.route('/dataset')
def file():
	model = {
		'title': 'Dataset'
	}
	return render_template('dataset.html', model = model)

@app.route('/about')
def about():
	model = {
		'title' : 'About us'
	}
	return render_template('base.html', model = model)

@app.route('/contacts')
def contacts():
	model = {
		'title' : 'Contacts'
	}
	return render_template('base.html', model = model)
