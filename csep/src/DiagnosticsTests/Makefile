# 
# Top level Makefile to install diagnostics tests codes

.PHONY: default all install clean testclean

default: all

# ----------------------------------------------------------------------

diagnosticsTests_PROGRAM = pearson_residuals.R \
                           superthinned_residuals_testing.R \
                           deviance_residuals.R \
                           superthinned_residuals.R \
                           weighted_l_function.R

### all rules
all:

### Intall rules
install:
ifeq '$(DESTDIR)' ''
else
	@echo destdir=$(DESTDIR)/src/DiagnosticsTests

	mkdir -p $(DESTDIR)/src/DiagnosticsTests;
	cp $(diagnosticsTests_PROGRAM) $(DESTDIR)/src/DiagnosticsTests;
endif


### Clean rules
clean:

### Test Clean rules - do nothing
testclean:

### Check rules - do nothing
check:
