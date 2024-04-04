#! /bin/bash
while true
do
    docker logs matter-server > /dev/null 2>second.txt
    
    if [ $(cat "test.txt" | wc -l) -eq $(cat "second.txt" | wc -l) ]; then
        sleep 1
    else
        echo "recomputing"
        make node
        echo "done"
    fi
done
