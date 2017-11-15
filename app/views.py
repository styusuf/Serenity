from app import app
from .forms import SearchForm, LoginForm
from flask import render_template, flash, redirect
from .CheckUser import User



@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = SearchForm()
	if form.validate_on_submit():
		flash('Ingredients requested = %s' % (form.ingredients.data))
		return redirect('/searchresults')
	return render_template('index.html',
							title='Serenity',
							form=form)

@app.route('/searchresults', methods=['GET', 'POST'])
def searchResults():
	form = SearchForm()
	if form.validate_on_submit():
		flash('Ingredients requested = %s' % (form.ingredients.data))
		return redirect('/searchresults')
	return render_template('searchresults.html',
							title='Serenity',
							form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User(form.username.data, form.password.data)
		if user.verify():
			return redirect('/index')
		else:
			flash('Login failed!')
			return redirect('/login')
	return render_template('login.html',
							title="Serenity",
							form=form)



