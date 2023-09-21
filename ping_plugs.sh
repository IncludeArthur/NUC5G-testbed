#!/bin/bash

echo "nuc 1 plug test: "

if ping -c 1 10.196.80.207 &> /dev/null
then
	echo "success"
else
	echo "error"
fi


echo "nuc 2 plug test: "

if ping -c 1 10.196.80.209 &> /dev/null
then
        echo "success"
else
        echo "error"
fi

echo "nuc 3 plug test: "

if ping -c 1 10.196.80.205 &> /dev/null
then
        echo "success"
else
        echo "error"
fi

