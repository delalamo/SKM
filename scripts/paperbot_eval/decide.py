"""Ask any /v1/systemone server (Jev, Kev, Rizzo Flow, Von...) to decide papers.

usage: decide.py SAMPLE.jsonl OUT.jsonl ENDPOINT MODEL MAX_CONTEXT_TOKENS [SIMILAR] [REJECTED]
"""
import json, os, sys, time
from dataclasses import replace
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from scripts.paperbot.config import load_config
from scripts.paperbot.jev import JevDecider, candidate_document
from scripts.paperbot.records import PaperRecord
sample, out, endpoint, model, budget = sys.argv[1:6]
similar = int(sys.argv[6]) if len(sys.argv) > 6 else 12
rejected = int(sys.argv[7]) if len(sys.argv) > 7 else 5
cfg = replace(load_config(), decision_backend="jev", jev_endpoint=endpoint, jev_model=model,
              jev_max_context_tokens=int(budget), jev_similar_papers=similar,
              jev_rejected_papers=rejected, jev_max_workers=1,
              jev_context_layout=os.getenv("LAYOUT", "ranked"))
decider = JevDecider.from_config(cfg, api_key=os.getenv("TYPESAFE_API_KEY", ""))
decider.client.timeout = 900
done = set()
if os.path.exists(out):
  done = {json.loads(l)["id"] for l in open(out)}
with open(out, "a") as f:
  for line in open(sample):
    row = json.loads(line)
    if row["id"] in done:
      continue
    rec = PaperRecord.from_dict(row["record"])
    t = time.time()
    try:
      d = decider.decide(candidate_document(rec)); p, err = d.probability, None
    except Exception as e:
      p, err = None, str(e)[:300]
    f.write(json.dumps({"id": row["id"], "p": p, "seconds": round(time.time() - t, 2), "error": err}) + "\n"); f.flush()
    print(f"{p} {time.time()-t:.1f}s {rec.title[:60]}", file=sys.stderr, flush=True)
