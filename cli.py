#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import click

import controller as ctrl
from utils.msg_def import nuc_names

@click.group()
def main():
    pass

### UERANSIM
@main.command()
@click.option("--action", prompt=" start/stop", type=click.Choice(['start', 'stop']       , case_sensitive=False) )
@click.option("--nuc"   , prompt=" enter nuc" , type=click.Choice( nuc_names , case_sensitive=False) )
def ran(action, nuc):
    ctrl.ran(action, nuc)

### IPERF SERVER
@main.command()
@click.option("--action", prompt=" start/stop", type=click.Choice(['start', 'stop']       , case_sensitive=False) )
def iperf_server(action):
    ctrl.iperf_server(action)

### IPERF CLIENT
@main.command()
@click.option( "--time_sec" , prompt=" iperf duration in sec." , type=int )
@click.option( "--bwt_mbps" , prompt=" Mbps"                   , type=int )
def iperf_cli_start( time_sec, bwt_mbps ):
    ctrl.iperf_cli_start( time_sec, bwt_mbps )

@main.command()
def iperf_cli_stop( ):
    ctrl.iperf_cli_stop( )

### STRESS-NG
@main.command()
@click.option( "--nuc" , prompt=" enter nuc" , type=click.Choice( nuc_names , case_sensitive=False) )
@click.option( "--time_sec" , prompt=" duration in sec." , type=int )
@click.option( "--cpu_perc" , prompt=" cpu percentage"         , type=int )
def cpu_stress_start( nuc, time_sec, cpu_perc ):
    ctrl.cpu_stress_start( nuc, time_sec, cpu_perc )

@main.command()
@click.option( "--nuc" , prompt=" enter nuc" , type=click.Choice( nuc_names , case_sensitive=False) )
def cpu_stress_stop( nuc ):
    ctrl.cpu_stress_stop( nuc )

### OGS MONITORING
@main.command()
@click.option( "--nuc"    , prompt=" enter nuc" , type=click.Choice( nuc_names , case_sensitive=False) )
@click.option( "--action" , prompt=" enter nuc" , type=click.Choice( ['start','stop'] , case_sensitive=False) )
def ogs_monitor( nuc , action):
    ctrl.ogs_monitor( nuc , action)

### POWER MONITORING
@main.command()
@click.option( "--nuc"    , prompt=" enter nuc" , type=click.Choice( nuc_names , case_sensitive=False) )
@click.option( "--action" , prompt=" enter nuc" , type=click.Choice( ['start','stop'] , case_sensitive=False) )
def pwr_monitor( nuc , action):
    ctrl.pwr_monitor( nuc , action)

if __name__ == "__main__":
    main()



