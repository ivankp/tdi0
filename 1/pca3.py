#!/usr/bin/env python3

import json, math
import numpy as np
from sklearn.decomposition import PCA
from collections import defaultdict

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

rating_range = [math.inf,-math.inf]

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
    r = g[i_rating]
    if r < rating_range[0]:
        rating_range[0] = r
    if r > rating_range[1]:
        rating_range[1] = r

rating_range = [ f(x) for f,x in zip([math.floor,math.ceil],rating_range) ]

print('PCA 2')
pca2 = PCA(n_components=2)
X2D = pca2.fit_transform(X)

polygons = [[
[-0.6233733036393774, 0.7308384305525926],
[-0.7620179840791842, 0.8473042295711546],
[-0.7620179840791842, 1.0103563481971414],
[-0.6192955189205596, 1.0988703554512487],
[-0.46026191488666357, 1.0616012997653086],
[-0.31753944972803905, 0.9078664450608067],
[-0.35016172747858176, 0.7401556944740775],
[-0.4765730537619348, 0.7075452707488801]
],[
[-0.6641511508275559, 0.4839309366332414],
[-0.790562477110909, 0.40007556133987654],
[-1.0189184213647082, 0.4885895685939836],
[-1.0637740532717046, 0.7494729583955626],
[-0.8761959562060837, 0.8333283336889272],
[-0.6723067202651916, 0.6795934789844253]
],[
[-0.5581287481382917, 0.260316602517602],
[-0.5581287481382917, 0.4233687211435888],
[-0.4113284982608496, 0.5118827283976959],
[-0.18705033872586796, 0.45132051290804376],
[-0.138116922100054, 0.2975856582035421],
[-0.23598375535168215, 0.17180259526349495],
[-0.40317292882321376, 0.18111985918497986]
],[
[-0.9006626645189908, 0.2649752344783449],
[-0.7293957063286414, 0.28360976232131474],
[-0.5540509634194739, 0.19043712310646477],
[-0.3868617899479423, -0.000566787283976744],
[-0.4888064079183885, -0.14032574610625126],
[-0.8109514007049982, -0.14032574610625126],
[-0.9781405741765299, -0.005225419244719198]
],[
[-0.12180578322478253, -0.42450229571154274],
[-0.32161723444685686, -0.32201239257520786],
[-0.32161723444685686, -0.15430164198847862],
[-0.12588356794360034, -0.005225419244719198],
[0.10655016102901671, -0.08442216257734136],
[0.09839459159138109, -0.2987192327714956]
],[
[-0.39909514410439595, -0.29406060081075314],
[-0.13403913738123596, -0.4571127194367395],
[-0.13403913738123596, -0.5735785184553017],
[-0.4357952065737567, -0.731972005120546],
[-0.6600733661087379, -0.6294821019842116],
[-0.6600733661087379, -0.41052639982931494]
],[
[0.037227820809113465, -0.5642612545338164],
[-0.06471679716133272, -0.6993615813953489],
[0.04538339024674931, -0.8484378041391079],
[0.33082832056399836, -0.8111687484531682],
[0.3756839524709945, -0.6341407339449536]
],[
[0.338983890001634, -0.9043413876680177],
[0.2778171192193666, -0.9369518113932154],
[0.3879173066274477, -1.2444215208022187],
[0.5958843272871586, -1.2910078404096437],
[0.5632620495366152, -1.0906866660977168],
[0.4205395843779911, -0.9183172835502451]
]]

def contains(polygon, point):
    n = len(polygon)
    x0, y0 = polygon[n-1]
    x, y = point
    inside = False

    for i in range(n):
        p = polygon[i]
        x1, y1 = p
        if ((y1>y)!=(y0>y)) and (x<(x0-x1)*(y-y1)/(y0-y1)+x1):
            inside = not inside
        x0 = x1
        y0 = y1

    return inside;

group_ratings = [ [] for _ in range(len(polygons)) ]
group_summary = [ None for _ in range(len(polygons)) ]

for pi,polygon in enumerate(polygons):
    print(f'\narea {pi+1}:')
    local_attrs = [ defaultdict(int) for a in attrs ]
    gn = 0
    for g,p in zip(data,X2D):
        if contains(polygon,p):
            for j,i in enumerate([i_mechanics,i_categories]):
                for a in g[i]:
                    local_attrs[j][a] += 1
            group_ratings[pi].append(g[i_rating])
            gn += 1
    gs = [ gn, [], [] ]
    group_summary[pi] = gs
    for a,aname,s in zip(local_attrs,['Mechanics','Categories'],gs[1:]):
        print(f'  {aname}:')
        for k,n in sorted(a.items(),key=lambda x:x[1],reverse=True)[:5]:
            print(f'    {n:4} {k}')
            s.append([n*100/gn,k])

nbins = (rating_range[1]-rating_range[0])*4
hists = [ np.histogram(gr,nbins,rating_range,density=True) for gr in group_ratings ]
mean_stdev = sorted((
        [i,np.mean(gr),np.std(gr)] for i,gr in enumerate(group_ratings)
    ), key=lambda x: x[1], reverse=True)


with open('pca_groups_summary.json','w') as f:
    json.dump(
        [ [i+1,[m,s],*group_summary[i]] for i,m,s in mean_stdev ],
        f,separators=(',',':'))

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patheffects as PathEffects

lim = [[-1.3,2.7],[-1.4,2.1]]

with PdfPages('pca3.pdf') as pdf:
    plt.scatter(*X2D.T,s=2,alpha=0.5, linewidth=0)
        # c=[ 'r' if contains(polygons[0],p) else 'b' for p in X2D ]
    plt.xlim(*lim[0])
    plt.ylim(*lim[1])
    plt.title('PCA')

    for pi,pts in enumerate(polygons):
        plt.plot(*zip(*pts,pts[0]),'r-')
        txt = plt.text(
            sum( x for x,y in pts )/len(pts),
            sum( y for x,y in pts )/len(pts),
            f'{pi+1}', c='r', ha='center', va='center')
        txt.set_path_effects([
            PathEffects.withStroke(linewidth=3,foreground='w',alpha=0.75)])

    pdf.savefig(bbox_inches='tight')
    plt.close()

    plt.title('Rating distributions')
    for (hi, mean, stdev), c in zip(
        mean_stdev,
        plt.cm.rainbow(np.linspace(1,0,len(hists)))
    ):
        cnt, bins = hists[hi]
        n = len(cnt)
        # plt.hist(bins[:-1], bins, weights=cnt)
        plt.errorbar(
            [ (bins[i]+bins[i+1])/2 for i in range(n) ],
            cnt,
            None,
            [ (bins[i+1]-bins[i])/2 for i in range(n) ],
            ' ', linewidth=2, label=f'{hi+1}: {mean:.2f}±{stdev:.2f}',
            c=c)

    plt.xlim(4,9)
    plt.ylim(0,0.65)
    plt.legend()
    pdf.savefig(bbox_inches='tight')
    plt.close()
