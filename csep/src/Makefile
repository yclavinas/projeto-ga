### 'src' level Makefile to build CSEP

SUBDIRS = generic \
          GMTScripts \
          AlarmBasedTests \
          DiagnosticsTests \
          get_Catalog \
          RELMTests \
          SCECModels \
          
ifeq ($(DISABLE_DECLUSTER_CODE), false)
	SUBDIRS += ReasenbergDecluster
endif

DIST_SUBDIRS = generic

TARGET ?= all

###  Build rules
.PHONY: default all $(SUBDIRS) install check clean testclean distcheck

###### Default Rules (no target is provided)
default: all

###### All Rules 
all: $(SUBDIRS)

$(SUBDIRS):
	if test -d $@; then \
		cd $@; $(MAKE) all; \
	fi

###### Install Rules
install:
	@for dir in $(SUBDIRS); do \
		if test -d $$dir; then \
			pushd $$dir; $(MAKE) install; popd; \
		fi \
	done

###### Test Rules
check:
	@for dir in $(SUBDIRS); do \
		if test -d $$dir; then \
			pushd $$dir; $(MAKE) check; popd; \
		fi \
	done

# Rule to test generic CSEP distribution
distcheck:
	@for dir in $(DIST_SUBDIRS); do \
		if test -d $$dir; then \
			pushd $$dir; $(MAKE) distcheck; popd; \
		fi \
	done

####### Clean Rules
clean:
	@for dir in $(SUBDIRS); do \
		if test -d $$dir; then \
			cd $$dir; $(MAKE) clean; cd $(PWD); \
		fi \
	done

###### Test Clean Rules
testclean:
	@for dir in $(SUBDIRS); do \
		if test -d $$dir; then \
			cd $$dir; $(MAKE) testclean; cd $(PWD); \
		fi \
	done
