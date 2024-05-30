#!/bin/bash

dir="/home/user/honeypot-matter-thread/src"


cd /usr/share/grafana/csv
python3 -m http.server 9999  > /home/user/logs/httpServer.log &

python3 $dir/homeassistant/main.py > /home/user/logs/homeassistant.log &

python3 $dir/matter/main.py > /home/user/logs/matter.log  &

python3 $dir/stat.py > /home/user/logs/stat.log &
