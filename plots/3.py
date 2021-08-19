#!/usr/bin/env python3

import json

with open('../characteristics_frequency.json') as f:
    freq = json.load(f)

# mechs = [ x[0] for x in freq['all'][0] if x[1]>1000 ]
mechs = [ x[0] for x in freq['all'][1] if x[1]>1000 ]
print(len(mechs))

with open('../bgg_data_clean.json') as f:
    games = json.load(f)

cols  = games['columns']
data  = games['data']

for i,x in enumerate(cols):
    locals()['i_'+x] = i

years = list(range(2000,2022))

avg = [ [ [[0,0],[0,0]] for _ in years ] for m in mechs ]

for g in data:
    skip = True
    # gm = g[i_mechanics]
    gm = g[i_categories]
    for m in gm:
        if m in mechs:
            skip = False
            break
    if skip:
        continue
    for i,m in enumerate(mechs):
        r = avg[i][g[i_year]-2000][0 if m in gm else 1]
        r[0] += 1
        r[1] += g[i_rating]
        # r[1] += g[i_bayes_rating]
        # r[1] += g[i_num_expansions]

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

with PdfPages('avg_over_time.pdf') as pdf:
    for m,rs in zip(mechs,avg):
        plt.figure(figsize=(10,4))
        plt.plot( *zip(*( (y,r/n) for y,((n,r),_) in zip(years,rs) if n>0 )),
            '-o', label='this' )
        plt.plot( *zip(*( (y,r/n) for y,(_,(n,r)) in zip(years,rs) if n>0 )),
            '-o', label='other' )
        plt.title(m)
        plt.legend()
        pdf.savefig(bbox_inches='tight')
        plt.close()

