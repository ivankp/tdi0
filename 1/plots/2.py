#!/usr/bin/env python3

import json

with open('../characteristics_frequency.json') as f:
    data = json.load(f)

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# from matplotlib import rc
# rc('text', usetex=True)
# rc('font', family='serif', size=12)

mechs = [ x[:2] for x in data['all'][0] if x[1]>1000 ]

with PdfPages('multipage_pdf.pdf') as pdf:
    for m, n in mechs:
        print(n,m)
        years  = [ ]
        rating = [ ]
        for i,y in enumerate(data['yearly']):
            x = next((x for x in y[0] if x[0]==m),None)
            if not (x is None):
                years .append(i+2000)
                rating.append(x[3])

        plt.figure(figsize=(10,4))
        plt.plot(years, rating, 'b-o')
        plt.title(f'{m} {n}')
        pdf.savefig(bbox_inches='tight')
        plt.close()

