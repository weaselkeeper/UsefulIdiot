#!/usr/bin/env python
""" bounce a (random) service """

# This only works on sysv init systems for now.
# Look at the contents of /etc/init.d, pick a random one, and see if it's
# currently running, if it is not, drop it from the list, and make another
# random pick, repeat until you get a running service. Then restart it, and
# return the results to the calling process.
# This is a dangerous module as some daemons don't take kindly to status
# requests,  we might want to reconsider this one.

# for now, all this does, is find a running service to play with, but as noted,
# there are dangers.
# This should probably just take a service option and bounce that. Or choose
# from a list given in options

import os
import subprocess
from random import shuffle


def run(options={}):
    """ run the command  handed us"""
    not_running = 1
    s_list = os.listdir('/etc/init.d')
    while not_running:
        shuffle(s_list)
        service = '/etc/init.d/' + s_list.pop()
        if 'dryrun' in options:
            if options['dryrun']:
                success = 0
                message = 'I would have tried to bounce: %s ' % service
                return success, message
        try:
            service_status = subprocess.Popen([service, 'status'],
                                              stdout=subprocess.PIPE).communicate()[0]
        except OSError:
            # try again
            break
        if 'running' in service_status.lower():
            service_status = subprocess.Popen([service, 'restart'],
                                              stdout=subprocess.PIPE).communicate()[0]
            not_running = 0
    return 0, service_status

if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    _success, _message = run()
    print _success, _message
