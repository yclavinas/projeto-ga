### 'src/get_Catalog' level Makefile to build CSEP

SUBDIRS = getCatalog_Decluster

TARGET ?= all

###  Build rules
.PHONY: default all $(SUBDIRS) install check clean testclean

###### Default Rules (no target is provided)
default: all

###### All Rules 
all:


###### Install Rules
install:
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/get_Catalog

	mkdir -p $(DESTDIR)/src/get_Catalog;
	cp *.m *.awk *.sed $(DESTDIR)/src/get_Catalog;
endif

	@for dir in $(SUBDIRS); do \
		pushd $$dir; $(MAKE) install; popd; \
	done

###### Test Rules
check:


####### Clean Rules
clean:


###### Test Clean Rules
testclean:
