import os
import io
import uuid
import datetime
import json
from main import app, db, lm
from models import Dataset, User
from flask import render_template, flash, redirect, url_for, session, g, request, send_file, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import FileUploadForm, LoginForm, RegistrationForm
from datautil import get_parsed_file
import forecast

@app.before_request
def before_request():
	g.user = current_user
	
@app.route('/')
@app.route('/index')
def index():
	model = {
		'title' : 'Home'
	}
	return render_template('index.html', model = model)

@app.route("/datasets", methods = ['GET', 'POST'])
def datasets():
	if not current_user.is_authenticated:
		return redirect(url_for('no_access'))

	datasets = Dataset.query.filter(Dataset.user_id == current_user.id).all()

	for ds in datasets:
		ds.distinctive_name = ds.distinctive_name or ds.filename
		if ds.distinctive_name == ds.filename:
			ds.display_filename = ''
		else: 
			ds.display_filename = ds.filename
			
	model = {
		'title': 'Datasets',
		'datasets': datasets
	}
	form = FileUploadForm()
	if form.validate_on_submit():

		dsFile = form.fileName.data

		separator = form.separator.data
		distinctive_name = form.distinctive_name.data

		filename = secure_filename(dsFile.filename)
		guid = str(uuid.uuid4())
		
		dsFile.seek(0)
		dt = dsFile.read()
		
		dbDs = Dataset(filename, guid, g.user, datetime.datetime.utcnow(), separator, distinctive_name, dt)
		
		db.session.add(dbDs)
		db.session.commit()
		return redirect(url_for('datasets'))
	
	model['form'] = form

	return render_template('datasets.html', model = model)

@app.route('/dataset/<dsId>', defaults = { 'pgId': 1})
@app.route('/dataset/<dsId>/<pgId>')
def dataset(dsId, pgId):
	if not current_user.is_authenticated:
		return redirect(url_for('no_access'))

	ds = Dataset.query.get(dsId)

	if ds is None or ds is not None and ds.user.id is not current_user.id:
		return redirect(url_for('no_access'))
	
	if ds.distinctive_name is None:
		ds.distinctive_name = ds.filename
		
	pf = get_parsed_file(ds.data, ds.separator);
	pf['minlen'] = int(len(pf['data']) / 2)
	pf['maxlen'] = len(pf['data'])
	model = {
		'title' : 'Dataset',
		'dataset' :  pf,
		'file' : ds ,
		'page' : pgId
	}
	return render_template('dataset' + str(pgId) + '.html', model = model)

@app.route('/download/dataset/<datasetId>')
def download_dataset(datasetId):
	
	if not current_user.is_authenticated:
		return redirect(url_for('no_access'))
	
	dataset = Dataset.query.get(datasetId)

	if dataset.user.id != current_user.id:
		return redirect(url_for('no_access'))

	return send_file(io.BytesIO(dataset.data),
                     attachment_filename=dataset.filename,
					 mimetype='application/octet-stream',
					 as_attachment=True) 

@app.route('/delete/dataset/<datasetId>')
def delete_dataset(datasetId):
	if not current_user.is_authenticated:
		return redirect(url_for('no_access'))
	
	dataset = Dataset.query.get(datasetId)

	if dataset.user.id != current_user.id:
		return redirect(url_for('no_access'))

	Dataset.query.filter_by(id=datasetId).delete()
	db.session.commit()

	return redirect(url_for('datasets'))

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


####### authorization

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		login = form.login.data
		password = form.password.data
		remember_me = form.remember_me.data

		user = User.query.filter(User.username == login).filter(User.password == password).first()
		
		if user is not None:
			login_user(user, remember_me)
			return redirect(url_for('index'))
		else:
			flash('Invalid login or password. Please, try again')

	model = {
		'title' : 'Sign In',
		'form' : form
	}
	return render_template('login.html', 
		model = model)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	model = {
		'title': 'Registration'
	}
	form = RegistrationForm()
	if form.validate_on_submit():

		login = form.login.data
		email = form.email.data
		password = form.password.data
		password_confirmation = form.password_confirmation.data

		can_create = True
		if	password != password_confirmation:
			flash('Password and its confirmation should match each other')
			can_create = False
		
		probably_existing_user = User.query.filter(User.email == email).first()
		if probably_existing_user is not None:
			flash('User with email ' + email + ' already exists')
			can_create = False

		probably_existing_user = User.query.filter(User.username == login).first()
		if probably_existing_user is not None:
			flash('User with nickname "' + login + '" already exists')
			can_create = False

		if can_create:
			user = User(login, email, password, datetime.datetime.utcnow())

			db.session.add(user)
			db.session.commit()

			login_user(user)
			return redirect(url_for('index'))

	model['form'] = form
	return render_template('registration.html', model = model)

@app.route('/user', defaults = { 'userId' : -1 })
@app.route('/user/<userId>')
def user(userId):

	if not current_user.is_authenticated:
		return redirect(url_for('no_access'))

	fixedUserId = current_user.id if userId is -1 else userId
	requested_user = User.query.filter(User.id == fixedUserId).first()
	
	if requested_user is None or requested_user is not None and requested_user.id is not current_user.id:
		return redirect(url_for('no_access'))

	model = {
		'title': 'User', 
		'user' : requested_user 
	}

	return render_template('user.html', model = model)

##### end of authorization

@app.route('/no_access')
def no_access():
	model = {
		'title' : 'Access denied'
	}
	return render_template('no_access.html', model = model)


@app.route('/get_data', methods = ['GET'])
def get_data():
	dataset = request.args.get('dataset', 0, type = int)
	horizon = request.args.get('horizon', 0, type = int)
	count = request.args.get('count', 0, type = int)
	forecast_model = request.args.get('forecast_model', 'Naive', type = str)
	outlier_detector = request.args.get('outlier_detector', '3sigma', type = str)

	result = forecast.forecast(dataset, 1, horizon, count, forecast_model, outlier_detector)

	output = []
	for x in range (0, len(result['data'])):
		output.append({
			'timestamp': result['timestamp'][x],
			'real': result['data'][x],
			'forecast': None, 
			'confidence_interval_upper': None,
			'confidence_interval_lower': None,
			'outlier': result['outlier'][x],
			'data_count': result['data_count'],
			'stop_condition': result['stop_condition']
		})

	output[-1]['forecast'] = output[-1]['real']
	output[-1]['confidence_interval_upper'] = output[-1]['real']
	output[-1]['confidence_interval_lower'] = output[-1]['real']

	for x in range(0, len(result['forecast'])):
		output.append({
			'timestamp': result['timestamp'][len(result['data']) + x],
			'real': None,
			'forecast': result['forecast'][x],
			'confidence_interval_upper': result['confidence_interval_upper'][x],
			'confidence_interval_lower': result['confidence_interval_lower'][x],
			'outlier': result['outlier'][len(result['data']) + x] ,
			'data_count': result['data_count'],
			'stop_condition': result['stop_condition']
		})
	return jsonify(output)