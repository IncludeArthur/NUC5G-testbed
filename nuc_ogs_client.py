#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import redis
import subprocess
import time
import psutil
import logging
import datetime
import pathlib

from subprocess import DEVNULL, STDOUT
from threading  import Thread

from utils.msg_def import msg_ogs_nuc, msg_stress_cpu, msg_ogs_measure, mon_itrfs, msg_sca_measure
from utils.pskill import kill_processes


class Monitor( Thread ):
    def __init__(self, if_name):
        super(Monitor, self).__init__()
        self._running = True
        self.periodicity = 1 # seconds
        self.if_name = if_name

        sample = psutil.net_io_counters(pernic=True)
        self.last_thr_sample_time = time.time()
        self.last_thr_sample      = sample[if_name].bytes_recv
        self.last_pck_sample      = sample[if_name].packets_recv
        logging.debug( f'{nuc_name} client received message: Monitoring started' )

    def terminate( self ):
        self._running = False

    def run( self ):
        while self._running:

            cpu = psutil.cpu_percent()
            r.ts().add(f'{nuc_name}:cpu_perc', "*", cpu )

            cur_time = time.time()
            sample = psutil.net_io_counters(pernic=True)
            sample_recv = sample[self.if_name].bytes_recv
            sample_pck = sample[self.if_name].packets_recv
            bit_rate = (sample_recv - self.last_thr_sample) * 8 / 1e6 / (cur_time - self.last_thr_sample_time)
            pck_rate = (sample_pck - self.last_pck_sample) / (cur_time - self.last_thr_sample_time)
            self.last_thr_sample_time = cur_time
            self.last_pck_sample      = sample_pck
            self.last_thr_sample      = sample_recv
            r.ts().add(f'{nuc_name}:mbps', "*", bit_rate )
            r.ts().add(f'{nuc_name}:pcks', "*", pck_rate )

            logging.debug( f'{nuc_name} report measure: cpu={cpu} thr={ bit_rate } pck={pck_rate}' )

            time.sleep( self.periodicity )


nuc_name = os.uname()[1]

# Workaround to have the VM called nuc1
if nuc_name == 'ubuntu':
    nuc_name = 'nuc1'

my_folder = pathlib.Path(__file__).parent.resolve() 
logfile = f'{my_folder}/log/{nuc_name}.log'

r = redis.StrictRedis(host='192.168.0.6', port=6379, password="", decode_responses=True)
rp = r.pubsub()
rp.subscribe(nuc_name)

mon : Monitor = None

logging.basicConfig(    format='%(asctime)s %(levelname)-8s %(message)s' ,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=logfile, 
                        level=logging.DEBUG )

if __name__ == "__main__":

    # Ensure no stress-ng instances are active
    os.system( 'pkill -f -9 stress-ng' )

    for message in rp.listen():
        if message["type"] == "subscribe":
            continue

        if message["channel"] == nuc_name:
            m = msg_ogs_nuc( message['data'] )

            ### stress-ng
            if m.type == 'cpu_stress':
                msg = msg_stress_cpu( message['data'] )
                logging.info( f'{nuc_name} client received message: {msg.get_msg_str()}' )

                if msg.action == "start":
                    # stress-ng --cpu 4 --cpu-load 40 -t 2m;
                    #   --> '-t 0' run stress-ng forever
                    cmd = f'stress-ng --cpu 4 --cpu-load {msg.load} -t {msg.time}s'
                    p = subprocess.Popen( cmd.split() , stdout=DEVNULL, stderr=STDOUT )

                if msg.action == "stop":
                    p.terminate()
                    time.sleep(0.5)
                    p.poll()
                    
            ### measurement report
            if m.type == 'ogs_measure':
                msg = msg_ogs_measure( message['data'] )
                logging.info( f'{nuc_name} client received message: {msg.get_msg_str()}' )

                if msg.action == "start":
                    if not mon:
                        mon = Monitor(mon_itrfs[nuc_name])
                        mon.start()
                
                if msg.action == "stop":
                    if not mon==None:
                        mon.terminate()
                        mon = None

            ### scaphandre
            if m.type == 'sca_measure':
                msg = msg_sca_measure( message['data'] )
                logging.info( f'{nuc_name} client received message: {msg.get_msg_str()}' )

                if msg.action == "start":
                    # For now the results are stored locally on a json file
                    # I need to find a way of sending them back using Redis
                    filepath = '/home/nuc/UnitnTestbed/scaphandre/'+ msg.file + '.json'
                    cmd = f'/home/nuc/scaphandre/target/release/scaphandre json -m {msg.procs} -s 1 -f {filepath}'
                    p = subprocess.Popen( cmd.split() , stdout=DEVNULL, stderr=STDOUT )

                if msg.action == "stop":
                    p.terminate()
                    time.sleep(0.5)
                    p.poll()
