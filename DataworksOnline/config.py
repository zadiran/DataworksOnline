import os
import uuid

class Config():
	CSRF_ENABLED = True
	SECRET_KEY = str(uuid.uuid4())
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/DataworksOnline'