#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import redis, os, json, time, yaml
import logging
import pathlib
import subprocess

from subprocess import DEVNULL, STDOUT

from utils.pskill import kill_processes
import utils.msg_def as defs

class ueransim:
    def __init__(self):
        
        self.cmd_start_gnb   = 'echo "nuc" | sudo -S ../UERANSIM/build/nr-gnb -c ../UERANSIM/config/[nuc]-gnb.yaml > log/ran.log  2>&1 &'
        self.cmd_start_ue    = 'echo "nuc" | sudo -S ../UERANSIM/build/nr-ue -c ../UERANSIM/config/[nuc]-ue.yaml  > log/ran.log  2>&1 &'
        self.cmd_start_multiple_ues = 'echo "nuc" | sudo -S ../UERANSIM/build/nr-ue -c ../UERANSIM/config/[nuc]-ue.yaml -n [users]  > log/ran.log  2>&1 &'
        # self.cmd_get_ps_list = 'echo "nuc" | sudo -S ../UERANSIM/build/nr-cli [imsi] -e ps-list'
        self.cmd_get_ps_list = '../UERANSIM/build/nr-cli [imsi] -e ps-list'
        self.cmd_stopall     = 'echo "nuc" | sudo -S pkill -9 -f nr-'

        self.gnb_proc : subprocess.Popen = None
        self.ue_proc  : subprocess.Popen = None
        self.ue_imsi  : str = None
        self.n_ues    : int = 0

        os.system( self.cmd_stopall )

    def start_gnb(self, nuc:str):
        if not self.gnb_proc == None:
            print( f'gNB already instantiated' )
            return
        cmd = self.cmd_start_gnb.replace('[nuc]',nuc)
        # p = subprocess.Popen( cmd.split(), stdout=subprocess.PIPE, universal_newlines=True )
        # self.gnb_proc = p
        os.system( cmd )
        self.gnb_proc = True
        logging.info( f'gNB started' )

    def start_ue(self, nuc:str):
        if not self.ue_proc == None:
            logging.info(  f'UE already instantiated with IP {self.get_ue_ip()}' )
            return
        self.ue_imsi = defs.imsis[nuc]
        cmd = self.cmd_start_ue.replace('[nuc]',nuc)
        # p = subprocess.Popen( cmd.split() , stdout=subprocess.PIPE, universal_newlines=True )
        # self.ue_proc = p
        os.system( cmd )
        self.ue_proc = True
        self.n_ues = 1
        logging.info(  f"Starting UE and connecting to {nuc}" )
        self.wait_ue_connection_up()
        logging.info( f"UE {self.ue_imsi} is connected via IP {self.get_ue_ip()}" )

    def start_multiple_ues(self, nuc:str, n_ues:int):
        if not self.ue_proc == None:
            logging.info(  f'UE already instantiated with IP {self.get_ue_ip()}' )
            return
        self.ue_imsi = defs.imsis[nuc]
        cmd = self.cmd_start_multiple_ues.replace('[nuc]',nuc).replace('[users]', str(n_ues))
        os.system( cmd )
        self.ue_proc = True
        self.n_ues = n_ues
        logging.info(  f"Starting {n_ues} UEs and connecting to {nuc}" )
        for i in range(n_ues):
            self.wait_ue_connection_up(i)
            logging.info( f"UE {self.next_ue_imsi(i)} is connected via IP {self.get_ue_ip(i)}" )

    def next_ue_imsi(self, i):
        ue_id = str(i+1)
        imsi = self.ue_imsi[:-(len(ue_id))] + ue_id
        return imsi

    def get_ps_list( self , n=0 ):
        if self.ue_imsi:
            cmd = self.cmd_get_ps_list.replace('[imsi]', self.next_ue_imsi(n) )
            p = subprocess.run( cmd.split() , stdout=subprocess.PIPE,stderr=DEVNULL, universal_newlines=True )
            return yaml.safe_load( p.stdout )
        else:
            logging.info( f"Trying to get ps_list but ue_imsi is None" )

    def wait_ue_connection_up( self, n=0 ):
        done = False
        while done == False:
            done = self.check_ue_connection( n )

    def check_ue_connection( self , n=0):
        dct = self.get_ps_list( n )
        if dct == None:
            return False
        for k,vals in dct.items():
            if vals['state']=='PS-ACTIVE':
                return True
        return False

    def get_ue_ip( self, n=0 ):
        dct = self.get_ps_list( n )
        if dct == None:
            return None
        for _,vals in dct.items():
            return vals["address"]
        return None

    def stop_ueransim(self):
        # if self.gnb_proc: 
        #     self.gnb_proc.terminate()
        #     time.sleep(0.5)
        #     self.gnb_proc.poll()
        #     self.gnb_proc = None
        # if self.ue_proc:
        #     self.ue_proc.terminate()
        #     time.sleep(0.5)
        #     self.ue_proc.poll()
        #     self.ue_proc  = None
        cmd = self.cmd_stopall
        p = os.system( cmd )
        self.gnb_proc = None
        self.ue_proc  = None
        self.ue_imsi  = None
        self.n_ues    = 0


# COMMON DEFINITION
nuc_name = os.uname()[1]
my_folder = pathlib.Path(__file__).parent.resolve() 
controller_ip: str = '192.168.0.6'
iperf_port   : int = 50000
logfile = f'{my_folder}/log/{nuc_name}.log'

ran      = ueransim()
channels = ['ueransim', 'iperf_cli', 'itg_cli']
r = redis.StrictRedis(host='192.168.0.6', port=6379, password="", decode_responses=True)
rp = r.pubsub()

logging.basicConfig(    format='%(asctime)s %(levelname)-8s %(message)s' ,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=logfile, 
                        level=logging.DEBUG )

# MAIN LOOP
if __name__ == "__main__":

    for c in channels:
        rp.subscribe( c )
    
    for message in rp.listen():
        if message["type"] == "subscribe":
            continue
        
        ### UERANSIM
        if message["channel"] == 'ueransim':
            msg_par = json.loads( message['data'] ) 
            logging.info( msg_par )

            if msg_par['action'] == "start":
                ran.start_gnb( msg_par['nuc'] )
                
                if msg_par['n_ues'] == 1:
                    ran.start_ue(  msg_par['nuc'] )
                else:
                    ran.start_multiple_ues( msg_par['nuc'], msg_par['n_ues'])

            if msg_par['action'] == "stop":
                ran.stop_ueransim( )

        ### IPERF CLIENT
        if message["channel"] == 'iperf_cli':
            msg = json.loads( message['data'] )
            logging.info( msg )
            
            if msg['action'] == "start":
                # msg_data = { 'action':'start' , 'time_sec':time_sec, 'bwt_mbps':bwt_mbps }
                # iperf3 -c 192.168.0.6 -p 50000 -B 10.45.0.10 -t 0 -b 20M
                #   -->  '-t 0' or '-t inf' runs iperf indefinitely  
                # cmd = f'iperf3 -c {controller_ip} -p {iperf_port} -B {ran.get_ue_ip()} -t {msg["time_sec"]} -b {msg["bwt_mbps"]}M'
                # logging.info( cmd )
                # p = subprocess.Popen( cmd.split(), stdout=subprocess.PIPE, universal_newlines=True )
                if msg['bwt_mbps'] == 0:
                    logging.info('not starting iperf for 0 Mbps')
                else:
                    if msg['n_ues'] == 1:
                        cmd = f'iperf3 -c {controller_ip} -p {iperf_port} -B {ran.get_ue_ip()} -t {msg["time_sec"]} -b {msg["bwt_mbps"]}M > /dev/null 2>&1 &'
                        logging.info( cmd )
                        os.system( cmd )
                    else:
                        split_bwt = msg['bwt_mbps'] // msg['n_ues']
                        for i in range(msg['n_ues']):
                            cmd = f'iperf3 -c {controller_ip} -p {iperf_port + i} -B {ran.get_ue_ip(i)} -t {msg["time_sec"]} -b {split_bwt}M > /dev/null 2>&1 &'
                            logging.info( cmd )
                            os.system( cmd )

            if msg['action'] == "stop":
                logging.info( 'stopping iperf clients' )
                # kill_processes('iperf3')
                cmd = 'pkill -f -9 iperf3'
                subprocess.run( cmd.split() )

        ### D-ITG CLIENT
        if message["channel"] == 'itg_cli':
            msg = json.loads( message['data'] )
            logging.info( msg )

            if msg['action'] == 'start':
                if msg['pckt_rate'] == 0:
                    logging.info('not starting itg for 0 pps')
                else:
                    log_path = f'/home/nuc/UnitnTestbed/itg/itg_{msg["pckt_rate"]}_{msg["pckt_size"]}'
                    cmd = f'ITGSend -a {controller_ip} -rp 32769 -C {msg["pckt_rate"]} -c {msg["pckt_size"]} -t 32000 -i uesimtun0 -x {log_path} -l {log_path} > /dev/null 2>&1 &'
                    logging.info( cmd )
                    os.system( cmd )

            if msg['action'] == 'stop':
                logging.info( 'stopping itg clients' )
                cmd = 'pkill -f -9 ITGSend'
                subprocess.run( cmd.split() )
