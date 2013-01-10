#!/usr/bin/env python

def run(options={}):
    import subprocess
    from random import choice
    servicelist = subprocess.check_output(['/sbin/service','--status-all'])
    print servicelist

run()
