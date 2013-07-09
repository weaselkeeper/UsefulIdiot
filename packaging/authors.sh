#!/bin/sh
# script from http://stackoverflow.com/questions/12133583
# In turn, I grabbed it from Ansible
set -e

# Get a list of authors ordered by number of commits
# and remove the commit count column
AUTHORS=$(git --no-pager shortlog -nse | cut -f 2- | sort -f)
if [ -z "$AUTHORS" ] ; then
    echo "Authors list was empty"
    exit 1
fi

# Display the authors list and write it to the file
echo "$AUTHORS" | tee "$(git rev-parse --show-toplevel)/AUTHORS.TXT"
