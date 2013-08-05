#!/usr/bin/env python
"""
Setup script.
"""

from distutils.core import setup


setup(name = "usefulidiot",
    version = "0.4",
    description = "UsefulIdiot, a minion of menace",
    long_description = "Randomly mess with your servers.",
    author = "Jim Richardson",
    author_email = 'weaselkeeper@gmail.com',
    url = "https://github.com/weaselkeeper/usefulidiot",
    download_url = "https://github.com/weaselkeeper/usefulidiot",
    platforms = ['any'],
    license = "GPLv2",
    package_dir = {'usefulidiot': 'src/' },
    packages = ['usefulidiot'],
    classifiers = [
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Programming Language :: Python'],
)
