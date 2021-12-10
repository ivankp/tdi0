#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np

import sklearn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor

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

class ScaleByYear(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.m = {
            key: vals for key,*vals in
            X.groupby('year').agg({'owned':['mean','std']}).to_records()
        }
        return self
    def transform(self, X):
        def scale(x):
            mean, std = self.m[x[0]]
            return (x[1]-mean)/std
        return X[['year','owned']].apply(scale,axis=1)

y_all = ScaleByYear().fit_transform(df).to_numpy()

print('fitting')

forest_gs = GridSearchCV(
    RandomForestRegressor(n_estimators=1000, n_jobs=32),
    { 'max_depth': [40,45,50,55,60],
      'max_features': [40,45,50,55,60]
    },
    cv=3,
    verbose=3
).fit(X_all, y_all)

