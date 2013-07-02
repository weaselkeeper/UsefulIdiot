#!/usr/bin/env python


# Restart puppet on target machine, if someone has manually killed puppet, or
# it died for some reason, it will be restarted.  If they are relying on it
# being down, they are in for a surprise. 
#
# Serves them right for not disabling puppet correctly.


# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have been done, but do not actually kill
# the selected pid
#

import subprocess

def run(options={}):
    """main loop for this plugin"""

    success = 0
    message = 'puppet has not been restarted'

    if 'dryrun' in options:
        if options['dryrun'] == True:
            message = 'I would have restarted puppet on this server'
            return success, message

    message=restart_puppet()

    return success, message

def restart_puppet():
    """restarting puppet, as root of course."""
    process = subprocess.Popen(['/sbin/service','puppet restart'], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    return output


if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    run()

