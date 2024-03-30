#! /bin/bash

docker logs homeassistant 2> haLogs > HaOutputLogs
mv haLogs ./logs/homeassistant
mv HaOutputLogs ./logs/homeassistant
echo "homeassistant logs has been written to '\logs\homeassistant' directory"