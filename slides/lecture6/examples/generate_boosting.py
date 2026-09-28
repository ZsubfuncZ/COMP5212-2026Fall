"""Reproduce the lecture's constructed boosting data, plots and arithmetic.
Python standard library only.
The CART/boosting implementation is deliberately small and pedagogical.
"""
from pathlib import Path
import csv, json, math, random
ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures'
OUT=ROOT/'examples'
FIG.mkdir(exist_ok=True)

def mean(v): return sum(v)/len(v)
def truth(x): return math.sin(1.6*x)+0.22*x

def fit_tree(x, y, depth=2, min_leaf=3):
    prediction=mean(y)
    node={'value':prediction}
    if depth==0 or len(x)<2*min_leaf: return node
    best=None
    for k in range(min_leaf,len(x)-min_leaf+1):
        if x[k-1]==x[k]: continue
        left,right=mean(y[:k]),mean(y[k:])
        sse=sum((v-left)**2 for v in y[:k])+sum((v-right)**2 for v in y[k:])
        if best is None or sse<best[0]: best=(sse,k,(x[k-1]+x[k])/2)
    if best is None: return node
    _,k,cut=best
    node.update(cut=cut,left=fit_tree(x[:k],y[:k],depth-1,min_leaf),right=fit_tree(x[k:],y[k:],depth-1,min_leaf))
    return node

def predict(tree, x):
    while 'cut' in tree: tree=tree['left'] if x<=tree['cut'] else tree['right']
    return tree['value']

def coords(x,y): return ' '.join(f'({a:.8g},{b:.8g})' for a,b in zip(x,y))
def plot(x,y,style): return '\\addplot['+style+'] coordinates {'+coords(x,y)+'};\n'
BASE=r'''font=\scriptsize,tick label style={font=\scriptsize},label style={font=\scriptsize},
axis line style={black!50},grid=major,grid style={black!10},scaled ticks=false,
legend style={font=\scriptsize,draw=none,fill=white,legend cell align=left},'''
def axis(body, options):
    return '\\begin{tikzpicture}\n\\begin{axis}[\n'+BASE+'\n'+options+'\n]\n'+body+'\\end{axis}\n\\end{tikzpicture}\n'

def write_fig(name,body): (FIG/(name+'.tex')).write_text('% Original reproducible teaching example. See examples/generate_boosting.py.\n'+body)

rng=random.Random(521223)
x=sorted(rng.uniform(0,6) for _ in range(60))
y=[truth(v)+rng.gauss(0,.38) for v in x]
xval=[rng.uniform(0,6) for _ in range(500)]
yval=[truth(v)+rng.gauss(0,.38) for v in xval]
grid=[6*i/400 for i in range(401)]
f0=mean(y); p=[f0]*len(x); pv=[f0]*len(xval); pg=[f0]*len(grid)
eta=.12
runs=[]; checkpoints={0:list(pg)}
for m in range(301):
    runs.append((m,mean([(a-b)**2 for a,b in zip(y,p)]),mean([(a-b)**2 for a,b in zip(yval,pv)])))
    if m in [1,10,60,300]: checkpoints[m]=list(pg)
    if m==300: break
    t=fit_tree(x,[a-b for a,b in zip(y,p)])
    p=[a+eta*predict(t,v) for a,v in zip(p,x)]
    pv=[a+eta*predict(t,v) for a,v in zip(pv,xval)]
    pg=[a+eta*predict(t,v) for a,v in zip(pg,grid)]
assert all(runs[i+1][1]<=runs[i][1]+1e-12 for i in range(300))
best=min(runs,key=lambda z:z[2])
body=plot(x,y,'only marks,mark=*,mark size=1.2pt,black!40,forget plot')
body+=plot(grid,[truth(v) for v in grid],'black,dashed,thick')+'\\addlegendentry{True mean}\n'
for m,col in [(1,'redplot'),(10,'blueplot'),(60,'green!45!black')]:
    body+=plot(grid,checkpoints[m],col+',thick')+f'\\addlegendentry{{Round {m}}}\n'
write_fig('boosting-fit',axis(body,r'width=.97\linewidth,height=4.7cm,xmin=0,xmax=6,ymin=-1.2,ymax=3.0,xlabel={Input $x$},ylabel={Response / prediction},legend columns=4,legend style={at={(.5,1.02)},anchor=south}'))
body=plot([z[0] for z in runs],[z[1] for z in runs],'blueplot,very thick')+'\\addlegendentry{Training MSE}\n'
body+=plot([z[0] for z in runs],[z[2] for z in runs],'redplot,very thick')+'\\addlegendentry{Validation MSE}\n'
body+=plot([best[0],best[0]],[0,.9],'black,dashed,forget plot')
body+=f'\\node[anchor=north west,font=\\scriptsize,fill=white,inner sep=2pt] at (axis cs:{best[0]+3},.87) {{Best validation: {best[0]} rounds}};\n'
write_fig('boosting-loss',axis(body,r'width=.97\linewidth,height=4.7cm,xmin=0,xmax=300,ymin=0,ymax=.95,xlabel={Number of corrections},ylabel={Mean squared error},legend pos=north east'))
# Exact, small squared-error illustration.
body=plot([1,2,3,4],[1,1,3,3],'black,only marks,mark=*,mark size=2.4pt')+'\\addlegendentry{Observed $y$}\n'
body+=plot([.6,4.4],[2,2],'black!60,dashed,thick')+'\\addlegendentry{$F_0=2$}\n'
body+=plot([.6,2.5,2.5,4.4],[1.5,1.5,2.5,2.5],'blueplot,very thick')+'\\addlegendentry{$F_1$}\n'
write_fig('boosting-residual',axis(body,r'width=\linewidth,height=4.0cm,xmin=.6,xmax=4.4,ymin=.5,ymax=3.8,xtick={1,2,3,4},xlabel={$x$},ylabel={Response / prediction},legend columns=3,legend style={at={(.5,1.02)},anchor=south}'))
# Three successive corrections in the exact four-point example.
round_rows=[]
pieces=[r'\begin{tikzpicture}']
for m in [1,2,3]:
    prev=2**(-(m-1)); after=prev/2
    old=[1+prev,1+prev,3-prev,3-prev]
    new=[1+after,1+after,3-after,3-after]
    residual=[-prev,-prev,prev,prev]
    round_rows.append({'round':m,'residual_targets':residual,'predictions':new,'mse':after**2})
    assert abs(mean([(a-b)**2 for a,b in zip([1,1,3,3],new)])-4**(-m))<1e-12
    xpos=(m-1)*4.35
    top=plot([1,2,3,4],[1,1,3,3],'black,only marks,mark=*,mark size=1.7pt')
    top+=plot([.6,2.5,2.5,4.4],[old[0],old[0],old[2],old[2]],'black!50,dashed,thick')
    top+=plot([.6,2.5,2.5,4.4],[new[0],new[0],new[2],new[2]],'blueplot,very thick')
    options=rf'scale only axis,width=2.7cm,height=1.05cm,at={{({xpos}cm,1.85cm)}},anchor=south west,xmin=.6,xmax=4.4,ymin=.7,ymax=3.3,xtick={{1,2,3,4}},xticklabels=,ytick={{1,2,3}},title={{Round {m}}},title style={{font=\small}},ylabel={{$F_{m-1}\to F_{m}$}}'
    pieces.append('\\begin{axis}['+BASE+options+']\n'+top+'\\end{axis}')
    bottom=plot([.6,4.4],[0,0],'black!40,dashed')
    bottom+=plot([1,2,3,4],residual,'redplot,only marks,mark=*,mark size=1.7pt')
    bottom+=plot([.6,2.5,2.5,4.4],[-prev,-prev,prev,prev],'redplot,very thick')
    options=rf'scale only axis,width=2.7cm,height=1.05cm,at={{({xpos}cm,0cm)}},anchor=south west,xmin=.6,xmax=4.4,ymin=-1.15,ymax=1.15,xtick={{1,2,3,4}},ytick={{-1,0,1}},xlabel={{$x$}},ylabel={{$r_{m}=h_{m}$}}'
    pieces.append('\\begin{axis}['+BASE+options+']\n'+bottom+'\\end{axis}')
pieces.append(r'\end{tikzpicture}')
write_fig('boosting-rounds','\n'.join(pieces)+'\n')

# Check the logistic-loss gradient at several non-extreme scores.
def bce(z,y): return max(z,0)-y*z+math.log1p(math.exp(-abs(z)))
errs=[]
for z in [-3.,-.4,0.,1.2,4.]:
    pi=1/(1+math.exp(-z))
    for label in [0,1]:
        e=1e-4
        gd=(bce(z+e,label)-bce(z-e,label))/(2*e)
        errs.append(abs(gd-(pi-label)))
assert max(errs)<1e-8
# Write plot source data and report.
with (OUT/'boosting-trajectories.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['trees','training_mse','validation_mse']);w.writerows(runs)
with (OUT/'boosting-training-data.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['x','y']);w.writerows(zip(x,y))
with (OUT/'boosting-validation-data.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['x','y']);w.writerows(zip(xval,yval))
report={'seed':521223,'n_train':60,'n_validation':500,'noise_sd':.38,'depth':2,'min_leaf':3,'learning_rate':eta,'rounds':300,'best_validation_round':best[0],'best_validation_mse':best[2],'final_training_mse':runs[-1][1],'final_validation_mse':runs[-1][2],'max_gradient_check_error':max(errs),'four_point_rounds':round_rows}
(OUT/'boosting-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
print('PASS: logistic-loss gradient and training-loss monotonicity.')
