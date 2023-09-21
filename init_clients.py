#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import os
import time
import paramiko
import pathlib

nuc_name = os.uname()[1]
if not nuc_name == 'nuc5':
    print('Please execute me on nuc 5.')
    exit()

print('Starting client on nuc5')
os.system( 'pkill -9 -f nuc5_client.py' )
os.system( 'python3 nuc5_client.py > log/nuc5.log 2>&1 &'   )

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect('nuc4', port=22, username='nuc', password='nuc')
print('Starting client on nuc4')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command( 'pkill -9 -f nuc4_client.py\n' )
ssh_stdin.close()
time.sleep(1)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command( 'cd ~/UnitnTestbed && python3 nuc4_client.py > log/nuc4.log 2>&1 &\n' )
ssh_stdin.close()
time.sleep(1)
ssh.close()

for nuc in ['nuc1','nuc2','nuc3']:
    print(f'Starting client on {nuc}')
    ssh.connect(nuc, port=22, username='nuc', password='nuc')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command( 'pkill -9 -f nuc_ogs_client.py\n' )
    ssh_stdin.close()
    time.sleep(1)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command( f'cd ~/UnitnTestbed && python3 nuc_ogs_client.py > log/{nuc}.log 2>&1 &\n' )
    ssh_stdin.close()
    time.sleep(1)
    ssh.close()

