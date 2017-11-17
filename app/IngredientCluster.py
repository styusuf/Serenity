from sklearn.cluster import KMeans
import numpy as np

import pdb


def get_ingredient_clusters(group_info):
    """
    Clusters ingredients on frequency and returns information
    :param ingredient_info: Dictionary created in main file that holds all
        necessary information about ingredients
    :return: (Dictionary mapping ingredients to new cluster weights, Dictionary mapping clusters to number of members)
    """
    num_clusters = 3

    # Prepare data
    X = np.array([grp["group frequency"] for grp in group_info.values()])
    X = X.reshape(X.shape[0], 1)

    # Generate clusters from data
    clusters = KMeans(n_clusters=num_clusters, init='k-means++').fit(X)

    cluster_members = {}
    cluster_sizes = {}
    for idx, group in enumerate(group_info.values()):
        for ingredient in group["ingredient list"]:
            cluster_members[int(ingredient)] = clusters.labels_[idx]
            cluster_sizes[clusters.labels_[idx]] = cluster_sizes.get(clusters.labels_[idx], 0) + 1

    return cluster_members, cluster_sizes

if __name__ == "__main__":
    from LookUpTables import create_ingredient_info, create_group_info
    group_info, ingred_to_group = create_group_info()
    ingredient_info = create_ingredient_info(ingred_to_group)
    cluster_members, cluster_sizes = get_ingredient_clusters(group_info)

    # Output to stdout size of each cluster
    print "Cluster Sizes:"
    for i in range(len(cluster_sizes)):
        print "Cluster", i,  "has", cluster_sizes[i], "constituents"
