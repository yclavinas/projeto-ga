# 
# Top level Makefile to build Triple_S forecast model executables

.PHONY: default all install clean testclean

default: all

# ----------------------------------------------------------------------

alarmTests_PROGRAM = Sandbox

bin_PROGRAMS = $(alarmTests_PROGRAM)

alarmTests_SOURCES = ArrayUtil.java \
                     Catalog.java \
                     DateUtil.java \
                     MathUtil.java \
                     ROCTools.java \
                     Utility.java \
                     CSEPForecast.java \
                     CatalogNoTime.java \
                     GeoUtil.java \
                     MolchanTools.java \
                     Sandbox.java
                   
### all rules
all: $(bin_PROGRAMS)

### Build rules for target program
$(alarmTests_PROGRAM): $(alarmTests_SOURCES)
	javac $^

### Intall rules
install: all
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/AlarmBasedTests

	mkdir -p $(DESTDIR)/src/AlarmBasedTests;
	cp *.class $(DESTDIR)/src/AlarmBasedTests;
endif


### Clean rules
clean:
	rm -f *.class

### Test Clean rules - do nothing
testclean:

### Check rules - do nothing
check:
