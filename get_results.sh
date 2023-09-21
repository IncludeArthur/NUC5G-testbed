#!/bin/bash

folder=$(realpath "$0")
folder=$(dirname $folder)

scp  nuc@nuc5:~/UnitnTestbed/results/*.json $folder/results

echo Results copyed in $folder/results
