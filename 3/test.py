#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np

import sklearn
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction import DictVectorizer
# from sklearn.preprocessing import FunctionTransformer, PolynomialFeatures
# from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
# from sklearn.cluster import KMeans
# from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
# from sklearn import metrics

import matplotlib.pyplot as plt

df = pd.read_pickle('df.pkl')
print('num games:',len(df))

class DictEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        for xs in X:
            yield { x: 1 for x in xs }

binary_encoder = Pipeline([
    ('encode',   DictEncoder()),
    ('vectorize',DictVectorizer(sparse=False))
])

X_all = Pipeline([
    ('features',ColumnTransformer([
        ('attrs',Pipeline([
            ('encode',binary_encoder),
            ('pca',PCA(n_components=int(sys.argv[1])))
        ]),'attrs'),
        ('age','passthrough',[
            'poll_age','poll_npl_min','poll_npl_max','dur_min','dur_max'
        ])
    ]))
]).fit_transform(df)
print(X_all.shape)

class ScaleRatingByYear(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.m = {
            key: vals for key,*vals in
            X.groupby('year').agg({'rating':['mean','std']}).to_records()
        }
        return self
    def transform(self, X):
        def scale(x):
            mean, std = self.m[x[0]]
            return (x[1]-mean)/std
        return X[['year','rating']].apply(scale,axis=1)

y_all = ScaleRatingByYear().fit_transform(df).to_numpy()

X_train, X_test, y_train, y_test = train_test_split(
    X_all, y_all,
    test_size = 0.25,
    random_state = 123
)

print('fitting')
forest = RandomForestRegressor(
    n_estimators = 1000,
    max_depth = int(sys.argv[2]),
    max_features = int(sys.argv[3]),
    n_jobs = 4
)
forest.fit(X_train, y_train)

print('train:',forest.score(X_train, y_train))
print('test:',forest.score(X_test, y_test))
