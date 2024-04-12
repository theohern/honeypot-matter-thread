# honeypot-matter-thread
honeypot using Matter/Thread 

## network or IP changes

change the IP of the "homeassistant" in the file /etc/hosts. \
!! Do not change anything else !! 

## Start the honeypot

### make sure that all containers are running
There should be 9 containers running : 6 supervisors, 1 homeassistant ,1 addon_core_matter_server,  1 addon_core_openthread_router

### start grafana 
    sudo systemct restart grafana

### initiate the files for the honeypot 
    cd "/home/thernandez/honeypot-matter-thread/src" && sudo ./init.sh

### start the honeypot 
    sudo systemctl restart honeypot