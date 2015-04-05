#!/usr/bin/env python

# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually reboot
# the selected server
#

import subprocess
import socket

hostname = socket.gethostname()

def run(options={}):
    """main loop for this plugin"""

    _success = 1
    _message = 'reboot unsuccessful'

    if 'dryrun' in options:
        if options['dryrun'] == True:
            _success = 0
            _message = 'I would have rebooted server %s' % hostname
            return _success, _message
    _success, _message = reboot_system()
    return _success, _message

def reboot_system():
    """you realize this is dangerous, right?"""
    # Use the following command for testing.
    try:
        shutdown = subprocess.Popen(['/sbin/shutdown', 'now'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = shutdown.communicate()
        return_code = shutdown.returncode
        if return_code == 0:
            _success = 0
            _message = 'rebooting server %s' % hostname
        else:
            _success = 1
            _message = 'unable to reboot server %s due to %s' % (hostname, err)
        return _success, _message
    except Exception as error:
        _success = 1
        _message = 'unable to reboot server %s due to %s' % (hostname, error)
        return _success, _message

if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    _success, _message = run()
    print _success, _message

