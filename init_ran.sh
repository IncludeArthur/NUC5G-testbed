#!/bin/bash

if [ "$HOSTNAME" != "nuc4" ]; then
    echo "I should run in NUC 4, while I'm running in $HOSTNAME"
    exit 0
fi
if [ $# -eq 0 ]; then
    echo "Tell me the NUC number"
    exit 0
fi

nuc_number=$1

# Clear all previous instance if running
echo "nuc" | sudo -S pkill -9 nr-

# Start gNB and UE
echo "nuc" | sudo -S ~/UERANSIM/build/nr-gnb -c ~/UERANSIM/config/nuc$nuc_number-gnb.yaml > log/ran.log  2>&1 &
sleep 2
echo "nuc" | sudo -S ~/UERANSIM/build/nr-ue  -c ~/UERANSIM/config/nuc$nuc_number-ue.yaml  > log/ran.log  2>&1 &
sleep 1

# Show created interface
ip -brief address show uesimtun0  | awk '{print $1" "$3}'  | awk -F/ '{print $1}'


