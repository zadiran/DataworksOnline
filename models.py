from main import db, lm
from flask_login import UserMixin

class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	username = db.Column(db.String(), nullable=False, unique = True)
	email = db.Column(db.String(), nullable=False, unique = True)
	password = db.Column(db.String(), nullable=False)
	creation_date = db.Column(db.DateTime(), nullable = False)

	datasets = db.relationship('Dataset', backref = 'user', lazy = 'dynamic')

	def __init__(self, username, email, password, creation_date):
		self.username = username
		self.email = email
		self.password = password
		self.creation_date = creation_date

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class Dataset(db.Model):
	__tablename__ = 'datasets'

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	filename = db.Column(db.String(), nullable=False)
	guid = db.Column(db.String(), nullable=False, unique = True)
	upload_date = db.Column(db.DateTime(), nullable = False)

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __init__(self, filename, guid, user, upload_date):
		self.filename = filename
		self.guid = guid
		self.user_id = user.id
		self.upload_date = upload_date

