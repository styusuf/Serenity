from app import app
from .forms import SearchForm, LoginForm
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from .CheckUser import User
from .setup import searchRecipes, createGlobals
import json

[dbi, ingredient_info, group_info, rank, qa] = createGlobals()


def add_to_dict(dictionary, key, val):
    try:
        dictionary[key].append(val)
    except KeyError:
        dictionary[key] = [val]

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
        num_recipes = len(recipes)
        dish_types = dict()
        all_recipes = set([x.id for x in recipes])
        for recipe in recipes:
            for dish in recipe.dishTypes:
                add_to_dict(dish_types, dish, recipe.id)
            if recipe.isVegan:
                add_to_dict(dish_types, "vegan", recipe.id)
            if recipe.isVeg:
                add_to_dict(dish_types, "vegetarian", recipe.id)
            if recipe.isDairyFree:
                add_to_dict(dish_types, "dairy free", recipe.id)
            if recipe.isGlutenFree:
                add_to_dict(dish_types, "gluten free", recipe.id)
        for key in dish_types.keys():
            if len(dish_types[key]) == num_recipes:
                del dish_types[key]
        for key in dish_types.keys():
            set_a = set(dish_types[key])
            set_diff = all_recipes.difference(set_a)
            dish_types[key] = list(set_diff)
        if form.validate_on_submit():
            ingredients = form.ingredients.data
            return redirect(url_for('searchResults', q=ingredients))
        return render_template('searchresults.html',
                                title='Serenity',
                                form=form,
                                recipes=recipes,
                                ingredients=ingredients,
                                dish_types=dish_types)
    else:
        # form = LoginForm()
        flash('Please Login First!')
        return redirect('/login')
        # return render_template('login.html',
        #                        title="Serenity",
                               # form=form)






