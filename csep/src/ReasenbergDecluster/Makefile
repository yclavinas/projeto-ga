# 
# Top level Makefile to build executables for Reasenberg declustering code

.PHONY: default all install clean testclean

default: all

# ----------------------------------------------------------------------

ifort_VERSION = ifort.version
decluster_PROGRAM = cluster2000x

bin_PROGRAMS = $(decluster_PROGRAM)

decluster_SOURCES = cluster2000x.f

FOPTIONS = -g
                   
### all rules
all: $(bin_PROGRAMS)
	ifort --version > $(ifort_VERSION)

### Build rules for target program
$(decluster_PROGRAM): $(decluster_SOURCES)
	ifort $(FOPTIONS) -o $@ $^

### Intall rules
install: all
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/ReasenbergDecluster

	mkdir -p $(DESTDIR)/src/ReasenbergDecluster;
	cp $(bin_PROGRAMS) $(ifort_VERSION) $(DESTDIR)/src/ReasenbergDecluster;
endif


### Clean rules
clean:
	rm -f $(bin_PROGRAMS)

### Test Clean rules - do nothing
testclean:

### Check rules - do nothing
check: install

### Install rules
install:
