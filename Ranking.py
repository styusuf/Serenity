class Ranking:
    """Ranking Class"""

    def __init__(self):
        """
        Constructor for the ranking class. This sets up all the variables needed to rank. We want to create one ranking
        object when the app is kicked off, but not create another after that.
        """
        # Initialize info for tf-idf
        self.num_recipes = 3964  #TODO: read from file

        # TODO: Initialize info for ingredient frequencies
        self.ingred_freq = {} # ingredient frequency lookup table
        self.default_freq = 1/max(self.ingred_freq)  # TODO: replace with frequency of most frequent ingredient

        # TODO: Initialize info for query frequency
        self.qf_lut = {}  # query frequency lookup table

    def __del__(self):
        """
        Destructor for the ranking class. This should save the workflow.
        :return: None
        """
        # save work flow weights
        pass

    def rank_results(self, results, orig_query):
        """
        Orders the queried results and returns them for displaying
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :return: Ordered list of query results
        """
        pass

    def rank_adjustment(self, results, orig_query):
        """
        Ranking by similarity between original query and returned results. We needed to adjust the query in this case.
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :return: similarity weights for each query
        """
        pass

    def rank_no_adjustment(self, results, orig_query):
        """
        Ranking by dissimilarity between original query and returned results. We did not need to adjust the query in
        this case.
        :param results: List of Query results
        :param orig_query: Query object describing what user requested
        :return: Ordered list of tuples of recipes and their scores [(recipe0, score0), ..., (recipeN, scoreN)]
        """
        ret = []
        for recipe in results:
            # remove all of the overlapping ingredients
            rem_ingred = []

            # generate score by using geometric sum of frequencies
            score = 1
            for ingred in rem_ingred:
                score *= self.ingred_freq.get(ingred, self.default_freq)
            score *= -1
            ret.append(recipe, score)

        # sort in increasing decreasing order (least negative first)
        ret = sorted(ret, key=lambda x: -x[1])

        return ret

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
