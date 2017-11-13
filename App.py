import sys
from DBInteract import DBInteract
from QueryAdjuster import QueryAdjuster
from Ranking import Ranking

def create_ingredient_info():
    """
    Creates object that will hold all information that will need to be accessed
    about an ingredient in calculating its rank and predicting queries.
    :return: Dictionary of dictionaries. Key is ingredient id
    """
    ingredient_info = {} # ingredient lookup table
    with open("TestData/frequency.txt") as infile:
        infile.readline()
        infile.readline()
        i = 0
        for line in infile:
            split = line.split('|')
            if len(split) != 3:
                continue
            id_val = int(split[0].lstrip())
            name = split[1].strip().replace("'", '')
            frequency = float(split[2].lstrip().strip())
            group = None

            new_ingred = {"name": name, "frequency": frequency, "group": group, "feature number": i}
            ingredient_info[id_val] = new_ingred
            i += 1

    return ingredient_info

def main(ingredient_list):
    '''
    Returns the recipes for the given list of ingredients
    :param ingredient_list: list of all ingredients
    :return: list of ranked recipes
    '''
    dbi = DBInteract()
    ingredient_info = create_ingredient_info()
    rank = Ranking(ingredient_info)
    qa = QueryAdjuster()

    adj_ingredient_list = qa.get_adj_query(ingredient_list, ingredient_info)
    recipes = dbi.get_recipes(adj_ingredient_list, verbose=True)
    ranked, scores = rank.rank_results(recipes, ingredient_list, ingredient_info)
    if len(ranked) > 0:
        for i in range(0, len(ranked)):
            print "{}. {} ({})".format(i+1, ranked[i].title, ranked[i].image['image'])
    else:
        print "No Results!"


if __name__ == '__main__':
    # print sys.argv[1:]
    i_list = [int(a) for a in sys.argv[1:]]
    main(i_list)
