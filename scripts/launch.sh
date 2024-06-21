#! /bin/bash

echo "creating grafana directories..."
cd /usr/share

if [ ! -d grafana ]; then
	echo "creating /usr/share/grafana"
	mkdir grafana && cd grafana
else
	echo "folder /usr/share/grafana already exists"
fi

if [ ! -d grafana ]; then       
	echo "creating /usr/share/grafana/csv"
	mkdir csv
else
	echo "folder /usr/share/grafana/csv already exists"
fi

cd /home/user

if [ -f honeypot-matter-thread.zip ]; then
        if [ -d honeypot-matter-thread ]; then
       		rm -rf honeypot-matter-thread
	fi	
	echo "extracting honeypot's files..."
	unzip honeypot-matter-thread.zip > /dev/null
else
	echo "honeypots's file do not exist... exiting"
	exit 1
fi

echo "Initialisation .csv files..."

cd /home/user/honeypot-matter-thread
./src/init.sh

cd /home/user/honeypot-matter-thread

if [ ! -d venv ]; then
	echo "creating a python environnement..."
	python3 -m venv venv
	. ./venv/bin/activate
	echo "intsalling docker for python..."
	pip install docker < /dev/null 
	cp ../basehttpadapter.py /home/user/honeypot-matter-thread/venv/lib/python3.12/site-packages/docker/transport

else
	echo "python environement already exists..."
fi


cd /home/user
echo "creating log files..."
if [ ! -d logs ]; then
	mkdir /home/user/logs && cd /home/user/logs
	touch homeassistant.log httpServer.log matter.log stat.log
else
	echo "logs files already exixts"
fi

cd /home/user/honeypot-matter-thread
if [ "$1" != "no" ]; then
	echo "Start running the honeypot"
	. ./venv/bin/activate
	./src/honeypot.sh 
fi
