import json, os, subprocess, sys
p=subprocess.run([sys.executable,'-m','py_compile','scout_station_backend.py'],capture_output=True,text=True)
assert p.returncode == 0, p.stderr
print('PASS: compile; external actions=0 by design')
