#!/bin/bash

cd /usr/share/grafana/csv
python3 -m http.server --bind localhost 9999 &

python3 /home/thernandez/honeypot-matter-thread/src/homeassistant/main.py &

python3 /home/thernandez/honeypot-matter-thread/src/homeassistant/all_logs.py &

python3 /home/thernandez/honeypot-matter-thread/src/matter/main.py