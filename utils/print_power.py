#! /usr/bin/env python3

import requests as req
import json
import hashlib
import secrets
import time
import sys

plug_1 = 'http://10.196.80.205/config'
plug_2 = 'http://10.196.80.209/config'
plug_3 = 'http://10.196.80.207/config'

key = 'ngnlab'

header = {
        "from" : "testbed",
        "messageId" : "",
        "method" : "GET",
        "namespace" : "",
        "payloadVersion" : 1,
        "sign" : "",
        "timestamp": 0
}

payload = {"electricity": {"channel": 0}}

def craft_packet():
    messageid = secrets.token_hex(16)
    header["messageId"] = messageid

    header["namespace"] = "Appliance.Control.Electricity"

    timestamp = int(time.time())
    header["timestamp"] = timestamp

    sign = str(messageid) + key + str(timestamp)
    header["sign"] = hashlib.md5(sign.encode()).hexdigest()

    packet = {"header":header, "payload":payload}
    packet_json = json.dumps(packet)
    #print(json.dumps(packet, indent = 2))

    return packet_json


def print_power(plug_ip):
    while True:
        packet_json = craft_packet()
        response = req.post(plug_ip, data = packet_json, timeout = 30)

        # Power in milliwatts
        power = response.json()['payload']['electricity']['power']
        print(power)
        time.sleep(2)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Enter power plug name [plug_1|plug_2|plug_3]')
        quit()
    elif sys.argv[1] == 'plug_1':
        print_power(plug_1)
    elif sys.argv[1] == 'plug_2':
        print_power(plug_2)
    elif sys.argv[1] == 'plug_3':
        print_power(plug_3)
    else:
        print('Enter power plug name [plug_1|plug_2|plug3]')


