#! /bin/bash

docker logs matter-server 2> matterLogs > MatterOutputLogs
mv matterLogs ../logs/matter
mv MatterOutputLogs ../logs/matter
echo "Matter logs has been written to '\home\thernandez\honeypot\logs\matter' directory"
