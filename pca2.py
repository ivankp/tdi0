#!/usr/bin/env python3

import json
import numpy as np
from sklearn.decomposition import PCA

with open('characteristics_frequency.json') as f:
    freq = json.load(f)

attrs = [
    [ x[0] for x in freq['all'][j] if x[1]>10 ]
    for j in [0,1]
]
nattrs = sum(len(x) for x in attrs)
print(nattrs)

with open('bgg_data_clean.json') as f:
    games = json.load(f)

cols  = games['columns']
data  = games['data']
print(len(data))

for i,x in enumerate(cols):
    locals()['i_'+x] = i

X = np.empty([len(data),nattrs],dtype=bool)
print(X.shape)

def check_attrs(g):
    for j,i in enumerate([i_mechanics,i_categories]):
        for c in g[i]:
            if c in attrs[j]:
                return False
    return True

for gi,g in enumerate(data):
    if check_attrs(g): continue
    ai = 0
    for j,i in enumerate([i_mechanics,i_categories]):
        for a in attrs[j]:
            X[gi,ai] = a in g[i]
            ai += 1

print('PCA')
pca = PCA()
pca.fit(X)

cumsum = np.cumsum(pca.explained_variance_ratio_)

print('PCA 2')
pca2 = PCA(n_components=2)
X2D = pca2.fit_transform(X)

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

lim = [[-1.3,2.7],[-1.4,2.1]]

ratings = [ x[i_rating] for x in data ]
rmin = min(ratings)
rmax = max(ratings)

with PdfPages('pca.pdf') as pdf:
    plt.plot(range(1,len(cumsum)+1),cumsum,'-')
    ax = plt.gca()
    # ax.margins(0)
    plt.xlim(0,len(cumsum)+1)
    plt.ylim(0,1)
    ax.set_ylabel('Explained variance fraction')
    ax.set_xlabel('Number of dimensions')
    pdf.savefig(bbox_inches='tight')
    plt.close()

    plt.scatter(*X2D.T,s=2,alpha=0.5, linewidth=0)
    plt.xlim(*lim[0])
    plt.ylim(*lim[1])
    plt.title('PCA')
    pdf.savefig(bbox_inches='tight')
    plt.close()

    plt.scatter(*X2D.T,s=1, linewidth=0,
        c=ratings, cmap='rainbow', vmin=rmin, vmax=rmax)
    plt.xlim(*lim[0])
    plt.ylim(*lim[1])
    plt.title('PCA, rating color')
    pdf.savefig(bbox_inches='tight')
    plt.close()

    for aj,ai in enumerate([i_mechanics,i_categories]):
        for a in range(5):
            ii = [ i for i in range(len(data)) if attrs[aj][a] in data[i][ai] ]
            plt.scatter(
                *zip(*(X2D[i] for i in ii)),
                s=1,alpha=0.5, linewidth=0,
                c= [ ratings[i] for i in ii ],
                cmap='rainbow', vmin=rmin, vmax=rmax)
            plt.xlim(*lim[0])
            plt.ylim(*lim[1])
            plt.title('PCA '+(['Mechanics','Category'][aj])+' '+attrs[aj][a])
            pdf.savefig(bbox_inches='tight')
            plt.close()

