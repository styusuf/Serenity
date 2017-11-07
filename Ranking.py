import DBInteract
from IngredientCluster import get_ingredient_clusters
import numpy as np

import pdb

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

        self.default_freq = 1/self.ingred_freq["salt"]

        self.ingred_clusters, self.cluster_weights = get_ingredient_clusters()

        # TODO: Initialize info for query frequency
        self.qf_lut = {}  # query frequency lookup table

    def __del__(self):
        """
        Destructor for the ranking class. This should save the workflow.
        :return: None
        """
        # save work flow weights
        pass

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
        if not needed_adjustment:
            ranked_results, ranked_scores = self.rank_no_adjustment(results, orig_query, use_clusters=use_clusters)
        else:
            ranked_results, ranked_scores = self.rank_adjustment(results, orig_query, use_clusters=use_clusters)

        if top_k < len(ranked_results):
            return ranked_results[:top_k], ranked_scores[:top_k]
        else:
            return ranked_results, ranked_scores

    # Adjustment functions
    # TODO: Implement rank when query needs adjustment
    def rank_adjustment(self, results, orig_query, use_clusters=False):
        """
        Ranking by similarity between original query and returned results. We needed to adjust the query in this case.
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :param use_clusters: Flag indicating to use cluster frequencies instead of pure frequencies
        :return: similarity weights for each query
        """
        pass

    # No Adjustment functions
    def rna_pure_freq(self, missing_ingred):
        """
        Scores in the unadjusted query case by using the frequencies of each ingredient
        :param missing_ingred: List/set of ingredients missing from query
        :return: Score
        """
        ret = 0
        # To avoid overflowing, I'm using sum of log occurrences
        for ingredient in missing_ingred:
            ret += np.log(self.ingred_freq[self.id_to_ingred[ingredient]])
        return ret

    def rna_cluster_freq(self, missing_ingred):
        """
        Scores in the unadjusted query case by using the number of elements in the cluster
        :param missing_ingred: List/set of ingredients missing from query
        :return: Score
        """
        ret = 0
        # To avoid underflowing, I'm using sum of log occurrences
        for ingredient in missing_ingred:
            ret += np.log(1.0 / self.cluster_weights[self.ingred_clusters[self.id_to_ingred[ingredient]]])
        return ret

    def rank_no_adjustment(self, results, orig_query, use_clusters=False):
        """
        Ranking by dissimilarity between original query and returned results. We did not need to adjust the query in
        this case.
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :param use_clusters: Flag indicating to use cluster frequencies instead of pure frequencies
        :return: (Ordered list of recipes, Ordered list of scores)
        """
        scores = []
        set_orig_query = set(orig_query)
        for recipe in results:
            # remove all of the overlapping ingredients
            recipe_ingred = set()
            for ingredient in recipe.ingredients:
                try:
                    recipe_ingred.add(ingredient["id"])
                except:
                    pdb.set_trace()
                    continue
            missing_ingred = recipe_ingred.difference(set_orig_query)

            # generate score by using sum of log frequencies
            if use_clusters:
                score = self.rna_cluster_freq(missing_ingred)
            else:
                score = self.rna_pure_freq(missing_ingred)
            scores.append(score)

        # sort in increasing decreasing order
        if use_clusters:
            sort_idx = [i[0] for i in sorted(enumerate(scores), key=lambda x: -x[1])]
        else:
            sort_idx = [i[0] for i in sorted(enumerate(scores), key=lambda x: -x[1])]
            
        results = [results[i] for i in sort_idx]
        scores = [scores[i] for i in sort_idx]

        pdb.set_trace()
        return results, scores

    def update_qf(self, orig_query):
        """
        Updates the work flow weights
        :param orig_query:
        :return: None
        """
        new_max = 0
        for ing_amt_pair in orig_query: # assumes orig_query is setup as [(ing0, amt0), ..., (ingN, amtN)]
            ingred = ing_amt_pair[0]
            ingred = ingred.lower()
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

    ranked, scores = ranker.rank_results(results, query, use_clusters=True)
    for idx, recipe in enumerate(ranked):
        print "{0}: {1}".format(recipe.title, scores[idx])

if __name__ == "__main__":
    test_ranking()
