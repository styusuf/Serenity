from copy import copy
from DBInteract import DBInteract
from LookUpTables import create_ingredient_info, create_group_info
from QueryAdjuster import QueryAdjuster
from Ranking import Ranking
import sys

import pdb

def main(ingredient_list):
    '''
    Returns the recipes for the given list of ingredients
    :param ingredient_list: list of all ingredients
    :return: list of ranked recipes
    '''
    min_res = 10

    dbi = DBInteract()
    group_info, ingred_to_groups = create_group_info()
    ingredient_info = create_ingredient_info(ingred_to_groups)
    del ingred_to_groups
    rank = Ranking(group_info)
    qa = QueryAdjuster()

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

    ranked, scores = rank.rank_results(recipes, ingredient_list, ingredient_info, group_info)
    if len(ranked) > 0:
        for i in range(0, len(ranked)):
            print "{}. {} ({})".format(i+1, ranked[i].title, ranked[i].image['image'])
    else:
        print "No Results!"


if __name__ == '__main__':
    # print sys.argv[1:]
    i_list = [int(a) for a in sys.argv[1:]]
    main(i_list)
