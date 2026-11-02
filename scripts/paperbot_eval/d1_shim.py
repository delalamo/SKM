"""Expose LiquidAI d1-omni-600M through a /v1/systemone-shaped HTTP endpoint."""
import json, sys, torch
from http.server import BaseHTTPRequestHandler, HTTPServer
from transformers import AutoModel
torch.set_num_threads(4)
model = AutoModel.from_pretrained("LiquidAI/d1-omni-600M", trust_remote_code=True, dtype=torch.float32).eval()

class H(BaseHTTPRequestHandler):
  def do_POST(self):
    req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
    if "state" not in req or "questions" not in req:
      self.send_response(422); self.end_headers(); self.wfile.write(b'{"detail":"state and questions required"}'); return
    state = req["state"]
    if not isinstance(state, str):
      state = json.dumps(state, ensure_ascii=False, indent=1)
    try:
      with torch.inference_mode():
        out = model.system_one(state, req["questions"])
      body, code = json.dumps({"model": "d1-omni-600M", "answers": out.get("answers", out), "usage": {}}, default=float), 200
    except Exception as e:
      body, code = json.dumps({"detail": repr(e)[:500]}), 422
    self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers()
    self.wfile.write(body.encode())
  def log_message(self, *a): pass

print("ready", flush=True)
HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
