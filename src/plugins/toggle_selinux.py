#!/usr/bin/env python
"""
 Toggle selinux enforcement, if on, set off, if off, set on.
 plugin options:

 [dryrun]
 default: False
 If True, only print what would have beeen done, but do not actually toggle
 selinux
"""

DOCUMENTATION = '''
---
module: cronripper
short_description: delete old files in /tmp
description:
      - toggles selinux enforcing setting. Permissive/Enforcing
examples:
   - code: toggle_selinux
notes: []
# informational: requirements for nodes
requirements: python-selinux
author: Jim Richardson <weaselkeeper@gmail.com>
'''

import selinux
import sys

def run(options={}):
    """main loop for this plugin"""

    _success = 1
    _message = 'toggle unsuccessful, selinux setting unchanged'

    if 'dryrun' in options:
        if options['dryrun'] == True:
            _success = 0
            _message = 'I would have toggled selinux enforcing setting'
            return _success, _message

    # First, is SELinux available on this system?
    if selinux.is_selinux_enabled():
        try:
            is_enforce = selinux.security_getenforce()
        except:
            _success, _message = 1, 'SELinux is not available on this host'
            return _success, _message
    else:
        print 'selinux disabled, will not be able to toggle setting'
        sys.exit(1)

    _success, _message = toggle_selinux(is_enforce)
    return _success, _message


def toggle_selinux(is_enforce):
    """you realize this is dangerous, right?"""
    # Use the following command for testing.
    try:
        #toggle enforcing.
        selinux_target = not is_enforce
        selinux.security_setenforce(selinux_target)
        _success = 0
        _message = 'selinux policy set to %s' % selinux_target

    except Exception as error:
        _success = 1
        _message = 'unable to toggle selinux enforcing due to %s' % error
    return _success, _message


if __name__ == "__main__":
    #This is where we will begin when called from CLI
    success, message = run()
    print success, message

