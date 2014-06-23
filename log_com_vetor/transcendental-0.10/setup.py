#!/usr/bin/env python

import time
import sys
import os.path

from distutils.core import setup, Extension
from distutils.command.config import config
try:
  from distutils.command.config import log
except:
  pass
from distutils import sysconfig
python_include_path = sysconfig.get_python_inc()
python_config_vars = sysconfig.get_config_vars()

import numpy
major, minor, micro = numpy.__version__.split(".")
if (int(major), int(minor)) < (1, 6):
    print "This version of transcendental requires numpy version 1.6 or higher"
    print "(your version is %s)." % numpy.__version__
    sys.exit(0)

from numpy.distutils import misc_util

run_config = 0
for keyword in sys.argv:
    if keyword=='config':
	if sys.version_info[:2] < (2, 3):
	    print 'WARNING: If the configuration fails, please update to Python 2.3 or later'
        run_config = 1
        path = os.environ.get('PATH')
        if path:
            directories = path.split(":")
        else:
            directories = []
        directories.insert(0, '.')
        path = ":".join(directories)
        os.environ['PATH'] = path
   

#------------------------------------------------------------------------
# Configuration
#------------------------------------------------------------------------

class config_math (config):
    def run (self):
        try: log.set_verbosity(0)
        except: pass
        self.dump_source = 0
        self.configfile = open("config.h",'w')
        self.configfile.write('/* config.h file created by setup.py script ' + time.ctime() + '\n')
        self.configfile.write(' * run on ' + sys.platform + ' */ \n')
        self.config_toplevel()
        self.configfile.close()
        print 'wrote configuration file config.h'
#----------------------------------------------------------------------
    def config_isnan(self):
	# We need to check for big-endian or little-endian in some special
	# cases only. Don't check if not needed.
	self.endian_needtoknow = False

        # Check isnan presence, emulate otherwise
	# This function may be needed when testing for the architecture below.
	if python_config_vars.get('HAVE_DECL_ISNAN'):
            testcode = """\
#include <Python.h>
int main(int argc, char *argv[])
{ int flag = isnan(0./0.);
  if (flag==1) return 0;
  else return 1;
}
"""
            if self.try_run(testcode, include_dirs=[python_include_path], libraries=["m"]):
                print "using isnan found in Python.h"
                self.configfile.write("/* HAVE_DECL_ISNAN found in Python.h */\n")
	        self.isnan = "Python.h"
                return

        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ int flag = isnan(0./0.);
  if (flag==1) return 0;
  else return 1;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using isnan found in math.h"
            self.configfile.write("#define HAVE_DECL_ISNAN /* Found in math.h */\n")
	    self.isnan = "math.h"
            return

        print "math.h does not contain isnan, will emulate"
	self.isnan = ""
	self.endian_needtoknow = True


    def config_architecture(self):
        # determine architecture
        self.architecture = "UNK" # unknown
        testcode = """\
#define IBMPC
#include "arch.c"
"""
        include_path = []
        if self.isnan=="Python.h":
            testcode = "#include <Python.h>\n" + testcode
            include_path.append(python_include_path)
        elif self.isnan=="math.h":
            testcode = "#include <math.h>\n#define HAVE_DECL_ISNAN\n" + testcode
        if self.try_run(testcode, include_dirs=include_path, libraries=["m"]):
            print "detected ANSI/IEEE 754 standard architecture"
            self.architecture = "IBMPC"

        testcode = """\
#define MIEEE
#include "arch.c"
"""
        include_path = []
        if self.isnan=="Python.h":
            testcode = "#include <Python.h>\n" + testcode
            include_path.append(python_include_path)
        elif self.isnan=="math.h":
            testcode = "#include <math.h>\n#define HAVE_DECL_ISNAN\n" + testcode
        if self.try_run(testcode, include_dirs=include_path, libraries=["m"]):
            print "detected Motorola-type IEEE architecture"
            self.architecture = "MIEEE"

        testcode = """\
#define DEC
#include "arch.c"
"""
	# isnan not needed for DEC test
        if self.try_run(testcode,libraries=["m"]):
            print "detected DEC architecture"
            self.configfile.write('ARCH=DEC\n')
            self.architecture = "DEC"

        self.configfile.write('#define %s 1\n' % self.architecture)


    def config_infinities(self):
        # check if infinities are handled
        testcode = """\
#include <math.h>
int main(void)
{ double x = 1.0/0.0;
  if (x == HUGE_VAL) return 0;
  return 1;
}
"""
        if self.try_run(testcode):
            print "support for infinities detected"
            self.configfile.write('#define INFINITIES\n')
        else:
            print "no support for infinities"


    def config_nan(self):
        # check if not-a-number is handled
        testcode = """\
#include <math.h>
int main(void)
{ double x = 1.0/0.0 - 1.0/0.0;
  if (x != x) return 0;
  return 1;
}
"""
        if self.try_run(testcode):
            print "support for NaN detected"
            self.configfile.write('#define NANS\n')
        else:
            print "no support for NaN"


    def config_denormals(self):
        # check if denormals are handled
        testcode = """\
#define %s
#include "cephes/const.c"
int main(void)
{ double* x = (double*)UFLOWTHRESH;;
  double y = (*x)/2.0;
  if (y == 0.0) return 1;
  return 0;
}
""" % self.architecture
        if self.try_run(testcode):
            print "support for denormals detected"
            self.configfile.write('#define HAVE_DENORMAL\n')
        else:
            print "no support for denormals"


    def config_round(self):
        # check round presence, emulate otherwise
	if sys.version_info[:2] >= (2, 6):
            testcode = """\
#include <Python.h>
int main(int argc, char *argv[])
{ double x=round(2.9);
  if (x<2.999999 || x>3.000001) return 1;
  else return 0;
}
"""
            if self.try_run(testcode, include_dirs=[python_include_path], libraries=["m"]):
                print "using round found in libm"
                self.configfile.write("/* HAVE_ROUND found in Python.h */\n")
                return

        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=round(2.9);
  if (x<2.999999 || x>3.000001) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using round found in libm"
            self.configfile.write("#define HAVE_ROUND\n")
        else:
            print "libm does not contain round, will emulate"


    def config_cbrt(self):
        # check cbrt presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=cbrt(27.);
  if (x<2.999999 || x>3.000001) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using cbrt found in libm"
            self.configfile.write("#define HAVE_CBRT\n")
        else:
            print "libm does not contain cbrt, will emulate"


    def config_j0(self):
        # check j0 presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=j0(1.0);
  if (x<0.765197 || x>0.765199) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using j0 found in libm"
            self.configfile.write("#define HAVE_J0\n")
        else:
            print "libm does not contain j0, will emulate"


    def config_j1(self):
        # check j1 presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=j1(1.0);
  if (x<0.440050 || x>0.440052) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using j1 found in libm"
            self.configfile.write("#define HAVE_J1\n")
        else:
            print "libm does not contain j1, will emulate"


    def config_jn(self):
        # check jn presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=jn(1,1.0);
  if (x<0.440050 || x>0.440052) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using jn found in libm"
            self.configfile.write("#define HAVE_JN\n")
        else:
            print "libm does not contain jn, will emulate"


    def config_y0(self):
        # check y0 presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=y0(1.0);
  if (x<0.088256 || x>0.088258) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using y0 found in libm"
            self.configfile.write("#define HAVE_Y0\n")
        else:
            print "libm does not contain y0, will emulate"


    def config_y1(self):
        # check y1 presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=y1(1.0);
  if (x<-0.781214 || x>-0.781212) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using y1 found in libm"
            self.configfile.write("#define HAVE_Y1\n")
        else:
            print "libm does not contain y1, will emulate"


    def config_yn(self):
        # check yn presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=yn(1,1.0);
  if (x<-0.781214 || x>-0.781212) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using yn found in libm"
            self.configfile.write("#define HAVE_YN\n")
        else:
            print "libm does not contain yn, will emulate"


    def config_expm1(self):
        # check expm1 presence, emulate otherwise
	if sys.version_info[:2] >= (2, 6):
            testcode = """\
#include <Python.h>
int main(int argc, char *argv[])
{ double x=expm1(0.1);
  if (x<0.105170 || x>0.105172) return 1;
  else return 0;
}
"""
            if self.try_run(testcode, include_dirs=[python_include_path], libraries=["m"]):
                print "using expm1 found in libm"
                self.configfile.write("/* HAVE_EXPM1 found in Python.h */\n")
                return

        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=expm1(0.1);
  if (x<0.105170 || x>0.105172) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using expm1 found in libm"
            self.configfile.write("#define HAVE_EXPM1 /* found in math.h */\n")
            return

        print "libm does not contain expm1, will emulate"


    def config_log1p(self):
        # check log1p presence, emulate otherwise
	if sys.version_info[:2] >= (2, 6):
            testcode = """\
#include <Python.h>
int main(int argc, char *argv[])
{ double x=log1p(0.1);
  if (x<0.095310 || x>0.095311) return 1;
  else return 0;
}
"""
            if self.try_run(testcode, include_dirs=[python_include_path], libraries=["m"]):
                print "using log1p found in libm"
                self.configfile.write("/* HAVE_LOG1P found in Python.h */\n")
                return

        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=log1p(0.1);
  if (x<0.095310 || x>0.095311) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using log1p found in libm"
            self.configfile.write("#define HAVE_LOG1P /* found in math.h */\n")
            return

        print "libm does not contain log1p, will emulate"


    def config_erf(self):
        # check erf presence, emulate otherwise
	if python_config_vars.get('HAVE_ERF'):
            testcode = """\
#include <Python.h>
int main(int argc, char *argv[])
{ double x=erf(1.);
  if (x<0.842700 || x>0.842702) return 1;
  else return 0;
}
"""
            if self.try_run(testcode, include_dirs=[python_include_path], libraries=["m"]):
                print "using erf found in Python.h"
                self.configfile.write("/* HAVE_ERF found in Python.h */\n")
                return

        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=erf(1.);
  if (x<0.842700 || x>0.842702) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using erf found in libm"
            self.configfile.write("#define HAVE_ERF\n")
        else:
            print "libm does not contain erf, will emulate"


    def config_erfc(self):
        # check erfc presence, emulate otherwise
	if python_config_vars.get('HAVE_ERFC'):
            testcode = """\
#include <Python.h>
int main(int argc, char *argv[])
{ double x=erfc(1.);
  if (x<0.157299  || x>0.157301) return 1;
  else return 0;
}
"""
            if self.try_run(testcode, include_dirs=[python_include_path], libraries=["m"]):
                print "using erfc found in Python.h"
                self.configfile.write("/* HAVE_ERFC found in Python.h */\n")
                return

        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=erfc(1.);
  if (x<0.157299  || x>0.157301) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using erfc found in libm"
            self.configfile.write("#define HAVE_ERFC\n")
        else:
            print "libm does not contain erfc, will emulate"


    def config_gamma(self):
        # check gamma presence, emulate otherwise
	if python_config_vars.get('HAVE_GAMMA'):
            testcode = """\
#include <Python.h>
int main(int argc, char *argv[])
{ double x=gamma(0.5);
  if (x<1.772453  || x>1.772454) return 1;
  else return 0;
}
"""
            if self.try_run(testcode, include_dirs=[python_include_path], libraries=["m"]):
                print "using gamma found in Python.h"
                self.configfile.write("/* HAVE_GAMMA found in Python.h */\n")
                return
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=gamma(0.5);
  if (x<1.772453  || x>1.772454) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using gamma found in libm"
	    self.configfile.write("#define HAVE_GAMMA\n")
        else:
            print "libm does not contain gamma, will emulate"


    def config_lgamma(self):
        # check lgamma presence, emulate otherwise
	if sys.version_info[:2] >= (2, 6):
            testcode = """\
#include <Python.h>
int main(int argc, char *argv[])
{ double x=lgamma(0.5);
  if (x<0.572364  || x>0.572365) return 1;
  else return 0;
}
"""
            if self.try_run(testcode, include_dirs=[python_include_path], libraries=["m"]):
                print "using lgamma found in libm"
                self.configfile.write("/* HAVE_LGAMMA found in Python.h */\n")
                return

        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ double x=lgamma(0.5);
  if (x<0.572364  || x>0.572365) return 1;
  else return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using lgamma found in libm"
            self.configfile.write("#define HAVE_LGAMMA\n")
        else:
            print "libm does not contain lgamma, will emulate"

    def config_signbit(self):
        # check signbit presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ int flag;
  flag = signbit(2.);
  if (flag==1) return 1;
  flag = signbit(+0.);
  if (flag==1) return 1;
  flag = signbit(-0.);
  if (flag==0) return 1;
  flag = signbit(-2.);
  if (flag==0) return 1;
  return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using signbit found in math.h"
            self.configfile.write("#define HAVE_SIGNBIT\n")
        else:
            print "math.h does not contain signbit, will emulate"
	    self.endian_needtoknow = 1


    def config_isfinite(self):
        # check isfinite presence, emulate otherwise
        testcode = """\
#include <math.h>
int main(int argc, char *argv[])
{ int flag;
  flag = isfinite(0./0.);
  if (flag==1) return 1;
  flag = isfinite(1./0.);
  if (flag==1) return 1;
  flag = isfinite(1./1.);
  if (flag==0) return 1;
  return 0;
}
"""
        if self.try_run(testcode,libraries=["m"]):
            print "using isfinite found in math.h"
            self.configfile.write("#define HAVE_ISFINITE\n")
        else:
            print "math.h does not contain isfinite, will emulate"
	    self.endian_needtoknow = True


    def config_minuszero(self):
        # check if -0.0 and +0.0 are different
        testcode = """\
int main(int argc, char *argv[])
{ double x = +0.0;
  double y = -0.0;
  short* sx = (short*)&x;
  short* sy = (short*)&y;
  int n = sizeof(double) / sizeof(short);
  int i;
  for (i = 0; i < n; i++)
    if (sx[i]!=sy[i]) return 0;
  return 1;
}
"""
        if self.try_run(testcode):
            print "the values +0.0 and -0.0 are being distinguished"
            self.configfile.write("#define MINUSZERO\n")
        else:
            print "the values +0.0 and -0.0 are not being distinguished"

    def config_toplevel(self):
        print "  ============= begin transcendental configuration ============"

        self.config_isnan()
        self.config_architecture()
        self.config_infinities()
        self.config_nan()
        self.config_denormals()
        self.config_round()
        self.config_cbrt()
        self.config_j0()
        self.config_j1()
        self.config_jn()
        self.config_y0()
        self.config_y1()
        self.config_yn()
        self.config_expm1()
        self.config_log1p()
        self.config_erf()
        self.config_erfc()
        self.config_gamma()
        self.config_lgamma()
        self.config_signbit()
        self.config_isfinite()
        self.config_minuszero()

        if self.architecture=="UNK" and self.endian_needtoknow:
        # architecture unknown, we need to figure out if the machine is
	# big-endian or little-endian. This test is needed for signbit,
	# isfinite, and isnan only; don't test if those are available in the
	# standard C libraries.

	    testcode = """\
int signbit(double x)
{ union { double d; short s[4]; int i[2];} u;
  u.d = x;
  if(sizeof(int) == 4) return(u.i[0] < 0);
  return( u.s[0] < 0 );
}

int main(void)
{ union { double d; short s[4]; int i[2];} u;
  if(sizeof(int)==4)
  { u.d = 0.0;
    u.i[0] = -1;
    if(u.d > 0.0 && signbit(u.d)) return 1;
    if(u.d < 0.0 && !signbit(u.d)) return 1;
    u.d = 0.0;
    u.i[1] = -1;
    if(u.d > 0.0 && signbit(u.d)) return 1;
    if(u.d < 0.0 && !signbit(u.d)) return 1;
  }
  else
  { u.d = 0.0;
    u.s[0] = -1;
    if(u.d > 0.0 && signbit(u.d)) return 1;
    if(u.d < 0.0 && !signbit(u.d)) return 1;
    u.d = 0.0;
    u.s[3] = -1;
    if(u.d > 0.0 && signbit(u.d)) return 1;
    if(u.d < 0.0 && !signbit(u.d)) return 1;
  }
  return 0;
}
"""
            if self.try_run(testcode):
                print "big-endian machine detected"
                self.configfile.write("#define BIGENDIAN 1\n")
	    else:
		testcode = """\
int signbit(double x)
{ union {double d; short s[4]; int i[2];} u;
  u.d = x;
  if(sizeof(int)==4) return( u.i[1] < 0 );
  return( u.s[3] < 0 );
}

int main(void)
{ union { double d; short s[4]; int i[2];} u;
  if(sizeof(int)==4)
  { u.d = 0.0;
    u.i[0] = -1;
    if(u.d > 0.0 && signbit(u.d)) return 1;
    if(u.d < 0.0 && !signbit(u.d)) return 1;
    u.d = 0.0;
    u.i[1] = -1;
    if(u.d > 0.0 && signbit(u.d)) return 1;
    if(u.d < 0.0 && !signbit(u.d)) return 1;
  }
  else
  { u.d = 0.0;
    u.s[0] = -1;
    if(u.d > 0.0 && signbit(u.d)) return 1;
    if(u.d < 0.0 && !signbit(u.d)) return 1;
    u.d = 0.0;
    u.s[3] = -1;
    if(u.d > 0.0 && signbit(u.d)) return 1;
    if(u.d < 0.0 && !signbit(u.d)) return 1;
  }
  return 0;
}
"""
                if self.try_run(testcode):
                    print "little-endian machine detected"
                    self.configfile.write("#define BIGENDIAN 0\n")
		else:
		    print "============================================="
		    print "ERROR: unknown if big-endian or little-endian"
		    print "edit the config file before compiling"
		    print "============================================="
                    self.configfile.write("#define BIGENDIAN UNKNOWN /* replace with 0 or 1 */\n")

        print "  ============== end transcendental configuration ============="

#------------------------------------------------------------------------
# Installation
#------------------------------------------------------------------------

source = ['src/transcendental.c',
          'cephes/isnan.c',
          'cephes/cephes.c',
          'cephes/pol.c',
          'cephes/mtherr.c',
          'cephes/const.c']

extra_compile_args = ['-DANSIPROT']
architecture = 'UNK' # Unknown
if not run_config and not os.path.isfile("config.h"):
    import shutil
    shutil.copyfile("config.h.def","config.h")
       
libraries=['m']
if sys.platform == 'win32':
    libraries.append('mingwex')
    # This library contains __fpclassify. Maybe this is a mistake in mingw
include_dirs = ['src', 'cephes', numpy.get_include()]
library_dirs = []

# Add npymath stuff
info = misc_util.get_info('npymath')
libraries.extend(info['libraries'])
include_dirs.extend(info['include_dirs'])
library_dirs.extend(info['library_dirs'])


# Now we know everything needed to define the extension module

extension = Extension ( 'transcendental._transcendental',
                        source,
                        include_dirs=include_dirs,
                        library_dirs=library_dirs,
                        libraries=libraries,
			extra_compile_args=extra_compile_args)

# Now that we know how to build the extension, we can call setup

setup (
          name = "transcendental",
          version = "0.10",
          description = "Special functions",
          author = "Michiel de Hoon",
          author_email = "mdehoon 'AT' gsc.riken.jp",
          url = "http://bonsai.ims.u-tokyo.ac.jp/~mdehoon",
          license = "The license of the underlying Cephes library is unknown to me. The Python wrappers of the Cephes library are covered by the Python license.",
          cmdclass = {'config': config_math},
          package_dir = {'transcendental':'python'},
          packages = ['transcendental'],
          ext_modules = [extension]
   )

# Finished.
