#!/bin/bash

dir="/home/thernandez/honeypot-matter-thread/src"


cd /usr/share/grafana/csv
python3 -m http.server --bind localhost 9999 &

python3 $dir/homeassistant/main.py &

python3 $dir/matter/main.py &

python3 $dir/stat.py
