#!/bin/bash

if [ "$HOSTNAME" = "nuc5" ]; then
    mkdir -p results/

    # From nuc5, clean files on other nodes
    # ssh ubuntu@vm <<< 'cd ~/UnitnTestbed/ && rm *.py *.sh utils/*.py' > /dev/null
    ssh nuc@nuc1 <<< 'cd ~/UnitnTestbed/ && rm *.py *.sh utils/*.py' > /dev/null
    ssh nuc@nuc2  <<< 'cd ~/UnitnTestbed/ && rm *.py *.sh utils/*.py' > /dev/null
    ssh nuc@nuc3  <<< 'cd ~/UnitnTestbed/ && rm *.py *.sh utils/*.py' > /dev/null
    ssh nuc@nuc4  <<< 'cd ~/UnitnTestbed/ && rm *.py *.sh utils/*.py' > /dev/null
    # ssh ubuntu@vm <<< 'mkdir ~/UnitnTestbed/log' > /dev/null
    ssh nuc@nuc1 <<< 'mkdir ~/UnitnTestbed/log' > /dev/null
    ssh nuc@nuc2  <<< 'mkdir ~/UnitnTestbed/log' > /dev/null
    ssh nuc@nuc3  <<< 'mkdir ~/UnitnTestbed/log' > /dev/null
    ssh nuc@nuc4  <<< 'mkdir ~/UnitnTestbed/log' > /dev/null

    # From nuc5 Copy files on other nodes
    a=$(ls -p | grep -v /)
    a+=' 'utils
    cd ~/UnitnTestbed
    # scp -r $a ubuntu@vm:~/UnitnTestbed/
    scp -r $a nuc@nuc1:~/UnitnTestbed/
    scp -r $a nuc@nuc2:~/UnitnTestbed/
    scp -r $a nuc@nuc3:~/UnitnTestbed/
    scp -r $a nuc@nuc4:~/UnitnTestbed/
    
    exit 0
fi

# Clean and copy files to nuc5
ssh nuc@nuc5 <<< 'cd ~/UnitnTestbed/ && rm *.py *.sh utils/*.py' > /dev/null
a=$(ls -p | grep -v /)
scp -r $a nuc@nuc5:~/UnitnTestbed/
scp -r utils nuc@nuc5:~/UnitnTestbed

# Trigger the execution of this script on nuc5
ssh nuc@nuc5 'cd UnitnTestbed/ && ./deploy.sh'
