#!/usr/bin/env python

# Toggle selinux enforcement, if on, set off, if off, set on.
# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually toggle
# selinux
#

import subprocess
import os
import sys
import selinux

selinux_policy  = 'on'
selinux_target = 'on'
if selinux.is_selinux_enabled():
    try:
        is_enforce = selinux.security_getenforce()
    except:
        print 'error!'
        sys.exit(1)
else:
    print 'selinux disabled on this system, will not be able to toggle setting'
    sys.exit(1)

def run(options={}):
    """main loop for this plugin"""

    success = 1
    message = 'toggle unsuccessful, selinux setting unchanged'

    if 'dryrun' in options:
        if options['dryrun'] == True:
            success = 0
            message = 'I would have toggled selinux enforcing %s' % selinux_target
            return success, message
    success,message = toggle_selinux()
    return success,message

def toggle_selinux(is_enforce):
    """you realize this is dangerous, right?"""
    # Use the following command for testing.
    try:
        #toggle enforcing.
        selinux_target = not is_enforce
        selinux.security_setenforce(selinux_target)
        success = 0
        message = 'selinux policy set to %s' % selinux_target

    except Exception as error:
        success = 1
        message = 'unable to toggle selinux enforcing due to %s' % err
        return success,message





if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    # First, is SELinux available on this system?
    if os.path.exists('/selinux/enforcing'):
        success,message = 0,'SELinux is present and available.'
    else:
        success,message = 1,'Sorry, SELinux is not available on this host'
        print success,message
        sys.exit(1)
    success,message = run()
    print success,message

