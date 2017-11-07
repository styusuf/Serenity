import DBInteract
import numpy as np
import os.path
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor

import pdb

class PredictQuery:
    """predictQuery class - Predict number of query results returned"""

    def __init__(self):
        """predictQuery constructor"""
        self.models = {"linreg": None, "knn": None, "rf": None}

    def train(self, X, y, linreg=True, knn=True, rf=True, k=3, knn_weights="uniform", num_trees=10, max_depth=None):
        """
        Trains indicated models. By default, trains none.
        :param X: Training data features
        :param y: Training data targets
        :param linreg: Flag indicating whether or not linear regression model should be trained
        :param knn: Flag indicating whether or not k-nearest neighbors model should be trained
        :param rf: Flag indicating whether or not random forest model should be trained
        :param k: Number of NN to use in model
        :param knn_weights: How to weight the nearest neighbors. Check out sklearn for options
        :param num_trees: Number of trees in the forest
        :param max_depth: Max depth of any tree in the forest
        :return: None
        """
        if linreg:
            self.train_linreg(X, y)
            print "finished training linreg"
        if knn:
            self.train_knn(X, y, k=k, weights=knn_weights)
            print "finished training knn"
        if rf:
            self.train_rf(X, y, num_trees=num_trees, max_depth=max_depth)
            print "finished printing rf"

    def train_linreg(self, X, y):
        """
        Trains linear regression model
        :param X: Training data features
        :param y: Training data targets
        :return: Handle to linear regression model
        """
        lr = LinearRegression()
        lr.fit(X, y)
        self.models["linreg"] = lr
        return lr

    def train_knn(self, X, y, k=3, weights="uniform"):
        """
        Trains k nearest neighbor model.
        :param X: Training data features
        :param y: Training data targets
        :param k: Number of NN to use in model
        :param weights: How to weight the nearest neighbors. Check out sklearn for options
        :return: Handle to knn model
        """
        knn = KNeighborsRegressor(n_neighbors=k, weights=weights)
        knn.fit(X, y)
        self.models["knn"] = knn
        return knn

    def train_rf(self, X, y, num_trees=10, max_depth=None):
        """
        Trains random forest model
        :param X: Training data features
        :param y: Training data targets
        :param num_trees: Number of trees in the forest
        :param max_depth: Max depth of any tree in the forest
        :return: handle to random forest model
        """
        rf = RandomForestRegressor(n_estimators=num_trees, max_depth=max_depth)
        rf.fit(X, y)
        self.models["rf"] = rf
        return rf

    def test(self, X, y):
        """
        Tests models
        :param X: Testing data features
        :param y: Testing data targets
        :return: None
        """
        for key in self.models:
            if self.models[key] is not None:
                pred = self.models[key].predict(X)
                rmse = np.sqrt(mean_squared_error(y, pred))
                print "Model", key, "yields RMSE = ", rmse

def build_training_data():
    """
    Generates training samples and target values
    :return: (training features, training targets)
    """
    # set up variables
    feat_to_id = {}
    ret_X = []
    db_queries = []
    ret_y = []
    num_ingred = 0
    dbi = DBInteract.DBInteract()
    dbi.connect_to_db()
    with open("TestData/frequency.txt") as infile:
        infile.readline()
        infile.readline()
        for idx, line in enumerate(infile):
            split = line.split('|')
            if len(split) != 3:
                continue
            ingredient = int(split[0].lstrip())
            feat_to_id[idx] = ingredient
            num_ingred += 1

    choices = range(num_ingred)
    for k in range(1, 11):
        for _ in range(1, 2001):
            new_ingreds = np.random.choice(choices, k)
            new_feat = np.zeros(num_ingred)
            new_feat[new_ingreds] = 1
            ret_X.append(new_feat)
            db_queries.append([feat_to_id[x] for x in new_ingreds])
            db_result = dbi.get_recipes(db_queries[-1])
            ret_y.append(len(db_result))

    ret_X = np.array(ret_X)
    ret_y = np.array(ret_y)
    np.save("TestData/predict_query_train_X", ret_X)
    np.save("TestData/predict_query_train_y", ret_y)
    return ret_X, ret_y

def test_on_db_data():
    """
    Tests regression models on generated test data
    :return: None
    """
    # load or generate file
    if os.path.isfile("TestData/predict_query_train_X.npy"):
        all_X = np.load("TestData/predict_query_train_X.npy")
        all_y = np.load("TestData/predict_query_train_y.npy")
    else:
        all_X, all_y = build_training_data()

    # shuffle data
    all_data = np.c_[all_X, np.reshape(all_y, (all_y.shape[0], 1))]
    np.random.shuffle(all_data)

    # split training data
    n_train = int(0.8 * all_data.shape[0])
    train_X = all_data[0:n_train, 0:all_data.shape[1]]
    train_y = all_data[0:n_train, -1]

    test_X = all_data[n_train:, 0:all_data.shape[1]]
    test_y = all_data[n_train:, -1]

    # train
    pq = PredictQuery()
    pq.train(train_X, train_y, linreg=True, knn=True, rf=True, k=5, num_trees=20)

    # test
    print "Testing in-sample"
    pq.test(train_X, train_y)
    print "\nTesting out-of-sample"
    pq.test(test_X, test_y)

def test_on_diabetes():
    """
    Tests regression models on sklearn diabetes dataset
    :return: None
    """
    # load dataset
    diabetes = datasets.load_diabetes()

    # get features data
    diabetes_X = diabetes.data[:, np.newaxis, 2]
    diabetes_X_train = diabetes_X[:-20]
    diabetes_X_test = diabetes_X[-20:]

    # get target values
    diabetes_y_train = diabetes.target[:-20]
    diabetes_y_test = diabetes.target[-20:]
    pq = PredictQuery()

    # train models
    pq.train(diabetes_X_train, diabetes_y_train, linreg=True, knn=True, rf=True, k=10, num_trees=100)

    # test models
    pq.test(diabetes_X_test, diabetes_y_test)


if __name__ == "__main__":
    # test_on_diabetes()
    test_on_db_data()
