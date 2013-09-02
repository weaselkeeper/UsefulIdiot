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

def run(options={}):
    """main loop for this plugin"""

    success = 1
    message = 'toggle unsuccessful, selinux setting unchanged'

    if 'dryrun' in options:
        if options['dryrun'] == True:
            success = 0
            message = 'I would have toggled selinux enforcing %s' % selinux_target
            return success, message
    success,message = toggle_selinux(is_enforce)
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
        message = 'unable to toggle selinux enforcing due to %s' % error
    return success,message





if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    # First, is SELinux available on this system?
    import selinux
    success, message = 1, 'Operation failed'
    if selinux.is_selinux_enabled():
        try:
            is_enforce = selinux.security_getenforce()
            #print is_enforce
        except:
            success,message = 1,'Sorry, SELinux is not available on this host'
            #print success,message
            sys.exit(1)
    else:
        print 'selinux disabled on this system, will not be able to toggle setting'
        sys.exit(1)

    success,message = toggle_selinux(is_enforce)
    print success,message

