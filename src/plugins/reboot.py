#!/usr/bin/env python

# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually kill
# the selected pid
#

import subprocess
import socket

hostname = socket.gethostname()

def run(options={}):
    """main loop for this plugin"""

    success = 0
    message = 'reboot unsuccessful'

    if 'dryrun' in options:
        if options['dryrun'] == True:
            message = 'I would have rebooted server %s' % hostname
            return success, message
    success,message = reboot_system()
    return success,message

def reboot_system():
    """you realize this is dangerous, right?"""
    # Use the following command for testing.
    try:
        shutdown = subprocess.Popen(['/sbin/shutdown','now'],
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = shutdown.communicate()
        print out,err
        success = 1
        message = 'rebooting server %s' % hostname
        return success,message
    except Exception as error:
        success = 0
        message = 'unable to reboot server %s due to' % hostname,error
        return success,message

if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    success,message = run()
    print success,message

