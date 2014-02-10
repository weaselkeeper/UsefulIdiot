#!/usr/bin/env python
""" Restart puppet on target machine, if someone has manually killed puppet, or
 it died for some reason, it will be restarted.  If they are relying on it
 being down, they are in for a surprise.

 Serves them right for not disabling puppet correctly.


 plugin options:

 [dryrun]
 default: False
 If True, only print what would have been done, but do not actually restart
 puppet

"""
import subprocess

def run(options={}):
    """main loop for this plugin"""

    _success = 0
    _message = 'puppet has not been restarted'

    if 'dryrun' in options:
        if options['dryrun'] == True:
            _message = 'I would have restarted puppet on this server'
            return _success, _message

    _message = restart_puppet()

    return _success, _message

def restart_puppet():
    """restarting puppet, as root of course."""
    process = subprocess.Popen(['/sbin/service', 'puppet restart'],
            stdout=subprocess.PIPE)
    _message = process.communicate()[0]
    return _message


if __name__ == "__main__":
    #This is where we will begin when called from CLI
    success, message = run()
    print success, message

