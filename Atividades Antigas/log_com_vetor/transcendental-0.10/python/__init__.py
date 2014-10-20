import _transcendental

def cbrt(x):
  """\
  	Cube root



   SYNOPSIS:
  
   y = cbrt(x)
  
  
  
   DESCRIPTION:
  
   Returns the cube root of the argument, which may be negative.
  
   Range reduction involves determining the power of 2 of
   the argument.  A polynomial of degree 2 applied to the
   mantissa, and multiplication by the cube root of 1, 2, or 4
   approximates the root to within about 0.1%.  Then Newton's
   iteration is used three times to converge to an accurate
   result.
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC        -10,10     200000      1.8e-17     6.2e-18
      IEEE       0,1e308     30000      1.5e-16     5.0e-17
  """
  return _transcendental.cbrt(x)


def j0(x):
  """\
        Bessel function of order zero
  
  
  
   SYNOPSIS:
  
   y = j0(x)
  
  
  
   DESCRIPTION:
  
   Returns Bessel function of order zero of the argument.
  
   The domain is divided into the intervals [0, 5] and
   (5, infinity). In the first interval the following rational
   approximation is used:
  
  
          2         2
   (w - r  ) (w - r  ) P (w) / Q (w)
         1         2    3       8
  
              2
   where w = x  and the two r's are zeros of the function.
  
   In the second interval, the Hankel asymptotic expansion
   is employed with two rational functions of degree 6/6
   and 7/7.
  
  
  
   ACCURACY:
  
                        Absolute error:
   arithmetic   domain     # trials      peak         rms
      DEC       0, 30       10000       4.4e-17     6.3e-18
      IEEE      0, 30       60000       4.2e-16     1.1e-16
  """
  return _transcendental.j0(x)


def y0(x):
  """\
        Bessel function of the second kind, order zero
  
  
  
   SYNOPSIS:
  
   y = y0(x)
  
  
  
   DESCRIPTION:
  
   Returns Bessel function of the second kind, of order
   zero, of the argument.
  
   The domain is divided into the intervals [0, 5] and
   (5, infinity). In the first interval a rational approximation
   R(x) is employed to compute
     y0(x)  = R(x)  +   2 * log(x) * j0(x) / PI.
   Thus a call to j0() is required.
  
   In the second interval, the Hankel asymptotic expansion
   is employed with two rational functions of degree 6/6
   and 7/7.
  
  
  
   ACCURACY:
  
    Absolute error, when y0(x) < 1; else relative error:
  
   arithmetic   domain     # trials      peak         rms
      DEC       0, 30        9400       7.0e-17     7.9e-18
      IEEE      0, 30       30000       1.3e-15     1.6e-16
  """
  return _transcendental.y0(x)


def i0(x):
  """\
        Modified Bessel function of order zero
  
  
  
   SYNOPSIS:
  
   y = i0(x)
  
  
  
   DESCRIPTION:
  
   Returns modified Bessel function of order zero of the
   argument.
  
   The function is defined as i0(x) = j0( ix ).
  
   The range is partitioned into the two intervals [0,8] and
   (8, infinity).  Chebyshev polynomial expansions are employed
   in each interval.
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0,30         6000       8.2e-17     1.9e-17
      IEEE      0,30        30000       5.8e-16     1.4e-16
  """
  return _transcendental.i0(x)


def i0e(x):
  """\
        Modified Bessel function of order zero,
        exponentially scaled
  
  
  
   SYNOPSIS:
  
   y = i0e(x)
  
  
  
   DESCRIPTION:
  
   Returns exponentially scaled modified Bessel function
   of order zero of the argument.
  
   The function is defined as i0e(x) = exp(-|x|) j0( ix ).
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      0,30        30000       5.4e-16     1.2e-16
   See i0().
  """
  return _transcendental.i0e(x)


def k0(x):
  """\
        Modified Bessel function, third kind, order zero
  
   
   
   SYNOPSIS:
   
   y = k0(x) 
  
  
  
   DESCRIPTION:
  
   Returns modified Bessel function of the third kind
   of order zero of the argument.
  
   The range is partitioned into the two intervals [0,8] and
   (8, infinity).  Chebyshev polynomial expansions are employed
   in each interval.
  
  
  
   ACCURACY:
  
   Tested at 2000 random points between 0 and 8.  Peak absolute
   error (relative when K0 > 1) was 1.46e-14; rms, 4.26e-15.
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0, 30        3100       1.3e-16     2.1e-17
      IEEE      0, 30       30000       1.2e-15     1.6e-16
  
   ERROR MESSAGES:
  
     message         condition      value returned
    K0 domain          x <= 0          MAXNUM
  """
  return _transcendental.k0(x)


def k0e(x):
  """\
        Modified Bessel function, third kind, order zero,
        exponentially scaled
  
  
  
   SYNOPSIS:
  
   y = k0e(x)
  
  
  
   DESCRIPTION:
  
   Returns exponentially scaled modified Bessel function
   of the third kind of order zero of the argument.
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      0, 30       30000       1.4e-15     1.4e-16
   See k0().
  """
  return _transcendental.k0e(x)


def j1(x):
  """\
        Bessel function of order one
  
  
  
   SYNOPSIS:
  
   y = j1(x)
  
  
  
   DESCRIPTION:
  
   Returns Bessel function of order one of the argument.
  
   The domain is divided into the intervals [0, 8] and
   (8, infinity). In the first interval a 24 term Chebyshev
   expansion is used. In the second, the asymptotic
   trigonometric representation is employed using two
   rational functions of degree 5/5.
  
  
  
   ACCURACY:
  
                        Absolute error:
   arithmetic   domain      # trials      peak         rms
      DEC       0, 30       10000       4.0e-17     1.1e-17
      IEEE      0, 30       30000       2.6e-16     1.1e-16
  
  
  """
  return _transcendental.j1(x)


def y1(x):
  """\
  
        Bessel function of second kind of order one
  
  
  
   SYNOPSIS:
  
   y = y1(x)
  
  
  
   DESCRIPTION:
  
   Returns Bessel function of the second kind of order one
   of the argument.
  
   The domain is divided into the intervals [0, 8] and
   (8, infinity). In the first interval a 25 term Chebyshev
   expansion is used, and a call to j1() is required.
   In the second, the asymptotic trigonometric representation
   is employed using two rational functions of degree 5/5.
  
  
  
   ACCURACY:
  
                        Absolute error:
   arithmetic   domain      # trials      peak         rms
      DEC       0, 30       10000       8.6e-17     1.3e-17
      IEEE      0, 30       30000       1.0e-15     1.3e-16
  
   (error criterion relative when |y1| > 1).
  """
  return _transcendental.y1(x)


def i1(x):
  """\
        Modified Bessel function of order one
  
  
  
   SYNOPSIS:
  
   y = i1(x)
  
  
  
   DESCRIPTION:
  
   Returns modified Bessel function of order one of the
   argument.
  
   The function is defined as i1(x) = -i j1( ix ).
  
   The range is partitioned into the two intervals [0,8] and
   (8, infinity).  Chebyshev polynomial expansions are employed
   in each interval.
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0, 30        3400       1.2e-16     2.3e-17
      IEEE      0, 30       30000       1.9e-15     2.1e-16
  """
  return _transcendental.i1(x)
 

def i1e(x):
  """\
        Modified Bessel function of order one,
        exponentially scaled
  
  
  
   SYNOPSIS:
  
   y = i1e(x)
  
  
  
   DESCRIPTION:
  
   Returns exponentially scaled modified Bessel function
   of order one of the argument.
  
   The function is defined as i1(x) = -i exp(-|x|) j1( ix ).
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      0, 30       30000       2.0e-15     2.0e-16
   See i1().
  """
  return _transcendental.i1e(x)


def k1(x):
  """\
        Modified Bessel function, third kind, order one
  
  
  
   SYNOPSIS:
  
   y = k1(x) 
  
  
  
   DESCRIPTION:
  
   Computes the modified Bessel function of the third kind
   of order one of the argument.
  
   The range is partitioned into the two intervals [0,2] and
   (2, infinity).  Chebyshev polynomial expansions are employed
   in each interval.
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0, 30        3300       8.9e-17     2.2e-17
      IEEE      0, 30       30000       1.2e-15     1.6e-16
  
   ERROR MESSAGES:
  
     message         condition      value returned
   k1 domain          x <= 0          MAXNUM
  """
  return _transcendental.k1(x)


def k1e(x):
  """\
        Modified Bessel function, third kind, order one,
        exponentially scaled
  
  
  
   SYNOPSIS:
  
   y = k1e(x)
  
  
  
   DESCRIPTION:
  
   Returns exponentially scaled modified Bessel function
   of the third kind of order one of the argument:
  
        k1e(x) = exp(x) * k1(x).
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      0, 30       30000       7.8e-16     1.2e-16
   See k1().
  """
  return _transcendental.k1e(x)
 
 
def erf(x):
  """\
  	Error function
  
  
  
   SYNOPSIS:
  
   y = erf(x)
  
  
  
   DESCRIPTION:
  
   The integral is
  
                             x 
                              -
                   2         | |          2
     erf(x)  =  --------     |    exp( - t  ) dt.
                sqrt(pi)   | |
                            -
                             0
  
   The magnitude of x is limited to 9.231948545 for DEC
   arithmetic; 1 or -1 is returned outside this range.
  
   For 0 <= |x| < 1, erf(x) = x * P4(x**2)/Q5(x**2); otherwise
   erf(x) = 1 - erfc(x).
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0,1         14000       4.7e-17     1.5e-17
      IEEE      0,1         30000       3.7e-16     1.0e-16
  """
  return _transcendental.erf(x)



def erfc(x):
  """\
  	Complementary error function
  
  
  
   SYNOPSIS:
  
   y = erfc(x)
  
  
  
   DESCRIPTION:
  
  
    1 - erf(x) =
  
                             inf. 
                               -
                    2         | |          2
     erfc(x)  =  --------     |    exp( - t  ) dt
                 sqrt(pi)   | |
                             -
                              x
  
  
   For small x, erfc(x) = 1 - erf(x); otherwise rational
   approximations are computed.
  
   A special function expx2.c is used to suppress error amplification
   in computing exp(-x^2).
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      0,26.6417   30000       1.3e-15     2.2e-16
  
  
   ERROR MESSAGES:
  
     message         condition              value returned
   erfc underflow    x > 9.231948545 (DEC)       0.0
  """
  return _transcendental.erfc(x)


def ndtr(x):
  """\
  	Normal distribution function
  
  
  
   SYNOPSIS:
  
   y = ndtr(x)
  
  
  
   DESCRIPTION:
  
   Returns the area under the Gaussian probability density
   function, integrated from minus infinity to x:
  
                              x
                               -
                     1        | |          2
      ndtr(x)  = ---------    |    exp( - t /2 ) dt
                 sqrt(2pi)  | |
                             -
                            -inf.
  
               =  ( 1 + erf(z) ) / 2
               =  erfc(z) / 2
  
   where z = x/sqrt(2). Computation is via the functions
   erf and erfc with care to avoid error amplification in computing exp(-x^2).
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE     -13,0        30000       1.3e-15     2.2e-16
  
  
   ERROR MESSAGES:
  
     message         condition         value returned
   erfc underflow    x > 37.519379347       0.0
  """
  return _transcendental.ndtr(x)


def ndtri(x):
  """\
  	Inverse of Normal distribution function
  
  
  
   SYNOPSIS:
  
   x = ndtri(y)
       where 0 <= y <= 1.
  
  
  
   DESCRIPTION:
  
   Returns the argument, x, for which the area under the
   Gaussian probability density function (integrated from
   minus infinity to x) is equal to y.
  
  
   For small arguments 0 < y < exp(-2), the program computes
   z = sqrt( -2.0 * log(y) );  then the approximation is
   x = z - log(z)/z  - (1/z) P(1/z) / Q(1/z).
   There are two rational functions P/Q, one for 0 < y < exp(-32)
   and the other for y up to exp(-2).  For larger arguments,
   w = y - 0.5, and  x/sqrt(2pi) = w + w**3 R(w**2)/S(w**2)).
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain        # trials      peak         rms
      DEC      0.125, 1         5500       9.5e-17     2.1e-17
      DEC      6e-39, 0.135     3500       5.7e-17     1.3e-17
      IEEE     0.125, 1        20000       7.2e-16     1.3e-16
      IEEE     3e-308, 0.135   50000       4.6e-16     9.8e-17
  
  
   ERROR MESSAGES:
  
     message         condition    value returned
   ndtri domain       x <= 0        -MAXNUM
   ndtri domain       x >= 1         MAXNUM
  """
  return _transcendental.ndtri(x)


def dawsn(x):
  """\
  	Dawson's Integral
  
  
  
   SYNOPSIS:
  
   y = dawsn(x)
  
  
  
   DESCRIPTION:
  
   Approximates the integral
  
                               x
                               -
                        2     | |        2
    dawsn(x)  =  exp( -x  )   |    exp( t  ) dt
                            | |
                             -
                             0
  
   Three different rational approximations are employed, for
   the intervals 0 to 3.25; 3.25 to 6.25; and 6.25 up.
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      0,10        10000       6.9e-16     1.0e-16
      DEC       0,10         6000       7.4e-17     1.4e-17
  """
  return _transcendental.dawsn(x)


def gamma(x):
  """\
  	Gamma function
  
  
  
   SYNOPSIS:
  
   y = gamma(x)
  
  
  
   DESCRIPTION:
  
   Returns gamma function of the argument.  The result is
   correctly signed, and the sign (+1 or -1) is also
   returned in a global (extern) variable named sgngam.
   This variable is also filled in by the logarithmic gamma
   function lgam().
  
   Arguments |x| <= 34 are reduced by recurrence and the function
   approximated by a rational function of degree 6/7 in the
   interval (2,3).  Large arguments are handled by Stirling's
   formula. Large negative arguments are made positive using
   a reflection formula.  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC      -34, 34      10000       1.3e-16     2.5e-17
      IEEE    -170,-33      20000       2.3e-15     3.3e-16
      IEEE     -33,  33     20000       9.4e-16     2.2e-16
      IEEE      33, 171.6   20000       2.3e-15     3.2e-16
  
   Error for arguments outside the test range will be larger
   owing to error amplification by the exponential function.
  """
  return _transcendental.gamma(x)



def lgamma(x):
  """\
  	Natural logarithm of gamma function
  
  
  
   SYNOPSIS:
  
   y = lgamma(x)
  
  
  
   DESCRIPTION:
  
   Returns the base e (2.718...) logarithm of the absolute
   value of the gamma function of the argument.
   The sign (+1 or -1) of the gamma function is returned in a
   global (extern) variable named sgngam.
  
   For arguments greater than 13, the logarithm of the gamma
   function is approximated by the logarithmic version of
   Stirling's formula using a polynomial approximation of
   degree 4. Arguments between -33 and +33 are reduced by
   recurrence to the interval [2,3] of a rational approximation.
   The cosecant reflection formula is employed for arguments
   less than -33.
  
   Arguments greater than MAXLGM return MAXNUM and an error
   message.  MAXLGM = 2.035093e36 for DEC
   arithmetic or 2.556348e305 for IEEE arithmetic.
  
  
  
   ACCURACY:
  
  
   arithmetic      domain        # trials     peak         rms
      DEC     0, 3                  7000     5.2e-17     1.3e-17
      DEC     2.718, 2.035e36       5000     3.9e-17     9.9e-18
      IEEE    0, 3                 28000     5.4e-16     1.1e-16
      IEEE    2.718, 2.556e305     40000     3.5e-16     8.3e-17
   The error criterion was relative when the function magnitude
   was greater than one but absolute when it was less than one.
  
   The following test used the relative error criterion, though
   at certain points the relative error could be much higher than
   indicated.
      IEEE    -200, -4             10000     4.8e-16     1.3e-16
  """
  return _transcendental.lgamma(x)
 
 
def rgamma(x):
  """\
  	Reciprocal gamma function
  
  
  
   SYNOPSIS:
  
   y = rgamma(x)
  
  
  
   DESCRIPTION:
  
   Returns one divided by the gamma function of the argument.
  
   The function is approximated by a Chebyshev expansion in
   the interval [0,1].  Range reduction is by recurrence
   for arguments between -34.034 and +34.84425627277176174.
   1/MAXNUM is returned for positive arguments outside this
   range.  For arguments less than -34.034 the cosecant
   reflection formula is applied; lograrithms are employed
   to avoid unnecessary overflow.
  
   The reciprocal gamma function has no singularities,
   but overflow and underflow may occur for large arguments.
   These conditions return either MAXNUM or 1/MAXNUM with
   appropriate sign.
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC      -30,+30       4000       1.2e-16     1.8e-17
      IEEE     -30,+30      30000       1.1e-15     2.0e-16
   For arguments less than -34.034 the peak error is on the
   order of 5e-15 (DEC), excepting overflow or underflow.
  """
  return _transcendental.rgamma(x)



def psi(x):
  """\
  	Psi (digamma) function
  
  
   SYNOPSIS:
  
   y = psi(x)
  
  
   DESCRIPTION:
  
                d      -
     psi(x)  =  -- ln | (x)
                dx
  
   is the logarithmic derivative of the gamma function.
   For integer x,
                     n-1
                      -
   psi(n) = -EUL  +   >  1/k.
                      -
                     k=1
  
   This formula is used for 0 < n <= 10.  If x is negative, it
   is transformed to a positive argument by the reflection
   formula  psi(1-x) = psi(x) + pi cot(pi x).
   For general positive x, the argument is made greater than 10
   using the recurrence  psi(x+1) = psi(x) + 1/x.
   Then the following asymptotic expansion is applied:
  
                             inf.   B
                              -      2k
   psi(x) = log(x) - 1/2x -   >   -------
                              -        2k
                             k=1   2k x
  
   where the B2k are Bernoulli numbers.
  
   ACCURACY:
      Relative error (except absolute when |psi| < 1):
   arithmetic   domain     # trials      peak         rms
      DEC       0,30         2500       1.7e-16     2.0e-17
      IEEE      0,30        30000       1.3e-15     1.4e-16
      IEEE      -30,0       40000       1.5e-15     2.2e-16
  
   ERROR MESSAGES:
       message         condition      value returned
   psi singularity    x integer <=0      MAXNUM
  """
  return _transcendental.psi(x)


def fac(i):
  """\
  	Factorial function
  
  
  
   SYNOPSIS:
  
   y = fac(i)
       where i is an integer.
  
  
  
   DESCRIPTION:
  
   Returns factorial of i  =  1 * 2 * 3 * ... * i.
   fac(0) = 1.0.
  
   Due to machine arithmetic bounds the largest value of
   i accepted is 33 in DEC arithmetic or 170 in IEEE
   arithmetic.  Greater values, or negative ones,
   produce an error message and return MAXNUM.
  
  
  
   ACCURACY:
  
   For i < 34 the values are simply tabulated, and have
   full machine accuracy.  If i > 55, fac(i) = gamma(i+1);
   see gamma.
  
                        Relative error:
   arithmetic   domain      peak
      IEEE      0, 170    1.4e-15
      DEC       0, 33      1.4e-17
  """
  return _transcendental.fac(i)



def bdtr(k, n, p):
  """\
  	Binomial distribution
  
  
  
   SYNOPSIS:
  
   y = bdtr(k, n, p)
       where k, n are integers, and 0 <= p <= 1.
  
   DESCRIPTION:
  
   Returns the sum of the terms 0 through k of the Binomial
   probability density:
  
     k
     --  ( n )   j      n-j
     >   (   )  p  (1-p)
     --  ( j )
    j=0
  
   The terms are not summed directly; instead the incomplete
   beta integral is employed, according to the formula
  
   y = bdtr(k, n, p) = incbet(n-k, k+1, 1-p).
  
   The arguments must be positive, with p ranging from 0 to 1.
  
   ACCURACY:
  
   Tested at random points (a,b,p), with p between 0 and 1.
  
                 a,b                     Relative error:
   arithmetic  domain     # trials      peak         rms
    For p between 0.001 and 1:
      IEEE     0,100       100000      4.3e-15     2.6e-16
   See also incbet.
  
   ERROR MESSAGES:
  
     message         condition      value returned
   bdtr domain         k < 0            0.0
                       n < k
                       x < 0, x > 1
  """
  return _transcendental.bdtr(k,n,p)



def bdtrc(k,n,p):
  """\
  	Complemented binomial distribution
  
  
  
   SYNOPSIS:
  
   y = bdtrc(k, n, p)
       where k, n are integers, and 0 <= p <= 1.
  
   DESCRIPTION:
  
   Returns the sum of the terms k+1 through n of the Binomial
   probability density:
  
     n
     --  ( n )   j      n-j
     >   (   )  p  (1-p)
     --  ( j )
    j=k+1
  
   The terms are not summed directly; instead the incomplete
   beta integral is employed, according to the formula
  
   y = bdtrc( k, n, p ) = incbet( k+1, n-k, p ).
  
   The arguments must be positive, with p ranging from 0 to 1.
  
   ACCURACY:
  
   Tested at random points (a,b,p).
  
                 a,b                     Relative error:
   arithmetic  domain     # trials      peak         rms
    For p between 0.001 and 1:
      IEEE     0,100       100000      6.7e-15     8.2e-16
    For p between 0 and .001:
      IEEE     0,100       100000      1.5e-13     2.7e-15
  
   ERROR MESSAGES:
  
     message         condition      value returned
   bdtrc domain      x<0, x>1, n<k       0.0
  """
  return _transcendental.bdtrc(k,n,p)


def bdtri(k, n, y):
  """\
  	Inverse binomial distribution
  
  
  
   SYNOPSIS:
  
   p = bdtr(k, n, y)
       where k, n are integers, and 0 <= y <= 1.
  
   DESCRIPTION:
  
   Finds the event probability p such that the sum of the
   terms 0 through k of the Binomial probability density
   is equal to the given cumulative probability y.
  
   This is accomplished using the inverse beta integral
   function and the relation
  
   1 - p = incbi(n-k, k+1, y).
  
   ACCURACY:
  
   Tested at random points (a,b,p).
  
                 a,b                     Relative error:
   arithmetic  domain     # trials      peak         rms
    For p between 0.001 and 1:
      IEEE     0,100       100000      2.3e-14     6.4e-16
      IEEE     0,10000     100000      6.6e-12     1.2e-13
    For p between 10^-6 and 0.001:
      IEEE     0,100       100000      2.0e-12     1.3e-14
      IEEE     0,10000     100000      1.5e-12     3.2e-14
   See also incbi.
  
   ERROR MESSAGES:
  
     message         condition      value returned
   bdtri domain     k < 0, n <= k         0.0
                    x < 0, x > 1
  """
  return _transcendental.bdtri(k,n,y)


def nbdtr(k, n, p):
  """\
  	Negative binomial distribution
  
  
  
   SYNOPSIS:
  
   y = nbdtr(k, n, p)
       where k, n are integers and 0 <= p <= 1.
  
   DESCRIPTION:
  
   Returns the sum of the terms 0 through k of the negative
   binomial distribution:
  
     k
     --  ( n+j-1 )   n      j
     >   (       )  p  (1-p)
     --  (   j   )
    j=0
  
   In a sequence of Bernoulli trials, this is the probability
   that k or fewer failures precede the nth success.
  
   The terms are not computed individually; instead the incomplete
   beta integral is employed, according to the formula
  
   y = nbdtr( k, n, p ) = incbet( n, k+1, p ).
  
   The arguments must be positive, with p ranging from 0 to 1.
  
   ACCURACY:
  
   Tested at random points (a,b,p), with p between 0 and 1.
  
                 a,b                     Relative error:
   arithmetic  domain     # trials      peak         rms
      IEEE     0,100       100000      1.7e-13     8.8e-15
   See also incbet.
  """
  return _transcendental.nbdtr(k,n,p)
  

def nbdtrc(k,n,p):
  """\
  	Complemented negative binomial distribution
  
  
  
   SYNOPSIS:
  
   y = nbdtrc(k, n, p)
       where k, n are integers, and 0 <= p <= 1.
  
   DESCRIPTION:
  
   Returns the sum of the terms k+1 to infinity of the negative
   binomial distribution:
  
     inf
     --  ( n+j-1 )   n      j
     >   (       )  p  (1-p)
     --  (   j   )
    j=k+1
  
   The terms are not computed individually; instead the incomplete
   beta integral is employed, according to the formula
  
   y = nbdtrc(k, n, p) = incbet(k+1, n, 1-p).
  
   The arguments must be positive, with p ranging from 0 to 1.
  
   ACCURACY:
  
   Tested at random points (a,b,p), with p between 0 and 1.
  
                 a,b                     Relative error:
   arithmetic  domain     # trials      peak         rms
      IEEE     0,100       100000      1.7e-13     8.8e-15
   See also incbet.
  """
  return _transcendental.nbdtrc(k,n,p)



def nbdtri(k, n, y):
  """\
  	Functional inverse of negative binomial distribution
  
  
  
   SYNOPSIS:
  
   p = nbdtri(k, n, y)
       where k, n are integers, and 0 <= y <= 1.
  
   DESCRIPTION:
  
   Finds the argument p such that nbdtr(k,n,p) is equal to y.
  
   ACCURACY:
  
   Tested at random points (a,b,y), with y between 0 and 1.
  
                 a,b                     Relative error:
   arithmetic  domain     # trials      peak         rms
      IEEE     0,100       100000      1.5e-14     8.5e-16
   See also incbi.
  """
  return _transcendental.nbdtri(k, n, y)


def gdtr(a, b, x):
  """\
  	Gamma distribution function
  
  
  
   SYNOPSIS:
  
   y = gdtr(a, b, x)
  
  
  
   DESCRIPTION:
  
   Returns the integral from zero to x of the gamma probability
   density function:
  
  
                  x
          b       -
         a       | |   b-1  -at
   y =  -----    |    t    e    dt
         -     | |
        | (b)   -
                 0
  
    The incomplete gamma integral is used, according to the
   relation
  
   y = igam(b, ax).
  
  
   ACCURACY:
  
   See igam().
  
   ERROR MESSAGES:
  
     message         condition      value returned
   gdtr domain         x < 0            0.0
  """
  return _transcendental.gdtr(a,b,x)



def gdtrc(a, b, x):
  """\
  	Complemented gamma distribution function
  
  
  
   SYNOPSIS:
  
   y = gdtrc(a, b, x)
  
  
  
   DESCRIPTION:
  
   Returns the integral from x to infinity of the gamma
   probability density function:
  
  
                 inf.
          b       -
         a       | |   b-1  -at
   y =  -----    |    t    e    dt
         -     | |
        | (b)   -
                 x
  
    The incomplete gamma integral is used, according to the
   relation
  
   y = igamc(b, ax).
  
  
   ACCURACY:
  
   See igamc().
  
   ERROR MESSAGES:
  
     message         condition      value returned
   gdtrc domain         x < 0            0.0
  """
  return _transcendental.gdtrc(a,b,x) 



def pdtr(k, m):
  """\
  	Poisson distribution
  
  
  
   SYNOPSIS:
  
   y = pdtr(k, m)
       where k is an integer.
  
  
  
   DESCRIPTION:
  
   Returns the sum of the first k terms of the Poisson
   distribution:
  
     k         j
     --   -m  m
     >   e    --
     --       j!
    j=0
  
   The terms are not summed directly; instead the incomplete
   gamma integral is employed, according to the relation
  
   y = pdtr(k, m) = igamc(k+1, m).
  
   The arguments must both be positive.
  
  
  
   ACCURACY:
  
   See igamc().
  """
  return _transcendental.pdtr(k, m)



def pdtrc(k, m):
  """\
  	Complemented poisson distribution
  
  
  
   SYNOPSIS:
  
   y = pdtrc( k, m )
       where k is an integer.
  
  
  
   DESCRIPTION:
  
   Returns the sum of the terms k+1 to infinity of the Poisson
   distribution:
  
    inf.       j
     --   -m  m
     >   e    --
     --       j!
    j=k+1
  
   The terms are not summed directly; instead the incomplete
   gamma integral is employed, according to the formula
  
   y = pdtrc(k, m) = igam(k+1, m).
  
   The arguments must both be positive.
  
  
  
   ACCURACY:
  
   See igam.
  """
  return _transcendental.pdtrc(k, m)


def pdtri(k, y):
  """\
  	Inverse Poisson distribution
  
  
  
   SYNOPSIS:
  
   m = pdtri( k, y )
       where k is an integer and 0 <= y <= 1.
  
  
  
  
   DESCRIPTION:
  
   Finds the Poisson variable x such that the integral
   from 0 to x of the Poisson density is equal to the
   given probability y.
  
   This is accomplished using the inverse gamma integral
   function and the relation
  
      m = igami(k+1, y ).
  
  
  
  
   ACCURACY:
  
   See igami.
  
   ERROR MESSAGES:
  
     message         condition      value returned
   pdtri domain    y < 0 or y >= 1       0.0
                       k < 0
  """
  return _transcendental.pdtri(k, y)



def beta(a, b):
  """\
  	Beta function
  
  
  
   SYNOPSIS:
  
   y = beta( a, b )
  
  
  
   DESCRIPTION:
  
                     -     -
                    | (a) | (b)
   beta( a, b )  =  -----------.
                       -
                      | (a+b)
  
   For large arguments the logarithm of the function is
   evaluated using lgam(), then exponentiated.
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC        0,30        1700       7.7e-15     1.5e-15
      IEEE       0,30       30000       8.1e-14     1.1e-14
  
   ERROR MESSAGES:
  
     message         condition          value returned
   beta overflow    log(beta) > MAXLOG       0.0
                    a or b <0 integer        0.0
  """
  return _transcendental.beta(a,b)

 
def igam(a, x):
  """\
  	Incomplete gamma integral
  
  
  
   SYNOPSIS:
  
   y = igam(a, x)

  
   DESCRIPTION:
  
   The function is defined by
  
                             x
                              -
                     1       | |  -t  a-1
    igam(a,x)  =   -----     |   e   t   dt.
                    -      | |
                   | (a)    -
                             0
  
  
   In this implementation both arguments must be positive.
   The integral is evaluated by either a power series or
   continued fraction expansion, depending on the relative
   values of a and x.
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      0,30       200000       3.6e-14     2.9e-15
      IEEE      0,100      300000       9.9e-14     1.5e-14
  """
  return _transcendental.igam(a,x)



def igamc(a,x):
  """\
  	Complemented incomplete gamma integral
  
  
  
   SYNOPSIS:
  
   y = igamc(a, x)

  
   DESCRIPTION:
  
   The function is defined by
  
  
    igamc(a,x)   =   1 - igam(a,x)
  
                              inf.
                                -
                       1       | |  -t  a-1
                 =   -----     |   e   t   dt.
                      -      | |
                     | (a)    -
                               x
  
  
   In this implementation both arguments must be positive.
   The integral is evaluated by either a power series or
   continued fraction expansion, depending on the relative
   values of a and x.
  
   ACCURACY:
  
   Tested at random a, x.
                  a         x                      Relative error:
   arithmetic   domain   domain     # trials      peak         rms
      IEEE     0.5,100   0,100      200000       1.9e-14     1.7e-15
      IEEE     0.01,0.5  0,100      200000       1.4e-13     1.6e-15
  """
  return _transcendental.igamc(a,x)


def igami(a, p):
  """\
        Inverse of complemented imcomplete gamma integral
  
  
  
   SYNOPSIS:
  
   x = igami(a, p)
       where 0 <= p <= 1.
  
  
   DESCRIPTION:
  
   Given p, the function finds x such that
  
    igamc(a, x) = p.
  
   Starting with the approximate value
  
           3
    x = a t
  
    where
  
    t = 1 - d - ndtri(p) sqrt(d)
   
   and
  
    d = 1/9a,
  
   the routine performs up to 10 Newton iterations to find the
   root of igamc(a,x) - p = 0.
  
   ACCURACY:
  
   Tested at random a, p in the intervals indicated.
  
                  a        p                      Relative error:
   arithmetic   domain   domain     # trials      peak         rms
      IEEE     0.5,100   0,0.5       100000       1.0e-14     1.7e-15
      IEEE     0.01,0.5  0,0.5       100000       9.0e-14     3.4e-15
      IEEE    0.5,10000  0,0.5        20000       2.3e-13     3.8e-14
  """
  return _transcendental.igami(a,p)



def incbet(a, b, x):
  """\
  	Incomplete beta integral
  
  
   SYNOPSIS:
  
   y = incbet(a, b, x)
  
  
   DESCRIPTION:
  
   Returns incomplete beta integral of the arguments, evaluated
   from zero to x.  The function is defined as
  
                    x
       -            -
      | (a+b)      | |  a-1     b-1
    -----------    |   t   (1-t)   dt.
     -     -     | |
    | (a) | (b)   -
                   0
  
   The domain of definition is 0 <= x <= 1.  In this
   implementation a and b are restricted to positive values.
   The integral from x to 1 may be obtained by the symmetry
   relation
  
      1 - incbet(a, b, x)  =  incbet(b, a, 1-x).
  
   The integral is evaluated by a continued fraction expansion
   or, when b*x is small, by a power series.
  
   ACCURACY:
 
   Tested at uniformly distributed random points (a,b,x) with a and b
   in "domain" and x between 0 and 1.
                                          Relative error
   arithmetic   domain     # trials      peak         rms
      IEEE      0,5         10000       6.9e-15     4.5e-16
      IEEE      0,85       250000       2.2e-13     1.7e-14
      IEEE      0,1000      30000       5.3e-12     6.3e-13
      IEEE      0,10000    250000       9.3e-11     7.1e-12
      IEEE      0,100000    10000       8.7e-10     4.8e-11
   Outputs smaller than the IEEE gradual underflow threshold
   were excluded from these statistics.
  
   ERROR MESSAGES:
     message         condition      value returned
   incbet domain      x<0, x>1          0.0
   incbet underflow                     0.0
  """
  return _transcendental.incbet(a,b,x)



def incbi(a, b, y):
  """\
        Inverse of imcomplete beta integral
  
  
  
   SYNOPSIS:
  
   x = incbi(a, b, y)
  
  
  
   DESCRIPTION:
  
   Given y, the function finds x such that
  
    incbet( a, b, x ) = y .
  
   The routine performs interval halving or Newton iterations to find the
   root of incbet(a,b,x) - y = 0.
  
  
   ACCURACY:
  
                        Relative error:
                  x     a,b
   arithmetic   domain  domain  # trials    peak       rms
      IEEE      0,1    .5,10000   50000    5.8e-12   1.3e-13
      IEEE      0,1   .25,100    100000    1.8e-13   3.9e-15
      IEEE      0,1     0,5       50000    1.1e-12   5.5e-15
      VAX       0,1    .5,100     25000    3.5e-14   1.1e-15
   With a and b constrained to half-integer or integer values:
      IEEE      0,1    .5,10000   50000    5.8e-12   1.1e-13
      IEEE      0,1    .5,100    100000    1.7e-14   7.9e-16
   With a = .5, b constrained to half-integer or integer values:
      IEEE      0,1    .5,10000   10000    8.3e-11   1.0e-11 *
  """
  return _transcendental.incbi(a, b, y)



def fresnl(x):
  """\
  	Fresnel integral
  
  
  
   SYNOPSIS:
  
   S, C = fresnl(x)
  
  
   DESCRIPTION:
  
   Evaluates the Fresnel integrals
  
             x
             -
            | |
   C(x) =   |   cos(pi/2 t**2) dt,
          | |
           -
            0
  
             x
             -
            | |
   S(x) =   |   sin(pi/2 t**2) dt.
          | |
           -
            0
  
  
   The integrals are evaluated by a power series for x < 1.
   For x >= 1 auxiliary functions f(x) and g(x) are employed
   such that
  
   C(x) = 0.5 + f(x) sin( pi/2 x**2 ) - g(x) cos( pi/2 x**2 )
   S(x) = 0.5 - f(x) cos( pi/2 x**2 ) - g(x) sin( pi/2 x**2 )
  
  
  
   ACCURACY:
  
    Relative error.
  
   Arithmetic  function   domain     # trials      peak         rms
     IEEE       S(x)      0, 10       10000       2.0e-15     3.2e-16
     IEEE       C(x)      0, 10       10000       1.8e-15     3.3e-16
     DEC        S(x)      0, 10        6000       2.2e-16     3.9e-17
     DEC        C(x)      0, 10        5000       2.3e-16     3.9e-17
  /
  """
  return _transcendental.fresnl(x)


def stdtr(k, t):
  """\
  	Student's t distribution
  
  
  
   SYNOPSIS:
  
   y = stdtr(k, t)
       where k is an integer
  
  
   DESCRIPTION:
  
   Computes the integral from minus infinity to t of the Student
   t distribution with integer k > 0 degrees of freedom:
  
                                        t
                                        -
                                       | |
                -                      |         2   -(k+1)/2
               | ( (k+1)/2 )           |  (     x   )
         ----------------------        |  ( 1 + --- )        dx
                       -               |  (      k  )
         sqrt( k pi ) | ( k/2 )        |
                                     | |
                                      -
                                     -inf.
   
   Relation to incomplete beta integral:
  
          1 - stdtr(k,t) = 0.5 * incbet( k/2, 1/2, z )
   where
          z = k/(k + t**2).
  
   For t < -2, this is the method of computation.  For higher t,
   a direct method is derived from integration by parts.
   Since the function is symmetric about t=0, the area under the
   right tail of the density is found by calling the function
   with -t instead of t.
   
   ACCURACY:
  
   Tested at random 1 <= k <= 25.  The "domain" refers to t.
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE     -100,-2      50000       5.9e-15     1.4e-15
      IEEE     -2,100      500000       2.7e-15     4.9e-17
  """
  return _transcendental.stdtr(k,t)


def stdtri(k, p):
  """\
  	Functional inverse of Student's t distribution
  
  
  
   SYNOPSIS:
  
   t = stdtri(k, p)
       where i is an integer, and 0 <= p <= 1.
  
  
   DESCRIPTION:
  
   Given probability p, finds the argument t such that stdtr(k,t)
   is equal to p.
   
   ACCURACY:
  
   Tested at random 1 <= k <= 100.  The "domain" refers to p:
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE    .001,.999     25000       5.7e-15     8.0e-16
      IEEE    10^-6,.001    25000       2.0e-12     2.9e-14
  """
  return _transcendental.stdtri(k, p)


def chdtr(v, x):
  """\
  	Chi-square distribution
  
  
  
   SYNOPSIS:
  
   y = chdtr(v, x)
  
  
  
   DESCRIPTION:
  
   Returns the area under the left hand tail (from 0 to x)
   of the Chi square probability density function with
   v degrees of freedom.
  
  
                                    inf.
                                      -
                          1          | |  v/2-1  -t/2
    P( x | v )   =   -----------     |   t      e     dt
                      v/2  -       | |
                     2    | (v/2)   -
                                     x
  
   where x is the Chi-square variable.
  
   The incomplete gamma integral is used, according to the
   formula
  
  	y = chdtr(v, x) = igam(v/2.0, x/2.0).
  
  
   The arguments must both be positive.
  
  
  
   ACCURACY:
  
   See igam().
  
   ERROR MESSAGES:
  
     message         condition      value returned
   chdtr domain   x < 0 or v < 1        0.0
  """
  return _transcendental.chdtr(v, x)



def chdtrc(v, x):
  """\
  	Complemented Chi-square distribution
  
  
  
   SYNOPSIS:
  
   y = chdtrc(v, x)
  
  
  
   DESCRIPTION:
  
   Returns the area under the right hand tail (from x to
   infinity) of the Chi square probability density function
   with v degrees of freedom:
  
  
                                    inf.
                                      -
                          1          | |  v/2-1  -t/2
    P( x | v )   =   -----------     |   t      e     dt
                      v/2  -       | |
                     2    | (v/2)   -
                                     x
  
   where x is the Chi-square variable.
  
   The incomplete gamma integral is used, according to the
   formula
  
  	y = chdtr( v, x ) = igamc( v/2.0, x/2.0 ).
  
  
   The arguments must both be positive.
  
  
  
   ACCURACY:
  
   See igamc().
  
   ERROR MESSAGES:
  
     message         condition      value returned
   chdtrc domain  x < 0 or v < 1        0.0
  """
  return _transcendental.chdtrc(v, x)


def chdtri(v, y):
  """\
  	Inverse of complemented Chi-square distribution
  
  
  
   SYNOPSIS:
  
   x = chdtri(v, y)
       with 0 <= y <= 1.
  
  
  
  
   DESCRIPTION:
  
   Finds the Chi-square argument x such that the integral
   from x to infinity of the Chi-square density is equal
   to the given cumulative probability y.
  
   This is accomplished using the inverse gamma integral
   function and the relation
  
      x/2 = igami(df/2, y)
  
  
  
  
   ACCURACY:
  
   See igami.
  
   ERROR MESSAGES:
  
     message         condition      value returned
   chdtri domain   y < 0 or y > 1        0.0
                       v < 1
  
  """
  return _transcendental.chdtri(v, y)



def fdtr(a, b, x):
  """\
  	F distribution
  
  
  
   SYNOPSIS:
  
   y = fdtr(a, b, x)
       where a, b are integers.

  
   DESCRIPTION:
  
   Returns the area from zero to x under the F density
   function (also known as Snedcor's density or the
   variance ratio density).  This is the density
   of x = (u1/a)/(u2/b), where u1 and u2 are random
   variables having Chi square distributions with a
   and b degrees of freedom, respectively.
  
   The incomplete beta integral is used, according to the
   formula
  
  	P(x) = incbet(a/2, b/2, (a*x/(b + a*x)).
  
  
   The arguments a and b are greater than zero, and x is
   nonnegative.
  
   ACCURACY:
  
   Tested at random points (a,b,x).
  
                  x     a,b                     Relative error:
   arithmetic  domain  domain     # trials      peak         rms
      IEEE      0,1    0,100       100000      9.8e-15     1.7e-15
      IEEE      1,5    0,100       100000      6.5e-15     3.5e-16
      IEEE      0,1    1,10000     100000      2.2e-11     3.3e-12
      IEEE      1,5    1,10000     100000      1.1e-11     1.7e-13
   See also incbet.
  
  
   ERROR MESSAGES:
  
     message         condition      value returned
   fdtr domain     a<0, b<0, x<0         0.0
  
  """
  return _transcendental.fdtr(a, b, x)



def fdtrc(a, b, x):
  """\
  	Complemented F distribution
  
  
  
   SYNOPSIS:
  
   y = fdtrc(a, b, x)
       where a, b are integers.

  
   DESCRIPTION:
  
   Returns the area from x to infinity under the F density
   function (also known as Snedcor's density or the
   variance ratio density).
  
  
                        inf.
                         -
                1       | |  a-1      b-1
   1-P(x)  =  ------    |   t    (1-t)    dt
              B(a,b)  | |
                       -
                        x
  
  
   The incomplete beta integral is used, according to the
   formula
  
  	P(x) = incbet(b/2, a/2, (b/(b + a*x)).
  
  
   ACCURACY:
  
   Tested at random points (a,b,x) in the indicated intervals.
                  x     a,b                     Relative error:
   arithmetic  domain  domain     # trials      peak         rms
      IEEE      0,1    1,100       100000      3.7e-14     5.9e-16
      IEEE      1,5    1,100       100000      8.0e-15     1.6e-15
      IEEE      0,1    1,10000     100000      1.8e-11     3.5e-13
      IEEE      1,5    1,10000     100000      2.0e-11     3.0e-12
   See also incbet.
  
   ERROR MESSAGES:
  
     message         condition      value returned
   fdtrc domain    a<0, b<0, x<0         0.0
  
  """
  return _transcendental.fdtrc(a, b, x)



def fdtri(a, b, p):
  """\
  	Inverse of complemented F distribution
  
  
  
   SYNOPSIS:
  
   x = fdtri(a, b, p)
       where a, b are integers.

  
   DESCRIPTION:
  
   Finds the F density argument x such that the integral
   from x to infinity of the F density is equal to the
   given probability p.
  
   This is accomplished using the inverse beta integral
   function and the relations
  
        z = incbi( b/2, a/2, p )
        x = b (1-z) / (a z).
  
   Note: the following relations hold for the inverse of
   the uncomplemented F distribution:
  
        z = incbi( a/2, b/2, p )
        x = b z / (a (1-z)).
  
   ACCURACY:
  
   Tested at random points (a,b,p).
  
                a,b                     Relative error:
   arithmetic  domain     # trials      peak         rms
    For p between .001 and 1:
      IEEE     1,100       100000      8.3e-15     4.7e-16
      IEEE     1,10000     100000      2.1e-11     1.4e-13
    For p between 10^-6 and 10^-3:
      IEEE     1,100        50000      1.3e-12     8.4e-15
      IEEE     1,10000      50000      3.0e-12     4.8e-14
   See also fdtrc.
  
   ERROR MESSAGES:
  
     message         condition      value returned
   fdtri domain   p <= 0 or p > 1       0.0
                       v < 1
  
  """
  return _transcendental.fdtri(a, b, p)


def jn(n, x):
  """\
        Bessel function of integer order
  
  
  
   SYNOPSIS:
  
   y = jn(n, x)
  
  
  
   DESCRIPTION:
  
   Returns Bessel function of order n, where n is a
   (possibly negative) integer.
  
   The ratio of jn(x) to j0(x) is computed by backward
   recurrence.  First the ratio jn/jn-1 is found by a
   continued fraction expansion.  Then the recurrence
   relating successive orders is applied until j0 or j1 is
   reached.
  
   If n = 0 or 1 the routine for j0 or j1 is called
   directly.
  
  
  
   ACCURACY:
  
                        Absolute error:
   arithmetic   range      # trials      peak         rms
      DEC       0, 30        5500       6.9e-17     9.3e-18
      IEEE      0, 30        5000       4.4e-16     7.9e-17
  
  
   Not suitable for large n or x. Use jv() instead.
  
  """
  return _transcendental.jn(n, x)


def jv(v, x):
  """\
        Bessel function of noninteger order
  
  
  
   SYNOPSIS:
  
   y = jv(v, x)
  
  
  
   DESCRIPTION:
  
   Returns Bessel function of order v of the argument,
   where v is real.  Negative x is allowed if v is an integer.
  
   Several expansions are included: the ascending power
   series, the Hankel expansion, and two transitional
   expansions for large v.  If v is not too large, it
   is reduced by recurrence to a region of best accuracy.
   The transitional expansions give 12D accuracy for v > 500.
  
  
  
   ACCURACY:
   Results for integer v are indicated by *, where x and v
   both vary from -125 to +125.  Otherwise,
   x ranges from 0 to 125, v ranges as indicated by "domain."
   Error criterion is absolute, except relative when |jv()| > 1.
  
   arithmetic  v domain  x domain    # trials      peak       rms
      IEEE      0,125     0,125      100000      4.6e-15    2.2e-16
      IEEE   -125,0       0,125       40000      5.4e-11    3.7e-13
      IEEE      0,500     0,500       20000      4.4e-15    4.0e-16
   Integer v:
      IEEE   -125,125   -125,125      50000      3.5e-15*   1.9e-16*
  """
  return _transcendental.jv(v,x)


def yn(n, x):
  """\
        Bessel function of second kind of integer order
  
  
  
   SYNOPSIS:
  
   y = yn(n, x)
  
  
  
   DESCRIPTION:
  
   Returns Bessel function of order n, where n is a
   (possibly negative) integer.
  
   The function is evaluated by forward recurrence on
   n, starting with values computed by the routines
   y0() and y1().
  
   If n = 0 or 1 the routine for y0 or y1 is called
   directly.
  
  
  
   ACCURACY:
  
  
                        Absolute error, except relative
                        when y > 1:
   arithmetic   domain     # trials      peak         rms
      DEC       0, 30        2200       2.9e-16     5.3e-17
      IEEE      0, 30       30000       3.4e-15     4.3e-16
  
  
   ERROR MESSAGES:
  
     message         condition      value returned
   yn singularity   x = 0              MAXNUM
   yn overflow                         MAXNUM
  
   Spot checked against tables for x, n between 0 and 100.
  """
  return _transcendental.yn(n, x)


def yv(v, x):
  """\
        Bessel function of second kind of noninteger order
  
  
  
   SYNOPSIS:
  
   y = yv(v, x)
  
  
  
   DESCRIPTION:
  
   Returns Bessel function of the second kind of order v of the
   argument, where v is real.



   ACCURACY:
  
   Not accurately characterized, but spot checked against tables.
  """
  return _transcendental.yv(v,x)


def iv(v, x):
  """\
        Modified Bessel function of noninteger order
  
  
  
   SYNOPSIS:
  
   y = iv(v, x)
  
  
  
   DESCRIPTION:
  
   Returns modified Bessel function of order v of the
   argument.  If x is negative, v must be integer valued.
  
   The function is defined as Iv(x) = Jv( ix ).  It is
   here computed in terms of the confluent hypergeometric
   function, according to the formula
  
                v  -x
   Iv(x) = (x/2)  e   hyperg( v+0.5, 2v+1, 2x ) / gamma(v+1)
  
   If v is a negative integer, then v is replaced by -v.
  
  
   ACCURACY:
  
   Tested at random points (v, x), with v between 0 and
   30, x between 0 and 28.
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0,30          2000      3.1e-15     5.4e-16
      IEEE      0,30         10000      1.7e-14     2.7e-15
  
   Accuracy is diminished if v is near a negative integer.
  """
  return _transcendental.iv(v,x)


def kn(n, x):
  """\
        Modified Bessel function, third kind, integer order
  
  
  
   SYNOPSIS:
  
   y = kn(n, x)
  
  
  
   DESCRIPTION:
  
   Returns modified Bessel function of the third kind
   of order n of the argument.
  
   The range is partitioned into the two intervals [0,9.55] and
   (9.55, infinity).  An ascending power series is used in the
   low range, and an asymptotic expansion in the high range.
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0,30         3000       1.3e-9      5.8e-11
      IEEE      0,30        90000       1.8e-8      3.0e-10
  
   Error is high only near the crossover point x = 9.55
   between the two expansions used.
  """
  return _transcendental.kn(n,x)


def airy(x):
  """\
        Airy function
  
  
  
   SYNOPSIS:
  
   ai, aip, bi, bip = airy(x)
         
  
  
   DESCRIPTION:
  
   Solution of the differential equation
  
        y"(x) = xy. 
  
   The function returns the two independent solutions Ai, Bi
   and their first derivatives Ai'(x), Bi'(x).
  
   Evaluation is by power series summation for small x,
   by rational minimax approximations for large x.
  
  
  
   ACCURACY:
   Error criterion is absolute when function <= 1, relative
   when function > 1, except * denotes relative error criterion.
   For large negative x, the absolute error increases as x^1.5.
   For large positive x, the relative error increases as x^1.5.
  
   Arithmetic  domain   function  # trials      peak         rms
   IEEE        -10, 0     Ai        10000       1.6e-15     2.7e-16
   IEEE          0, 10    Ai        10000       2.3e-14*    1.8e-15*
   IEEE        -10, 0     Ai'       10000       4.6e-15     7.6e-16
   IEEE          0, 10    Ai'       10000       1.8e-14*    1.5e-15*
   IEEE        -10, 10    Bi        30000       4.2e-15     5.3e-16
   IEEE        -10, 10    Bi'       30000       4.9e-15     7.3e-16
   DEC         -10, 0     Ai         5000       1.7e-16     2.8e-17
   DEC           0, 10    Ai         5000       2.1e-15*    1.7e-16*
   DEC         -10, 0     Ai'        5000       4.7e-16     7.8e-17
   DEC           0, 10    Ai'       12000       1.8e-15*    1.5e-16*
   DEC         -10, 10    Bi        10000       5.5e-16     6.8e-17
   DEC         -10, 10    Bi'        7000       5.3e-16     8.7e-17
  """
  return _transcendental.airy(x)


def expn(n,x):
  """\
                Exponential integral En
  
  
  
   SYNOPSIS:
  
   y = expn(n, x)
  
  
  
   DESCRIPTION:
  
   Evaluates the exponential integral
  
                   inf.
                     -
                    | |   -xt
                    |    e
        E (x)  =    |    ----  dt.
         n          |      n
                  | |     t
                   -
                    1
  
  
   Both n and x must be nonnegative.
  
   The routine employs either a power series, a continued
   fraction, or an asymptotic formula depending on the
   relative values of n and x.
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0, 30        5000       2.0e-16     4.6e-17
      IEEE      0, 30       10000       1.7e-15     3.6e-16
  """
  return _transcendental.expn(n, x)


def shichi(x):
  """\
        Hyperbolic sine and cosine integrals
  
  
  
   SYNOPSIS:
  
   Chi, Shi = shichi(x)
  
  
   DESCRIPTION:
  
   Approximates the integrals
  
                              x
                              -
                             | |   cosh t - 1
     Chi(x) = eul + ln x +   |    -----------  dt,
                           | |          t
                            -
                            0
  
                 x
                 -
                | |  sinh t
     Shi(x) =   |    ------  dt
              | |       t
               -
               0
  
   where eul = 0.57721566490153286061 is Euler's constant.
   The integrals are evaluated by power series for x < 8
   and by Chebyshev expansions for x between 8 and 88.
   For large x, both functions approach exp(x)/2x.
   Arguments greater than 88 in magnitude return MAXNUM.
  
  
   ACCURACY:
  
   Test interval 0 to 88.
                        Relative error:
   arithmetic   function  # trials      peak         rms
      DEC          Shi       3000       9.1e-17
      IEEE         Shi      30000       6.9e-16     1.6e-16
          Absolute error, except relative when |Chi| > 1:
      DEC          Chi       2500       9.3e-17
      IEEE         Chi      30000       8.4e-16     1.4e-16
  """
  return _transcendental.shichi(x)


def sici(x):
  """\
        Sine and cosine integrals
  
  
  
   SYNOPSIS:
  
   Si, Ci = sici(x)
  
  
   DESCRIPTION:
  
   Evaluates the integrals
  
                            x
                            -
                           |  cos t - 1
     Ci(x) = eul + ln x +  |  --------- dt,
                           |      t
                          -
                           0
               x
               -
              |  sin t
     Si(x) =  |  ----- dt
              |    t
             -
              0
  
   where eul = 0.57721566490153286061 is Euler's constant.
   The integrals are approximated by rational functions.
   For x > 8 auxiliary functions f(x) and g(x) are employed
   such that
  
   Ci(x) = f(x) sin(x) - g(x) cos(x)
   Si(x) = pi/2 - f(x) cos(x) - g(x) sin(x)
  
  
   ACCURACY:
      Test interval = [0,50].
   Absolute error, except relative when > 1:
   arithmetic   function   # trials      peak         rms
      IEEE        Si        30000       4.4e-16     7.3e-17
      IEEE        Ci        30000       6.9e-16     5.1e-17
      DEC         Si         5000       4.4e-17     9.0e-18
      DEC         Ci         5300       7.9e-17     5.2e-18
  """
  return _transcendental.sici(x)


def hyperg(a, b, x):
  """\
        Confluent hypergeometric function
  
  
  
   SYNOPSIS:
  
   y = hyperg(a, b, x)
  
  
  
   DESCRIPTION:
  
   Computes the confluent hypergeometric function
  
                            1           2
                         a x    a(a+1) x
     F ( a,b;x )  =  1 + ---- + --------- + ...
    1 1                  b 1!   b(b+1) 2!
  
   Many higher transcendental functions are special cases of
   this power series.
  
   As is evident from the formula, b must not be a negative
   integer or zero unless a is an integer with 0 >= a > b.
  
   The routine attempts both a direct summation of the series
   and an asymptotic expansion.  In each case error due to
   roundoff, cancellation, and nonconvergence is estimated.
   The result with smaller estimated error is returned.
  
  
  
   ACCURACY:
  
   Tested at random points (a, b, x), all three variables
   ranging from 0 to 30.
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC       0,30         2000       1.2e-15     1.3e-16
 qtst1:
 21800   max =  1.4200E-14   rms =  1.0841E-15  ave = -5.3640E-17
 ltstd:
 25500   max = 1.2759e-14   rms = 3.7155e-16  ave = 1.5384e-18
      IEEE      0,30        30000       1.8e-14     1.1e-15
  
   Larger errors can be observed when b is near a negative
   integer or zero.  Certain combinations of arguments yield
   serious cancellation error in the power series summation
   and also are not in the region of near convergence of the
   asymptotic series.  An error message is printed if the
   self-estimated relative error is greater than 1.0e-12.
  """
  return _transcendental.hyperg(a,b,x)


def hyp2f1(a,b,c,x):
  """\
        Gauss hypergeometric function   F
                                       2 1
  
  
   SYNOPSIS:
  
   y = hyp2f1(a, b, c, x)
  
  
   DESCRIPTION:
  
  
    hyp2f1( a, b, c, x )  =   F ( a, b; c; x )
                             2 1
  
             inf.
              -   a(a+1)...(a+k) b(b+1)...(b+k)   k+1
     =  1 +   >   -----------------------------  x   .
              -         c(c+1)...(c+k) (k+1)!
            k = 0
  
    Cases addressed are
        Tests and escapes for negative integer a, b, or c
        Linear transformation if c - a or c - b negative integer
        Special case c = a or c = b
        Linear transformation for  x near +1
        Transformation for x < -0.5
        Psi function expansion if x > 0.5 and c - a - b integer
        Conditionally, a recurrence on c to make c-a-b > 0
  
   |x| > 1 is rejected.
  
   The parameters a, b, c are considered to be integer
   valued if they are within 1.0e-14 of the nearest integer
   (1.0e-13 for IEEE arithmetic).
  
   ACCURACY:
  
  
                 Relative error (-1 < x < 1):
   arithmetic   domain     # trials      peak         rms
      IEEE      -1,7        230000      1.2e-11     5.2e-14
  
   Several special cases also tested with a, b, c in
   the range -7 to 7.
  
   ERROR MESSAGES:
  
   A "partial loss of precision" message is printed if
   the internally estimated relative error exceeds 1^-12.
   A "singularity" message is printed on overflow or
   in cases not addressed (such as x < -1).
  /
  """
  return _transcendental.hyp2f1(a,b,c,x)

def ellpe(x):
  """\
        Complete elliptic integral of the second kind
  
  
  
   SYNOPSIS:
  
   y = ellpe(m1)
  
  
  
   DESCRIPTION:
  
   Approximates the integral
  
  
              pi/2
               -
              | |                 2
   E(m)  =    |    sqrt( 1 - m sin t ) dt
            | |
             -
              0
  
   Where m = 1 - m1, using the approximation
  
        P(x)  -  x log x Q(x).
  
   Though there are no singularities, the argument m1 is used
   rather than m for compatibility with ellpk().
  
   E(1) = 1; E(0) = pi/2.
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC        0, 1       13000       3.1e-17     9.4e-18
      IEEE       0, 1       10000       2.1e-16     7.3e-17
  
  
   ERROR MESSAGES:
  
     message         condition      value returned
   ellpe domain      x<0, x>1            0.0
  """
  return _transcendental.ellpe(x)


def ellie(phi,m):
  """\
        Incomplete elliptic integral of the second kind
  
  
  
   SYNOPSIS:
  
   y = ellie(phi, m)
  
  
  
   DESCRIPTION:
  
   Approximates the integral
  
  
                  phi
                   -
                  | |
                  |                   2
   E(phi_\m)  =    |    sqrt( 1 - m sin t ) dt
                  |
                | |
                 -
                  0
  
   of amplitude phi and modulus m, using the arithmetic -
   geometric mean algorithm.
  
  
  
   ACCURACY:
  
   Tested at random arguments with phi in [-10, 10] and m in
   [0, 1].
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC        0,2         2000       1.9e-16     3.4e-17
      IEEE     -10,10      150000       3.3e-15     1.4e-16
  """
  return _transcendental.ellie(phi,m)


def ellpk(m1):
  """\
        Complete elliptic integral of the first kind
  
  
  
   SYNOPSIS:
  
   y = ellpk( m1 )
  
  
  
   DESCRIPTION:
  
   Approximates the integral
  
  
  
              pi/2
               -
              | |
              |           dt
   K(m)  =    |    ------------------
              |                   2
            | |    sqrt( 1 - m sin t )
             -
              0
  
   where m = 1 - m1, using the approximation
  
       P(x)  -  log x Q(x).
  
   The argument m1 is used rather than m so that the logarithmic
   singularity at m = 1 will be shifted to the origin; this
   preserves maximum accuracy.
  
   K(0) = pi/2.
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      DEC        0,1        16000       3.5e-17     1.1e-17
      IEEE       0,1        30000       2.5e-16     6.8e-17
  
   ERROR MESSAGES:
  
     message         condition      value returned
   ellpk domain       x<0, x>1           0.0
  """
  return _transcendental.ellpk(m1)


def ellik(phi,m):
  """\
        Incomplete elliptic integral of the first kind
  
  
  
   SYNOPSIS:
  
   y = ellik(phi, m)
  
  
  
   DESCRIPTION:
  
   Approximates the integral
  
  
  
                  phi
                   -
                  | |
                  |           dt
   F(phi_\m)  =    |    ------------------
                  |                   2
                | |    sqrt( 1 - m sin t )
                 -
                  0
  
   of amplitude phi and modulus m, using the arithmetic -
   geometric mean algorithm.
  
  
  
  
   ACCURACY:
  
   Tested at random points with m in [0, 1] and phi as indicated.
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE     -10,10       200000      7.4e-16     1.0e-16
  
  """
  return _transcendental.ellik(phi,m)


def ellpj(u,m):
  """\
        Jacobian Elliptic Functions
  
  
  
   SYNOPSIS:
  
   sn, cn, dn, phi = ellpj(u, m)
  
  
  
   DESCRIPTION:
  
  
   Evaluates the Jacobian elliptic functions sn(u|m), cn(u|m),
   and dn(u|m) of parameter m between 0 and 1, and real
   argument u.
  
   These functions are periodic, with quarter-period on the
   real axis equal to the complete elliptic integral
   ellpk(1.0-m).
  
   Relation to incomplete elliptic integral:
   If u = ellik(phi,m), then sn(u|m) = sin(phi),
   and cn(u|m) = cos(phi).  Phi is called the amplitude of u.
  
   Computation is by means of the arithmetic-geometric mean
   algorithm, except when m is within 1e-9 of 0 or 1.  In the
   latter case with m close to 1, the approximation applies
   only for phi < pi/2.
  
   ACCURACY:
  
   Tested at random points with u between 0 and 10, m between
   0 and 1.
  
              Absolute error (* = relative error):
   arithmetic   function   # trials      peak         rms
      DEC       sn           1800       4.5e-16     8.7e-17
      IEEE      phi         10000       9.2e-16*    1.4e-16*
      IEEE      sn          50000       4.1e-15     4.6e-16
      IEEE      cn          40000       3.6e-15     4.4e-16
      IEEE      dn          10000       1.3e-12     1.8e-14
  
    Peak error observed in consistency check using addition
   theorem for sn(u+v) was 4e-16 (absolute).  Also tested by
   the above relation to the incomplete elliptic integral.
   Accuracy deteriorates when u is large.
  
  """
  return _transcendental.ellpj(u,m)


def spence(x):
  """\
        Dilogarithm
  
  
  
   SYNOPSIS:
  
   y = spence(x)
  
  
  
   DESCRIPTION:
  
   Computes the integral
  
                      x
                      -
                     | | log t
   spence(x)  =  -   |   ----- dt
                   | |   t - 1
                    -
                    1
  
   for x >= 0.  A rational approximation gives the integral in
   the interval (0.5, 1.5).  Transformation formulas for 1/x
   and 1-x are employed outside the basic expansion range.
  
  
  
   ACCURACY:
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      0,4         30000       3.9e-15     5.4e-16
      DEC       0,4          3000       2.5e-16     4.5e-17
  
  """
  return _transcendental.spence(x)


def zeta(x, q):
  """\
        Riemann zeta function of two arguments
  
  
  
   SYNOPSIS:
  
   y = zeta(x, q)
  
  
  
   DESCRIPTION:
  
  
  
                   inf.
                    -        -x
     zeta(x,q)  =   >   (k+q)
                    -
                   k=0
  
   where x > 1 and q is not a negative integer or zero.
   The Euler-Maclaurin summation formula is used to obtain
   the expansion
  
                  n
                  -       -x
   zeta(x,q)  =   >  (k+q)
                  -
                 k=1
  
             1-x                 inf.  B   x(x+1)...(x+2j)
        (n+q)           1         -     2j
    +  ---------  -  -------  +   >    --------------------
          x-1              x      -                   x+2j+1
                     2(n+q)      j=1       (2j)! (n+q)
  
   where the B2j are Bernoulli numbers.  Note that (see zetac.c)
   zeta(x,1) = zetac(x) + 1.
  
  
  
   ACCURACY:
  
  
  
   REFERENCE:
  
   Gradshteyn, I. S., and I. M. Ryzhik, Tables of Integrals,
   Series, and Products, p. 1073; Academic Press, 1980.
  """
  return _transcendental.zeta(x,q)


def zetac(x):
  """\
        Riemann zeta function
  
  
  
   SYNOPSIS:
  
   y = zetac(x)
  
  
  
   DESCRIPTION:
  
  
  
                  inf.
                   -    -x
     zetac(x)  =   >   k   ,   x > 1,
                   -
                  k=2
  
   is related to the Riemann zeta function by
  
        Riemann zeta(x) = zetac(x) + 1.
  
   Extension of the function definition for x < 1 is implemented.
   Zero is returned for x > log2(MAXNUM).
  
   An overflow error may occur for large negative x, due to the
   gamma function in the reflection formula.
  
   ACCURACY:
  
   Tabulated values have full machine accuracy.
  
                        Relative error:
   arithmetic   domain     # trials      peak         rms
      IEEE      1,50        10000       9.8e-16     1.3e-16
      DEC       1,50         2000       1.1e-16     1.9e-17
  
  """
  return _transcendental.zetac(x)


def struve(v,x):
  """\
        Struve function
  
  
  
   SYNOPSIS:
  
   y = struve(v, x)
  
  
  
   DESCRIPTION:
  
   Computes the Struve function Hv(x) of order v, argument x.
   Negative x is rejected unless v is an integer.
  
   This module also contains the hypergeometric functions 1F2
   and 3F0 and a routine for the Bessel function Yv(x) with
   noninteger v.
  
  
  
   ACCURACY:
  
   Not accurately characterized, but spot checked against tables.
  """
  return _transcendental.struve(v,x)
