#!/usr/bin/env python3

import json

with open('characteristics_frequency.json') as f:
    freq = json.load(f)

print('mechanics:' ,len(freq['all'][0]))
print('categories:',len(freq['all'][1]))

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

with PdfPages('fig/attrs.pdf') as pdf:
    for j,m in enumerate(['Mechanics','Categories']):
        plt.barh(*[*zip(*reversed(freq['all'][j][:20]))][:2])

        plt.title(m)
        pdf.savefig(bbox_inches='tight')
        plt.close()

