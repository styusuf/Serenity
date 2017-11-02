import numpy as np
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

    def train(self, X, y, linreg=False, knn=False, rf=False, k=3, knn_weights="uniform", num_trees=10, max_depth=None):
        """
        Trains indicated models. By default, trains none.
        :param data: Training data
        :param linreg: Flag indicating whether or not linear regression model should be trained
        :param knn: Flag indicating whether or not k-nearest neighbors model should be trained
        :param rf: Flag indicating whether or not random forest model should be trained
        :return: None
        """
        if linreg:
            self.train_linreg(X, y)
        if knn:
            self.train_knn(X, y, k=k, weights=knn_weights)
        if rf:
            self.train_rf(X, y, num_trees=num_trees, max_depth=max_depth)

    def train_linreg(self, X, y):
        """
        Trains linear regression model
        :param data: Training data
        :return: handle to linear regression model
        """
        lr = LinearRegression()
        lr.fit(X, y)
        self.models["linreg"] = lr

    def train_knn(self, X, y, k=3, weights="uniform"):
        """
        Trains k nearest neighbor model.
        :param k: Number of NN to use in model
        :return: Handle to linear regression model
        """
        knn = KNeighborsRegressor(n_neighbors=k, weights=weights)
        knn.fit(X, y)
        self.models["knn"] = knn

    def train_rf(self, X, y, num_trees=10, max_depth=None):
        """
        Trains random forest model
        :param data: Training data
        :param num_trees: Number of trees in the forest
        :param max_depth: Max depth of any tree in the forest
        :return: handle to random forest model
        """
        rf = RandomForestRegressor(n_estimators=num_trees, max_depth=max_depth)
        rf.fit(X, y)
        self.models["rf"] = rf

    def test(self, X, y):
        """
        Tests models
        :param data: Testing data
        :return: None
        """
        for key in self.models:
            if self.models[key] is not None:
                pred = self.models[key].predict(X)
                rmse = np.sqrt(mean_squared_error(y, pred))
                print "Model", key, "yields RMSE = ", rmse


def test_on_diabetes():
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
    test_on_diabetes()