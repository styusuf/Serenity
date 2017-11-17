import os.path
import pickle
import numpy as np
import DBInteract
from IngredientCluster import get_ingredient_clusters


# TODO: add breakdown of missing ingredient clusters
class RankingMetrics:
    def __init__(self, n_missing_q=0, n_missing_recipe=0, missing_by_cluster={}, score=0):
        self.n_missing_in_query = n_missing_q
        self.n_missing_in_recipe = n_missing_recipe
        self.missing_by_cluster = missing_by_cluster
        self.score = score

class Ranking:
    def __init__(self, group_info):
        """
        Constructor for the ranking class. This sets up all the variables needed to rank. We want to create one ranking
            object when the app is kicked off, but not create another after that.
        :param group_info: Dictionary created in main file that holds all
            necessary information about groups
        """
        # Initialize info for qf-idf
        self.num_recipes = 20015  #TODO: read from file

        # Initialize info required for
        self.ingred_clusters, self.cluster_weights = get_ingredient_clusters(group_info)
        self.clusters_to_name = {} # used in debugging
        for cluster in range(3):
            if self.cluster_weights[cluster] < 20:
                self.clusters_to_name[cluster] = "common"
            elif self.cluster_weights[cluster] < 1000:
                self.clusters_to_name[cluster] = "uncommon"
            else:
                self.clusters_to_name[cluster] = "rare"

        if os.path.isfile("app/TestData/qf_data.p"):
            self.qf_lut = pickle.load( open("app/TestData/qf_data.p", "rb"))
        else:
            self.qf_lut = {}  # query frequency lookup table
            self.qf_lut["total"] = 0
            self.qf_lut["max"] = 0

    def __del__(self):
        """
        Destructor for the ranking class. This should save the workflow.
        :return: None
        """
        # save work flow weights
        pickle.dump(self.qf_lut, open("app/TestData/qf_data.p", "wb"))

    def rank_results(self, results, orig_query, ingredient_info, group_info, top_k=10, use_clusters=False):
        """
        Orders the queried results and returns them for displaying
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :param ingredient_info: Dictionary created in main file that holds all
            necessary information about ingredients
        :param group_info: Dictionary created in main file that holds all
            necessary information about groups
        :param top_k: Number of results that will be displayed
        :param use_clusters: Flag indicating to use clusters or pure frequencies
        :return: (Ordered list of query results, Ordered list of scores)
        """
        self.update_qf(orig_query)
        ranked_results, ranked_scores = self.do_ranking(results, orig_query, ingredient_info, group_info, use_clusters=use_clusters)

        if top_k < len(ranked_results):
            return ranked_results[:top_k], ranked_scores[:top_k]
        else:
            return ranked_results, ranked_scores

    # Helper Functions
    def get_metric(self, all_missing, missing_in_rec, missing_in_q, score):
        missing_by_cluster = {}
        for ingred in all_missing:
            cluster = self.clusters_to_name[self.ingred_clusters[ingred]]
            missing_by_cluster[cluster] = missing_by_cluster.get(cluster, 0) + 1
        ret = RankingMetrics(n_missing_q = len(missing_in_q), n_missing_recipe = len(missing_in_rec), missing_by_cluster=missing_by_cluster, score=score)
        return ret

    def use_pure_freq(self, missing_ingred, in_common, ingredient_info, group_info):
        """
        Scores in the unadjusted query case by using the frequencies of each ingredient
        :param missing_ingred: List/set of ingredients missing from query
        :param in_common: Tuple of information regarding ingredients and their quantities
            occurring in query and recipe
        :param ingredient_info: Dictionary created in main file that holds all
            necessary information about ingredient
        :param group_info: Dictionary created in main file that holds all
            necessary information about groups
        :return: Score
        """
        # To avoid overflowing, using sum of log occurrences
        ret = 0

        # Deal with missing ingredients
        for ingredient_id in missing_ingred:
            qf_contribution = (self.qf_lut.get(ingredient_id, 0) + 1.0) / (self.qf_lut.get("max", 0) + 1.0)
            all_groups_freq = 0.0
            for grp in ingredient_info[ingredient_id]["group"]:
                all_groups_freq += group_info[grp]["group frequency"]
            ret += np.log(all_groups_freq / self.num_recipes) + np.log(qf_contribution)

        # Deal with quantities
        for ingredient_tup in in_common:
            qf_contribution = (self.qf_lut.get(ingredient_tup[0], 0) + 1.0) / (self.qf_lut.get("max", 0) + 1.0)
            all_groups_freq = 0.0
            for grp in ingredient_info[ingredient_tup[0]]["group"]:
                all_groups_freq += group_info[grp]["group frequency"]

            # cap quantities
            if ingredient_tup[2] > ingredient_tup[1]:
                quantity_scaling = 0.0
            else:
                quantity_scaling = (ingredient_tup[1]  - ingredient_tup[2]) / (ingredient_tup[1])
            ret += quantity_scaling * (np.log(all_groups_freq / self.num_recipes) + np.log(qf_contribution))
        return ret

    def use_cluster_freq(self, missing_ingred, in_common):
        """
        Scores in the unadjusted query case by using the number of elements in the cluster
        :param missing_ingred: List/set of ingredients missing from query
        :param in_common: Tuple of information regarding ingredients and their quantities
            occurring in query and recipe
        :return: Score
        """
        # To avoid underflowing, using sum of log occurrences
        ret = 0

        # Deal with missing ingredients
        for ingredient_id in missing_ingred:
            qf_contribution = (self.qf_lut.get(ingredient_id, 0) + 1.0) / (self.qf_lut.get("max", 0) + 1.0)
            ret += np.log(1.0 / self.cluster_weights[self.ingred_clusters[ingredient_id]]) + np.log(qf_contribution)

        # Deal with quantities
        for ingredient_tup in in_common:
            qf_contribution = (self.qf_lut.get(ingredient_tup[0], 0) + 1.0) / (self.qf_lut.get("max", 0) + 1.0)

            # cap quantities
            if ingredient_tup[2] > ingredient_tup[1]:
                quantity_scaling = 0.0
            else:
                quantity_scaling = (ingredient_tup[1]  - ingredient_tup[2]) / (ingredient_tup[1])
            ret += quantity_scaling * (np.log(1.0 / self.cluster_weights[self.ingred_clusters[ingredient_tup[0]]]) + np.log(qf_contribution))
        return ret

    def do_ranking(self, results, orig_query, ingredient_info, group_info, use_clusters=False):
        """
        Ranking by dissimilarity between original query and returned results. We did not need to adjust the query in
        this case.
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :param ingredient_info: Dictionary created in main file that holds all
            necessary information about ingredients
        :param group_info: Dictionary created in main file that holds all
            necessary information about groups
        :param use_clusters: Flag indicating to use cluster frequencies instead of pure frequencies
        :return: (Ordered list of recipes, Ordered list of scores)
        """
        scores = []
        metrics = []
        set_orig_query = set(orig_query.keys())
        for recipe in results:
            # remove all of the overlapping ingredients
            recipe_ingred = set()
            in_common = []
            for ingredient in recipe.ingredients:
                recipe_ingred.add(ingredient["id"])
                if ingredient["id"] in set_orig_query:
                    in_common.append((ingredient["id"], ingredient["amount"], orig_query[ingredient["id"]]))
            missing_in_rec = recipe_ingred.difference(set_orig_query)  # in recipe but not query
            missing_in_q = set_orig_query.difference(recipe_ingred)  # in query but not recipe
            all_missing_ingred = missing_in_q.union(missing_in_rec)

            # generate score by using sum of log frequencies
            if use_clusters:
                score = self.use_cluster_freq(all_missing_ingred, in_common)
            else:
                score = self.use_pure_freq(all_missing_ingred, in_common, ingredient_info, group_info)
            scores.append(score)

            # TODO: add breakdown of missing ingredient clusters
            metrics.append(self.get_metric(all_missing_ingred, missing_in_rec, missing_in_q, score))

        # sort in decreasing order
        sort_idx = [i[0] for i in sorted(enumerate(scores), key=lambda x: -x[1])]

        results = [results[i] for i in sort_idx]
        scores = [scores[i] for i in sort_idx]
        metrics = [metrics[i] for i in sort_idx]

        return results, metrics

    def update_qf(self, orig_query):
        """
        Updates the work flow weights
        :param orig_query: Query object describing what user requested
        :return: None
        """
        new_max = 0
        for ingred in orig_query:  #TODO: assumes orig_query is setup as [(ing0, amt0), ..., (ingN, amtN)]
            # ingred = ing_amt_pair[0]
            ingred = ingred
            new_val = self.qf_lut.get(ingred, 0) + 1
            self.qf_lut[ingred] = new_val
            if new_val > new_max:
                new_max = new_val
        self.qf_lut["total"] += len(orig_query)

        # keep track of most frequent so we can smooth qf
        if new_max > self.qf_lut["max"]:
            self.qf_lut["max"] = new_max

def test_ranking():
    dbi = DBInteract.DBInteract()
    dbi.connect_to_db()

    from setup import create_ingredient_info
    ingredient_info = create_ingredient_info()
    from LookUpTables import create_ingredient_info, create_group_info
    group_info, ingred_to_group = create_group_info()
    ingredient_info = create_ingredient_info(ingred_to_group)

    ranker = Ranking(group_info)

    query = [5062, 19296]
    query_with_amounts = {5062:1, 19296:1}
    results = dbi.get_recipes(query, verbose=True)

    print "Using Pure Frequencies"
    print "Name\tMissing in Recipe\tMissing in Query\tScore"
    print "--------------------------------------------------------------------"
    ranked, metrics = ranker.rank_results(results, query_with_amounts, ingredient_info, group_info, use_clusters=False)
    for idx, recipe in enumerate(ranked):
        print "{0}: {1}, {2}, {3}, {4}".format(recipe.title, metrics[idx].missing_by_cluster, metrics[idx].n_missing_in_query, metrics[idx].n_missing_in_recipe, metrics[idx].score)
    print
    print "Using Cluster Frequencies"
    print "Name\tMissing in Query\tMissing in Recipe\tScore"
    print "--------------------------------------------------------------------"
    ranked, metrics = ranker.rank_results(results, query_with_amounts, ingredient_info, group_info, use_clusters=True)
    for idx, recipe in enumerate(ranked):
        print "{0}: {1}, {2}, {3}, {4}".format(recipe.title, metrics[idx].missing_by_cluster, metrics[idx].n_missing_in_query, metrics[idx].n_missing_in_recipe, metrics[idx].score)

# TODO: This will break!!! No quantities...
def test_ranking_by_hand():
    from RecipeClass import Recipe
    from LookUpTables import create_ingredient_info, create_group_info
    group_info, ingred_to_group = create_group_info
    ingredient_info = create_ingredient_info(ingred_to_group)
    ranker = Ranking(group_info)

    query = [2047, 19296, 5062]
    results = []
    new = Recipe()
    new.title="Chicken, Honey, and Salt"
    new.ingredients=[{"id": 5062}, {"id": 19296}, {"id": 2047}]
    results.append(new)

    new = Recipe()
    new.title="Chicken and Honey"
    new.ingredients=[{"id": 5062}, {"id": 19296}]
    results.append(new)

    new = Recipe()
    new.title="Salt and Honey"
    new.ingredients=[{"id": 19296}, {"id": 2047}]
    results.append(new)

    new = Recipe()
    new.title="Salt and Chicken"
    new.ingredients=[{"id": 5062}, {"id": 2047}]
    results.append(new)

    new = Recipe()
    new.title="Chicken"
    new.ingredients=[{"id": 5062}]
    results.append(new)

    new = Recipe()
    new.title="Honey"
    new.ingredients=[{"id": 19296}]
    results.append(new)

    new = Recipe()
    new.title="Salt"
    new.ingredients=[{"id": 2047}]
    results.append(new)

    print "Using Pure Frequencies"
    print "Name\tMissing in Recipe\tMissing in Query\tScore"
    print "--------------------------------------------------------------------"
    ranked, metrics = ranker.rank_results(results, query, ingredient_info, group_info, use_clusters=False)
    for idx, recipe in enumerate(ranked):
        print "{0}: {1}, {2}, {3}, {4}".format(recipe.title, metrics[idx].missing_by_cluster, metrics[idx].n_missing_in_query, metrics[idx].n_missing_in_recipe, metrics[idx].score)
    print
    print "Using Cluster Frequencies"
    print "Name\tMissing in Query\tMissing in Recipe\tScore"
    print "--------------------------------------------------------------------"
    ranked, metrics = ranker.rank_results(results, query, ingredient_info, group_info, use_clusters=True)
    for idx, recipe in enumerate(ranked):
        print "{0}: {1}, {2}, {3}, {4}".format(recipe.title, metrics[idx].missing_by_cluster, metrics[idx].n_missing_in_query, metrics[idx].n_missing_in_recipe, metrics[idx].score)

if __name__ == "__main__":
    np.seterr(all='raise')
    test_ranking()
    # test_ranking_by_hand()
