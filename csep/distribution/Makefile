### 'distribution' level Makefile to build CSEP

TARGET ?= all

###  Build rules
.PHONY: default all dist

###### Default Rules (no target is provided)
default: all

###### All Rules 
all:


###### Install Rules
dist:
	rpmbuild -ba csep.spec;
	rpmbuild -ba csepca.spec;
	rpmbuild -ba csepwp.spec;
	rpmbuild -ba csepglobal.spec;
	rpmbuild -ba csepnz.spec;
	rpmbuild -ba csepjapan.spec;
	rpmbuild -ba csepeu.spec;
	rpmbuild -ba csepoceanic.spec;
