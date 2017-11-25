from app import app
from .forms import SearchForm, LoginForm
from flask import render_template, flash, redirect, url_for, request, session
from .CheckUser import User
from .setup import searchRecipes, createGlobals


[dbi, ingredient_info, group_info, rank, qa] = createGlobals()

def displaySearchResults(data):
    ingredients_ids = [int(a) for a in data.split(',')]
    return searchRecipes(ingredients_ids, dbi, ingredient_info, group_info, rank, qa)

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        if user.verify():
            session['logged_in'] = True
            return redirect('/index')
        else:
            flash('Login failed!')
            return redirect('/login')
    return render_template('login.html',
                            title="Serenity",
                           form=form)

@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
        form = LoginForm()
        return redirect('/login')
    else:
        flash('Please Login first')
        return redirect('/login')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if session.get('logged_in'):
        form = SearchForm()
        if form.validate_on_submit():
            ingredients = form.ingredients.data
            return redirect(url_for('searchResults', q=ingredients))
        return render_template('index.html',
                                title='Serenity',
                                form=form)
    else:
        # form = LoginForm()
        flash('Please Login First!')
        return redirect('/login')
        # return render_template('login.html',
        #                        title="Serenity",
        #                        form=form)

@app.route('/searchresults', methods=['GET', 'POST'])
def searchResults():
    if session.get('logged_in'):
        form = SearchForm()
        ingredients = request.args.get('q')
        recipes = displaySearchResults(ingredients)

        # Get dish types of recipes
        dish_types = []
        for recipe in recipes:
            for d_type in recipe.dishTypes:
                if d_type not in dish_types:
                    dish_types.append(d_type)
        dish_dict = {} # Dictionary of dishtype as key and recipe ids of recipes with that dishtype as values
        for d_type in dish_types:
            dish_dict[d_type] = []

        for d_type in dish_types:
            for recipe in recipes:
                if d_type in recipe.dishTypes:
                    dish_dict[d_type].append(recipe.id)

        dish_dict = {k.title(): v for k, v in dish_dict.items()} # Update dish_type string to be title format

        if form.validate_on_submit():
            ingredients = form.ingredients.data
            return redirect(url_for('searchResults', q=ingredients))
        return render_template('searchresults.html',
                                title='Serenity',
                                form=form,
                                recipes=recipes,
                                ingredients=ingredients,
                                dish_dict = dish_dict)
    else:
        # form = LoginForm()
        flash('Please Login First!')
        return redirect('/login')
        # return render_template('login.html',
        #                        title="Serenity",
                               # form=form)






