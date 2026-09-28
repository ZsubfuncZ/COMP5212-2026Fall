#!/usr/bin/env python3
"""Reproduce constructed tree/bagging figures with Python standard library only.

Data: n=64 training rows and n=800 independent validation rows, uniform X on
[0,1], Y=2+sin(2*pi*X)+0.8*X+N(0,0.32^2). Seed=5212. Greedy univariate CART
minimizes child SSE, root depth=0; all plots and CSVs are deterministic.
"""
from pathlib import Path
import csv, json, math, random
ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT/'figures'
RNG = random.Random(5212)
def mean(v): return sum(v)/len(v)
def target(x): return 2+math.sin(2*math.pi*x)+0.8*x
def sample(n):
    xs=sorted(RNG.random() for _ in range(n))
    return [(x,target(x)+RNG.gauss(0,.32)) for x in xs]
train,valid=sample(64),sample(800)
def sse(rows):
    if not rows: return 0.
    sy=sum(y for x,y in rows)
    return sum(y*y for x,y in rows)-sy*sy/len(rows)
def fit(rows,depth,maxdepth):
    rows=sorted(rows)
    node={'value':mean([y for x,y in rows]), 'n':len(rows)}
    if depth>=maxdepth or len(rows)<2: return node
    candidates=[]
    for i in range(1,len(rows)):
        if rows[i-1][0] == rows[i][0]: continue
        candidates.append((sse(rows[:i])+sse(rows[i:]),(rows[i-1][0]+rows[i][0])/2,i))
    if not candidates: return node
    loss,cut,i=min(candidates)
    if sse(rows)-loss<1e-12: return node
    node.update(cut=cut,left=fit(rows[:i],depth+1,maxdepth),right=fit(rows[i:],depth+1,maxdepth))
    return node
def pred(tree,x):
    if 'cut' not in tree: return tree['value']
    return pred(tree['left'] if x<=tree['cut'] else tree['right'],x)
def mse(tree,rows): return mean([(y-pred(tree,x))**2 for x,y in rows])
def pieces(tree,lo=0,hi=1):
    if 'cut' not in tree: return [(lo,tree['value']),(hi,tree['value'])]
    return pieces(tree['left'],lo,tree['cut'])+pieces(tree['right'],tree['cut'],hi)
def coords(values): return ' '.join(f'({x:.6g},{y:.6g})' for x,y in values)
def plot(values,style):return '\\addplot['+style+'] coordinates {'+coords(values)+'};\n'
def axis(body,extra='',height='4.5cm'):
    return r'\begin{tikzpicture}'+'\n'+r'\begin{axis}[width=\linewidth,height='+height+r',axis lines=left,xmin=0,xmax=1,ymin=0.7,ymax=4.0,xlabel={$x$},ylabel={$y$},tick label style={font=\scriptsize},label style={font=\small},legend style={font=\scriptsize,draw=none,at={(0.5,1.04)},anchor=south,legend columns=3},clip=false,'+extra+']\n'+body+r'\end{axis}'+'\n'+r'\end{tikzpicture}'+'\n'
def write(name,text): (FIG/('foundations-'+name+'.tex')).write_text(text)
grid=[i/200 for i in range(201)]
xs=[r[0] for r in train]; ys=[r[1] for r in train]
xbar,ybar=mean(xs),mean(ys)
beta=sum((x-xbar)*(y-ybar) for x,y in train)/sum((x-xbar)**2 for x in xs)
a=ybar-beta*xbar
points=plot(train,'only marks,mark=*,mark size=1.25pt,blueplot,opacity=.7')
truth=plot([(x,target(x)) for x in grid],'inkplot,dashed,thick')
write('motivation',axis(points+r'\addlegendentry{Data}'+plot([(0,a),(1,a+beta)],'redplot,very thick')+r'\addlegendentry{OLS}'+truth+r'\addlegendentry{True mean}'))
shallow=fit(train,0,2)
write('partition',axis(points+r'\addlegendentry{Data}'+plot(pieces(shallow),'redplot,very thick')+r'\addlegendentry{Tree}'+truth+r'\addlegendentry{True mean}'))
depthresults=[]
for d in range(1,11):
    tree=fit(train,0,d)
    depthresults.append((d,mse(tree,train),mse(tree,valid)))
deep=fit(train,0,8)
write('depth-fit',axis(points.replace('only marks,','forget plot,only marks,')+plot(pieces(shallow),'blueplot,very thick')+r'\addlegendentry{Depth 2}'+plot(pieces(deep),'redplot,thick')+r'\addlegendentry{Depth 8}',height='3.85cm'))
write('depth-error',r'''\begin{tikzpicture}
\begin{axis}[width=\linewidth,height=3.85cm,axis lines=left,xmin=1,xmax=10,ymin=0,ymax=.36,xlabel={Maximum depth},ylabel={MSE},xtick={2,4,6,8,10},tick label style={font=\scriptsize},label style={font=\small},legend style={font=\scriptsize,draw=none,at={(.5,1.04)},anchor=south,legend columns=2}]
'''+plot([(d,tr) for d,tr,va in depthresults],'blueplot,thick,mark=*')+r'\addlegendentry{Training}'+plot([(d,va) for d,tr,va in depthresults],'redplot,thick,mark=square*')+r'\addlegendentry{Validation}'+r'\end{axis}\end{tikzpicture}')
boots=[]; trees=[]
for b in range(100):
    inds=[RNG.randrange(len(train)) for _ in train]
    boots.append(inds); trees.append(fit([train[i] for i in inds],0,8))
avg=lambda x:mean([pred(t,x) for t in trees])
body=''
for i,t in enumerate(trees[:3]):
    body+=plot(pieces(t),'lightplot,thin,opacity=.9'+(',forget plot' if i>0 else ''))
    if i==0: body+=r'\addlegendentry{Trees}'
body+=plot([(x,avg(x)) for x in grid],'blueplot,very thick')+r'\addlegendentry{Mean (100)}'+truth+r'\addlegendentry{Truth}'
write('bootstrap',axis(body,height='3.85cm'))
write('correlation',r'''\begin{tikzpicture}
\begin{axis}[width=.97\linewidth,height=4.5cm,axis lines=left,xmin=1,xmax=100,ymin=0,ymax=1.02,xlabel={Number of trees $B$},ylabel={$\operatorname{Var}(\bar f)/v$},xtick={1,20,40,60,80,100},tick label style={font=\scriptsize},label style={font=\small},legend style={font=\scriptsize,draw=none,at={(.5,1.04)},anchor=south,legend columns=3}]
'''+''.join(plot([(b,rho+(1-rho)/b) for b in range(1,101)],style)+f'\\addlegendentry{{$\\rho={rho:g}$}}\n' for rho,style in [(0,'blueplot,thick'),(.2,'redplot,thick'),(.8,'inkplot,dashed,thick')])+r'\end{axis}\end{tikzpicture}')
report={'seed':5212,'n_train':64,'n_validation':800,'noise_sd':.32,'root_depth':0,'depth_results':[{'depth':d,'train_mse':tr,'validation_mse':va} for d,tr,va in depthresults], 'ols_intercept':a,'ols_slope':beta,'tree_depth2':shallow,'bootstrap_B':100,'single_depth8_valid_mse':mse(deep,valid),'bagged_valid_mse':mean([(y-avg(x))**2 for x,y in valid]),'oob_fraction_mean':mean([1-len(set(b))/len(train) for b in boots]),'six_point_sse_threshold_2.5':sse([(1,1),(2,1)])+sse([(3,2),(4,5),(5,6),(6,6)]),'six_point_sse_threshold_3.5':sse([(1,1),(2,1),(3,2)])+sse([(4,5),(5,6),(6,6)])}
(ROOT/'examples'/'foundations-results.json').write_text(json.dumps(report,indent=2)+'\n')
with (ROOT/'examples'/'foundations-data.csv').open('w') as f:
    writer=csv.writer(f);writer.writerow(['split','x','y','true_mean'])
    for split,rows in [('training',train),('validation',valid)]:writer.writerows((split,x,y,target(x)) for x,y in rows)
with (ROOT/'examples'/'foundations-bootstrap-indices.csv').open('w') as f:
    writer=csv.writer(f);writer.writerow(['tree','draw','training_row_zero_based'])
    writer.writerows((b,j,i) for b,inds in enumerate(boots) for j,i in enumerate(inds))
# Algorithm checks: exhaustive split threshold and exact leaf mean on toy data.
toy=fit([(1,1),(2,1),(3,2),(4,5),(5,6),(6,6)],0,1)
assert toy['cut']==3.5
assert abs(toy['left']['value']-4/3)<1e-12
assert abs(toy['right']['value']-17/3)<1e-12
assert all(depthresults[i+1][1]<=depthresults[i][1]+1e-12 for i in range(9))
assert abs(report['six_point_sse_threshold_3.5']-4/3)<1e-12
print(json.dumps({k:v for k,v in report.items() if k!='tree_depth2'},indent=2))
print('PASS: exhaustive split, leaf means, training SSE monotonicity, exact example.')
