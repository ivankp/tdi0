#!/usr/bin/env python3

import json

with open('pca_groups_summary.json') as f:
    data = json.load(f)

def make_row(r,col):
    if r==1:
        return f'{col[0]:.2f}±{col[1]:.2f}'
    elif r==3 or r==4:
        s = '<table>'
        for n,a in col:
            s += f'<tr><td>{n:.0f}%</td><td>{a}</td></tr>'
        s += '</table>'
        return s
    else:
        return f'{col}'

with open('pca_groups_summary.html','w') as out:
    out.write('<table>')
    for r,row in enumerate(zip(*data)):
        s = ''
        if r==0:
            s = 'group'
        elif r==1:
            s = 'mean±stdev'
        elif r==2:
            s = 'N games'
        elif r==3:
            s = 'Mechanics'
        elif r==4:
            s = 'Categories'
        out.write('<tr><td>'+s+'</td>')
        for col in row:
            out.write('<td>'+make_row(r,col)+'</td>')
        out.write('</tr>')
    out.write('</table>')
