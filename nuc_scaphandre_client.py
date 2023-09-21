#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import redis, os, json, time, yaml
import logging
import pathlib
import subprocess

from subprocess import DEVNULL, STDOUT

from utils.pskill import kill_processes
import utils.msg_def as defs

# MAIN LOOP
if __name__ == "__main__":

	filename = './log/scaph_test.json'

	cmd = f'echo "nuc" | sudo -S /home/nuc/scaphandre/target/debug/scaphandre json -t 10 -m 0 -f {filename}'
	#p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	#os.system( cmd )

	p = subprocess.Popen( cmd.split() , stdout=DEVNULL, stderr=STDOUT )
	time.sleep( test_time )
	p.terminate()