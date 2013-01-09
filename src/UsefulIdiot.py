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
# used in UsefulIdiot()
import os
import sys
import logging

#used in ConfigFile()
import ConfigParser

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

    def __init__(self, plugin, path):
        """Initialize the idiot"""
        log.debug('in UsefulIdiot().__init__(self, %s, %s)' % (plugin, path))

        import imp

        log.debug('importing ' + path)
        self.module = imp.load_source(plugin, path)

    def run(self):
        """Execute the plugin's run method"""
        log.debug('in UsefulIdiot().run()')

        self.module.run()

class ConfigFile(object):
    """Object to facilitate config file access"""
    log.debug('in class ConfigFile()')

    filename = None
    configparser = None

    def __init__(self, filename):
        """Initialize ConfigFile object"""
        log.debug('in ConfigFile().init(self, %s)' % filename)

        self.filename = filename
        self.configparser = self.get_config(filename)

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
            log.debug('in ConfigFile().get_item().do_fail(%s)' % err)
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
    args = cmd_parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    configfile = '/etc/usefulidiot/usefulidiot.conf'
    if os.path.isfile(configfile):
        log.debug('reading config from: %s' % configfile)
    elif os.path.isfile('../config/usefulidiot.conf'):
        log.debug('reading config from: ../config/usefulidiot.conf')
        configfile = '../config/usefulidiot.conf'
    else:
        log.debug('unable to read config file: %s' % configfile)
        sys.exit(1)
    cfg = ConfigFile(configfile)

    plugins = []
    plugins.append(cfg.get_item('plugins'))
    if not plugins:
        log.debug('no plugins found')
        print 'No plugins found. Exiting.'
        sys.exit(1)
    log.debug('found plugin(s): %s' % plugins)
    loaded_plugin = choice(plugins)
    log.debug('randomly selected plugin: %s' % loaded_plugin)

    log.debug('locating plugin to load...')
    plugin_dir = cfg.get_item('plugin_dir')
    if not os.path.isdir(plugin_dir):
        log.debug('plugin directory does not exist: %s' % plugin_dir)
        print 'Plugin directory does not exist: %s' % plugin_dir
        sys.exit(1)
    log.debug('attempting to load plugin from %s' % plugin_dir)
    if os.path.isfile(plugin_dir + loaded_plugin):
        log.debug('plugin found at: ' + plugin_dir + loaded_plugin)
        plugin_path = plugin_dir + loaded_plugin
        loaded_plugin = loaded_plugin.split('.')[0]
    elif os.path.isfile(plugin_dir + loaded_plugin + '.py'):
        log.debug('plugin found at: ' + plugin_dir + loaded_plugin + '.py')
        plugin_path = plugin_dir + loaded_plugin + '.py'
    else:
        log.debug('unable to find plugin')
        print 'Unable to locate plugin ' + loaded_plugin
        sys.exit(1)

    idiot = UsefulIdiot(loaded_plugin, plugin_path)
    idiot.run()
