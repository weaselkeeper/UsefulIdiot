#!/usr/bin/env python

def run(options={}):
    import os
    from random import choice
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit() and pid > 1]
    print 'I would have killed: ' + choice(pids)

