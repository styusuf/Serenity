from sklearn.cluster import KMeans
import numpy as np
import pdb


def get_ingredient_clusters(ingredient_info):
    """
    Clusters ingredients on frequency and returns information
    :param ingredient_info: Dictionary created in main file that holds all
        necessary information about ingredients
    :return: (Dictionary mapping ingredients to new cluster weights, Dictionary mapping clusters to number of members)
    """
    num_clusters = 3

    # Prepare data
    X = sorted([ing for ing in ingredient_info.values()], key=lambda x: x["feature number"])
    all_ingredients = sorted([ing for ing in ingredient_info], key=lambda x: ingredient_info[x]["feature number"])
    X = [ing["frequency"] for ing in X]
    X = np.array(X)
    X = X.reshape(X.shape[0], 1)

    # Generate clusters from data
    clusters = KMeans(n_clusters=num_clusters, init='k-means++').fit(X)

    cluster_members = {}
    for idx, ingredient in enumerate(all_ingredients):
        cluster_members[ingredient] = clusters.labels_[idx]
    cluster_sizes = {}
    for i in range(num_clusters):
        cluster_sizes[i] = len(clusters.labels_[clusters.labels_ == i])

    return cluster_members, cluster_sizes

if __name__ == "__main__":
    from app import create_ingredient_info
    ingredient_info = create_ingredient_info()
    cluster_members, cluster_sizes = get_ingredient_clusters(ingredient_info)

    # Output to stdout size of each cluster
    print "Cluster Sizes:"
    for i in range(len(cluster_sizes)):
        print "Cluster", i,  "has", cluster_sizes[i], "constituents"
