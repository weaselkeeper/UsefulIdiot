SHELL := /bin/bash

DEBFULLNAME=Jim Richardson
DEBEMAIL=weaselkeeper@gmail.com
SOURCE_URL=https://github.com/tomahawk-player/tomahawk.git
BASEDIR := $(shell git rev-parse --show-toplevel)

NAME=usefulidiot
VERSION=0.3
RELEASE=0

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
nosetests:
	mkdir newtests
	PYTHONPATH=./ nosetests -v -w newtests/ 2>&1 | tee test.log



###########
## Build packages

common: authors

rpm: common
	cd $(BASEDIR) && mkdir -p BUILD_TEMP/rpm
	cd BUILD_TEMP/rpm
	git archive HEAD --format tar.gz --output $(NAME)-$(VERSION)_$(RELEASE).tar.gz

deb: common
	cd $(BASEDIR) && mkdir -p BUILD_TEMP/debian && echo 'setting up temp build env'
	cd BUILD_TEMP/debian

clean:
	rm -rf newtests
	rm test.log
	cd $(BASEDIR) && rm -rf BUILD_TEMP && rm -f AUTHORS.TXT $(NAME)-$(VERSION)_$(RELEASE).tar.gz
