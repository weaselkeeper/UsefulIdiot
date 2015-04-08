#!/usr/bin/env python
DOCUMENTATION = '''
---
module: cronripper
short_description: delet user's crontab
description:
     - Delete's a (random) user's crontab
options:
  user:
    description:
      - which user shall lose their crontab? random means pick any crontab in
        /var/spool/cron
    required: false
    default: 'random'
    aliases: []

examples:
   - code: cronripper name='jgomez'
   - code: cronripper name='random'
   - code: cronripper
notes: []
# informational: requirements for nodes
requirements: [ crontab, ]
author: Jim Richardson <weaselkeeper@gmail.com>
'''

# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually delete
# the selected user's cron
#


import subprocess
from random import choice
import os


def run(options={}):
    """main loop for this plugin"""

    _success = 1
    _message = "cronripper did not complete it's run"

    # this is the user whose cron we will kill
    target_user = get_user()
    _message = "unable to remove crontab for user %s " % target_user

    if 'dryrun' in options:
        if options['dryrun']:
            _message = 'I would have decronned: %s ' % target_user
            return _success, _message

    _success, _message = kill_crontab(target_user)

    return _success, _message


def kill_crontab(user):
    """try to delete the crontab for user, returning the result"""
    try:
        user_var = '-u' + user
        cronkill = subprocess.Popen(['crontab', '-r', user_var],
                                    stdout=subprocess.PIPE,\
                                    stderr=subprocess.PIPE)
        out, err = cronkill.communicate()
        rc = cronkill.poll()
        if rc:
            #Something went wrong, return not 0
            _success = rc
            _message = err
        else:
            _success = 0
            _message = 'removed crontab for user %s' % user
        return _success, _message

    except Exception as error:
        _success = 1
        _message = 'unable to remove crontab for %s due to %s' % (user, error)
        return _success, _message


def get_user():
    """get list of valid users with crontabs"""
    users = subprocess.Popen(['getent', 'passwd'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    user_list, error = users.communicate()
    user = choice(user_list.split('\n'))
    username = user.split(':')[0]
    cronfile = '/var/spool/cron/' + username
    if not os.path.exists(cronfile):
        user = get_user()
    return username


if __name__ == "__main__":
    # This is where we will begin when called from CLI
    success, message = run()
    print success, message
