#!/usr/bin/env python3

import json

with open('characteristics_frequency.json') as f:
    freq = json.load(f)

for m in freq['all']:
    m = [ x for x in m if x[1]>100 ]

    print()
    for x in m:
        print('%5d %s' % (x[1],x[0]))

    print()
    for x in sorted(m,key=lambda x: x[2],reverse=True):
        print('%.3f %s' % (x[2],x[0]))

    print()
    for x in sorted(m,key=lambda x: x[3],reverse=True):
        print('%.3f %s' % (x[3],x[0]))
