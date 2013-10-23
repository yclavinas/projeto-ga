### 'src/RELMTests' level Makefile to build CSEP

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
	@echo destdir=$(DESTDIR)/src/RELMTests

	mkdir -p $(DESTDIR)/src/RELMTests;
	cp *.m $(DESTDIR)/src/RELMTests;
endif


###### Test Rules
check:


####### Clean Rules
clean:


###### Test Clean Rules
testclean:
