# 
# Top level Makefile to test CSEP functionality

.PHONY: default all check testclean clean install distcheck

default: all

SUBDIRS = unitTest

SRC = AlarmBasedEvaluationTests.py \
      AlarmBasedWithMaskEvaluationTests.py \
      BogusForecastModel1.py \
      BogusForecastModel2.py \
      BogusForecastModel3.py \
      CSEPTest.py \
      GenericDistributionTest.py \
      CSEPTestCase.py \
      CSEPUnitTest.py \
      CatalogPostProcessing.py \
      CatalogPreProcessing.py \
      CatalogRetrieval.py \
      EvaluationTests.py \
      RandomAlarmBasedEvaluationTests.py \
      RandomEvaluationTests.py \
      DiagnosticEvaluationTests.py \
      CruiseControlOptionParser.py \
      StatisticalEvaluationTests.py

NATURAL_LAB_SRC = GlobalForecastsTests.py \
                  WesternPacificForecastsTests.py \
                  CaliforniaForecastsTests.py \
                  OceanicTransformFaultsTests.py


### Nothing to do for all
all:

### Check rules
check: distcheck
	python ./CSEPUnitTest.py -v --redirectLoggingOutput=CSEPUnitTest.py.log
	python ./CSEPTest.py -v --redirectLoggingOutput=CSEPTest.py.log
	
	@for src in $(NATURAL_LAB_SRC); do \
		if test -f $$src; then \
			python ./$$src -v --redirectLoggingOutput=$$src.log; \
		fi \
	done

# Rule to test generic CSEP distribution
distcheck: testclean
	python ./GenericDistributionTest.py -v --redirectLoggingOutput=GenericDistributionTest.py.log


### Clean rules - do nothing 
clean:

### Test Clean rules
testclean:
ifdef CSEP_RESULTS_DIR
	rm -rf $(CSEP_RESULTS_DIR)/results*
else
	rm -rf results*
endif


### Install rules - do nothing if destination directory is not provided
install:
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/generic/test
	mkdir -p $(DESTDIR)/src/generic/test;
	
	# Copy reference data: use rsync since it's automatically ignores all .svn folders
	rsync -aC data $(DESTDIR)/src/generic/test;

	# Set write permissions for all reference data: some of the tests update
	# configuration files
	echo "Setting write permissions for $(DESTDIR)/src/generic/test/data"; \
	     chmod -R a+w $(DESTDIR)/src/generic/test/data;
	
	@for src in $(NATURAL_LAB_SRC); do \
		if test -f $$src; then \
			echo Copying $$src to $(DESTDIR)/src/generic/test; \
			cp $$src $(DESTDIR)/src/generic/test; \
		fi \
	done
	
	cp $(SRC) $(DESTDIR)/src/generic/test;

	@for dir in $(SUBDIRS); do \
		pushd $$dir; $(MAKE) install; popd; \
	done
endif
