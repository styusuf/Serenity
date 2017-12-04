from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired

class SearchForm(Form):
	ingredients = StringField('ingredients', validators=[DataRequired()])

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])