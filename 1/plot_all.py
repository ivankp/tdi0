#!/usr/bin/env python3

import json
from collections import defaultdict

print('reading')
with open('bgg_data_clean.json') as f:
    games = json.load(f)

cols  = games['columns']
index = games['index']
data  = games['data']

for i,x in enumerate(cols):
    locals()['i_'+x] = i

years = list(range(2000,2022))
rating_all = [ [0,0] for _ in years ]
bayes_rating_all = [ [0,0] for _ in years ]

print('processing')
for g in data:
    i = g[i_year]-2000

    ry = rating_all[i]
    ry[0] += 1
    ry[1] += g[i_rating]

    ry = bayes_rating_all[i]
    ry[0] += 1
    ry[1] += g[i_bayes_rating]

rating_all = [ x/n for n,x in rating_all ]
bayes_rating_all = [ x/n for n,x in bayes_rating_all ]

# print(rating_all)
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

with PdfPages('fig/all_ratings.pdf') as pdf:
    plt.plot(years,bayes_rating_all, linestyle='-', marker='o', label='Adjusted rating')
    plt.plot(years,rating_all, linestyle='-', marker='o', label='Raw rating')
    plt.legend()
    pdf.savefig(bbox_inches='tight')
    plt.close()

    cnt, bins = np.histogram([ x[i_bayes_rating] for x in data ],80,[0,10],density=True)
    n = len(cnt)
    plt.errorbar(
        [ (bins[i]+bins[i+1])/2 for i in range(n) ],
        cnt,
        None,
        [ (bins[i+1]-bins[i])/2 for i in range(n) ],
        ' ', linewidth=2, label='Adjusted rating')

    cnt, bins = np.histogram([ x[i_rating] for x in data ],80,[0,10],density=True)
    n = len(cnt)
    plt.errorbar(
        [ (bins[i]+bins[i+1])/2 for i in range(n) ],
        cnt,
        None,
        [ (bins[i+1]-bins[i])/2 for i in range(n) ],
        ' ', linewidth=2, label='Raw rating')

    ax = plt.gca()
    ax.set_yscale('log')
    plt.xlim(0,10)
    # plt.ylim(0,None)
    plt.legend()
    pdf.savefig(bbox_inches='tight')
    plt.close()

