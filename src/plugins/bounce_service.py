#!/usr/bin/env python


# This only works on sysv init systems for now. 
# Look at the contents of /etc/init.d, pick a random one, and see if it's
# currently running, if it is not, drop it from the list, and make another
# random pick, repeat until you get a running service. Then restart it, and
# return the results to the calling process.
# This is a dangerous module as some daemons don't take kindly to status
# requests,  we might want to reconsider this one.

# for now, all this does, is find a running service to play with, but as noted,
# there are dangers.

import os
import subprocess
from random import shuffle


def select_service():
    not_running = 1
    s_list = os.listdir('/etc/init.d')
    while not_running:
        shuffle(s_list)
        service = '/etc/init.d/' + s_list.pop()
        try:
            service_status = subprocess.Popen([service,'status'],
                stdout=subprocess.PIPE).communicate()[0]
        except:
            OSError
            # try again
            break
        if 'running' in service_status.lower():
            not_running = 0
    return service,service_status


service,status = select_service()
print service,status
