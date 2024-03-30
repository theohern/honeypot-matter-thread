#! /bin/bash

if [ ! -d ./logs ]; then
	mkdir ./logs
	echo "creating /logs directory"
else
	echo "directory /logs already exists"
fi

if [ ! -d ./logs/matter ];then
	mkdir ./logs/matter
	echo "creating /logs/matter directory"
else
	echo "directory /logs/matter already exists"
fi

if [ ! -d ./logs/thread ];then
	mkdir ./logs/thread
	echo "creating /logs/thread directory"
else
	echo "directory /logs/thread already exists"
fi

if [ ! -d ./logs/homeassistant ];then
	mkdir ./logs/homeassistant
	echo "creating /logs/homeassistant directory"
else
	echo "directory /logs/homeassistant already exists"
fi

echo "To clean all the file, run 'make clean'"
