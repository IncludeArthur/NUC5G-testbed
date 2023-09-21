import json
from collections import namedtuple

nuc_names = ['nuc1', 'nuc2', 'nuc3']

redis_ts_names = [  'nuc1:cpu_perc', 'nuc1:mbps', 'nuc1:power', 
                    'nuc2:cpu_perc', 'nuc2:mbps', 'nuc2:power',
                    'nuc3:cpu_perc', 'nuc3:mbps', 'nuc3:power' ]

mon_itrfs = {   'nuc1':'eno1' ,# 'nuc1':'ogstun' , 
                'nuc2':'ogstun' , 
                'nuc3': 'eno1' }

imsis = {   'nuc1': 'imsi-001010000000001' , 
            'nuc2': 'imsi-001020000000001', 
            'nuc3': 'imsi-001030000000001' }

##### Definitions for Power measurements
tup = namedtuple( 'tup', [ 'nuc_to_plug', 'key', 'header', 'payload' ] )
pwr = tup( {    
                'nuc1': 'http://10.196.80.207/config',
                'nuc2': 'http://10.196.80.209/config',
                'nuc3': 'http://10.196.80.205/config'
            },
            'ngnlab', 
            {
                "from" : "testbed",
                "messageId" : "",
                "method" : "GET",
                "namespace" : "",
                "payloadVersion" : 1,
                "sign" : "",
                "timestamp": 0
            },
            {"electricity": {"channel": 0}}
        )

##### Definitions for Redis messages
class msg():
    def get_dict(self):    return self.__dict__
    def get_msg_str(self): return json.dumps(self.__dict__)

class msg_ogs_nuc( msg ):
    def __init__(self, msg:str=None) -> None:
        if msg == None:
            self.type : str = None
        else:
            d = json.loads(msg)
            self.type = d['type'] # [ cpu_stress | measure ]

class msg_stress_cpu( msg ):
    def __init__(self, in_dict=None) -> None:
        self.type   : str = 'cpu_stress'
        if in_dict == None:
            self.action : str = None
            self.load   : str = None
            self.time   : str = None
        else:
            d = json.loads(in_dict)
            self.action = d['action'] # [ start | stop ]
            self.load   = d['load']   # load in %
            self.time   = d['time']   # time in seconds
    
class msg_ogs_measure( msg ):
    def __init__(self, in_dict=None) -> None:
        self.type   : str = 'ogs_measure'
        if in_dict == None:
            self.action : str = None
        else:
            d = json.loads(in_dict)
            self.action = d['action'] # [ start | stop ]

class msg_pwr_measure( msg ):
    def __init__(self, in_dict=None) -> None:
        self.type   : str = 'power'
        if in_dict == None:
            self.nuc : str = None
            self.action : str = None
        else:
            d = json.loads(in_dict)
            self.nuc    = d['nuc']    # [ start | stop ]
            self.action = d['action'] # [ start | stop ]

class msg_sca_measure( msg ):
    def __init__(self, in_dict=None) -> None:
        self.type   : str = 'sca_measure'
        if in_dict == None:
            self.action : str = None
            self.file : str = None
            self.procs : str = None
        else:
            d = json.loads(in_dict)
            self.action = d['action'] # [ start | stop ]
            self.file   = d['file']   # name of local save file
            self.procs  = d['procs']  #number of processes to watch
