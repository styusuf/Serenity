import sys
from DBInteract import DBInteract
from Ranking import Ranking

def Main(ingredient_list):
    '''
    Returns the recipes for the given list of ingredients
    :param ingredient_list: list of all ingredients
    :return: list of ranked recipes
    '''
    dbi = DBInteract()
    rank = Ranking()

    recipes = dbi.get_recipes(ingredient_list, verbose=True)
    ranked, scores = rank.rank_results(recipes, ingredient_list)
    if len(ranked) > 0:
        for i in range(0, len(ranked)):
            print "{}. {} ({})".format(i+1, ranked[i].title, ranked[i].image['image'])
    else:
        print "No Results!"


if __name__ == '__main__':
    # print sys.argv[1:]
    i_list = [int(a) for a in sys.argv[1:]]
    Main(i_list)