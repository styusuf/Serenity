import numpy as np
import PredictQuery as pq

import pdb

class QueryAdjuster:
    def __init__(self):
        self.pq = pq.PredictQuery()
        self.rmse = 15

    def get_adj_query(self, orig_query, ingredient_info, min_res=25, verbose=True):
        """
        Predicts the number of results that will be returned by database for the
            given query and adjusts the query to get enough results for the user
            to choose from.
        :param orig_query: List of ingredient ids describing what user requested
        :param ingredient_info: Dictionary created in main file that holds all
            necessary information about ingredients
        :param verbose: Whether or not debug statements should print
        """
        # Sort by frequency
        adj_query = sorted(orig_query, key=lambda x: -ingredient_info[x]["frequency"])
        query_vec = np.zeros(len(ingredient_info)).reshape(1, -1)
        for ingred in orig_query:
            feat_idx = ingredient_info[ingred]["feature number"]
            query_vec[0, feat_idx] = 1.0

        predicted_num = self.pq.models["nn"].predict(query_vec)
        if verbose:
            print ("Predicted number of recipes for query: {} is {}".format(adj_query, predicted_num))

        # Adjust query if needed
        while (predicted_num < (2 * min_res + self.rmse)) and (adj_query):
            # Remove most rare ingredient
            removed = adj_query.pop()
            feat_idx = ingredient_info[removed]["feature number"]
            query_vec[0, feat_idx] = 0

            # The new recipes should be a superset of the old recipes, so needed
            #   only for the new query to be above the threshold
            predicted_num = self.pq.models["nn"].predict(query_vec)
            if verbose:
                print ("Predicted number of recipes for query: {} is {}".format(adj_query, predicted_num))

        return adj_query


if __name__ == "__main__":
    from App import create_ingredient_info
    ingredient_info = create_ingredient_info()

    qa = QueryAdjuster()
    query = [2047, 19335, 1123, 11215, 2050]
    adj_query = qa.get_adj_query(query, ingredient_info)
    print "Original query: {}\nadjusted to: {}.".format(query, adj_query)
