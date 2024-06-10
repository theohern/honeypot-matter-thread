#!/bin/bash

apk add tshark

INTERFACE="7" 

FILTER="tcp port 5580"

OUTPUT_FILE="/usr/share/grafana/csv/websocket.csv"

tshark -i "$INTERFACE" -f "$FILTER" -T fields \
    -e _ws.col.Time \
    -e ip.src \
    -e tcp.srcport \
    -e ip.dst \
    -e tcp.dstport \
    -e _ws.col.Protocol \
    -e _ws.col.Info \
    -E header=y -E separator=, > "$OUTPUT_FILE"

