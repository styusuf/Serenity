from app import app
from .forms import SearchForm, LoginForm
from flask import render_template, flash, redirect, url_for, request
from .CheckUser import User
from .setup import searchRecipes, createGlobals

[dbi, ingredient_info, rank, qa] = createGlobals()

def displaySearchResults(data):
    ingredients_ids = [int(a) for a in data.split(',')]
    return searchRecipes(ingredients_ids, dbi, ingredient_info, rank, qa)

@app.route('/', methods=['GET','POST'])
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

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        ingredients = form.ingredients.data
        return redirect(url_for('searchResults', q=ingredients))
    return render_template('index.html',
                            title='Serenity',
                            form=form)

@app.route('/searchresults', methods=['GET', 'POST'])
def searchResults():
    form = SearchForm()
    ingredients = request.args.get('q')
    recipes = displaySearchResults(ingredients)
    if form.validate_on_submit():
        ingredients = form.ingredients.data
        return redirect(url_for('searchResults', q=ingredients))
    return render_template('searchresults.html',
                            title='Serenity',
                            form=form,
                            recipes=recipes)





