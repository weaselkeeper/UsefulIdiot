# Makefile is a confused mess.  Needs significant cleanup
NAME = usefulidiot
VERSION=0.4
RELEASE=0
SHELL := /bin/bash
SPECFILE = $(firstword $(wildcard *.spec))
WORKDIR := $(shell pwd)/work
SRCRPMDIR ?= $(shell pwd)
SPECFILE = packaging/rpm/usefulidiot.spec

DEBFULLNAME=Jim Richardson
DEBEMAIL=weaselkeeper@gmail.com
SOURCE_URL=https://github.com/weaselkeeper/usefulidiot.git
BASEDIR := $(shell git rev-parse --show-toplevel)

BUILDDIR ?= $(WORKDIR)
RPMDIR ?= $(shell pwd)
SOURCEDIR := $(shell pwd)
TAR := /bin/tar
RPM_DEFINES := --define "_sourcedir $(SOURCEDIR)" \
		--define "_builddir $(BUILDDIR)" \
		--define "_srcrpmdir $(SRCRPMDIR)" \
		--define "_rpmdir $(RPMDIR)" \

VER_REL := $(shell rpm $(RPM_DEFINES) -q --qf "%{VERSION} %{RELEASE}\n" --specfile $(SPECFILE)| head -1)

ifndef VERSION
	VERSION := $(word 1, $(VER_REL))
endif
ifndef RELEASE
	RELEASE := $(word 2, $(VER_REL))
endif
ifndef RPM
	RPM := rpmbuild
endif
ifndef RPM_WITH_DIRS
	RPM_WITH_DIRS = $(RPM) $(RPM_DEFINES)
endif

TARSRC = $(NAME)-$(VERSION)

#TODO: this should probably be a tag rather than just the latest commit.
TAG             := $(shell git log ./ | head -1 | sed 's/commit //')

###########
## Some setup

authors:
	sh packaging/authors.sh

common: authors

testall: authors deb srpm rpm

# Build targets

# Debian related.
deb: common
	cp -r src/* LICENSE conf/* README.md packaging/deb
	cd BUILD_TEMP/debian && equivs-build $(NAME)

# Redhat related
build-srpm:
	$(RPM) -bs $(RPM_DEFINES) $(SPECFILE)

build-rpm:
	$(RPM) -bb $(RPM_DEFINES) $(SPECFILE)

all: srpm

sources:
	@mkdir usefulidiot
	@cp    src/UsefulIdiot.py usefulidiot
	@cp -r src/plugins usefulidiot
	@cp -r config usefulidiot
	@mkdir -p $(SOURCEDIR)
	@mkdir -p $(WORKDIR)
	@/bin/tar -jcf $(SOURCEDIR)/$(TARSRC).tar.bz2 $(NAME)

srpm: sources build-srpm 

rpm: sources build-rpm 


# Cleanup
clean:
	@echo "cleaning up "
	@/bin/rm -rf $(WORKDIR)
	@/bin/rm -rf usefulidiot
	@/bin/rm -rf usefulidiot*rpm
	@/bin/rm -rf usefulidiot*tar*
	@rm -rf newtests
	@rm -f test.log
	@cd $(BASEDIR) && rm -rf BUILD_TEMP && rm -f AUTHORS.TXT $(NAME)-$(VERSION)_$(RELEASE).tar.gz
	@find $(BASEDIR) -iname *.py[co] | xargs -i rm -f {}
	@rm -rf noarch
	@rm -f packaging/deb/*py packaging/deb/*conf packaging/deb/LICENSE packaging/deb/README.md packaging/deb/*.deb

# Usage
help:
	@echo 'Makefile for UsefulIdiot, currently supports deb and rpm '
	@echo ' builds from current source tree.				'
	@echo "Usage: make <target>"
	@echo "Available targets are:"
	@echo " sources			Create tarball"
	@echo "	srpm			Create srpm"
	@echo "	rpm			Create rpm"
	@echo "	clean			Remove work dir"
	@echo "	deb			Create debian package"


#Tests
nosetests:
# no tests written yet, but here's the framework
	mkdir newtests
	PYTHONPATH=./ nosetests -v -w newtests/ 2>&1 | tee test.log



###########
## Build packages


#rpm: common
#	cd $(BASEDIR) && mkdir -p BUILD_TEMP/rpm
#	cd BUILD_TEMP/rpm
#	git archive HEAD --format tar.gz --output $(NAME)-$(VERSION)_$(RELEASE).tar.gz


