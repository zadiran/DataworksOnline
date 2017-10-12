from flask_wtf import Form
from wtforms import FileField, BooleanField, TextField, PasswordField
from wtforms.validators import Required, Length, Email

class FileUploadForm(Form):
	fileName = FileField('fileName', validators = [Required()])

class LoginForm(Form):
	login = TextField('login', validators = [Required()])
	password = PasswordField('password', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

class RegistrationForm(Form):
	login = TextField('login', validators = [Required(), Length(min = 4, max = 20)])
	email = TextField('email', validators = [Required(), Email(), Length(max = 50)])
	password = PasswordField('password', validators = [Required(), Length(min = 6, max = 20)])
	password_confirmation = PasswordField('password_confirmation', validators = [Required(), Length(min = 6, max = 20)])
