import os
import uuid
import datetime
from main import app, db, lm
from models import Dataset, User
from flask import render_template, flash, redirect, url_for, session, g, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import FileUploadForm, LoginForm, RegistrationForm

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
	datasets = Dataset.query.filter(Dataset.id != 50).all()
	model = {
		'title': 'Datasets',
		'msg' : 'Upload file',
		'datasets' : datasets
	}
	form = FileUploadForm()
	if form.validate_on_submit():
		files_folder = 'files'
		dsFile = form.fileName.data

		filename = secure_filename(dsFile.filename)
		guid = str(uuid.uuid4())

		dsFile.save(os.path.join(app.config['BASEDIR'], files_folder, guid))

		dbDs = Dataset(filename, guid, g.user, datetime.datetime.utcnow())

		db.session.add(dbDs)
		db.session.commit()

		model['msg'] = secure_filename(dsFile.filename)
	
	model['form'] = form
	return render_template('datasets.html', model = model)


@app.route('/dataset/<dsId>')
def dataset(dsId):
	ds = Dataset.query.get(dsId);
	print(str(ds))
	if(ds is None):
		return 'aaaa'
	model = {
		'title' : 'Dataset' + str(dsId),
		'filename' : ds.filename 
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

##### end of authorization