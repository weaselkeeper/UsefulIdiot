#!/usr/bin/env python

# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually reap /tmp
# of old files
#


DOCUMENTATION = '''
---
module: cronripper
short_description: delete old files in /tmp
description:
     - Deletes all files in /tmp older than N days (default 10)
options:                                                                       g
  age:
    description:                                                               g
      - Files in /tmp older than <age> days will be deleted. Default 10
    required: false
    default: '10'
    aliases: []                                                                g
                                                                               g
examples:                                                                      g
   - code: tempreaper age=1
notes: []                                                                      g
# informational: requirements for nodes                                        g
requirements: [ bash, ]
author: Jim Richardson <weaselkeeper@gmail.com>                                g
'''

import os
import time
def run(options={}):
    """main loop for this plugin"""

    success = 1
    message = "tempreaper was unable to complete it's run"
    age = 10
    if age in options:
        age = options.age

    if 'dryrun' in options:
        if options['dryrun'] == True:
            message = 'I would have deleted files in /tmp older than %d days' %age
            return success, message

    success,message = tmp_reaper(age)

    return success, message

def tmp_reaper(age):
    success,message = 1,"tempreaper was unable to complete it's run"
    for f in os.listdir('/tmp'):
        tmpfile = os.path.join('/tmp',f)
        if os.stat(tmpfile).st_mtime < time.time()- ( age * 86400 ):
            os.remove(tmpfile)
            success, message = 0,"No files left in /tmp older than %d" % age
    return success,message

if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    success,message = run()
    print success,message
