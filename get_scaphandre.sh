#!/bin/bash


folder=$(realpath "$0")
folder=$(dirname $folder)

scp  nuc@$1:~/UnitnTestbed/scaphandre/*.json $folder/scaphandre_test

echo Results copyed in $folder/scaphandre_test


