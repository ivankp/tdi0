#!/usr/bin/env python3

import json
import numpy as np

with open('characteristics_frequency.json') as f:
    freq = json.load(f)

attrs = [
    [ x[0] for x in freq['all'][j] if x[1]>100 ]
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

print('SVD')
U, s, Vt = np.linalg.svd(X)

# print(s)
# print(X)
# for i in range(2):
#     print(f'component {i}')
#     print(Vt.T[:,i])

print('writing')
# np.savez_compressed('pca.npz',U=U,s=s,V=Vt.T)
with open('pca1.json','w') as f:
    json.dump({
        's': s.tolist(),
        'V': Vt.T.tolist()
    },f,separators=(',',':'))

