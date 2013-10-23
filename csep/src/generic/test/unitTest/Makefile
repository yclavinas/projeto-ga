# 
# 'src/generic/test/unitTest' Makefile to test CSEP functionality

.PHONY: default all install

default: all


### Nothing to do for all
all:


### Install rules - do nothing if destination directory is not provided
install:
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/generic/test/unitTest
	mkdir -p $(DESTDIR)/src/generic/test/unitTest;
	cp *.py $(DESTDIR)/src/generic/test/unitTest;
endif
