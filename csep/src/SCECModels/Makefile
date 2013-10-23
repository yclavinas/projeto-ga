### 'src/SCECModels' level Makefile to build CSEP

SUBDIRS = postProcessing 

# Add models to the build process only if 
ifeq ($(DISABLE_MODELS), false)
ifeq ($(DISTRIBUTION_BUILD),)
	SUBDIRS += California WesternPacific Global OceanicTransformFaults
else
	SUBDIRS += NewZealand Japan EU
endif
endif


TARGET ?= all

###  Build rules
.PHONY: default all $(SUBDIRS) install check clean testclean

###### Default Rules (no target is provided)
#default: all

###### All Rules 
all: $(SUBDIRS)
	@echo $(SUBDIRS)

$(SUBDIRS):
	if test -d $@; then \
		cd $@; $(MAKE) all; \
	fi

# Check if generic Python modules are available for installation
have_generic_modules := $(wildcard *.py)

###### Install Rules
install:
ifeq '$(DESTDIR)' ''
else
ifeq ($(strip $(have_generic_modules)),)
else
	# Copy generic modules 
	@echo destdir=$(DESTDIR)/src/SCECModels
	mkdir -p $(DESTDIR)/src/SCECModels;
	cp *.py $(DESTDIR)/src/SCECModels;
endif
endif

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

####### Clean Rules
clean:
	@for dir in $(SUBDIRS); do \
		if test -d $$dir; then \
			cd $$dir; $(MAKE) clean; cd $(PWD); \
		fi \
	done

####### Test clean rules
testclean:
	@for dir in $(SUBDIRS); do \
		if test -d $$dir; then \
			cd $$dir; $(MAKE) testclean; cd $(PWD); \
		fi \
	done
