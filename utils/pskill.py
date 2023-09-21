#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil, sys

def kill_processes(process_tag):
    p_list = []
    for p in psutil.process_iter():
        p_cmdline = ' '.join(p.cmdline())
        if process_tag in p_cmdline:
            p_list.append(p)

    for p in p_list:
        p.kill()

if __name__ == "__main__":
    process_tag = sys.argv[1]
    kill_processes(process_tag)
