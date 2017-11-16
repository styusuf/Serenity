import pdb

def create_ingredient_info(ingred_to_groups):
    """
    Creates object that will hold all information that will need to be accessed
    about an ingredient in calculating its rank and predicting queries.
    :return: Dictionary of dictionaries. Key is ingredient id
    """
    ingredient_info = {} # ingredient lookup table
    with open("TestData/frequency.txt", 'r') as infile:
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
            group = ingred_to_groups[id_val]

            new_ingred = {"name": name, "frequency": frequency, "group": group, "feature number": i}
            ingredient_info[id_val] = new_ingred
            i += 1

    return ingredient_info

def create_group_info():
    """
    Creates object that will hold all information that will need to be accessed
    about a group of synonymous ingredients
    :return: Tuple of dictionaries of dictionaries. First is group id -> data. Second is ingredient id -> group id
    """
    group_info = {}  # group lookup table
    ingred_to_groups = {}
    with open("TestData/groups.txt", 'r') as infile:
        for line in infile:
            split_ = line.split('|')
            ingred_id_list = [int(x) for x in split_[0].split(',')]
            group_id = int(split_[1])
            group_freq = float(split_[2])

            for id_ in ingred_id_list:
                ingred_to_groups.setdefault(int(id_), []).append(group_id)
            group_info[group_id] = {"ingredient list": ingred_id_list, "group frequency": group_freq}

    return group_info, ingred_to_groups

def find_most_freq_syn(ingredient_info, group_info, ing):
    """
    Finds the synonym of the given ingredient with the highest frequency
    :param ingredient_info: Dictionary created in main file that holds all
        necessary information about ingredients
    :param group_info: Dictionary created in main file that holds all
        necessary information about groups
    :param ing: Ingredient in question
    """
    mf_synonym = ing
    mf_syn_freq = ingredient_info[ing]["frequency"]
    for grp in ingredient_info[ing]["group"]:
        for syn in group_info[grp]["ingredient list"]:
            if ingredient_info[syn]["frequency"] > mf_syn_freq:
                mf_syn_freq = ingredient_info[syn]["frequency"]
                mf_synonym = syn

    return mf_synonym
