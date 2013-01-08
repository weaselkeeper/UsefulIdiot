#!/usr/bin/env python
# vim: set expandtab:
"""
**********************************************************************
GPL License
***********************************************************************
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

***********************************************************************/

:author: Jim Richardson
:email: weaselkeeper@gmail.com

:author: David Wahlstrom
:email: david.wahlstrom@gmail.com

"""
import os
import sys
import logging

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%y.%m.%d %H:%M:%S'
                   )
console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.WARN)
logging.getLogger("usefulidiot").addHandler(console)
log = logging.getLogger("usefulidiot")


class UsefulIdiot(object):
    """Object to instantiate and control a useful idiot"""
    log.debug('in class UsefulIdiot()')

    def __init__(self):
        """Intialize the idiot"""
        log.debug('in UsefulIdiot().__init__()')

        plugins = []

    def configure(self):
        """Read configuration for this idiot"""
        log.debug('in UsefulIdiot().configure()')

        from ConfigParser import SafeConfigParser

        parser = SafeConfigParser()
        configfile = '/etc/usefulidiot/usefulidiot.conf'
        if os.path.isfile(configfile):
            log.debug('reading config from: %s' % configfile)
        else:
            log.debug('unable to read config file: %s' % configfile)
            sys.exit(1)
        parser.read(configfile)
        self.plugins = parser.get('default', 'plugins')

if __name__ == "__main__":
    """This is where we will begin when called from CLI"""

    import argparse
    cmd_parser = argparse.ArgumentParser(description='Command a useful idiot to do something to your server')
    cmd_parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Enable debugging during execution', default=None)

    idiot = UsefulIdiot()
