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

# used in ConfigFile()
import ConfigParser

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%y.%m.%d %H:%M:%S')
console = logging.StreamHandler(sys.stderr)
console.setLevel(logging.WARN)
logging.getLogger("usefulidiot").addHandler(console)
log = logging.getLogger("usefulidiot")


class UsefulIdiot(object):
    """Object to instantiate and control a useful idiot"""
    log.debug('in class UsefulIdiot()')

    def __init__(self, plugin, path, options={}):
        """Initialize the idiot"""
        log.debug('in UsefulIdiot().__init__(self, %s, %s)', plugin, path)

        import imp

        log.debug('importing ' + path)
        self.module = imp.load_source(plugin, path)
        self.options = options
        self.status = 'SUCCESS'
        self.message = ''

    def run(self):
        """Execute the plugin's run method"""
        log.debug('in UsefulIdiot().run()')
        self.status, self.message = self.module.run(self.options)

    def get_run_status(self):
        """Retrieve the return status/msg of the module that was executed"""
        log.debug('in UsefulIdiot().get_run_status()')

        final_status = {}
        final_status['status'] = self.status
        final_status['message'] = self.message

        return final_status


class ConfigFile(object):
    """Object to facilitate config file access"""
    log.debug('in class ConfigFile()')

    filename = None
    configparser = None

    def __init__(self, filename):
        """Initialize ConfigFile object"""
        log.debug('in ConfigFile().init(self, %s)', filename)

        self.filename = filename
        self.configparser = self.get_config(filename)

    def get_config(self, myfile):
        """Load config file for parsing"""
        log.debug('in ConfigFile().get_config(self, %s)', myfile)
        config = ConfigParser.ConfigParser()
        config.read(myfile)
        log.debug('returning config: %s', config)
        return config

    def get_item(self, cfgitem, section='default', hard_fail=False):
        """Retrieve value for requested key from the config file"""
        log.debug('in ConfigFile().get_item(self, %s, %s, %s)', cfgitem,
                  section, hard_fail)

        def do_fail(err):
            """ do something with a caught error """
            log.debug('in ConfigFile().get_item().do_fail(%s)', err)
            if hard_fail:
                log.error(err)
                sys.exit(-1)
            else:
                log.debug(err)

        item = None
        try:
            item = self.configparser.get(section, cfgitem)
        except ConfigParser.NoOptionError, e:
            do_fail(e)
        except ConfigParser.NoSectionError, e:
            do_fail(e)

        log.debug('returning item: %s', item)
        return item

if __name__ == "__main__":
    # This is where we will begin when called from CLI

    import argparse
    try:
        import json
    except ImportError:
        import simplejson as json
    from random import choice

    cmd_parser = argparse.ArgumentParser(
        description='Command a useful idiot to do something to your server.')
    cmd_parser.add_argument(
        '-n', '--dry-run', dest='dryrun', action='store_true',
        help='Dry run, do not actually perform action', default=False)
    cmd_parser.add_argument('-l', '--list_plugins', dest='list_plugins',
                            action='store_true',
                            help='List available plugins', default=False)
    cmd_parser.add_argument('-d', '--debug', dest='debug',
                            action='store_true',
                            help='Enable debugging during execution.',
                            default=None)
    cmd_parser.add_argument('-o', '--options', dest='options', action='store',
                            default=None,
                            help='Key/value options to pass to the plugin. \
                            Must be in key=value form, seperated by a comma \
                            with no space. Example: foo=bar,baz=blah')
    cmd_parser.add_argument('-p', '--plugin', dest='plugin_override',
                            action='store', default=None,
                            help='Specify a specific plugin to run.')
    cmd_parser.add_argument('-P', '--pluginpath', dest='plugin_dir_override',
                            action='store', default=None,
                            help='Specify a path to load plugins from.')
    cmd_parser.add_argument('-r', '--readable', dest='human_readable',
                            action='store_true', default=False,
                            help='Display output in human readable formant')
    cmd_parser.add_argument('-c', '--config', dest='config_override',
        action='store', default=None,
        help='Specify a path to an alternate config file')
    cmd_parser.add_argument('ansible_options', nargs='*')
    args = cmd_parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    options = {}
    # Note, this refers to the ansible options list above, not all the options
    # handed to UsefulIdiot via the command line
    tmp_options = args.options
    if tmp_options:
        for pair in tmp_options.split(','):
            key = pair.split('=')[0]
            value = pair.split('=')[1]
            options[key] = value
        # Now we add the dry-run option to the end, if set, to simplify the
        # calling process for the plugin
        if args.dryrun:
            options['dryrun'] = args.dryrun
    else:
        # need to add dryrun here, if no ansible options were passed
        options = {}
        if args.dryrun:
            options['dryrun'] = args.dryrun

    configfile = '/etc/usefulidiot/usefulidiot.conf'
    if args.config_override:
        configfile = args.config_override
        log.debug('config file location overriden on invocation, attempting \
            to use %s as config file source', configfile)
    elif os.path.isfile(configfile):
        log.debug('reading config from: %s', configfile)
    elif os.path.isfile('../config/usefulidiot.conf'):
        log.debug('reading config from: ../config/usefulidiot.conf')
        configfile = '../config/usefulidiot.conf'
    else:
        log.debug('unable to read config file: %s', configfile)
        sys.exit(1)
    cfg = ConfigFile(configfile)

    log.debug('detecting plugin(s) to use...')
    plugins = []
    try:
        log.debug('checking plugin override')
        if args.plugin_override:
            plugins.append(args.plugin_override)
            log.debug('overriding plugins to: %s', plugins)
        else:
            log.debug('no plugin override detected')
            raise NameError
    except NameError:
        plugins = cfg.get_item('plugins').split(',')
        log.debug('plugins override not found, pulling from config file: %s'
                  , plugins)
    log.debug('found plugin(s) to use: %s', plugins)
    if args.list_plugins:
        print 'available plugins are:'
        for element in plugins:
            print element,
        sys.exit(0)

    if not plugins:
        log.debug('no plugins found')
        print 'ERROR: No plugins found. Exiting.'
        sys.exit(1)
    log.debug('found plugin(s): %s', plugins)
    loaded_plugin = choice(plugins)
    log.debug('randomly selected plugin: %s', loaded_plugin)

    log.debug('detecting plugin(s) directory...')
    try:
        log.debug('checking plugin_dir override')
        if args.plugin_dir_override:
            plugin_dir = args.plugin_dir_override
            log.debug('overriding plugin_dir to: %s', plugin_dir)
        else:
            raise NameError
    except NameError:
        log.debug('no override provided for plugin_dir, checking config file')
        plugin_dir = cfg.get_item('plugin_dir')
        if not plugin_dir:
            log.debug('plugin_dir not found in config file')
            plugin_dir = '/usr/share/usefulidiot/plugins/'
            log.debug('plugin_dir set to default: %s', plugin_dir)
    log.debug('found plugin(s) directory to be: %s', plugin_dir)

    if not plugin_dir:
        print 'ERROR: Unable to determine plugin directory'
        sys.exit(1)

    if not os.path.isdir(plugin_dir):
        log.debug('plugin directory does not exist: %s', plugin_dir)
        print 'ERROR: Plugin directory does not exist: %s' % plugin_dir
        sys.exit(1)
    log.debug('attempting to load plugin from %s', plugin_dir)
    if os.path.isfile(plugin_dir + loaded_plugin):
        log.debug('plugin found at: ' + plugin_dir + loaded_plugin)
        plugin_path = plugin_dir + loaded_plugin
        loaded_plugin = loaded_plugin.split('.')[0]
    elif os.path.isfile(plugin_dir + loaded_plugin + '.py'):
        log.debug('plugin found at: ' + plugin_dir + loaded_plugin + '.py')
        plugin_path = plugin_dir + loaded_plugin + '.py'
    else:
        log.debug('unable to find plugin')
        print 'ERROR: Unable to locate plugin ' + loaded_plugin
        sys.exit(1)

    if args.dryrun:
        dryrun = True
    else:
        dryrun = False

    idiot = UsefulIdiot(loaded_plugin, plugin_path, options)
    idiot.run()
    if args.human_readable:
        print idiot.get_run_status()['message']
        sys.exit(idiot.get_run_status()['status'])
    else:
        print json.dumps(idiot.get_run_status())
