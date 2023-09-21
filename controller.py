#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import docker
import redis
import json
import subprocess
import os

from utils.pskill import kill_processes
from utils.msg_def import msg_stress_cpu , msg_ogs_measure, msg_pwr_measure, msg_sca_measure

try:
    d_client = docker.from_env()
except:
    print('Is docker installed?')
try:
    d_client.containers.get("my_redis")
except:
    print('Starting redis')
    d_client.containers.run(   "redis/redis-stack",
                                    name="my_redis",
                                    ports={ "6379/tcp": 6379,
                                            "8001/tcp": 8001 },
                                    detach=True)

redis_ip = d_client.containers.get("my_redis").attrs['NetworkSettings']['IPAddress']
redis_cli = redis.StrictRedis(host=redis_ip, port=6379, password="", decode_responses=True)


### UERANSIM
def ran(action, nuc=None, n_ues=1):
    if action == 'start':
        msg_data = { 'action':action , 'nuc':nuc , 'n_ues':n_ues }
        redis_cli.publish( 'ueransim' ,  json.dumps(msg_data) )

    if action == 'stop':
        msg_data = { 'action':action , 'nuc':None }
        redis_cli.publish( 'ueransim' ,  json.dumps(msg_data) )

### IPERF SERVER
def iperf_server(action, n_ues=1):
    if action == 'start':
        for i in range(n_ues):
            port = 50000 + i
            cmd = f'iperf3 -s -p {port} > /dev/null 2>&1 &'
            os.system( cmd )

    elif action == 'stop':
        cmd = 'pkill -f -9 iperf3'
        subprocess.run( cmd.split() )

### IPERF CLIENT
def iperf_cli_start( time_sec, bwt_mbps, n_ues=1 ):
    msg_data = { 'action':'start' , 'time_sec':time_sec, 'bwt_mbps':bwt_mbps, 'n_ues':n_ues }
    redis_cli.publish( 'iperf_cli' ,  json.dumps(msg_data) )

def iperf_cli_stop( ):
    msg_data = { 'action':'stop' }
    redis_cli.publish( 'iperf_cli' ,  json.dumps(msg_data) )

### D-ITG SERVER
def itg_server(action):
    if action == 'start':
        cmd = 'ITGRecv > /dev/null 2>&1 &'
        os.system( cmd )

    elif action == 'stop':
        cmd = 'pkill -f -9 ITGRecv'
        subprocess.run( cmd.split() )

### D-ITG CLIENT
def itg_cli_start(pckt_rate, pckt_size):
    msg_data = { 'action':'start', 'pckt_rate':pckt_rate, 'pckt_size':pckt_size}
    redis_cli.publish( 'itg_cli' , json.dumps(msg_data))

def itg_cli_stop( ):
    msg_data = { 'action':'stop' }
    redis_cli.publish( 'itg_cli' ,  json.dumps(msg_data) )

### STRESS-NG
def cpu_stress_start( nuc, time_sec, cpu_perc ):
    msg = msg_stress_cpu()
    msg.action = 'start'
    msg.load   = cpu_perc
    msg.time   = time_sec
    redis_cli.publish( nuc , msg.get_msg_str() )

def cpu_stress_stop( nuc ):
    msg = msg_stress_cpu()
    msg.action = 'stop'
    redis_cli.publish( nuc ,  msg.get_msg_str() )

### OGS MONITORING
def ogs_monitor( nuc , action):
    msg = msg_ogs_measure()
    msg.action = action
    redis_cli.publish( nuc ,  msg.get_msg_str() )

### POWER MONITORING
def pwr_monitor( nuc , action):
    msg = msg_pwr_measure()
    msg.nuc    = nuc
    msg.action = action
    redis_cli.publish( "power" ,  msg.get_msg_str() )

### SCAPHANDRE
def scaphandre_start( nuc, filename, processes=0 ):
    msg = msg_sca_measure()
    msg.action = 'start'
    msg.file   = filename
    msg.procs = processes
    redis_cli.publish( nuc , msg.get_msg_str() )

def scaphandre_stop( nuc ):
    msg = msg_sca_measure()
    msg.action = 'stop'
    redis_cli.publish( nuc ,  msg.get_msg_str() )

### REDIS
def redis_print_ts():
    for key in redis_cli.scan_iter("*"):
        if redis_cli.type(key) == 'TSDB-TYPE':
            print(key)

def redis_clean():
    for key in redis_cli.scan_iter("*"):
        redis_cli.delete(key)

def redis_save_res( result_file ):
    ts_dict = dict()
    min_time = 0
    for key in redis_cli.scan_iter("*"):
        if redis_cli.type(key) == 'TSDB-TYPE':
            ts = redis_cli.ts().range(key, 0, "+")
            time_stamp, val = map(list, zip(*ts))
            if min_time == 0:
                min_time = time_stamp[0]
            else:
                min_time = min( [min_time,time_stamp[0]] )
            ts_dict[key] = dict()
            ts_dict[key]["time"] = time_stamp
            ts_dict[key]["val"]  = val

    # ts_dict['mintime'] = min_time
    for key in ts_dict:
        ts_dict[key]["time"] = [(i-min_time)/1e3 for i in ts_dict[key]["time"]] # time in seconds

    if not result_file == "":
        with open( result_file, 'w') as outfile:
            json.dump( ts_dict, outfile , indent=2 )        
    
    


