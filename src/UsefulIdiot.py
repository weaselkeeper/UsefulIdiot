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

    def __init__(self, plugin):
        """Initialize the idiot"""
        log.debug('in UsefulIdiot().__init__(self, %s)' % plugin)

class ConfigFile(object):
    """Object to facilitate config file access"""
    log.debug('in class ConfigFile()')

    import ConfigParser
    filename = None
    configparser = None

    def __init__(self, filename):
        """Initialize ConfigFile object"""
        log.debug('in ConfigFile().init(self, %s)' % filename)
        self.filename = filename
        self.configparser = self._get_config(filename)

    def get_config(self, myfile):
        """Load config file for parsing"""
        log.debug('in ConfigFile().get_config(self, %s)' % myfile)
        config = ConfigParser.ConfigParser()
        config.read(myfile)
        log.debug('returning config: %s' % config)
        return config

    def get_item(self, cfgitem, section='default', hard_fail=False):
        """Retrieve value for requested key from the config file"""
        log.debug('in ConfigFile().get_item(self, %s, %s, %s)' % (cfgitem,
            section, hard_fail))

        def do_fail(err):
           if hard_fail:
              log.error(err)
              sys.exit(-1)
           else:
              log.info(err)

        item = None
        try:
           item = self.configparser.get(section, cfgitem)
        except ConfigParser.NoOptionError, e:
            do_fail(e)
        except ConfigParser.NoSectionError, e:
            do_fail(e)

        log.debug('returning item: %s' % item)
        return item

if __name__ == "__main__":
    """This is where we will begin when called from CLI"""

    import argparse
    from random import choice
    cmd_parser = argparse.ArgumentParser(
        description='Command a useful idiot to do something to your server')
    cmd_parser.add_argument('-d', '--debug', dest='debug',
        action='store_true', help='Enable debugging during execution',
        default=None)

    configfile = '/etc/usefulidiot/usefulidiot.conf'
    if os.path.isfile(configfile):
        log.debug('reading config from: %s' % configfile)
    elif os.path.isfile('../usefulidiot.conf'):
        log.debug('reading config from: ../conf/usefulidiot.conf')
        configfile = '../conf/usefulidiot.conf'
    else:
        log.debug('unable to read config file: %s' % configfile)
        sys.exit(1)
    cfg = ConfigFile(configfile)

    plugins = []
    plugins.append(cfg.get_item('plugins'))
    log.debug('found plugin(s): %s' % plugins)
    loaded_plugin = choice(plugins)
    log.debug('randomly selected plugin: %s' % loaded_plugin)

    idiot = UsefulIdiot(loaded_plugin)
