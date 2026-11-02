"""Compare decider outputs with the current SPECTER2 workflow on the same sample.

usage: compare.py SAMPLE.jsonl NAME=OUT.jsonl[@threshold] ...
"""
import json, sys
sample = [json.loads(l) for l in open(sys.argv[1])]
base = {r["id"]: r["specter2"] for r in sample}
weight = {r["id"]: r.get("weight", 1.0) for r in sample}
CUT = 0.80

def ranks(values):
  order = sorted(range(len(values)), key=lambda i: values[i])
  r = [0.0] * len(values); i = 0
  while i < len(order):
    j = i
    while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]: j += 1
    for k in range(i, j + 1): r[order[k]] = (i + j) / 2
    i = j + 1
  return r

def spearman(a, b):
  ra, rb = ranks(a), ranks(b); n = len(a)
  ma, mb = sum(ra) / n, sum(rb) / n
  cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
  va = sum((x - ma) ** 2 for x in ra) ** .5; vb = sum((y - mb) ** 2 for y in rb) ** .5
  return cov / (va * vb) if va and vb else float("nan")

print(f"sample={len(sample)}  SPECTER2 accepts (>{CUT}): {sum(v > CUT for v in base.values())}")
print(f"{'decider':<22}{'n':>4}{'thr':>6}{'acc':>5}{'both':>6}{'recall':>8}{'precis':>8}{'agree':>7}{'kappa':>7}{'rho':>7}{'top-k':>7}{'s/paper':>9}{'est/day':>8}")
for arg in sys.argv[2:]:
  name, rest = arg.split("=", 1)
  path, _, thr = rest.partition("@"); thr = float(thr or 0.5)
  rows = {}
  for l in open(path):
    r = json.loads(l)
    if r.get("p") is not None: rows[r["id"]] = r
  ids = [i for i in base if i in rows]
  if not ids: print(name, "no results"); continue
  b = [base[i] > CUT for i in ids]; d = [rows[i]["p"] > thr for i in ids]; w = [weight[i] for i in ids]
  both = sum(wi for x, y, wi in zip(b, d, w) if x and y)
  nb = sum(wi for x, wi in zip(b, w) if x); nd = sum(wi for y, wi in zip(d, w) if y); W = sum(w)
  agree = sum(wi for x, y, wi in zip(b, d, w) if x == y) / W
  pe = (nb / W) * (nd / W) + (1 - nb / W) * (1 - nd / W)
  kappa = (agree - pe) / (1 - pe) if pe < 1 else float("nan")
  rho = spearman([base[i] for i in ids], [rows[i]["p"] for i in ids])
  k = sum(1 for x in b if x)
  topb = set(sorted(ids, key=lambda i: -base[i])[:k]); topd = set(sorted(ids, key=lambda i: -rows[i]["p"])[:k])
  topk = len(topb & topd) / k if k else float("nan")
  sec = sum(rows[i]["seconds"] for i in ids) / len(ids)
  print(f"{name:<22}{len(ids):>4}{thr:>6.2f}{sum(d):>5}{both:>6.0f}{both/nb if nb else 0:>8.2f}{both/nd if nd else 0:>8.2f}{agree:>7.2f}{kappa:>7.2f}{rho:>7.2f}{topk:>7.2f}{sec:>9.1f}{nd:>8.0f}")
