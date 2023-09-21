# from collections import namedtuple

# msg_ueransim_fileds = ['action','nuc']
# msg_ueransim = namedtuple( 'msg_ueransim', ['action','nuc'] )
# msgstr = f"a bb"
# print(msgstr.split())
# msg_par = msg_ueransim._make( msgstr.split() )
# print(msg_par)
# aa = msg_ueransim( 'start','nuc1' )
# print(str(aa))

# print('--------------------')
# from typing import Dict
# IPS: Dict[str, str] = {
#     "epc": "10.80.95.10",
#     "enb": "10.80.95.11",
#     "ue": "10.80.97.12",
# }

# print('--------------------')
# import copy
# from collections import namedtuple

# tup = namedtuple( 'tup', [ 'plug_1' ,'plug_2' , 'plug_3', 'key', 'header', 'payload' ] )
# pwr = tup(
#             'http://10.196.80.205/config',
#             'http://10.196.80.209/config',
#             'http://10.196.80.207/config',
#             'ngnlab', 
#             {   "from" : "testbed",
#                 "messageId" : "",
#                 "method" : "GET",
#                 "namespace" : "",
#                 "payloadVersion" : 1,
#                 "sign" : "",
#                 "timestamp": 0 },
#             {"electricity": {"channel": 0}}
#         )
# print(pwr.header)
# print(type(pwr.header))

# d = copy.deepcopy(pwr.header)
# d['messageId'] = 'message'

# print(d['messageId'])
# print(pwr.header['messageId'])
