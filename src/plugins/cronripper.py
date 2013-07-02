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

import os

def run(options={}):
    """main loop for this plugin"""

    from random import choice

    success = 0
    message = "cronripper did not complete it's run"

    # this is the pid we will kill
    target_user = choice(get_user())
    message = "cronripper was unable to remove crontab for user %s " % target_user

    if 'dryrun' in options:
        if options['dryrun'] == True:
            message = 'I would have decronned: ' + target_user
            return success, message

    success = kill_crontab(target_user)
    message = "User %s is now cron free!" % target_user

    return success, message

def kill_crontab(user):
    """try to delete the crontab for user, returning the result"""

    try:
        "NOTDONE YET  Get os.subprocess to kill teh cron!"
        return 0
    except OSError:
        #somefailure and error checking here.
        return 1
    #pid already gone, so nothing to kill :(
    return 1

def get_user():
    """get list of valid users with crontabs"""
    user =  "# DO stuff"
    return user


if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    run()
