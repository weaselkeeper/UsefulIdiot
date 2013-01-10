#!/usr/bin/env python

# plugin options:
#
# [dry-run]
# default: False
# If True, only print what would have beeen done, but do not actually uninstall
# the selected package
#

import rpm
import sys

def run(options={}):
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

    if 'dry-run' in options:
        if 'true' in options['dry-run'].lower():
            message = 'I would have uninstalled: %s' % target_package
            return success, message
            
    sucess = rpm_uninstall(target_package)

    return success, message

def rpm_uninstall(pkg):
    """try to uninstall the package, returning the result"""

    return 0
