#!/usr/bin/env python
"""
 plugin options:

 [dryrun]
 default: False
 If True, only print what would have beeen done, but do not actually reap /tmp
 of old files
"""
DOCUMENTATION = '''
---
module: cronripper
short_description: delete old files in /tmp
description:
     - Deletes all files in /tmp older than N days (default 10)
options:
  age:
    description:
      - Files in /tmp older than <age> days will be deleted. Default 10
    required: false
    default: '10'
    aliases: []

examples:
   - code: tempreaper age=1
notes: []
# informational: requirements for nodes
requirements: [ bash, ]
author: Jim Richardson <weaselkeeper@gmail.com>
'''

import os
import time
import shutil


def run(options={}):
    """main loop for this plugin"""

    _success = 1
    _message = "tempreaper was unable to complete it's run"
    age = 10
    if age in options:
        age = options.age

    if 'dryrun' in options:
        if options['dryrun']:
            _message = 'files in /tmp older than %d days deleted' % age
            return _success, _message

    _success, _message = tmp_reaper(age)

    return _success, _message


def tmp_reaper(age):
    """ Main function, do what you do """
    _success, _message = 1, "tempreaper was unable to complete it's run"
    for _file in os.listdir('/tmp'):
        tmpfile = os.path.join('/tmp', _file)
        if os.stat(tmpfile).st_mtime < time.time()-(age * 86400):
            try:
                os.remove(tmpfile)
            except OSError:
                shutil.rmtree(tmpfile)
            _success = 0
            _message = "No files left in /tmp older than %d days" % age
    return _success, _message

if __name__ == "__main__":
    # This is where we will begin when called from CLI
    success, message = run()
    print success, message
