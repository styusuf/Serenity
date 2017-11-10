import DBInteract
from IngredientCluster import get_ingredient_clusters
import numpy as np
import os.path
import pickle

import pdb

# TODO: add breakdown of missing ingredient clusters
class RankingMetrics:
    def __init__(self, n_missing_q=0, n_missing_recipe=0, missing_by_cluster={}, score=0):
        self.n_missing_in_query = n_missing_q
        self.n_missing_in_recipe = n_missing_recipe
        self.missing_by_cluster = missing_by_cluster
        self.score = score

class Ranking:
    def __init__(self):
        """
        Constructor for the ranking class. This sets up all the variables needed to rank. We want to create one ranking
        object when the app is kicked off, but not create another after that.
        """
        # Initialize info for tf-idf
        self.num_recipes = 20015  #TODO: read from file

        self.ingred_freq = {} # ingredient frequency lookup table
        self.id_to_ingred = {}
        with open("TestData/frequency.txt") as infile:
            infile.readline()
            infile.readline()
            for line in infile:
                split = line.split('|')
                if len(split) != 3:
                    continue
                id_val = int(split[0].lstrip())
                ingredient = split[1].strip().replace("'", '')
                frequency = int(split[2].lstrip().strip())
                self.ingred_freq[ingredient] = frequency
                self.id_to_ingred[id_val] = ingredient

        self.ingred_clusters, self.cluster_weights = get_ingredient_clusters()
        self.clusters_to_name = {}
        for cluster in range(3):
            if self.cluster_weights[cluster] < 20:
                self.clusters_to_name[cluster] = "common"
            elif self.cluster_weights[cluster] < 1000:
                self.clusters_to_name[cluster] = "uncommon"
            else:
                self.clusters_to_name[cluster] = "rare"

        if os.path.isfile("TestData/qf_data.p"):
            self.qf_lut = pickle.load( open("TestData/qf_data.p", "rb"))
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
        pickle.dump(self.qf_lut, open("TestData/qf_data.p", "wb"))

    def rank_results(self, results, orig_query, top_k=10, needed_adjustment=False, use_clusters=False):
        """
        Orders the queried results and returns them for displaying
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :param top_k: Number of results that will be displayed
        :param needed_adjustment: Flag indicating whether the query was adjusted
        :param use_clusters: Flag indicating to use clusters or pure frequencies
        :return: (Ordered list of query results, Ordered list of scores)
        """
        self.update_qf(orig_query)
        ranked_results, ranked_scores = self.do_ranking(results, orig_query, use_clusters=use_clusters)

        if top_k < len(ranked_results):
            return ranked_results[:top_k], ranked_scores[:top_k]
        else:
            return ranked_results, ranked_scores

    # Helper Functions
    def get_metric(self, all_missing, missing_in_rec, missing_in_q, score):
        missing_by_cluster = {}
        for ingred in all_missing:
            cluster = self.clusters_to_name[self.ingred_clusters[self.id_to_ingred[ingred]]]
            missing_by_cluster[cluster] = missing_by_cluster.get(cluster, 0) + 1
        ret = RankingMetrics(n_missing_q = len(missing_in_q), n_missing_recipe = len(missing_in_rec), missing_by_cluster=missing_by_cluster, score=score)
        return ret

    def use_pure_freq(self, missing_ingred):
        """
        Scores in the unadjusted query case by using the frequencies of each ingredient
        :param missing_ingred: List/set of ingredients missing from query
        :return: Score
        """
        ret = 0
        # To avoid overflowing, I'm using sum of log occurrences
        for ingredient in missing_ingred:
            qf_contribution = (self.qf_lut.get(ingredient, 0) + 1.0) / (self.qf_lut.get("max", 0) + 1.0)
            ret += np.log(float(self.ingred_freq[self.id_to_ingred[ingredient]]) / self.num_recipes) + np.log(qf_contribution)
        return ret

    def use_cluster_freq(self, missing_ingred):
        """
        Scores in the unadjusted query case by using the number of elements in the cluster
        :param missing_ingred: List/set of ingredients missing from query
        :return: Score
        """
        ret = 0
        # To avoid underflowing, I'm using sum of log occurrences
        for ingredient in missing_ingred:
            qf_contribution = (self.qf_lut.get(ingredient, 0) + 1.0) / (self.qf_lut.get("max", 0) + 1.0)
            ret += np.log(1.0 / self.cluster_weights[self.ingred_clusters[self.id_to_ingred[ingredient]]]) + np.log(qf_contribution)
        return ret

    def do_ranking(self, results, orig_query, use_clusters=False):
        """
        Ranking by dissimilarity between original query and returned results. We did not need to adjust the query in
        this case.
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :param use_clusters: Flag indicating to use cluster frequencies instead of pure frequencies
        :return: (Ordered list of recipes, Ordered list of scores)
        """
        scores = []
        metrics = []
        set_orig_query = set(orig_query)
        for recipe in results:
            # remove all of the overlapping ingredients
            recipe_ingred = set()
            for ingredient in recipe.ingredients:
                recipe_ingred.add(ingredient["id"])
            missing_in_rec = recipe_ingred.difference(set_orig_query)  # in recipe but not query
            missing_in_q = set_orig_query.difference(recipe_ingred)  # in query but not recipe
            all_missing_ingred = missing_in_q.union(missing_in_rec)

            # generate score by using sum of log frequencies
            if use_clusters:
                score = self.use_cluster_freq(all_missing_ingred)
            else:
                score = self.use_pure_freq(all_missing_ingred)
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

    ingred_to_id = {}
    with open("TestData/frequency.txt") as infile:
        infile.readline()
        infile.readline()
        for idx, line in enumerate(infile):
            split = line.split('|')
            if len(split) != 3:
                continue
            id_val = int(split[0].lstrip())
            ingredient = split[1].strip().replace("'", '')
            ingred_to_id[ingredient] = id_val

    ranker = Ranking()

    query_names = ["chicken breast", "honey"]
    query = [ingred_to_id[i] for i in query_names]
    results = dbi.get_recipes(query, verbose=True)

    print "Using Pure Frequencies"
    print "Name\tMissing in Recipe\tMissing in Query\tScore"
    print "--------------------------------------------------------------------"
    ranked, metrics = ranker.rank_results(results, query, use_clusters=False)
    for idx, recipe in enumerate(ranked):
        print "{0}: {1}, {2}, {3}, {4}".format(recipe.title, metrics[idx].missing_by_cluster, metrics[idx].n_missing_in_query, metrics[idx].n_missing_in_recipe, metrics[idx].score)
    print
    print "Using Cluster Frequencies"
    print "Name\tMissing in Query\tMissing in Recipe\tScore"
    print "--------------------------------------------------------------------"
    ranked, metrics = ranker.rank_results(results, query, use_clusters=True)
    for idx, recipe in enumerate(ranked):
        print "{0}: {1}, {2}, {3}, {4}".format(recipe.title, metrics[idx].missing_by_cluster, metrics[idx].n_missing_in_query, metrics[idx].n_missing_in_recipe, metrics[idx].score)
    
if __name__ == "__main__":
    np.seterr(all='raise')
    test_ranking()
