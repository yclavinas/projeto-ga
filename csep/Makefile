### Top level Makefile to build CSEP

SHELL=/bin/sh


### Check if it's a distribution or SCEC testing center build
NATURAL_LABORATORIES_SRC = CaliforniaForecastFactory.init.xml \
                           WesternPacificForecastFactory.init.xml \
                           GlobalForecastFactory.init.xml \
                           OceanicTransformFaultsForecastFactory.init.xml

have_forecasts_models := $(wildcard *ForecastFactory.init.xml)

ifeq ($(strip $(have_forecasts_models)),)
	export DISTRIBUTION_BUILD := 1
else
	export DISTRIBUTION_BUILD := 
endif

# Assume that distributions are built from 'trunk' directory
ifeq '$(DISTSOURCE)' ''
   export DIST_SOURCE := trunk
else
   export DIST_SOURCE := $(DISTSOURCE)
endif

# Allow to disable declustering code, which requires ifort compiler,
# from command-line:
# DISABLE_DECLUSTER_CODE=true
export DISABLE_DECLUSTER_CODE ?= false

# Allow to disable build of models binaries, that are checked out from repository,
# from command-line:
# DISABLE_MODELS=true 
export DISABLE_MODELS ?= false


SUBDIRS = src
GENERIC_DIST_SUBDIRS = data configuration cronjobs distribution

TARGET ?= all

###  Build rules
.PHONY: default all $(SUBDIRS) install check clean testclean distcheck


###### Default Rules (no target is provided)
default: all

###### All Rules 
all: $(SUBDIRS)

$(SUBDIRS):
	@cd $@; $(MAKE) all


### Define directory for testing center configuration files
ifeq '$(DESTDIR)' ''
   export TESTING_CENTER_CONFIG_DIR := $(shell pwd)/TestingCenterConfiguration
else
   export TESTING_CENTER_CONFIG_DIR := $(DESTDIR)/TestingCenterConfiguration
endif


###### Install Rules
install:
	mkdir -p $(TESTING_CENTER_CONFIG_DIR)

ifeq '$(DESTDIR)' ''
else
	@for s in $(GENERIC_DIST_SUBDIRS); do \
		if test -d $$s; then \
			echo $$s exists; mkdir -p $(DESTDIR); rsync -aC $$s $(DESTDIR); \
		fi \
	done

	@for s in $(NATURAL_LABORATORIES_SRC); do \
		if test -f $$s; then \
			echo $$s exists; mkdir -p $(DESTDIR); cp $$s $(DESTDIR); \
		fi \
	done

endif

	@for dir in $(SUBDIRS); do \
		pushd $$dir; $(MAKE) install; popd; \
	done



###### Generic Distribution Test Rules
distcheck: testclean
	@for dir in $(SUBDIRS); do \
		pushd $$dir; $(MAKE) distcheck; popd; \
	done


###### Test Rules
check:
	@for dir in $(SUBDIRS); do \
		pushd $$dir; $(MAKE) check; popd; \
	done

####### Clean Rules
clean:
	@for dir in $(SUBDIRS); do \
		cd $$dir; $(MAKE) clean; cd $(PWD); \
	done

	find . -name '*.pyc' -exec rm -rf {} \; -print
	find . -name '*~' -exec rm -rf {} \; -print



###### Test Clean Rules
testclean:
	@for dir in $(SUBDIRS); do \
		cd $$dir; $(MAKE) testclean; cd $(PWD); \
	done

###### Distribution Rules
version_string := "13.4.0"
dist_dir := csep-$(version_string)
minidist_dir := csepmini-$(version_string)
ca_dist_dir := csepca-$(version_string)
wp_dist_dir := csepwp-$(version_string)
global_dist_dir := csepglobal-$(version_string)
oceanic_dist_dir := csepoceanic-$(version_string)
nz_dist_dir := csepnz-$(version_string)
japan_dist_dir := csepjapan-$(version_string)
eu_dist_dir := csepeu-$(version_string)

### All distributions
dist: genericdist cadist wpdist globaldist nzdist japandist minidist eudist oceanicdist
	cp ../csep*.tar.gz /home/csep/rpmbuild/SOURCES;
	cd distribution; make dist;

AUX = build.xml Makefile NEWS
AUX_DIRS = src $(GENERIC_DIST_SUBDIRS)

### Generic distribution 	  
genericdist: clean testclean
	ls $(AUX) | sed s:^:$(dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS) | sed s:^:$(dist_dir)/: >>MANIFEST	
	@(cd ..; ln -s $(DIST_SOURCE) $(dist_dir))
	@(cd ..; tar zcvf $(dist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn' \
--exclude 'SCECModels/California' --exclude 'SCECModels/WesternPacific' \
--exclude 'SCECModels/Global' --exclude 'SCECModels/NewZealand' \
--exclude 'SCECModels/Japan' --exclude 'SCECModels/EU' \
--exclude 'SCECModels/OceanicTransformFaults')

	@(cd ..; rm $(dist_dir);)


### miniCSEP distribution 	  
minidist: clean testclean
	ls $(AUX) | sed s:^:$(dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS) | sed s:^:$(dist_dir)/: >>MANIFEST
	ls src/generic/test/data | grep -v genericDistribution | \
	grep -v TestForecastFactory.init.xml | \
	awk '{print "src/generic/test/data/"$$0}' > EXCLUDE.txt	
	@(cd ..; ln -s $(DIST_SOURCE) $(dist_dir))
	@(cd ..; tar zcvf $(minidist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn' \
--exclude 'SCECModels/California' --exclude 'SCECModels/WesternPacific' \
--exclude 'SCECModels/Global' --exclude 'SCECModels/NewZealand' \
--exclude 'SCECModels/Japan' --exclude 'SCECModels/EU' \
--exclude 'SCECModels/OceanicTransformFaults' --exclude-from $(DIST_SOURCE)/EXCLUDE.txt)

	@(cd ..; rm $(dist_dir);)



### California models distribution 
AUX_CA = Makefile \
         CaliforniaForecastFactory.init.xml \
         src/Makefile \
         src/SCECModels/Makefile

AUX_DIRS_CA = src/SCECModels/California

cadist: clean testclean
	ls $(AUX_CA) | sed s:^:$(ca_dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS_CA) | sed s:^:$(ca_dist_dir)/: >>MANIFEST	
	@(cd ..; ln -s $(DIST_SOURCE) $(ca_dist_dir))
	@(cd ..; tar zcvf $(ca_dist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn')
	@(cd ..; rm $(ca_dist_dir);)


### WesternPacific models distribution
AUX_WP = Makefile \
         WesternPacificForecastFactory.init.xml \
         src/Makefile \
         src/SCECModels/Makefile
AUX_DIRS_WP = src/SCECModels/WesternPacific

wpdist: clean testclean
	ls $(AUX_WP) | sed s:^:$(wp_dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS_WP) | sed s:^:$(wp_dist_dir)/: >>MANIFEST	
	@(cd ..; ln -s $(DIST_SOURCE) $(wp_dist_dir))
	@(cd ..; tar zcvf $(wp_dist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn')
	@(cd ..; rm $(wp_dist_dir);)


### Global models distribution
AUX_GLOBAL = Makefile \
             GlobalForecastFactory.init.xml \
             src/Makefile \
             src/SCECModels/Makefile

AUX_DIRS_GLOBAL = src/SCECModels/Global

globaldist: clean testclean
	ls $(AUX_GLOBAL) | sed s:^:$(global_dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS_GLOBAL) | sed s:^:$(global_dist_dir)/: >>MANIFEST	
	@(cd ..; ln -s $(DIST_SOURCE) $(global_dist_dir))
	@(cd ..; tar zcvf $(global_dist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn')
	@(cd ..; rm $(global_dist_dir);)


### Oceanic Transform Faults models distribution
AUX_OCEANIC = Makefile \
              OceanicTransformFaultsForecastFactory.init.xml \
              src/Makefile \
              src/SCECModels/Makefile

AUX_DIRS_OCEANIC = src/SCECModels/OceanicTransformFaults

oceanicdist: clean testclean
	ls $(AUX_OCEANIC) | sed s:^:$(oceanic_dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS_OCEANIC) | sed s:^:$(oceanic_dist_dir)/: >>MANIFEST	
	@(cd ..; ln -s $(DIST_SOURCE) $(oceanic_dist_dir))
	@(cd ..; tar zcvf $(oceanic_dist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn')
	@(cd ..; rm $(oceanic_dist_dir);)


### New Zealand Distribution
AUX_NZ = Makefile \
         src/Makefile \
         src/SCECModels/Makefile

AUX_DIRS_NZ = src/SCECModels/NewZealand

nzdist: clean testclean
	ls $(AUX_NZ) | sed s:^:$(nz_dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS_NZ) | sed s:^:$(nz_dist_dir)/: >>MANIFEST	
	@(cd ..; ln -s $(DIST_SOURCE) $(nz_dist_dir))
	@(cd ..; tar zcvf $(nz_dist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn')
	@(cd ..; rm $(nz_dist_dir);)


### Japan Distribution
AUX_JAPAN = Makefile \
            src/Makefile \
            src/SCECModels/Makefile

AUX_DIRS_JAPAN = src/SCECModels/Japan

japandist: clean testclean
	ls $(AUX_JAPAN) | sed s:^:$(japan_dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS_JAPAN) | sed s:^:$(japan_dist_dir)/: >>MANIFEST	
	@(cd ..; ln -s $(DIST_SOURCE) $(japan_dist_dir))
	@(cd ..; tar zcvf $(japan_dist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn')
	@(cd ..; rm $(japan_dist_dir);)

### EU Distribution
AUX_EU = Makefile \
		 src/Makefile \
         src/SCECModels/Makefile

AUX_DIRS_EU = src/SCECModels/EU

eudist: clean testclean
	ls $(AUX_EU) | sed s:^:$(eu_dist_dir)/: >MANIFEST
	ls -d $(AUX_DIRS_EU) | sed s:^:$(eu_dist_dir)/: >>MANIFEST	
	@(cd ..; ln -s $(DIST_SOURCE) $(eu_dist_dir))
	@(cd ..; tar zcvf $(eu_dist_dir).tar.gz `cat $(DIST_SOURCE)/MANIFEST` --exclude '.svn')
	@(cd ..; rm $(eu_dist_dir);)
