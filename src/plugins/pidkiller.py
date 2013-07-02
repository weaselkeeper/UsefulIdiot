#!/usr/bin/env python

# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually kill
# the selected pid
#
# [ensure]
# default: False
# If True, this app will keep trying to kill a pid until it successfully does
# so.  It is possible for a pid to be gone before this app tries to kill it,
# thus making it no-op.

import os

def run(options={}):
    """main loop for this plugin"""

    from random import choice

    success = 0
    message = "pidkiller did not complete it's run"

    # this is the pid we will kill
    target_pid = choice(get_pids())
    message = "pidkiller did not complete it's run, for some reason, failing to kill Process %s" % target_pid

    if 'dryrun' in options:
        if options['dryrun'] == True:
            message = 'I would have killed: ' + target_pid
            return success, message

    if 'ensure' in options:
        if True in options['ensure']:
            success = 1
            while success == 1:
                target_pid = choice(get_pids)
                success = kill_pid(target_pid)
            message = "pid %s successfully killed!" % target_pid

    return success, message

def kill_pid(pid):
    """try to kill the pid, returning the result"""

    if pid in get_pids():
        try:
            os.kill(pid, 9)
            return 0
        except OSError:
            #pid already gone, so nothing to kill :(
            return 1
    #pid already gone, so nothing to kill :(
    return 1

def get_pids():
    """get list of running pids"""
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    if 1 in pids:
        pids.remove(1)

    return pids

if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    success,message = run()
    print success,message

