### 'src/SCECModels/postProcessing' level Makefile to build CSEP


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
	@echo destdir=$(DESTDIR)/src/SCECModels/postProcessing
	mkdir -p $(DESTDIR)/src/SCECModels/postProcessing;
	cp *.py $(DESTDIR)/src/SCECModels/postProcessing;
endif


###### Test Rules
check:


####### Clean Rules
clean:


####### Test clean rules
testclean:
