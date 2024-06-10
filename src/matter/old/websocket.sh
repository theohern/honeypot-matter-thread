#! /bin/bash

tshark -i enp0s18 -f "tcp port 5580" -w websocket.pcap &

while (true); do
	sleep 10
	tshark -r websocket.pcap -Y 'http.request.method == "GET"' > websocket.txt
done
