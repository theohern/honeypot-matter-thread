#! /bin/bash

docker logs matter-server 2> matterLogs > MatterOutputLogs
mv matterLogs ./logs/matter
mv MatterOutputLogs ./logs/matter
echo "Matter logs has been written to '\logs\matter' directory"
