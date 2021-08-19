#!/usr/bin/env python3

import json
from collections import defaultdict

print('reading')
with open('../bgg_data_clean.json') as f:
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
# from matplotlib import rc
# rc('text', usetex=True)
# rc('font', family='serif', size=12)

plt.plot(years,bayes_rating_all, linestyle='-', marker='o')
plt.plot(years,rating_all, linestyle='-', marker='o')
plt.savefig('plot.pdf', bbox_inches='tight')

