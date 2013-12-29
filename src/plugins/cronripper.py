#!/usr/bin/env python

# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually delete
# the selected user's cron
#

DOCUMENTATION = '''                                                            g
---                                                                            g
module: cronripper                                                             g
short_description: delet user's crontab                                        g
description:                                                                   g
     - Delete's a (random) user's crontab                                      g
options:                                                                       g
  user:                                                                        g
    description:                                                               g
      - which user shall lose their crontab? random means pick any crontab in  g
        /var/spool/cron                                                        g
    required: false                                                            g
    default: 'random'                                                          g
    aliases: []                                                                g
                                                                               g
examples:                                                                      g
   - code: cronripper name='jgomez'                                            g
   - code: cronripper name='random'                                            g
   - code: cronripper                                                          g
notes: []                                                                      g
# informational: requirements for nodes                                        g
requirements: [ crontab, ]                                                     g
author: Jim Richardson <weaselkeeper@gmail.com>                                g
'''

import subprocess
from random import choice
import os


def run(options={}):
    """main loop for this plugin"""

    _success = 1
    _message = "cronripper did not complete it's run"

    # this is the user whose cron we will kill
    target_user = get_user()
    _message = "cronripper was unable to remove crontab for user %s " % target_user

    if 'dryrun' in options:
        if options['dryrun'] == True:
            _message = 'I would have decronned: %s ' % target_user
            return _success, _message

    _success = kill_crontab(target_user)
    _message = "User %s is now cron free!" % target_user

    return _success, _message

def kill_crontab(user):
    """try to delete the crontab for user, returning the result"""
    try:
        user_var = '-u' + user
        cronkill = subprocess.Popen(['crontab', '-r', user_var],
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = cronkill.communicate()
        _success = 0
        _message = 'removed crontab for user %s' % user
        return _success, _message

    except Exception as error:
        _success = 1
        _message = 'unable to remove crontab for %s due to %s' % (user, error)
        return _success, _message


def get_user():
    """get list of valid users with crontabs"""
    users = subprocess.Popen(['getent','passwd'],
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    user_list, error = users.communicate()
    user = choice(user_list.split('\n'))
    username = user.split(':')[0]
    cronfile = '/var/spool/cron/' + username
    if not os.path.exists(cronfile):
        user = get_user()
    return username


if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    success, message = run()
    print success, message
