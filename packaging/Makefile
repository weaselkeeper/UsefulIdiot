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
## TOMAHAWK

deb:
	cd $(BASEDIR) && mkdir BUILD_TEMP && cd BUILD_TEMP


rpm:
	pass

clean:
	cd $(BASEDIR) && rm -rf BUILD_TEMP && cd -
