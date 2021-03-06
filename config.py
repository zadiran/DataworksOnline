import os
import uuid

class Config():
	
	def __init__(self):
		pass

def configure_app(app):
	config = Config()
	
	configuration = os.environ.get('RUNNER', 'LOCAL')
	if configuration == 'LOCAL': # configuration for local runs
		config.SQLALCHEMY_DATABASE_URI = 'postgresql://Dataworks:1234@localhost/DataworksOnline'
		app.debug = True

	elif configuration == 'PRODUCTION': # run on server
		config.SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
	
	app.config.from_object(config)
	app.secret_key = str(uuid.uuid4())
	app.config['CSRF_ENABLED'] = True
	app.config['SESSION_TYPE'] = 'filesystem'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))