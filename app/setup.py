from copy import copy
from DBInteract import DBInteract
from LookUpTables import create_ingredient_info, create_group_info
import numpy as np
from QueryAdjuster import QueryAdjuster
from Ranking import Ranking
import sys

def createGlobals():
    group_info, ingred_to_groups = create_group_info()
    dbi = DBInteract()
    ingredient_info = create_ingredient_info(ingred_to_groups)
    # del ingred_to_groups
    rank = Ranking(group_info)
    qa = QueryAdjuster()
    return [dbi, ingredient_info, group_info, rank, qa]

def searchRecipes(ingredient_list, dbi, ingredient_info, group_info, rank, qa):
    '''
    Returns the recipes for the given list of ingredients
    :param ingredient_list: list of all ingredients
    :return: list of ranked recipes
    '''
    # adj_ingredient_list = qa.get_adj_query(ingredient_list, ingredient_info)
    # adj_ingredient_list = ingredient_list
    # recipes = dbi.get_recipes(adj_ingredient_list, verbose=True)
    # ranked, scores = rank.rank_results(recipes, ingredient_list, ingredient_info, group_info)
    # if len(ranked) > 0:
    #     for i in range(0, len(ranked)):
    #         print "{}. {} ({})".format(i+1, ranked[i].title, ranked[i].image['image'])
    # else:
    #     print "No Results!"
    min_res = 10

    if type(ingredient_list[0]) is not tuple:
        query_with_amounts = {x:np.inf for x in ingredient_list}
    else:
        query_with_amounts = {x[0]:x[1] for x in ingredient_list}

    # Set up necessary objects
    # [dbi, ingredient_info, group_info, rank, qa] = createGlobals()
    # dbi = DBInteract()
    # group_info, ingred_to_groups = create_group_info()
    # ingredient_info = create_ingredient_info(ingred_to_groups)
    # del ingred_to_groups
    # rank = Ranking(group_info)
    # qa = QueryAdjuster()

    # Use ML to adjust query
    adj_ingredient_list = qa.get_adj_query(ingredient_list, ingredient_info, group_info)
    tmp_adj_query = copy(adj_ingredient_list)
    recipes = []
    # Just in case ML model was wrong, need to requery
    if len(tmp_adj_query) > 1:
        while (len(recipes) < 2*min_res) and (len(tmp_adj_query) > 1):
            recipes = dbi.get_recipes_with_synonyms(tmp_adj_query, ingredient_info, group_info, verbose=True)
            tmp_adj_query.pop()
    else:
        recipes = dbi.get_recipes_with_synonyms(tmp_adj_query, ingredient_info, group_info, verbose=True)

    ranked, scores = rank.rank_results(recipes, query_with_amounts, ingredient_info, group_info, top_k = 20)
    return ranked
    # if len(ranked) > 0:
    #     for i in range(0, len(ranked)):
    #         print "{}. {} ({})".format(i+1, ranked[i].title, ranked[i].image['image'])
    # else:
    #     print "No Results!"


if __name__ == '__main__':
    # print sys.argv[1:]
    [dbi, ingredient_info, group_info, rank, qa] = createGlobals()
    i_list = [2047]
    for each in searchRecipes(i_list, dbi, ingredient_info, group_info, rank, qa):
        print each.title
