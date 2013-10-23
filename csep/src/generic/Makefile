### 'src' level Makefile to build CSEP

SUBDIRS = test matlab
DIST_SUBDIRS = test

TARGET ?= all

###  Build rules
.PHONY: default all $(SUBDIRS) install check clean testclean distcheck

###### Default Rules (no target is provided)
default: all

###### All Rules 
all: $(SUBDIRS)

$(SUBDIRS):
	@cd $@; $(MAKE) all

###### Install Rules
install:
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/generic

	mkdir -p $(DESTDIR)/src/generic;
	cp *.py $(DESTDIR)/src/generic;
	rsync -aC utils $(DESTDIR)/src/generic;
endif

	@for dir in $(SUBDIRS); do \
		pushd $$dir; $(MAKE) install; popd; \
	done

###### Test Rules
check:
	@for dir in $(SUBDIRS); do \
		pushd $$dir; $(MAKE) check; popd; \
	done

# Rule to test generic CSEP distribution
distcheck:
	@for dir in $(DIST_SUBDIRS); do \
		pushd $$dir; $(MAKE) distcheck; popd; \
	done

####### Clean Rules
clean:
	@for dir in $(SUBDIRS); do \
		cd $$dir; $(MAKE) clean; cd $(PWD); \
	done

###### Test Clean Rules
testclean:
	@for dir in $(SUBDIRS); do \
		cd $$dir; $(MAKE) testclean; cd $(PWD); \
	done
