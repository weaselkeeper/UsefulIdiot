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
    shutdown = "/sbin/shutdown -r now"
    # Use the following command for testing.
    shutdown = '/bin/echo "help me!"'
    try:
        subprocess.check_call(shutdown.split())
        success = 1
        message = 'rebooting server %s' % hostname
        return success,message
    except:
        success = 0
        message = 'unable to reboot server %s' % hostname
        return success,message
run()
