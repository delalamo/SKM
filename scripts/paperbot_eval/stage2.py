"""Two-stage view: SPECTER2 > 0.5 shortlist (88/day), then a decision model re-judges it."""
import json, sys
sample = [json.loads(l) for l in open("sample.jsonl")]
top = [r for r in sample if r["specter2"] >= 0.5]
print(f"shortlist sample: {len(top)} (10 SPECTER2 accepts + {len(top)-10} of 78 borderline, weight {top and max(r['weight'] for r in top):.1f})")
print(f"{'model':<14}{'thr':>5}{'kept/10':>8}{'borderline promoted/day':>25}{'issues/day':>12}")
for arg in sys.argv[1:]:
  name, path = arg.split("=")
  p = {json.loads(l)["id"]: json.loads(l)["p"] for l in open(path)}
  rows = [r for r in top if p.get(r["id"]) is not None]
  for thr in (0.5, 0.6, 0.7, 0.8, 0.9):
    kept = sum(1 for r in rows if r["specter2"] > 0.8 and p[r["id"]] > thr)
    prom = sum(r["weight"] for r in rows if r["specter2"] <= 0.8 and p[r["id"]] > thr)
    n_acc = sum(1 for r in rows if r["specter2"] > 0.8)
    print(f"{name:<14}{thr:>5.1f}{kept:>5}/{n_acc:<2}{prom:>25.0f}{kept+prom:>12.0f}")

print("\nAUC inside the shortlist (P that a SPECTER2 accept outranks a borderline paper; 0.5 = chance):")
for arg in sys.argv[1:]:
  name, path = arg.split("=")
  p = {json.loads(l)["id"]: json.loads(l)["p"] for l in open(path)}
  pos = [p[r["id"]] for r in top if r["specter2"] > 0.8 and p.get(r["id"]) is not None]
  neg = [p[r["id"]] for r in top if r["specter2"] <= 0.8 and p.get(r["id"]) is not None]
  if pos and neg:
    auc = sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))
    print(f"  {name:<14}{auc:.2f}  (n={len(pos)}+{len(neg)})")
