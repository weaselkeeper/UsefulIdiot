#!/usr/bin/env python

# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually kill
# the selected pid
#

import subprocess

def run(options={}):
    """main loop for this plugin"""

    from random import choice

    success = 0
    message = 'reboot unsuccessful'

    if 'dryrun' in options:
        if options['dryrun'] == True:
            message = 'I would have rebooted this server'
            return success, message

    reboot_system()

    return success, message

def reboot_system():
    """you realize this is dangerous, right?"""
    shutdown = 'echo "shutting down"'
    #shutdown = "/sbin/shutdown -r now"
    process = subprocess.Popen(shutdown.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
