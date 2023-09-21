#!/bin/bash

h=$HOSTNAME

if [ "$h" = "ubuntu" ]; then
    echo "ubuntu" | sudo -S ./kill_open5gs.sh
    echo "ubuntu" | sudo -S ./start_core_d.sh #run_core_d.sh ?
fi
if [ "$h" = "nuc2" ]; then
    echo "nuc" | sudo -S ./kill_open5gs.sh
    echo "nuc" | sudo -S ./start_core_d.sh
fi
if [ "$h" = "nuc3" ]; then
    cd ~/docker_open5gs
    docker compose down
	source .env
	echo "nuc" | sudo -S docker compose -f sa-deploy.yaml up -d
fi
