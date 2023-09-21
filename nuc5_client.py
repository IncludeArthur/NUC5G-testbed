#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import secrets
import requests
import redis
import json
import hashlib
import copy

from threading import Thread

from utils.msg_def import pwr, msg_pwr_measure

class PowerMonitor( Thread ):
    def __init__( self ):
        super(PowerMonitor, self).__init__()
        self._running = True
        self.periodicity = 1 # seconds
        self.nuc = None
        
    def terminate( self ):
        self._running = False

    def craft_packet( self ):
        messageid = secrets.token_hex(16)
        header = copy.deepcopy(pwr.header)

        header["messageId"] = messageid
        header["namespace"] = "Appliance.Control.Electricity"

        timestamp = int(time.time())
        header["timestamp"] = timestamp

        sign = str(messageid) + pwr.key + str(timestamp)
        header["sign"] = hashlib.md5(sign.encode()).hexdigest()

        packet = {"header":header, "payload":pwr.payload}
        packet_json = json.dumps(packet)
        #print(json.dumps(packet, indent = 2))

        return packet_json

    def run( self ):
        while self._running:
            packet_json = self.craft_packet()
            response = requests.post( pwr.nuc_to_plug[self.nuc], data = packet_json, timeout = 30)

            # Power in milliwatts
            power = response.json()['payload']['electricity']['power']
            # print(power)
            r.ts().add(f'{self.nuc}:power', "*", power )

            time.sleep( self.periodicity )

r = redis.StrictRedis(host='192.168.0.6', port=6379, password="", decode_responses=True)
rp = r.pubsub()
channels = ['power']

pwr_mon : PowerMonitor = None


###### MAIN LOOP
if __name__ == "__main__":

    for c in channels:
        rp.subscribe( c )
    
    for message in rp.listen():
        if message["type"] == "subscribe":
            continue
        
        ### POWER MEASURE
        if message["channel"] == 'power':
            msg = msg_pwr_measure( message['data'] )

            if msg.action == 'start':
                if not pwr_mon:
                    pwr_mon = PowerMonitor()
                    pwr_mon.nuc = msg.nuc
                    pwr_mon.start()

            if msg.action == 'stop':
                if not pwr_mon==None:
                    pwr_mon.terminate()
                    pwr_mon = None
