#!/bin/bash
set -eux
apt-get update
apt-get install -y docker.io
systemctl enable docker
systemctl start docker
docker rm -f bootstrap-app 2>/dev/null || true
docker run -d --name bootstrap-app --restart unless-stopped -p 5000:5000 python:3.12-slim python -c "from http.server import BaseHTTPRequestHandler,HTTPServer; H=type('H',(BaseHTTPRequestHandler,),{'do_GET':lambda s:s.send_response(200) or s.end_headers() or s.wfile.write(b'EC2 ready for Jenkins deployment')}); HTTPServer(('0.0.0.0',5000),H).serve_forever()"
