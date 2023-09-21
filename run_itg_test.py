#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import time
import itertools
import controller as c

nuc  = "nuc2"

#bwt_list = [100, 200, 300, 400, 500, 600]
# testlist = list(itertools.product(cpu_list,bwt_list))

#testlist = [(0,2000)]
testlist = [(0,0),(0,10000),(0,20000),(0,30000),(0,40000),(0,50000),(0,60000),(0,70000),(0,80000)]
#testlist = [(0,10000),(0,60000)]

pckt_size = 512
test_time = 30

# set to true to run scaphandre power measuraments
use_scaphandre = False
watch_processes = 5

c.ran('stop')
c.itg_server('stop')

c.ran('start',nuc)
c.itg_server('start')

time.sleep(2)

for test in testlist:
    cpu = test[0]
    bwt = test[1]

    print( f'Starting test in nuc {nuc}: itg {bwt}pps; cpu {cpu}% ')
    c.redis_clean()
    c.itg_cli_start( pckt_rate=bwt, pckt_size=pckt_size )
#    c.cpu_stress_start( nuc=nuc , time_sec=0, cpu_perc=cpu )
    time.sleep( 2 )

    # Start monitoring
    c.ogs_monitor( nuc , 'start')
    c.pwr_monitor( nuc , 'start')
    if use_scaphandre: 
        filename = nuc+str(cpu)+'_'+str(bwt)
        c.scaphandre_start(nuc=nuc, filename=filename, processes=watch_processes)
        print(f'scaphandre measure in nuc {nuc}, watching {watch_processes} processes, saving data to {filename}')

    time.sleep( test_time )

    # Stop monitoring
    c.ogs_monitor( nuc , 'stop')
    c.pwr_monitor( nuc , 'stop')
    if use_scaphandre: c.scaphandre_stop( nuc )

#    c.cpu_stress_stop(nuc=nuc)
    c.itg_cli_stop()

    c.redis_save_res(f'results/{nuc}_itg_512b_{bwt}pps.json')

c.ran('stop')
c.itg_server('stop')



