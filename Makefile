SHELL := /bin/bash

BASEDIR=$(CURDIR)

DEBFULLNAME=Jim Richardson
DEBEMAIL=weaselkeeper@gmail.com
SOURCE_URL=https://github.com/tomahawk-player/tomahawk.git


NIGHTLY=$(shell date +'%Y.%m.%d.nightly')

help:
	@echo 'Makefile for UsefulIdiot, currently supports deb and rpm '
	@echo ' builds from current source tree.				'
	@echo 'Usage:							'
	@echo '   make debian or make rpm				'

###########
## Some setup

authors:
	sh packaging/authors.sh

###########
## Build packages

rpm: authors
	cd $(BASEDIR) && mkdir -p BUILD_TEMP/rpm
	cd BUILD_TEMP/rpm

deb: authors
	cd $(BASEDIR) && mkdir -p BUILD_TEMP/debian && echo 'setting up temp build env'
	cd BUILD_TEMP/debian

clean:
	cd $(BASEDIR) && rm -rf BUILD_TEMP && rm -f AUTHORS.TXT cd -
