from sklearn.cluster import KMeans
import numpy as np
import pdb


def get_ingredient_clusters():
    """
    Clusters ingredients on frequency and returns information
    :return: (Dictionary mapping ingredients to new cluster weights, Dictionary mapping clusters to number of members)
    """
    num_clusters = 3
    # Read in data
    X = []
    ingred = []
    with open("TestData/frequency.txt", 'r') as infile:
        infile.readline()
        infile.readline()
        for line in infile:
            split = line.split('|')
            if len(split) != 3:
                continue
            ingred.append(split[1].strip().replace("'", ''))
            X.append(int(split[2].lstrip().strip()))
    X = np.array(X)
    X = X.reshape(X.shape[0], 1)

    # Generate clusters from data
    clusters = KMeans(n_clusters=num_clusters, init='k-means++').fit(X)

    ret = {}
    for idx, ingredient in enumerate(ingred):
        ret[ingredient] = clusters.labels_[idx]
    cluster_sizes = {}
    for i in range(num_clusters):
        cluster_sizes[i] = len(clusters.labels_[clusters.labels_ == i])

    return ret, cluster_sizes


if __name__ == "__main__":
    num_clusters = 3
    # Read in data
    X = []
    ingred = []
    with open("TestData/frequency.txt", 'r') as infile:
        infile.readline()
        infile.readline()
        for line in infile:
            split = line.split('|')
            if len(split) != 3:
                continue
            ingred.append(split[1].strip().replace("'", ''))
            X.append(int(split[2].lstrip().strip()))
    X = np.array(X)
    X = X.reshape(X.shape[0], 1)

    # Generate clusters from data
    clusters = KMeans(n_clusters=num_clusters, init='k-means++').fit(X)

    # Output to file ingredient - cluster pairs
    with open("Output/IngredientCluster_pairs.txt", 'w') as outfile:
        for i in range(len(ingred)):
            outfile.write(ingred[i] + " " + str(clusters.labels_[i]) + "\n")

    # Output to stdout cluster centers and cutoffs
    print "Cluster Centers:"
    print clusters.cluster_centers_
    print "Cluster Cutoffs:"
    for i in range(num_clusters-1):
        print "Cutoff between Clusters", i, "and", i+1, "=", (clusters.cluster_centers_[i] + clusters.cluster_centers_[i+1])/2

    # Output to stdout size of each cluster
    print "Cluster Sizes:"
    for i in range(num_clusters):
        print "Cluster", i,  "has", len(clusters.labels_[clusters.labels_ == i]), "constituents"

    # Write cluster centers to file
    with open("Output/IngredientCluster_centers.txt", 'w') as outfile:
        for i in range(num_clusters):
            outfile.write(str(clusters.cluster_centers_[i][0]) + "\n")
