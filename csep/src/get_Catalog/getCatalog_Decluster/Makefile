### 'src/get_Catalog/getCatalog_Decluster' level Makefile to build CSEP

###  Build rules
.PHONY: default all install

###### Default Rules (no target is provided)
default: all

###### All Rules 
all:


###### Install Rules
install:
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/get_Catalog/getCatalog_Decluster

	mkdir -p $(DESTDIR)/src/get_Catalog/getCatalog_Decluster;
	cp *.m *.mat $(DESTDIR)/src/get_Catalog/getCatalog_Decluster;
endif

