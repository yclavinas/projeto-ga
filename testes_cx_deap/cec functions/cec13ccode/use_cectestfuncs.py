#!python
"""
I want to learn how to complile C-code into a dll and use it from within python
why: to be able to use the CEC-2013 test function suite

once the shared library test_func.so exists, with this script you can use and
plot the test functions
"""
# import numpy as np
from numpy import pi, zeros, linspace
from ctypes import cdll
import ctypes as ct

k=21  # which function to use

tf = cdll.LoadLibrary('./test_func.so')

tf.test_func.argtypes=[ct.POINTER(ct.c_double),ct.POINTER(ct.c_double),ct.c_int,ct.c_int,ct.c_int]

tf.test_func.restype=None

n=10; m=2; h=180
xlim=[-27.,-17.]; ylim=[7.,17.];
xwidth=xlim[1]-xlim[0]; ywidth=ylim[1]-ylim[0];
dx=xwidth/(m-1.); dy=ywidth/(h-1.);
x=linspace(xlim[0],xlim[1],m+1)
y=linspace(ylim[0],ylim[1],h+1)

npdat=zeros(n*m)
dat = (ct.c_double * len(npdat))()
for i,val in enumerate(npdat):
    dat[i] = 0.476158262229

npf=zeros(m)
f = (ct.c_double * len(npf))()
for i,val in enumerate(npf):
    f[i] = val 

print 'now function ',k
r1=tf.test_func(dat,f,ct.c_int(n),ct.c_int(m),ct.c_int(k))
for pt in f:
    print pt,
    exit(0)

