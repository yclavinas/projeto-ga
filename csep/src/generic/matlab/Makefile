### 'src/generic/matlab' level Makefile to build CSEP


TARGET ?= all

###  Build rules
.PHONY: default all install check clean testclean

###### Default Rules (no target is provided)
default: all

###### All Rules 
all:

###### Install Rules
install:
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/generic/matlab

	mkdir -p $(DESTDIR)/src/generic/matlab;
	cp *.m $(DESTDIR)/src/generic/matlab
endif


###### Test Rules
check:

####### Clean Rules
clean:

###### Test Clean Rules
testclean:
