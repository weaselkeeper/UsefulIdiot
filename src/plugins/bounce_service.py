#!/usr/bin/env python

# Bare bones start, only works for RH and friends, due to location of service
# comamand
# TODO  Need to be a bit more catholic in detecting service status.

def oscheck():
    import platform
    if platform.dist()[0] == 'debian':
        check_service = '/usr/sbin/service'
        check_service_opts = '--status-all'
    else:
        check_service = '/sbin/service'
        check_service_opts = '--list-all'

    return check_service, check_service_opts

def run(options={}):
    import subprocess
    from random import choice
    _service,_opts=oscheck()
    servicelist = subprocess.check_output([_service,_opts])
    print servicelist

run()
