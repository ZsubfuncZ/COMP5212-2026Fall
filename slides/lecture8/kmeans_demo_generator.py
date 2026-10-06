#!/usr/bin/env python3
"""Generate the 2-D browser demo and its static slide preview."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


ROOT = Path(__file__).resolve().parent
ASSET_DIR = ROOT / "assets"
ORANGE = "#FF5500"
GREEN = "#4C7954"
BLUE = "#6F8296"
PALETTE = [ORANGE, GREEN, BLUE]


def main() -> None:
    # The slide preview is deterministic. The browser can generate fresh data
    # with any true class count from 2 through 20.
    X, y = make_blobs(
        n_samples=180,
        centers=[[-2.0, 0.0], [2.0, 0.0], [0.0, 2.6]],
        cluster_std=[1.0, 1.0, 0.9],
        random_state=0,
    )
    random_initializations = {
        "random A": [106, 122, 2],
        "random B": [152, 153, 56],
    }
    results = {}
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.9), sharex=True, sharey=True)
    for ax, (name, indices) in zip(axes, random_initializations.items()):
        init = X[indices]
        model = KMeans(n_clusters=3, init=init, n_init=1, max_iter=100, random_state=0).fit(X)
        results[name] = {
            "indices": indices,
            "inertia": float(model.inertia_),
            "n_iter": int(model.n_iter_),
            "centers": model.cluster_centers_.tolist(),
        }
        for cluster_id, color in enumerate(PALETTE):
            mask = model.labels_ == cluster_id
            ax.scatter(X[mask, 0], X[mask, 1], s=19, alpha=0.70, color=color, linewidths=0)
        ax.scatter(
            init[:, 0], init[:, 1], s=95, facecolors="none", edgecolors="#222222",
            linewidths=1.3, label="random initial centers",
        )
        ax.scatter(
            model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], marker="X",
            s=150, color="#222222", edgecolor="white", linewidth=1.0, label="final means",
        )
        ax.set_title(
            f"{name}\nfinal SSE = {model.inertia_:.1f}, {model.n_iter_} iterations",
            color=ORANGE, fontweight="bold",
        )
        ax.set_xlabel("feature 1")
        ax.grid(alpha=0.18)
        ax.set_aspect("equal", adjustable="box")
    axes[0].set_ylabel("feature 2")
    axes[1].legend(frameon=False, loc="lower right")
    fig.suptitle(
        "Same 2-D data, independent random Lloyd starts",
        color=ORANGE, fontsize=17, fontweight="bold", y=1.02,
    )
    fig.text(
        0.5, 0.015,
        "Synthetic blobs · K = 3 · hollow circles are random initial centers · X markers are final means",
        ha="center", fontsize=10, color="#4E5B64",
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.88])
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(ASSET_DIR / "fig_initialization_demo.png", dpi=220, bbox_inches="tight")
    fig.savefig(ASSET_DIR / "fig_initialization_demo.pdf", bbox_inches="tight")
    plt.close(fig)

    payload = {"points": X.tolist(), "true_labels": y.tolist(), "true_k": 3}
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    html = HTML_TEMPLATE.replace("__DATA__", data)
    (ROOT / "kmeans_demo.html").write_text(html, encoding="utf-8")
    (ROOT / "kmeans_demo_data.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({"figure": "assets/fig_initialization_demo.pdf", "demo": "kmeans_demo.html", "results": results}, indent=2))


HTML_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2-D K-means: random data and random Lloyd starts</title>
<style>
  :root { --orange:#ff5500; --green:#4c7954; --ink:#1e2428; --muted:#64727d; }
  body { margin:0; background:#f7f8f9; color:var(--ink); font-family:system-ui,-apple-system,Segoe UI,sans-serif; }
  main { max-width:980px; margin:24px auto; padding:0 18px 32px; }
  h1 { margin:0 0 6px; color:var(--orange); font-size:clamp(24px,4vw,38px); }
  p { margin:6px 0 12px; color:var(--muted); }
  .toolbar { display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin:14px 0; }
  .control { display:inline-flex; align-items:center; gap:6px; white-space:nowrap; }
  input[type=range] { width:132px; accent-color:var(--orange); }
  output { display:inline-block; min-width:1.5em; font-weight:700; color:var(--orange); text-align:center; }
  select,button { font:inherit; border-radius:6px; padding:8px 11px; border:1px solid #bbc5cc; background:white; cursor:pointer; }
  button.primary { background:var(--orange); color:white; border-color:var(--orange); }
  button:hover { filter:brightness(.97); }
  canvas { display:block; width:100%; max-width:900px; background:white; border:1px solid #ccd4d9; border-radius:8px; }
  .stats { display:flex; gap:12px; flex-wrap:wrap; margin-top:12px; font-variant-numeric:tabular-nums; }
  .card { background:white; border-left:4px solid var(--green); padding:10px 14px; border-radius:5px; box-shadow:0 1px 2px #00000010; }
</style>
</head>
<body>
<main>
  <h1>2-D K-means: random data and random Lloyd starts</h1>
  <p>Generate a fresh set of Gaussian-like blobs, choose its true number of classes, then run Lloyd's algorithm with a separate value of <em>K</em>.</p>
  <div class="toolbar">
    <label class="control" for="dataK">data classes K<sub>true</sub>:
      <input id="dataK" type="range" min="2" max="20" step="1" value="3"><output id="dataKValue">3</output>
    </label>
    <label class="control" for="algorithmK">algorithm K:
      <input id="algorithmK" type="range" min="2" max="20" step="1" value="3"><output id="algorithmKValue">3</output>
    </label>
    <button id="newData" class="primary">New random data</button>
    <button id="reset">Resample centers</button>
    <button id="step">One iteration</button>
    <button id="run" class="primary">Run to convergence</button>
  </div>
  <canvas id="plot" width="900" height="500"></canvas>
  <div class="stats">
    <div class="card">data K<sub>true</sub>: <strong id="dataKStat">3</strong></div>
    <div class="card">algorithm K: <strong id="algorithmKStat">3</strong></div>
    <div class="card">iteration: <strong id="iteration">0</strong></div>
    <div class="card">SSE: <strong id="sse">—</strong></div>
    <div class="card">status: <strong id="status">random initialization</strong></div>
  </div>
  <p>Every reset samples the algorithm's K initial centers uniformly from the data points. Before the first assignment, colors show the generated classes; after a Lloyd step, colors show nearest-center assignments.</p>
</main>
<script>
const DEFAULT_DATA = __DATA__;
const canvas = document.getElementById('plot');
const ctx = canvas.getContext('2d');
const dataKInput = document.getElementById('dataK');
const algorithmKInput = document.getElementById('algorithmK');
let DATA = {points: DEFAULT_DATA.points.map(p=>p.slice()), true_labels: DEFAULT_DATA.true_labels.slice(), true_k: DEFAULT_DATA.true_k};
let algorithmK = Number(algorithmKInput.value);
let centers, labels, iteration, sse, converged, timer, B;
let rngState = (Date.now() ^ Math.floor(Math.random()*0xffffffff)) >>> 0;

function rand() {
  rngState = (1664525 * rngState + 1013904223) >>> 0;
  return rngState / 4294967296;
}
function randn() {
  let u = 0, v = 0;
  while (u === 0) u = rand();
  while (v === 0) v = rand();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}
function distance2(a,b) { const dx=a[0]-b[0], dy=a[1]-b[1]; return dx*dx+dy*dy; }
function colorFor(k,total) {
  const hue = (24 + 360 * k / Math.max(total,1)) % 360;
  return `hsl(${hue.toFixed(1)}, 65%, 45%)`;
}
function generateData(k) {
  const classCenters = [], minDistance2 = 1.15 * 1.15;
  let attempts = 0;
  while (classCenters.length < k && attempts++ < 8000) {
    const candidate = [rand()*8.4-4.2, rand()*5.8-2.9];
    if (classCenters.every(c=>distance2(c,candidate) >= minDistance2)) classCenters.push(candidate);
  }
  if (classCenters.length < k) {
    classCenters.length = 0;
    for (let i=0; i<k; i++) {
      const angle = 2*Math.PI*i/k;
      classCenters.push([3.35*Math.cos(angle), 2.45*Math.sin(angle)]);
    }
  }
  const sigma = k >= 14 ? 0.30 : (k >= 9 ? 0.38 : 0.48);
  const generatedPoints = [], trueLabels = [];
  const pointsPerClass = 18;
  classCenters.forEach((c,k0)=>{
    for (let i=0; i<pointsPerClass; i++) {
      generatedPoints.push([c[0] + sigma*randn(), c[1] + sigma*randn()]);
      trueLabels.push(k0);
    }
  });
  return {points: generatedPoints, true_labels: trueLabels, true_k: k};
}
function bounds() {
  const xs = DATA.points.map(p=>p[0]), ys = DATA.points.map(p=>p[1]);
  return {xmin:Math.min(...xs)-0.8, xmax:Math.max(...xs)+0.8, ymin:Math.min(...ys)-0.8, ymax:Math.max(...ys)+0.8};
}
function updateBounds() { B = bounds(); }
function sx(x) { return 50 + (x-B.xmin)/(B.xmax-B.xmin)*(canvas.width-80); }
function sy(y) { return canvas.height-42 - (y-B.ymin)/(B.ymax-B.ymin)*(canvas.height-75); }
function sampleIndices(n,total) {
  const pool = Array.from({length:total},(_,i)=>i), out=[];
  for (let i=0; i<n; i++) { const j=i+Math.floor(rand()*(total-i)); [pool[i],pool[j]]=[pool[j],pool[i]]; out.push(pool[i]); }
  return out;
}
function assign() {
  labels = DATA.points.map(p=>{ let best=0, bd=Infinity; centers.forEach((c,k)=>{const d=distance2(p,c); if(d<bd){bd=d;best=k;}}); return best; });
  sse = DATA.points.reduce((sum,p,i)=>sum+distance2(p,centers[labels[i]]),0);
}
function updateMeans() {
  const sums = centers.map(()=>[0,0]), counts = centers.map(()=>0);
  DATA.points.forEach((p,i)=>{ const k=labels[i]; sums[k][0]+=p[0]; sums[k][1]+=p[1]; counts[k]++; });
  let movement=0;
  centers = centers.map((c,k)=>{ if(!counts[k]) return c.slice(); const next=[sums[k][0]/counts[k],sums[k][1]/counts[k]]; movement+=distance2(c,next); return next; });
  return movement;
}
function step() {
  if(converged) return;
  assign(); const movement=updateMeans(); iteration++; assign();
  converged = movement < 1e-8;
  document.getElementById('status').textContent = converged ? 'converged' : 'running';
  draw();
}
function reset() {
  clearTimeout(timer);
  const inds=sampleIndices(algorithmK, DATA.points.length);
  centers=inds.map(i=>DATA.points[i].slice());
  iteration=0; labels=null; sse=null; converged=false;
  document.getElementById('status').textContent='random initialization';
  draw();
}
function newData() {
  clearTimeout(timer);
  DATA = generateData(Number(dataKInput.value));
  updateBounds();
  reset();
}
function run() { if(converged) return; step(); if(!converged) timer=setTimeout(run,220); }
function syncControls() {
  dataKInput.nextElementSibling.value = dataKInput.value;
  algorithmKInput.nextElementSibling.value = algorithmKInput.value;
  document.getElementById('dataKStat').textContent = DATA.true_k;
  document.getElementById('algorithmKStat').textContent = algorithmK;
}
function draw() {
  ctx.clearRect(0,0,canvas.width,canvas.height); ctx.fillStyle='white'; ctx.fillRect(0,0,canvas.width,canvas.height);
  ctx.strokeStyle='#cbd4da'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(50,canvas.height-42); ctx.lineTo(canvas.width-30,canvas.height-42); ctx.moveTo(50,canvas.height-42); ctx.lineTo(50,30); ctx.stroke();
  const displayedLabels = labels || DATA.true_labels, displayedK = labels ? centers.length : DATA.true_k;
  DATA.points.forEach((p,i)=>{ ctx.beginPath(); ctx.arc(sx(p[0]),sy(p[1]),4,0,2*Math.PI); ctx.fillStyle=colorFor(displayedLabels[i],displayedK); ctx.globalAlpha=.74; ctx.fill(); ctx.globalAlpha=1; });
  centers.forEach((c,k)=>{ ctx.beginPath(); ctx.arc(sx(c[0]),sy(c[1]),10,0,2*Math.PI); ctx.fillStyle='white'; ctx.fill(); ctx.lineWidth=2; ctx.strokeStyle='#222'; ctx.stroke(); ctx.beginPath(); ctx.moveTo(sx(c[0])-7,sy(c[1])-7); ctx.lineTo(sx(c[0])+7,sy(c[1])+7); ctx.moveTo(sx(c[0])+7,sy(c[1])-7); ctx.lineTo(sx(c[0])-7,sy(c[1])+7); ctx.strokeStyle=colorFor(k,centers.length); ctx.stroke(); });
  document.getElementById('iteration').textContent=iteration;
  document.getElementById('sse').textContent=sse==null?'—':sse.toFixed(1);
  syncControls();
}
dataKInput.addEventListener('input',()=>{ dataKInput.nextElementSibling.value=dataKInput.value; });
dataKInput.addEventListener('change',newData);
algorithmKInput.addEventListener('input',()=>{ algorithmK=Number(algorithmKInput.value); algorithmKInput.nextElementSibling.value=algorithmK; });
algorithmKInput.addEventListener('change',()=>{ algorithmK=Number(algorithmKInput.value); reset(); });
document.getElementById('newData').addEventListener('click',newData);
document.getElementById('reset').addEventListener('click',reset);
document.getElementById('step').addEventListener('click',step);
document.getElementById('run').addEventListener('click',run);
updateBounds(); reset();
</script>
</body>
</html>
'''


if __name__ == "__main__":
    main()
