#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import controller as c

c.ran('stop')
c.iperf_server('stop')
c.iperf_cli_stop()
c.redis_clean()

c.ogs_monitor( 'nuc2' , 'start')
c.pwr_monitor( 'nuc2' , 'start')
time.sleep(10)
for cpu in [10,20,30,40,50,60,70,80,90,100]:
    c.cpu_stress_start( nuc='nuc2' , time_sec=0, cpu_perc=cpu )
    time.sleep( 30 )
    c.cpu_stress_stop(nuc='nuc2')
c.ogs_monitor( 'nuc2' , 'stop')
c.pwr_monitor( 'nuc2' , 'stop')

c.redis_save_res('results/nuc2_cpu_test.json')




