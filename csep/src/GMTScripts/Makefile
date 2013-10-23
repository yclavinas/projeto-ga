# 
# 'src/GMTScripts' Makefile to set executable permissions on GMP map related scripts

TARGET ?= all install check testclean clean

###  Build rules
.PHONY: default all $(SUBDIRS) testclean clean check

###### Default Rules (no target is provided)
default: all

script_SOURCES = forecast.gmt \
                 forecast.nw.gmt \
                 forecast.sw.gmt \
                 forecast.global.gmt \
                 forecast.nz.gmt
                 
script_DATA = *.dat
                 
python_script_SOURCES = pov2cpt.py
all_SOURCES = $(script_SOURCES) $(python_script_SOURCES)


### all rules
all:
	@for each in $(all_SOURCES); do \
		echo "Setting executable permissions for $$each"; chmod a+x $$each; \
	done

###### Install Rules
install: all
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/GMTScripts
	mkdir -p $(DESTDIR)/src/GMTScripts;
	chmod a+w $(DESTDIR)/src/GMTScripts;
	cp *.pov $(all_SOURCES) $(script_DATA) $(DESTDIR)/src/GMTScripts;
endif


###### Test Rules
check:

####### Clean Rules
clean:

###### Test Clean Rules
testclean:
