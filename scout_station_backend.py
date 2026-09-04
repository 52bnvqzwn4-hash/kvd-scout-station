#!/usr/bin/env python3
"""Local-only Scout Station backend skeleton.

Inspired by current public GitHub patterns reviewed from agent-os and flow-next:
local-first control, durable state, explicit preparation, receipts, and proof gates.
This server never publishes, sends, uploads, or contacts a platform.
"""
from __future__ import annotations
import json, os, secrets, threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / "scout_station_state"
STATE_DIR.mkdir(exist_ok=True)
STATE_FILE = STATE_DIR / "state.json"
LOCK = threading.Lock()

def now(): return datetime.now(timezone.utc).isoformat()
def load():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"station":"kvd-scout-station","version":"0.1","mode":"LOCAL_ONLY","updated_at":now(),"handoffs":[],"proof_ledger":[]}
def save(s):
    tmp=STATE_FILE.with_suffix('.tmp')
    tmp.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
    os.replace(tmp, STATE_FILE)

def response(handler, code, payload):
    body=json.dumps(payload,indent=2).encode()
    handler.send_response(code); handler.send_header('Content-Type','application/json'); handler.send_header('Content-Length',str(len(body))); handler.end_headers(); handler.wfile.write(body)

class Handler(BaseHTTPRequestHandler):
    server_version='ScoutStationBackend/0.1'
    def log_message(self, *_): pass
    def do_GET(self):
        with LOCK: state=load()
        if self.path == '/health': response(self,200,{"status":"VERIFIED","mode":"LOCAL_ONLY","external_actions":False,"timestamp":now()})
        elif self.path == '/api/state': response(self,200,state)
        else: response(self,404,{"status":"NOT_FOUND"})
    def do_POST(self):
        if self.path != '/api/handoff': return response(self,404,{"status":"NOT_FOUND"})
        try: n=int(self.headers.get('Content-Length','0')); data=json.loads(self.rfile.read(n))
        except Exception: return response(self,400,{"status":"BLOCKED","reason":"INVALID_JSON"})
        required=('caption','destination','assets')
        if any(k not in data for k in required): return response(self,400,{"status":"BLOCKED","reason":"MISSING_REQUIRED_FIELD"})
        record={"handoff_id":"handoff_"+secrets.token_hex(8),"state":"PREPARED","created_at":now(),"external_request_sent":False,"proof_required":True,"payload":data}
        with LOCK:
            state=load(); state['handoffs'].append(record); state['updated_at']=now(); save(state)
        response(self,201,record)

def main():
    host=os.getenv('SCOUT_HOST','127.0.0.1'); port=int(os.getenv('SCOUT_PORT','8787'))
    print(json.dumps({"status":"PREPARED","bind":f"{host}:{port}","external_actions":False,"state_file":str(STATE_FILE)}))
    ThreadingHTTPServer((host,port),Handler).serve_forever()
if __name__=='__main__': main()
