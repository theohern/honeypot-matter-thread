#! /bin/bash

docker logs -f matter-server 2> ./logs/matter/matterLogs > ./logs/matter/MatterOutputLogs
echo "Matter logs has been written to '\logs\matter' directory"
