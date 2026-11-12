#!/bin/bash
cd "$(dirname "$0")/site" || exit 1
(sleep 1; open http://localhost:8000) &
python3 -m http.server 8000
