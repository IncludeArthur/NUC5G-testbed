#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import time
import itertools
import controller as c

nuc  = "nuc2"

cpu_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
bwt_list = [100, 200, 300, 400, 500, 600]
# testlist = list(itertools.product(cpu_list,bwt_list))

#testlist = [(0,100)]
#testlist = [(0,0),(0,100),(0,200),(0,300),(0,400),(0,500),(0,600),(0,700),(0,800)]
#testlist = [(0,100),(0,200)]

#testlist_nuc1 = [(50,0),(70,0)]
#testlist_nuc2 = [(40,0),(50,0),(60,0),(90,0)]
testlist = [(0,0),(10,0),(20,0),(30,0),(40,0),(50,0),(60,0),(70,0),(80,0),(90,0),(100,0)]

test_time = 60

# set to true to run scaphandre power measuraments
use_scaphandre = False
watch_processes = 5

c.ran('stop')
c.iperf_server('stop')

#c.ran('start',nuc)
# the number of clients ues is set directly in the nuc4_client for now
n_ues = 1
c.ran('start', nuc, n_ues)
c.iperf_server('start', n_ues)

time.sleep(5)

for test in testlist:
    cpu = test[0]
    bwt = test[1]

    print( f'Starting test in nuc {nuc}: iperf {bwt}Mbps; cpu {cpu}% ')
    c.redis_clean()
    c.iperf_cli_start( time_sec=0 , bwt_mbps=bwt, n_ues=n_ues )
    c.cpu_stress_start( nuc=nuc , time_sec=0, cpu_perc=cpu )
    time.sleep( 2 )

    # Start monitoring
    c.ogs_monitor( nuc , 'start')
    c.pwr_monitor( nuc , 'start')
    if use_scaphandre: 
        filename = nuc+str(cpu)+'_'+str(n_ues)+'ues_'+str(bwt)
        c.scaphandre_start(nuc=nuc, filename=filename, processes=watch_processes)
        print(f'scaphandre measure in nuc {nuc}, watching {watch_processes} processes, saving data to {filename}')

    time.sleep( test_time )

    # Stop monitoring
    c.ogs_monitor( nuc , 'stop')
    c.pwr_monitor( nuc , 'stop')
    if use_scaphandre: c.scaphandre_stop( nuc )

    c.cpu_stress_stop(nuc=nuc)
    c.iperf_cli_stop()

    c.redis_save_res(f'results/hw/{nuc}_{n_ues}ues_{cpu}cpu_iperf_{bwt}Mbps.json')

c.ran('stop')
c.iperf_server('stop')



