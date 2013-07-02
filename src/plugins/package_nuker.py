#!/usr/bin/env python

# plugin options:
#
# [dryrun]
# default: False
# If True, only print what would have beeen done, but do not actually uninstall
# the selected package
#
# Currently, this plugin only supports rpm packages. Will likely add .deb at
# least. Additionally, it will faile if the package has others dependant upon
# it, unsure if we should force, or switch to using yum/apt and removing those
# dependant packages also.

import sys
try:
    import rpm
except ImportError:
        error = """No rpm module avaible, maybe this isn't an rpm system? 
Either install the rpm module, or find some other way"""
        print error
        sys.exit(1)

def run(options={}):
    print options.keys()
    """main loop for this plugin"""
    from random import choice

    success = 0
    message = "package_nuker completed it's run"

    # initialize RPM database connection
    ts = rpm.TransactionSet()

    # obtain a list of the packages that are installed
    packages_installed = []
    for pkg in ts.dbMatch():
        packages_installed.append(pkg)

    # this is the package we will uninstall
    target_package = choice(packages_installed)

    if 'dryrun' in options:
        if options['dryrun'] == True:
            message = 'I would have removed ' + target_package
            return success, message

    if options['dryrun']==True:
        message = 'I would have uninstalled: %s' % target_package['name']
        return success, message

    success = rpm_uninstall(target_package)

    return success, message

def rpm_uninstall(pkg):
    """try to uninstall the package, returning the result"""
    ts = rpm.TransactionSet()
    ts.addErase(pkg)
    return 0



if __name__ == "__main__":
    """This is where we will begin when called from CLI"""
    run()

