/*
Cephes Math Library Release 2.8:  June, 2000
Copyright 1984, 1987, 1991, 1995, 2000 by Stephen L. Moshier
Direct inquiries to 30 Frost Street, Cambridge, MA 02140
*/

#include "mconf.h"
#include <math.h>
#include <Python.h>

int sgngam = 0;

extern double MAXNUM, MACHEP, MINLOG, MAXLOG, CEPHESINFINITY;
extern double PI, TWOOPI, SQ2OPI, PIO4, THPIO4, PIO2, SQRTH;
#ifndef CEPHESINFINITY
#ifdef INFINITIES
extern double CEPHESINFINITY;
#endif
#endif
#ifndef NAN
#ifdef NANS
extern double NAN;
#endif
#endif

#ifdef HAVE_GAMMA
#define cephesgamma gamma
#endif

#ifdef ANSIPROT
extern double fabs ( double );
extern double frexp ( double, int * );
extern double ldexp (double, int);
extern double sqrt ( double );
extern double exp ( double );
extern double log ( double );
extern double sin ( double );
extern double cos ( double );
extern double tan ( double );
extern double asin (double);
extern double acos ( double );
extern double atan (double);
extern double sinh (double);
extern double cosh (double);
extern double tanh (double);
extern double cephesgamma ( double );
extern double lgamma ( double );
extern double psi ( double );
extern double floor ( double );
extern double round ( double );
extern double pow ( double, double );
extern double log1p ( double );
extern double expm1 ( double );
extern double expx2 (double, int);
#ifndef isnan
extern int isnan (double);
#endif
#ifndef isfinite
extern int isfinite (double);
#endif
extern double polevl (double, void *, int);
extern double p1evl (double, void *, int);
extern double chbevl (double, void *, int);
extern double yn (int, double);
extern double jv (double, double);
extern double igam ( double, double );
extern double igamc ( double, double );
extern double igami ( double, double );
extern double incbet ( double, double, double );
extern double incbi ( double, double, double );
double zetac (double);  
int airy ( double, double *, double *, double *, double * );
double j0 ( double );
double j1 ( double );
double y0 ( double );
double y1 ( double );
double i0 ( double );
double i1 ( double );
#ifndef HAVE_GAMMA
static double stirf ( double );
#endif
double yv (double, double);
double onef2 (double, double, double, double, double *);
double threef0 (double, double, double, double, double *);
double ellpe (double);
double ellpk (double);
double ellik (double, double);
double ellie (double, double);
double erf (double);
double erfc (double);
double hyp2f0 ( double, double, double, int, double * );
double hyperg (double, double, double);
double hyp2f1(double, double, double, double);
extern double ndtri ( double );
extern double cbrt ( double );
extern double hyperg ( double, double, double );
static double recur(double *, double, double *, int);
static double jvs(double, double);
static double hankel(double, double);
static double jnx(double, double);
static double jnt(double, double);
static double incbcf(double, double, double);
static double incbd(double, double, double);
static double pseries(double, double, double);
static double hy1f1p(double, double, double, double *);
static double hy1f1a(double, double, double, double *);
static double hyt2f1(double, double, double, double, double *);
static double hys2f1(double, double, double, double, double *);
static double erfce (double);
#else
double frexp(), ldexp(), floor(), round();
double sqrt(), fabs(), log(), sin(), cos(), tan(), asin(), atan(), acos();
double pow(), sinh(), cosh(), tanh(), exp();
double ellik(), ellpe(), ellpk(), ellie(), cephesgamma(), lgamma(), psi();
double p1evl(), polevl(), chbevl(), zetac(), onef2(), threef0();
double yn(), yv(), jv(), j0(), j1(), y0(), y1(), i0(), i1();
double erf(), erfc(), expx2(), log1p(), expm1();
double incbet(), incbi(), igam(), igamc(), igami(), ndtri(), cbrt(), hyperg();
double hyp2f0();
double hyp2f1();
double hyperg();
int airy();
#ifndef isfinite
int isfinite();
#endif
#ifndef isnan
int isnan();
#endif
static double recur(), jvs(), hankel(), jnx(), jnt();
static double incbcf(), incbd(), pseries();
static double stirf();
static double erfce();
static double hy1f1p();
static double hy1f1a();
static double hyt2f1();
static double hys2f1();
#endif

#define EUL 5.772156649015328606065e-1
#define BIG  1.44115188075855872E+17
#define DEBUG 0
#ifdef DEC
#define MAXGAM 34.84425627277176174
#else
#define MAXGAM 171.624376956302725
#endif

/*
#define SQ2OPI .79788456080286535588
#define PIO4 .78539816339744830962
#define THPIO4 2.35619449019234492885
*/

/* ========================================================================= */

/*							cbrt.c
 *
 *	Cube root
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, cbrt();
 *
 * y = cbrt( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the cube root of the argument, which may be negative.
 *
 * Range reduction involves determining the power of 2 of
 * the argument.  A polynomial of degree 2 applied to the
 * mantissa, and multiplication by the cube root of 1, 2, or 4
 * approximates the root to within about 0.1%.  Then Newton's
 * iteration is used three times to converge to an accurate
 * result.
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC        -10,10     200000      1.8e-17     6.2e-18
 *    IEEE       0,1e308     30000      1.5e-16     5.0e-17
 *
 */
/*							cbrt.c  */



#ifndef HAVE_CBRT
static double CBRT2  = 1.2599210498948731647672;
static double CBRT4  = 1.5874010519681994747517;
static double CBRT2I = 0.79370052598409973737585;
static double CBRT4I = 0.62996052494743658238361;

double cbrt(double x)
{
int e, rem, sign;
double z;

#ifdef NANS
if( isnan(x) )
  return x;
#endif
#ifdef INFINITIES
if( !isfinite(x) )
  return x;
#endif
if( x == 0 )
	return( x );
if( x > 0 )
	sign = 1;
else
	{
	sign = -1;
	x = -x;
	}

z = x;
/* extract power of 2, leaving
 * mantissa between 0.5 and 1
 */
x = frexp( x, &e );

/* Approximate cube root of number between .5 and 1,
 * peak relative error = 9.2e-6
 */
x = (((-1.3466110473359520655053e-1  * x
      + 5.4664601366395524503440e-1) * x
      - 9.5438224771509446525043e-1) * x
      + 1.1399983354717293273738e0 ) * x
      + 4.0238979564544752126924e-1;

/* exponent divided by 3 */
if( e >= 0 )
	{
	rem = e;
	e /= 3;
	rem -= 3*e;
	if( rem == 1 )
		x *= CBRT2;
	else if( rem == 2 )
		x *= CBRT4;
	}


/* argument less than 1 */

else
	{
	e = -e;
	rem = e;
	e /= 3;
	rem -= 3*e;
	if( rem == 1 )
		x *= CBRT2I;
	else if( rem == 2 )
		x *= CBRT4I;
	e = -e;
	}

/* multiply by power of 2 */
x = ldexp( x, e );

/* Newton iteration */
x -= ( x - (z/(x*x)) )*0.33333333333333333333;
#ifdef DEC
x -= ( x - (z/(x*x)) )/3.0;
#else
x -= ( x - (z/(x*x)) )*0.33333333333333333333;
#endif

if( sign < 0 )
	x = -x;
return(x);
}
#endif

/* ========================================================================= */

/*							spence.c
 *
 *	Dilogarithm
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, spence();
 *
 * y = spence( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Computes the integral
 *
 *                    x
 *                    -
 *                   | | log t
 * spence(x)  =  -   |   ----- dt
 *                 | |   t - 1
 *                  -
 *                  1
 *
 * for x >= 0.  A rational approximation gives the integral in
 * the interval (0.5, 1.5).  Transformation formulas for 1/x
 * and 1-x are employed outside the basic expansion range.
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0,4         30000       3.9e-15     5.4e-16
 *    DEC       0,4          3000       2.5e-16     4.5e-17
 *
 *
 */

/*							spence.c */



#ifdef UNK
static double AS[8] = {
  4.65128586073990045278E-5,
  7.31589045238094711071E-3,
  1.33847639578309018650E-1,
  8.79691311754530315341E-1,
  2.71149851196553469920E0,
  4.25697156008121755724E0,
  3.29771340985225106936E0,
  1.00000000000000000126E0,
};
static double BS[8] = {
  6.90990488912553276999E-4,
  2.54043763932544379113E-2,
  2.82974860602568089943E-1,
  1.41172597751831069617E0,
  3.63800533345137075418E0,
  5.03278880143316990390E0,
  3.54771340985225096217E0,
  9.99999999999999998740E-1,
};
#endif
#ifdef DEC
static unsigned short AS[32] = {
0034503,0013315,0034120,0157771,
0036357,0135043,0016766,0150637,
0037411,0007533,0005212,0161475,
0040141,0031563,0023217,0120331,
0040455,0104461,0007002,0155522,
0040610,0034434,0065721,0120465,
0040523,0006674,0105671,0054427,
0040200,0000000,0000000,0000000,
};
static unsigned short BS[32] = {
0035465,0021626,0032367,0144157,
0036720,0016326,0134431,0000406,
0037620,0161024,0133701,0120766,
0040264,0131557,0152055,0064512,
0040550,0152424,0051166,0034272,
0040641,0006233,0014672,0111572,
0040543,0006674,0105671,0054425,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short AS[32] = {
0x1bff,0xa70a,0x62d9,0x3f08,
0xda34,0x63be,0xf744,0x3f7d,
0x5c68,0x6151,0x21eb,0x3fc1,
0xf41b,0x64d1,0x266e,0x3fec,
0x5b6a,0x21c0,0xb126,0x4005,
0x3427,0x8d7a,0x0723,0x4011,
0x2b23,0x9177,0x61b7,0x400a,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short BS[32] = {
0xf90e,0xc69e,0xa472,0x3f46,
0x2021,0xd723,0x039a,0x3f9a,
0x343f,0x96f8,0x1c42,0x3fd2,
0xad29,0xfa85,0x966d,0x3ff6,
0xc717,0x8a4e,0x1aa2,0x400d,
0x526f,0x6337,0x2193,0x4014,
0x2b23,0x9177,0x61b7,0x400c,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short AS[32] = {
0x3f08,0x62d9,0xa70a,0x1bff,
0x3f7d,0xf744,0x63be,0xda34,
0x3fc1,0x21eb,0x6151,0x5c68,
0x3fec,0x266e,0x64d1,0xf41b,
0x4005,0xb126,0x21c0,0x5b6a,
0x4011,0x0723,0x8d7a,0x3427,
0x400a,0x61b7,0x9177,0x2b23,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short BS[32] = {
0x3f46,0xa472,0xc69e,0xf90e,
0x3f9a,0x039a,0xd723,0x2021,
0x3fd2,0x1c42,0x96f8,0x343f,
0x3ff6,0x966d,0xfa85,0xad29,
0x400d,0x1aa2,0x8a4e,0xc717,
0x4014,0x2193,0x6337,0x526f,
0x400c,0x61b7,0x9177,0x2b23,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif


double spence(double x)
{
double w, y, z;
int flag;

if( x < 0.0 )
	{
	mtherr( "spence", DOMAIN );
	return(0.0);
	}

if( x == 1.0 )
	return( 0.0 );

if( x == 0.0 )
	return( PI*PI/6.0 );

flag = 0;

if( x > 2.0 )
	{
	x = 1.0/x;
	flag |= 2;
	}

if( x > 1.5 )
	{
	w = (1.0/x) - 1.0;
	flag |= 2;
	}

else if( x < 0.5 )
	{
	w = -x;
	flag |= 1;
	}

else
	w = x - 1.0;


y = -w * polevl( w, AS, 7) / polevl( w, BS, 7 );

if( flag & 1 )
	y = (PI * PI)/6.0  - log(x) * log(1.0-x) - y;

if( flag & 2 )
	{
	z = log(x);
	y = -0.5 * z * z  -  y;
	}

return( y );
}

/* ========================================================================= */

/*							zeta.c
 *
 *	Riemann zeta function of two arguments
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, q, y, zeta();
 *
 * y = zeta( x, q );
 *
 *
 *
 * DESCRIPTION:
 *
 *
 *
 *                 inf.
 *                  -        -x
 *   zeta(x,q)  =   >   (k+q)  
 *                  -
 *                 k=0
 *
 * where x > 1 and q is not a negative integer or zero.
 * The Euler-Maclaurin summation formula is used to obtain
 * the expansion
 *
 *                n         
 *                -       -x
 * zeta(x,q)  =   >  (k+q)  
 *                -         
 *               k=1        
 *
 *           1-x                 inf.  B   x(x+1)...(x+2j)
 *      (n+q)           1         -     2j
 *  +  ---------  -  -------  +   >    --------------------
 *        x-1              x      -                   x+2j+1
 *                   2(n+q)      j=1       (2j)! (n+q)
 *
 * where the B2j are Bernoulli numbers.  Note that (see zetac.c)
 * zeta(x,1) = zetac(x) + 1.
 *
 *
 *
 * ACCURACY:
 *
 *
 *
 * REFERENCE:
 *
 * Gradshteyn, I. S., and I. M. Ryzhik, Tables of Integrals,
 * Series, and Products, p. 1073; Academic Press, 1980.
 *
 */


/* Expansion coefficients
 * for Euler-Maclaurin summation formula
 * (2k)! / B2k
 * where B2k are Bernoulli numbers
 */
static double AZ[] = {
12.0,
-720.0,
30240.0,
-1209600.0,
47900160.0,
-1.8924375803183791606e9, /*1.307674368e12/691*/
7.47242496e10,
-2.950130727918164224e12, /*1.067062284288e16/3617*/
1.1646782814350067249e14, /*5.109094217170944e18/43867*/
-4.5979787224074726105e15, /*8.028576626982912e20/174611*/
1.8152105401943546773e17, /*1.5511210043330985984e23/854513*/
-7.1661652561756670113e18 /*1.6938241367317436694528e27/236364091*/
};
/* 30 Nov 86 -- error in third coefficient fixed */


double zeta(double x, double q)
{
int i;
double a, b, k, s, t, w;

if( x == 1.0 )
	goto retinf;

if( x < 1.0 )
	{
domerr:
	mtherr( "zeta", DOMAIN );
	return(0.0);
	}

if( q <= 0.0 )
	{
	if(q == floor(q))
		{
		mtherr( "zeta", SING );
retinf:
		return( MAXNUM );
		}
	if( x != floor(x) )
		goto domerr; /* because q^-x not defined */
	}

/* Euler-Maclaurin summation formula */
/*
if( x < 25.0 )
*/
{
/* Permit negative q but continue sum until n+q > +9 .
 * This case should be handled by a reflection formula.
 * If q<0 and x is an integer, there is a relation to
 * the polygamma function.
 */
s = pow( q, -x );
a = q;
i = 0;
b = 0.0;
while( (i < 9) || (a <= 9.0) )
	{
	i += 1;
	a += 1.0;
	b = pow( a, -x );
	s += b;
	if( fabs(b/s) < MACHEP )
		goto done;
	}

w = a;
s += b*w/(x-1.0);
s -= 0.5 * b;
a = 1.0;
k = 0.0;
for( i=0; i<12; i++ )
	{
	a *= x + k;
	b /= w;
	t = a*b/AZ[i];
	s = s + t;
	t = fabs(t/s);
	if( t < MACHEP )
		goto done;
	k += 1.0;
	a *= x + k;
	b /= w;
	k += 1.0;
	}
done:
return(s);
}



/* Basic sum of inverse powers */
/*
pseres:

s = pow( q, -x );
a = q;
do
	{
	a += 2.0;
	b = pow( a, -x );
	s += b;
	}
while( b/s > MACHEP );

b = pow( 2.0, -x );
s = (s + b)/(1.0-b);
return(s);
*/
}

/* ========================================================================= */

 /*							zetac.c
 *
 *	Riemann zeta function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, zetac();
 *
 * y = zetac( x );
 *
 *
 *
 * DESCRIPTION:
 *
 *
 *
 *                inf.
 *                 -    -x
 *   zetac(x)  =   >   k   ,   x > 1,
 *                 -
 *                k=2
 *
 * is related to the Riemann zeta function by
 *
 *	Riemann zeta(x) = zetac(x) + 1.
 *
 * Extension of the function definition for x < 1 is implemented.
 * Zero is returned for x > log2(MAXNUM).
 *
 * An overflow error may occur for large negative x, due to the
 * gamma function in the reflection formula.
 *
 * ACCURACY:
 *
 * Tabulated values have full machine accuracy.
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      1,50        10000       9.8e-16	    1.3e-16
 *    DEC       1,50         2000       1.1e-16     1.9e-17
 *
 *
 */



/* Riemann zeta(x) - 1
 * for integer arguments between 0 and 30.
 */
#ifdef UNK
static double azetac[] = {
-1.50000000000000000000E0,
 1.70141183460469231730E38, /* infinity. */
 6.44934066848226436472E-1,
 2.02056903159594285400E-1,
 8.23232337111381915160E-2,
 3.69277551433699263314E-2,
 1.73430619844491397145E-2,
 8.34927738192282683980E-3,
 4.07735619794433937869E-3,
 2.00839282608221441785E-3,
 9.94575127818085337146E-4,
 4.94188604119464558702E-4,
 2.46086553308048298638E-4,
 1.22713347578489146752E-4,
 6.12481350587048292585E-5,
 3.05882363070204935517E-5,
 1.52822594086518717326E-5,
 7.63719763789976227360E-6,
 3.81729326499983985646E-6,
 1.90821271655393892566E-6,
 9.53962033872796113152E-7,
 4.76932986787806463117E-7,
 2.38450502727732990004E-7,
 1.19219925965311073068E-7,
 5.96081890512594796124E-8,
 2.98035035146522801861E-8,
 1.49015548283650412347E-8,
 7.45071178983542949198E-9,
 3.72533402478845705482E-9,
 1.86265972351304900640E-9,
 9.31327432419668182872E-10
};
#endif

#ifdef DEC
static unsigned short azetac[] = {
0140300,0000000,0000000,0000000,
0077777,0177777,0177777,0177777,
0040045,0015146,0022460,0076462,
0037516,0164001,0036001,0104116,
0037250,0114425,0061754,0022033,
0037027,0040616,0145174,0146670,
0036616,0011411,0100444,0104437,
0036410,0145550,0051474,0161067,
0036205,0115527,0141434,0133506,
0036003,0117475,0100553,0053403,
0035602,0056147,0045567,0027703,
0035401,0106157,0111054,0145242,
0035201,0002455,0113151,0101015,
0035000,0126235,0004273,0157260,
0034600,0071127,0112647,0005261,
0034400,0045736,0057610,0157550,
0034200,0031146,0172621,0074172,
0034000,0020603,0115503,0032007,
0033600,0013114,0124672,0023135,
0033400,0007330,0043715,0151117,
0033200,0004742,0145043,0033514,
0033000,0003225,0152624,0004411,
0032600,0002143,0033166,0035746,
0032400,0001354,0074234,0026143,
0032200,0000762,0147776,0170220,
0032000,0000514,0072452,0130631,
0031600,0000335,0114266,0063315,
0031400,0000223,0132710,0041045,
0031200,0000142,0073202,0153426,
0031000,0000101,0121400,0152065,
0030600,0000053,0140525,0072761
};
#endif

#ifdef IBMPC
static unsigned short azetac[] = {
0x0000,0x0000,0x0000,0xbff8,
0xffff,0xffff,0xffff,0x7fef,
0x0fa6,0xc4a6,0xa34c,0x3fe4,
0x310a,0x2780,0xdd00,0x3fc9,
0x8483,0xac7d,0x1322,0x3fb5,
0x99b7,0xd94f,0xe831,0x3fa2,
0x9124,0x3024,0xc261,0x3f91,
0x9c47,0x0a67,0x196d,0x3f81,
0x96e9,0xf863,0xb36a,0x3f70,
0x6ae0,0xb02d,0x73e7,0x3f60,
0xe5f8,0xe96e,0x4b8c,0x3f50,
0x9954,0xf245,0x318d,0x3f40,
0x3042,0xb2cd,0x20a5,0x3f30,
0x7bd6,0xa117,0x1593,0x3f20,
0xe156,0xf2b4,0x0e4a,0x3f10,
0x1bed,0xcbf1,0x097b,0x3f00,
0x2f0f,0xdeb2,0x064c,0x3ef0,
0x6681,0x7368,0x0430,0x3ee0,
0x44cc,0x9537,0x02c9,0x3ed0,
0xba4a,0x08f9,0x01db,0x3ec0,
0x66ea,0x5944,0x013c,0x3eb0,
0x8121,0xbab2,0x00d2,0x3ea0,
0xc77d,0x66ce,0x008c,0x3e90,
0x858c,0x8f13,0x005d,0x3e80,
0xde12,0x59ff,0x003e,0x3e70,
0x5633,0x8ea5,0x0029,0x3e60,
0xccda,0xb316,0x001b,0x3e50,
0x0845,0x76b9,0x0012,0x3e40,
0x5ae3,0x4ed0,0x000c,0x3e30,
0x1a87,0x3460,0x0008,0x3e20,
0xaebe,0x782a,0x0005,0x3e10
};
#endif

#ifdef MIEEE
static unsigned short azetac[] = {
0xbff8,0x0000,0x0000,0x0000,
0x7fef,0xffff,0xffff,0xffff,
0x3fe4,0xa34c,0xc4a6,0x0fa6,
0x3fc9,0xdd00,0x2780,0x310a,
0x3fb5,0x1322,0xac7d,0x8483,
0x3fa2,0xe831,0xd94f,0x99b7,
0x3f91,0xc261,0x3024,0x9124,
0x3f81,0x196d,0x0a67,0x9c47,
0x3f70,0xb36a,0xf863,0x96e9,
0x3f60,0x73e7,0xb02d,0x6ae0,
0x3f50,0x4b8c,0xe96e,0xe5f8,
0x3f40,0x318d,0xf245,0x9954,
0x3f30,0x20a5,0xb2cd,0x3042,
0x3f20,0x1593,0xa117,0x7bd6,
0x3f10,0x0e4a,0xf2b4,0xe156,
0x3f00,0x097b,0xcbf1,0x1bed,
0x3ef0,0x064c,0xdeb2,0x2f0f,
0x3ee0,0x0430,0x7368,0x6681,
0x3ed0,0x02c9,0x9537,0x44cc,
0x3ec0,0x01db,0x08f9,0xba4a,
0x3eb0,0x013c,0x5944,0x66ea,
0x3ea0,0x00d2,0xbab2,0x8121,
0x3e90,0x008c,0x66ce,0xc77d,
0x3e80,0x005d,0x8f13,0x858c,
0x3e70,0x003e,0x59ff,0xde12,
0x3e60,0x0029,0x8ea5,0x5633,
0x3e50,0x001b,0xb316,0xccda,
0x3e40,0x0012,0x76b9,0x0845,
0x3e30,0x000c,0x4ed0,0x5ae3,
0x3e20,0x0008,0x3460,0x1a87,
0x3e10,0x0005,0x782a,0xaebe
};
#endif


/* 2**x (1 - 1/x) (zeta(x) - 1) = P(1/x)/Q(1/x), 1 <= x <= 10 */
#ifdef UNK
static double PZC[9] = {
  5.85746514569725319540E11,
  2.57534127756102572888E11,
  4.87781159567948256438E10,
  5.15399538023885770696E9,
  3.41646073514754094281E8,
  1.60837006880656492731E7,
  5.92785467342109522998E5,
  1.51129169964938823117E4,
  2.01822444485997955865E2,
};
static double QZC[8] = {
/*  1.00000000000000000000E0,*/
  3.90497676373371157516E11,
  5.22858235368272161797E10,
  5.64451517271280543351E9,
  3.39006746015350418834E8,
  1.79410371500126453702E7,
  5.66666825131384797029E5,
  1.60382976810944131506E4,
  1.96436237223387314144E2,
};
#endif
#ifdef DEC
static unsigned short PZC[36] = {
0052010,0060466,0101211,0134657,
0051557,0154353,0135060,0064411,
0051065,0133157,0133514,0133633,
0050231,0114735,0035036,0111344,
0047242,0164327,0146036,0033545,
0046165,0065364,0130045,0011005,
0045020,0134427,0075073,0134107,
0043554,0021653,0000440,0177426,
0042111,0151213,0134312,0021402,
};
static unsigned short QZC[32] = {
/*0040200,0000000,0000000,0000000,*/
0051665,0153363,0054252,0137010,
0051102,0143645,0121415,0036107,
0050250,0034073,0131133,0036465,
0047241,0123250,0150037,0070012,
0046210,0160426,0111463,0116507,
0045012,0054255,0031674,0173612,
0043572,0114460,0151520,0012221,
0042104,0067655,0037037,0137421,
};
#endif
#ifdef IBMPC
static unsigned short PZC[36] = {
0x3736,0xd051,0x0c26,0x4261,
0x0d21,0x7746,0xfb1d,0x424d,
0x96f3,0xf6e9,0xb6cd,0x4226,
0xd25c,0xa743,0x333b,0x41f3,
0xc6ed,0xf983,0x5d1a,0x41b4,
0xa241,0x9604,0xad5e,0x416e,
0x7709,0xef47,0x1722,0x4122,
0x1fe3,0x6024,0x8475,0x40cd,
0x4460,0x7719,0x3a51,0x4069,
};
static unsigned short QZC[32] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x57c1,0x6b15,0xbade,0x4256,
0xa789,0xb461,0x58f4,0x4228,
0x67a7,0x764b,0x0707,0x41f5,
0xee01,0x1a03,0x34d5,0x41b4,
0x73a9,0xd266,0x1c22,0x4171,
0x9ef1,0xa677,0x4b15,0x4121,
0x0292,0x1a6a,0x5326,0x40cf,
0xf7e2,0xa7c3,0x8df5,0x4068,
};
#endif
#ifdef MIEEE
static unsigned short PZC[36] = {
0x4261,0x0c26,0xd051,0x3736,
0x424d,0xfb1d,0x7746,0x0d21,
0x4226,0xb6cd,0xf6e9,0x96f3,
0x41f3,0x333b,0xa743,0xd25c,
0x41b4,0x5d1a,0xf983,0xc6ed,
0x416e,0xad5e,0x9604,0xa241,
0x4122,0x1722,0xef47,0x7709,
0x40cd,0x8475,0x6024,0x1fe3,
0x4069,0x3a51,0x7719,0x4460,
};
static unsigned short QZC[32] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4256,0xbade,0x6b15,0x57c1,
0x4228,0x58f4,0xb461,0xa789,
0x41f5,0x0707,0x764b,0x67a7,
0x41b4,0x34d5,0x1a03,0xee01,
0x4171,0x1c22,0xd266,0x73a9,
0x4121,0x4b15,0xa677,0x9ef1,
0x40cf,0x5326,0x1a6a,0x0292,
0x4068,0x8df5,0xa7c3,0xf7e2,
};
#endif

/* log(zeta(x) - 1 - 2**-x), 10 <= x <= 50 */
#ifdef UNK
static double AZC[11] = {
 8.70728567484590192539E6,
 1.76506865670346462757E8,
 2.60889506707483264896E10,
 5.29806374009894791647E11,
 2.26888156119238241487E13,
 3.31884402932705083599E14,
 5.13778997975868230192E15,
-1.98123688133907171455E15,
-9.92763810039983572356E16,
 7.82905376180870586444E16,
 9.26786275768927717187E16,
};
static double BZC[10] = {
/* 1.00000000000000000000E0,*/
-7.92625410563741062861E6,
-1.60529969932920229676E8,
-2.37669260975543221788E10,
-4.80319584350455169857E11,
-2.07820961754173320170E13,
-2.96075404507272223680E14,
-4.86299103694609136686E15,
 5.34589509675789930199E15,
 5.71464111092297631292E16,
-1.79915597658676556828E16,
};
#endif
#ifdef DEC
static unsigned short AZC[44] = {
0046004,0156325,0126302,0131567,
0047050,0052177,0015271,0136466,
0050702,0060271,0070727,0171112,
0051766,0132727,0064363,0145042,
0053245,0012466,0056000,0117230,
0054226,0166155,0174275,0170213,
0055222,0003127,0112544,0101322,
0154741,0036625,0010346,0053767,
0156260,0054653,0154052,0031113,
0056213,0011152,0021000,0007111,
0056244,0120534,0040576,0163262,
};
static unsigned short BZC[40] = {
/*0040200,0000000,0000000,0000000,*/
0145761,0161734,0033026,0015520,
0147031,0013743,0017355,0036703,
0150661,0011720,0061061,0136402,
0151737,0125216,0070274,0164414,
0153227,0032653,0127211,0145250,
0154206,0121666,0123774,0042035,
0155212,0033352,0125154,0132533,
0055227,0170201,0110775,0072132,
0056113,0003133,0127132,0122303,
0155577,0126351,0141462,0171037,
};
#endif
#ifdef IBMPC
static unsigned short AZC[44] = {
0x566f,0xb598,0x9b9a,0x4160,
0x37a7,0xe357,0x0a8f,0x41a5,
0xfe49,0x2e3a,0x4c17,0x4218,
0x7944,0xed1e,0xd6ba,0x425e,
0x13d3,0xcb80,0xa2a6,0x42b4,
0xbe11,0xbf17,0xdd8d,0x42f2,
0x905a,0xf2ac,0x40ca,0x4332,
0xcaff,0xa21c,0x27b2,0xc31c,
0x4649,0x7b05,0x0b35,0xc376,
0x01c9,0x4440,0x624d,0x4371,
0xdcd6,0x882f,0x942b,0x4374,
};
static unsigned short BZC[40] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xc36a,0x86c2,0x3c7b,0xc15e,
0xa7b8,0x63dd,0x22fc,0xc1a3,
0x37a0,0x0c46,0x227a,0xc216,
0x9d22,0xce17,0xf551,0xc25b,
0x3955,0x75d1,0xe6b5,0xc2b2,
0x8884,0xd4ff,0xd476,0xc2f0,
0x96ab,0x554d,0x46dd,0xc331,
0xae8b,0x323f,0xfe10,0x4332,
0x5498,0x75cb,0x60cb,0x4369,
0x5e44,0x3866,0xf59d,0xc34f,
};
#endif
#ifdef MIEEE
static unsigned short AZC[44] = {
0x4160,0x9b9a,0xb598,0x566f,
0x41a5,0x0a8f,0xe357,0x37a7,
0x4218,0x4c17,0x2e3a,0xfe49,
0x425e,0xd6ba,0xed1e,0x7944,
0x42b4,0xa2a6,0xcb80,0x13d3,
0x42f2,0xdd8d,0xbf17,0xbe11,
0x4332,0x40ca,0xf2ac,0x905a,
0xc31c,0x27b2,0xa21c,0xcaff,
0xc376,0x0b35,0x7b05,0x4649,
0x4371,0x624d,0x4440,0x01c9,
0x4374,0x942b,0x882f,0xdcd6,
};
static unsigned short BZC[40] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0xc15e,0x3c7b,0x86c2,0xc36a,
0xc1a3,0x22fc,0x63dd,0xa7b8,
0xc216,0x227a,0x0c46,0x37a0,
0xc25b,0xf551,0xce17,0x9d22,
0xc2b2,0xe6b5,0x75d1,0x3955,
0xc2f0,0xd476,0xd4ff,0x8884,
0xc331,0x46dd,0x554d,0x96ab,
0x4332,0xfe10,0x323f,0xae8b,
0x4369,0x60cb,0x75cb,0x5498,
0xc34f,0xf59d,0x3866,0x5e44,
};
#endif

/* (1-x) (zeta(x) - 1), 0 <= x <= 1 */

#ifdef UNK
static double RZC[6] = {
-3.28717474506562731748E-1,
 1.55162528742623950834E1,
-2.48762831680821954401E2,
 1.01050368053237678329E3,
 1.26726061410235149405E4,
-1.11578094770515181334E5,
};
static double SZC[5] = {
/* 1.00000000000000000000E0,*/
 1.95107674914060531512E1,
 3.17710311750646984099E2,
 3.03835500874445748734E3,
 2.03665876435770579345E4,
 7.43853965136767874343E4,
};
#endif
#ifdef DEC
static unsigned short RZC[24] = {
0137650,0046650,0022502,0040316,
0041170,0041222,0057666,0142216,
0142170,0141510,0167741,0075646,
0042574,0120074,0046505,0106053,
0043506,0001154,0130073,0101413,
0144331,0166414,0020560,0131652,
};
static unsigned short SZC[20] = {
/*0040200,0000000,0000000,0000000,*/
0041234,0013015,0042073,0113570,
0042236,0155353,0077325,0077445,
0043075,0162656,0016646,0031723,
0043637,0016454,0157636,0071126,
0044221,0044262,0140365,0146434,
};
#endif
#ifdef IBMPC
static unsigned short RZC[24] = {
0x481a,0x04a8,0x09b5,0xbfd5,
0xd892,0x4bf6,0x0852,0x402f,
0x2f75,0x1dfc,0x1869,0xc06f,
0xb185,0x89a8,0x9407,0x408f,
0x7061,0x9607,0xc04d,0x40c8,
0x1675,0x842e,0x3da1,0xc0fb,
};
static unsigned short SZC[20] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x72ef,0xa887,0x82c1,0x4033,
0xafe5,0x6fda,0xdb5d,0x4073,
0xc67a,0xc3b4,0xbcb5,0x40a7,
0xce4b,0x9bf3,0xe3a5,0x40d3,
0xb9a3,0x581e,0x2916,0x40f2,
};
#endif
#ifdef MIEEE
static unsigned short RZC[24] = {
0xbfd5,0x09b5,0x04a8,0x481a,
0x402f,0x0852,0x4bf6,0xd892,
0xc06f,0x1869,0x1dfc,0x2f75,
0x408f,0x9407,0x89a8,0xb185,
0x40c8,0xc04d,0x9607,0x7061,
0xc0fb,0x3da1,0x842e,0x1675,
};
static unsigned short SZC[20] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4033,0x82c1,0xa887,0x72ef,
0x4073,0xdb5d,0x6fda,0xafe5,
0x40a7,0xbcb5,0xc3b4,0xc67a,
0x40d3,0xe3a5,0x9bf3,0xce4b,
0x40f2,0x2916,0x581e,0xb9a3,
};
#endif

#define MAXL2 127

/*
 * Riemann zeta function, minus one
 */
double zetac(double x)
{
int i;
double a, b, s, w;

if( x < 0.0 )
	{
#ifdef DEC
	if( x < -30.8148 )
#else
	if( x < -170.6243 )
#endif
		{
		mtherr( "zetac", OVERFLOW );
		return(0.0);
		}
	s = 1.0 - x;
	w = zetac( s );
	b = sin(0.5*PI*x) * pow(2.0*PI, x) * cephesgamma(s) * (1.0 + w) / PI;
	return(b - 1.0);
	}

if( x >= MAXL2 )
	return(0.0);	/* because first term is 2**-x */

/* Tabulated values for integer argument */
w = floor(x);
if( w == x )
	{
	i = x;
	if( i < 31 )
		{
#ifdef UNK
		return( azetac[i] );
#else
		return( *(double *)&azetac[4*i]  );
#endif
		}
	}


if( x < 1.0 )
	{
	w = 1.0 - x;
	a = polevl( x, RZC, 5 ) / ( w * p1evl( x, SZC, 5 ));
	return( a );
	}

if( x == 1.0 )
	{
	mtherr( "zetac", SING );
	return( MAXNUM );
	}

if( x <= 10.0 )
	{
	b = pow( 2.0, x ) * (x - 1.0);
	w = 1.0/x;
	s = (x * polevl( w, PZC, 8 )) / (b * p1evl( w, QZC, 8 ));
	return( s );
	}

if( x <= 50.0 )
	{
	b = pow( 2.0, -x );
	w = polevl( x, AZC, 10 ) / p1evl( x, BZC, 10 );
	w = exp(w) + b;
	return(w);
	}


/* Basic sum of inverse powers */


s = 0.0;
a = 1.0;
do
	{
	a += 2.0;
	b = pow( a, -x );
	s += b;
	}
while( b/s > MACHEP );

b = pow( 2.0, -x );
s = (s + b)/(1.0-b);
return(s);
}

/* ========================================================================= */

/*							struve.c
 *
 *      Struve function
 *
 *
 *
 * SYNOPSIS:
 *
 * double v, x, y, struve();
 *
 * y = struve( v, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Computes the Struve function Hv(x) of order v, argument x.
 * Negative x is rejected unless v is an integer.
 *
 * This module also contains the hypergeometric functions 1F2
 * and 3F0 and a routine for the Bessel function Yv(x) with
 * noninteger v.
 *
 *
 *
 * ACCURACY:
 *
 * Not accurately characterized, but spot checked against tables.
 *
 */

static double stop = 1.37e-17;

double onef2(double a, double b, double c, double x, double* err)
{
double n, a0, sum, t;
double an, bn, cn, max, z;

an = a;
bn = b;
cn = c;
a0 = 1.0;
sum = 1.0;
n = 1.0;
t = 1.0;
max = 0.0;

do
	{
	if( an == 0 )
		goto done;
	if( bn == 0 )
		goto error;
	if( cn == 0 )
		goto error;
	if( (a0 > 1.0e34) || (n > 200) )
		goto error;
	a0 *= (an * x) / (bn * cn * n);
	sum += a0;
	an += 1.0;
	bn += 1.0;
	cn += 1.0;
	n += 1.0;
	z = fabs( a0 );
	if( z > max )
		max = z;
	if( sum != 0 )
		t = fabs( a0 / sum );
	else
		t = z;
	}
while( t > stop );

done:

*err = fabs( MACHEP*max /sum );

#if DEBUG
	printf(" onef2 cancellation error %.5E\n", *err );
#endif

goto xit;

error:
#if DEBUG
printf("onef2 does not converge\n");
#endif
*err = 1.0e38;

xit:

#if DEBUG
printf("onef2( %.2E %.2E %.2E %.5E ) =  %.3E  %.6E\n", a, b, c, x, n, sum);
#endif
return(sum);
}




double threef0(double a, double b, double c, double x, double* err)
{
double n, a0, sum, t, conv, conv1;
double an, bn, cn, max, z;

an = a;
bn = b;
cn = c;
a0 = 1.0;
sum = 1.0;
n = 1.0;
t = 1.0;
max = 0.0;
conv = 1.0e38;
conv1 = conv;

do
	{
	if( an == 0.0 )
		goto done;
	if( bn == 0.0 )
		goto done;
	if( cn == 0.0 )
		goto done;
	if( (a0 > 1.0e34) || (n > 200) )
		goto error;
	a0 *= (an * bn * cn * x) / n;
	an += 1.0;
	bn += 1.0;
	cn += 1.0;
	n += 1.0;
	z = fabs( a0 );
	if( z > max )
		max = z;
	if( z >= conv )
		{
		if( (z < max) && (z > conv1) )
			goto done;
		}
	conv1 = conv;
	conv = z;
	sum += a0;
	if( sum != 0 )
		t = fabs( a0 / sum );
	else
		t = z;
	}
while( t > stop );

done:

t = fabs( MACHEP*max/sum );
#if DEBUG
	printf(" threef0 cancellation error %.5E\n", t );
#endif

max = fabs( conv/sum );
if( max > t )
	t = max;
#if DEBUG
	printf(" threef0 convergence %.5E\n", max );
#endif

goto xit;

error:
#if DEBUG
printf("threef0 does not converge\n");
#endif
t = 1.0e38;

xit:

#if DEBUG
printf("threef0( %.2E %.2E %.2E %.5E ) =  %.3E  %.6E\n", a, b, c, x, n, sum);
#endif

*err = t;
return(sum);
}





double struve(double v, double x)
{
double y, ya, f, g, h, t;
double onef2err, threef0err;

f = floor(v);
if( (v < 0) && ( v-f == 0.5 ) )
	{
	y = jv( -v, x );
	f = 1.0 - f;
	g =  2.0 * floor(f/2.0);
	if( g != f )
		y = -y;
	return(y);
	}
t = 0.25*x*x;
f = fabs(x);
g = 1.5 * fabs(v);
if( (f > 30.0) && (f > g) )
	{
	onef2err = 1.0e38;
	y = 0.0;
	}
else
	{
	y = onef2( 1.0, 1.5, 1.5+v, -t, &onef2err );
	}

if( (f < 18.0) || (x < 0.0) )
	{
	threef0err = 1.0e38;
	ya = 0.0;
	}
else
	{
	ya = threef0( 1.0, 0.5, 0.5-v, -1.0/t, &threef0err );
	}

f = sqrt( PI );
h = pow( 0.5*x, v-1.0 );

if( onef2err <= threef0err )
	{
	g = cephesgamma( v + 1.5 );
	y = y * h * t / ( 0.5 * f * g );
	return(y);
	}
else
	{
	g = cephesgamma( v + 0.5 );
	ya = ya * h / ( f * g );
	ya = ya + yv( v, x );
	return(ya);
	}
}




/* Bessel function of noninteger order
 */

double yv(double v, double x)
{
double y, t;
int n;

y = floor( v );
if( y == v )
	{
	n = v;
	y = yn( n, x );
	return( y );
	}
t = PI * v;
y = (cos(t) * jv( v, x ) - jv( -v, x ))/sin(t);
return( y );
}

/* Crossover points between ascending series and asymptotic series
 * for Struve function
 *
 *	 v	 x
 * 
 *	 0	19.2
 *	 1	18.95
 *	 2	19.15
 *	 3	19.3
 *	 5	19.7
 *	10	21.35
 *	20	26.35
 *	30	32.31
 *	40	40.0
 */

/* ========================================================================= */

/*							ellpe.c
 *
 *	Complete elliptic integral of the second kind
 *
 *
 *
 * SYNOPSIS:
 *
 * double m1, y, ellpe();
 *
 * y = ellpe( m1 );
 *
 *
 *
 * DESCRIPTION:
 *
 * Approximates the integral
 *
 *
 *            pi/2
 *             -
 *            | |                 2
 * E(m)  =    |    sqrt( 1 - m sin t ) dt
 *          | |    
 *           -
 *            0
 *
 * Where m = 1 - m1, using the approximation
 *
 *      P(x)  -  x log x Q(x).
 *
 * Though there are no singularities, the argument m1 is used
 * rather than m for compatibility with ellpk().
 *
 * E(1) = 1; E(0) = pi/2.
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC        0, 1       13000       3.1e-17     9.4e-18
 *    IEEE       0, 1       10000       2.1e-16     7.3e-17
 *
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * ellpe domain      x<0, x>1            0.0
 *
 */

/*							ellpe.c		*/

/* Elliptic integral of second kind */


#ifdef UNK
static double PE[] = {
  1.53552577301013293365E-4,
  2.50888492163602060990E-3,
  8.68786816565889628429E-3,
  1.07350949056076193403E-2,
  7.77395492516787092951E-3,
  7.58395289413514708519E-3,
  1.15688436810574127319E-2,
  2.18317996015557253103E-2,
  5.68051945617860553470E-2,
  4.43147180560990850618E-1,
  1.00000000000000000299E0
};
static double QE[] = {
  3.27954898576485872656E-5,
  1.00962792679356715133E-3,
  6.50609489976927491433E-3,
  1.68862163993311317300E-2,
  2.61769742454493659583E-2,
  3.34833904888224918614E-2,
  4.27180926518931511717E-2,
  5.85936634471101055642E-2,
  9.37499997197644278445E-2,
  2.49999999999888314361E-1
};
#endif

#ifdef DEC
static unsigned short PE[] = {
0035041,0001364,0141572,0117555,
0036044,0066032,0130027,0033404,
0036416,0053617,0064456,0102632,
0036457,0161100,0061177,0122612,
0036376,0136251,0012403,0124162,
0036370,0101316,0151715,0131613,
0036475,0105477,0050317,0133272,
0036662,0154232,0024645,0171552,
0037150,0126220,0047054,0030064,
0037742,0162057,0167645,0165612,
0040200,0000000,0000000,0000000
};
static unsigned short QE[] = {
0034411,0106743,0115771,0055462,
0035604,0052575,0155171,0045540,
0036325,0030424,0064332,0167756,
0036612,0052366,0063006,0115175,
0036726,0070430,0004533,0124654,
0037011,0022741,0030675,0030711,
0037056,0174452,0127062,0132122,
0037157,0177750,0142041,0072523,
0037277,0177777,0173137,0002627,
0037577,0177777,0177777,0101101
};
#endif

#ifdef IBMPC
static unsigned short PE[] = {
0x53ee,0x986f,0x205e,0x3f24,
0xe6e0,0x5602,0x8d83,0x3f64,
0xd0b3,0xed25,0xcaf1,0x3f81,
0xf4b1,0x0c4f,0xfc48,0x3f85,
0x750e,0x22a0,0xd795,0x3f7f,
0xb671,0xda79,0x1059,0x3f7f,
0xf6d7,0xea19,0xb167,0x3f87,
0xbe6d,0x4534,0x5b13,0x3f96,
0x8607,0x09c5,0x1592,0x3fad,
0xbd71,0xfdf4,0x5c85,0x3fdc,
0x0000,0x0000,0x0000,0x3ff0
};
static unsigned short QE[] = {
0x2b66,0x737f,0x31bc,0x3f01,
0x296c,0xbb4f,0x8aaf,0x3f50,
0x5dfe,0x8d1b,0xa622,0x3f7a,
0xd350,0xccc0,0x4a9e,0x3f91,
0x7535,0x012b,0xce23,0x3f9a,
0xa639,0x2637,0x24bc,0x3fa1,
0x568a,0x55c6,0xdf25,0x3fa5,
0x2eaa,0x1884,0xfffd,0x3fad,
0xe0b3,0xfecb,0xffff,0x3fb7,
0xf048,0xffff,0xffff,0x3fcf
};
#endif

#ifdef MIEEE
static unsigned short PE[] = {
0x3f24,0x205e,0x986f,0x53ee,
0x3f64,0x8d83,0x5602,0xe6e0,
0x3f81,0xcaf1,0xed25,0xd0b3,
0x3f85,0xfc48,0x0c4f,0xf4b1,
0x3f7f,0xd795,0x22a0,0x750e,
0x3f7f,0x1059,0xda79,0xb671,
0x3f87,0xb167,0xea19,0xf6d7,
0x3f96,0x5b13,0x4534,0xbe6d,
0x3fad,0x1592,0x09c5,0x8607,
0x3fdc,0x5c85,0xfdf4,0xbd71,
0x3ff0,0x0000,0x0000,0x0000
};
static unsigned short QE[] = {
0x3f01,0x31bc,0x737f,0x2b66,
0x3f50,0x8aaf,0xbb4f,0x296c,
0x3f7a,0xa622,0x8d1b,0x5dfe,
0x3f91,0x4a9e,0xccc0,0xd350,
0x3f9a,0xce23,0x012b,0x7535,
0x3fa1,0x24bc,0x2637,0xa639,
0x3fa5,0xdf25,0x55c6,0x568a,
0x3fad,0xfffd,0x1884,0x2eaa,
0x3fb7,0xffff,0xfecb,0xe0b3,
0x3fcf,0xffff,0xffff,0xf048
};
#endif


double ellpe(double x)
{

if( (x <= 0.0) || (x > 1.0) )
	{
	if( x == 0.0 )
		return( 1.0 );
	mtherr( "ellpe", DOMAIN );
	return( 0.0 );
	}
return( polevl(x,PE,10) - log(x) * (x * polevl(x,QE,9)) );
}

/* ========================================================================= */

/*							ellie.c
 *
 *	Incomplete elliptic integral of the second kind
 *
 *
 *
 * SYNOPSIS:
 *
 * double phi, m, y, ellie();
 *
 * y = ellie( phi, m );
 *
 *
 *
 * DESCRIPTION:
 *
 * Approximates the integral
 *
 *
 *                phi
 *                 -
 *                | |
 *                |                   2
 * E(phi_\m)  =    |    sqrt( 1 - m sin t ) dt
 *                |
 *              | |    
 *               -
 *                0
 *
 * of amplitude phi and modulus m, using the arithmetic -
 * geometric mean algorithm.
 *
 *
 *
 * ACCURACY:
 *
 * Tested at random arguments with phi in [-10, 10] and m in
 * [0, 1].
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC        0,2         2000       1.9e-16     3.4e-17
 *    IEEE     -10,10      150000       3.3e-15     1.4e-16
 *
 *
 */



/*	Incomplete elliptic integral of second kind	*/

double ellie(double phi, double m)
{
double a, b, c, e, temp;
double lphi, t, E;
int d, mod, npio2, sign;

if( m == 0.0 )
	return( phi );
lphi = phi;
npio2 = floor( lphi/PIO2 );
if( npio2 & 1 )
	npio2 += 1;
lphi = lphi - npio2 * PIO2;
if( lphi < 0.0 )
	{
	lphi = -lphi;
	sign = -1;
	}
else
	{
	sign = 1;
	}
a = 1.0 - m;
E = ellpe( a );
if( a == 0.0 )
	{
	temp = sin( lphi );
	goto done;
	}
t = tan( lphi );
b = sqrt(a);
/* Thanks to Brian Fitzgerald <fitzgb@mml0.meche.rpi.edu>
   for pointing out an instability near odd multiples of pi/2.  */
if( fabs(t) > 10.0 )
	{
	/* Transform the amplitude */
	e = 1.0/(b*t);
	/* ... but avoid multiple recursions.  */
	if( fabs(e) < 10.0 )
		{
		e = atan(e);
		temp = E + m * sin( lphi ) * sin( e ) - ellie( e, m );
		goto done;
		}
	}
c = sqrt(m);
a = 1.0;
d = 1;
e = 0.0;
mod = 0;

while( fabs(c/a) > MACHEP )
	{
	temp = b/a;
	lphi = lphi + atan(t*temp) + mod * PI;
	mod = (lphi + PIO2)/PI;
	t = t * ( 1.0 + temp )/( 1.0 - temp * t * t );
	c = ( a - b )/2.0;
	temp = sqrt( a * b );
	a = ( a + b )/2.0;
	b = temp;
	d += d;
	e += c * sin(lphi);
	}

temp = E / ellpk( 1.0 - m );
temp *= (atan(t) + mod * PI)/(d * a);
temp += e;

done:

if( sign < 0 )
	temp = -temp;
temp += npio2 * E;
return( temp );
}

/* ========================================================================= */

/*							ellpk.c
 *
 *	Complete elliptic integral of the first kind
 *
 *
 *
 * SYNOPSIS:
 *
 * double m1, y, ellpk();
 *
 * y = ellpk( m1 );
 *
 *
 *
 * DESCRIPTION:
 *
 * Approximates the integral
 *
 *
 *
 *            pi/2
 *             -
 *            | |
 *            |           dt
 * K(m)  =    |    ------------------
 *            |                   2
 *          | |    sqrt( 1 - m sin t )
 *           -
 *            0
 *
 * where m = 1 - m1, using the approximation
 *
 *     P(x)  -  log x Q(x).
 *
 * The argument m1 is used rather than m so that the logarithmic
 * singularity at m = 1 will be shifted to the origin; this
 * preserves maximum accuracy.
 *
 * K(0) = pi/2.
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC        0,1        16000       3.5e-17     1.1e-17
 *    IEEE       0,1        30000       2.5e-16     6.8e-17
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * ellpk domain       x<0, x>1           0.0
 *
 */

/*							ellpk.c */


#ifdef DEC
static unsigned short PK[] =
{
0035020,0127576,0040430,0051544,
0036025,0070136,0042703,0153716,
0036402,0122614,0062555,0077777,
0036441,0102130,0072334,0025172,
0036341,0043320,0117242,0172076,
0036312,0146456,0077242,0154141,
0036420,0003467,0013727,0035407,
0036564,0137263,0110651,0020237,
0036775,0001330,0144056,0020305,
0037305,0144137,0157521,0141734,
0040261,0071027,0173721,0147572
};
static unsigned short QK[] =
{
0034366,0130371,0103453,0077633,
0035557,0122745,0173515,0113016,
0036302,0124470,0167304,0074473,
0036575,0132403,0117226,0117576,
0036703,0156271,0047124,0147733,
0036766,0137465,0002053,0157312,
0037031,0014423,0154274,0176515,
0037107,0177747,0143216,0016145,
0037217,0177777,0172621,0074000,
0037377,0177777,0177776,0156435,
0040000,0000000,0000000,0000000
};
static unsigned short ac1[] = {0040261,0071027,0173721,0147572};
#define C1 (*(double *)ac1)
#endif

#ifdef IBMPC
static unsigned short PK[] =
{
0x0a6d,0xc823,0x15ef,0x3f22,
0x7afa,0xc8b8,0xae0b,0x3f62,
0xb000,0x8cad,0x54b1,0x3f80,
0x854f,0x0e9b,0x308b,0x3f84,
0x5e88,0x13d4,0x28da,0x3f7c,
0x5b0c,0xcfd4,0x59a5,0x3f79,
0xe761,0xe2fa,0x00e6,0x3f82,
0x2414,0x7235,0x97d6,0x3f8e,
0xc419,0x1905,0xa05b,0x3f9f,
0x387c,0xfbea,0xb90b,0x3fb8,
0x39ef,0xfefa,0x2e42,0x3ff6
};
static unsigned short QK[] =
{
0x6ff3,0x30e5,0xd61f,0x3efe,
0xb2c2,0xbee9,0xf4bc,0x3f4d,
0x8f27,0x1dd8,0x5527,0x3f78,
0xd3f0,0x73d2,0xb6a0,0x3f8f,
0x99fb,0x29ca,0x7b97,0x3f98,
0x7bd9,0xa085,0xd7e6,0x3f9e,
0x9faa,0x7b17,0x2322,0x3fa3,
0xc38d,0xf8d1,0xfffc,0x3fa8,
0x2f00,0xfeb2,0xffff,0x3fb1,
0xdba4,0xffff,0xffff,0x3fbf,
0x0000,0x0000,0x0000,0x3fe0
};
static unsigned short ac1[] = {0x39ef,0xfefa,0x2e42,0x3ff6};
#define C1 (*(double *)ac1)
#endif

#ifdef MIEEE
static unsigned short PK[] =
{
0x3f22,0x15ef,0xc823,0x0a6d,
0x3f62,0xae0b,0xc8b8,0x7afa,
0x3f80,0x54b1,0x8cad,0xb000,
0x3f84,0x308b,0x0e9b,0x854f,
0x3f7c,0x28da,0x13d4,0x5e88,
0x3f79,0x59a5,0xcfd4,0x5b0c,
0x3f82,0x00e6,0xe2fa,0xe761,
0x3f8e,0x97d6,0x7235,0x2414,
0x3f9f,0xa05b,0x1905,0xc419,
0x3fb8,0xb90b,0xfbea,0x387c,
0x3ff6,0x2e42,0xfefa,0x39ef
};
static unsigned short QK[] =
{
0x3efe,0xd61f,0x30e5,0x6ff3,
0x3f4d,0xf4bc,0xbee9,0xb2c2,
0x3f78,0x5527,0x1dd8,0x8f27,
0x3f8f,0xb6a0,0x73d2,0xd3f0,
0x3f98,0x7b97,0x29ca,0x99fb,
0x3f9e,0xd7e6,0xa085,0x7bd9,
0x3fa3,0x2322,0x7b17,0x9faa,
0x3fa8,0xfffc,0xf8d1,0xc38d,
0x3fb1,0xffff,0xfeb2,0x2f00,
0x3fbf,0xffff,0xffff,0xdba4,
0x3fe0,0x0000,0x0000,0x0000
};
static unsigned short ac1[] = {
0x3ff6,0x2e42,0xfefa,0x39ef
};
#define C1 (*(double *)ac1)
#endif

#ifdef UNK
static double PK[] =
{
 1.37982864606273237150E-4,
 2.28025724005875567385E-3,
 7.97404013220415179367E-3,
 9.85821379021226008714E-3,
 6.87489687449949877925E-3,
 6.18901033637687613229E-3,
 8.79078273952743772254E-3,
 1.49380448916805252718E-2,
 3.08851465246711995998E-2,
 9.65735902811690126535E-2,
 1.38629436111989062502E0
};

static double QK[] =
{
 2.94078955048598507511E-5,
 9.14184723865917226571E-4,
 5.94058303753167793257E-3,
 1.54850516649762399335E-2,
 2.39089602715924892727E-2,
 3.01204715227604046988E-2,
 3.73774314173823228969E-2,
 4.88280347570998239232E-2,
 7.03124996963957469739E-2,
 1.24999999999870820058E-1,
 4.99999999999999999821E-1
};
static double C1 = 1.3862943611198906188E0; /* log(4) */
#endif


double ellpk(double x)
{

if( (x < 0.0) || (x > 1.0) )
	{
	mtherr( "ellpk", DOMAIN );
	return( 0.0 );
	}

if( x > MACHEP )
	{
	return( polevl(x,PK,10) - log(x) * polevl(x,QK,10) );
	}
else
	{
	if( x == 0.0 )
		{
		mtherr( "ellpk", SING );
		return( MAXNUM );
		}
	else
		{
		return( C1 - 0.5 * log(x) );
		}
	}
}

/* ========================================================================= */

/*							ellik.c
 *
 *	Incomplete elliptic integral of the first kind
 *
 *
 *
 * SYNOPSIS:
 *
 * double phi, m, y, ellik();
 *
 * y = ellik( phi, m );
 *
 *
 *
 * DESCRIPTION:
 *
 * Approximates the integral
 *
 *
 *
 *                phi
 *                 -
 *                | |
 *                |           dt
 * F(phi_\m)  =    |    ------------------
 *                |                   2
 *              | |    sqrt( 1 - m sin t )
 *               -
 *                0
 *
 * of amplitude phi and modulus m, using the arithmetic -
 * geometric mean algorithm.
 *
 *
 *
 *
 * ACCURACY:
 *
 * Tested at random points with m in [0, 1] and phi as indicated.
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE     -10,10       200000      7.4e-16     1.0e-16
 *
 *
 */


/*	Incomplete elliptic integral of first kind	*/


double ellik(double phi, double m)
{
double a, b, c, e, temp, t, K;
int d, mod, sign, npio2;

if( m == 0.0 )
	return( phi );
a = 1.0 - m;
if( a == 0.0 )
	{
	if( fabs(phi) >= PIO2 )
		{
		mtherr( "ellik", SING );
		return( MAXNUM );
		}
	return(  log(  tan( (PIO2 + phi)/2.0 )  )   );
	}
npio2 = floor( phi/PIO2 );
if( npio2 & 1 )
	npio2 += 1;
if( npio2 )
	{
	K = ellpk( a );
	phi = phi - npio2 * PIO2;
	}
else
	K = 0.0;
if( phi < 0.0 )
	{
	phi = -phi;
	sign = -1;
	}
else
	sign = 0;
b = sqrt(a);
t = tan( phi );
if( fabs(t) > 10.0 )
	{
	/* Transform the amplitude */
	e = 1.0/(b*t);
	/* ... but avoid multiple recursions.  */
	if( fabs(e) < 10.0 )
		{
		e = atan(e);
		if( npio2 == 0 )
			K = ellpk( a );
		temp = K - ellik( e, m );
		goto done;
		}
	}
a = 1.0;
c = sqrt(m);
d = 1;
mod = 0;

while( fabs(c/a) > MACHEP )
	{
	temp = b/a;
	phi = phi + atan(t*temp) + mod * PI;
	mod = (phi + PIO2)/PI;
	t = t * ( 1.0 + temp )/( 1.0 - temp * t * t );
	c = ( a - b )/2.0;
	temp = sqrt( a * b );
	a = ( a + b )/2.0;
	b = temp;
	d += d;
	}

temp = (atan(t) + mod * PI)/(d * a);

done:
if( sign < 0 )
	temp = -temp;
temp += npio2 * K;
return( temp );
}

/* ========================================================================= */

/*							ellpj.c
 *
 *	Jacobian Elliptic Functions
 *
 *
 *
 * SYNOPSIS:
 *
 * double u, m, sn, cn, dn, phi;
 * int ellpj();
 *
 * ellpj( u, m, _&sn, _&cn, _&dn, _&phi );
 *
 *
 *
 * DESCRIPTION:
 *
 *
 * Evaluates the Jacobian elliptic functions sn(u|m), cn(u|m),
 * and dn(u|m) of parameter m between 0 and 1, and real
 * argument u.
 *
 * These functions are periodic, with quarter-period on the
 * real axis equal to the complete elliptic integral
 * ellpk(1.0-m).
 *
 * Relation to incomplete elliptic integral:
 * If u = ellik(phi,m), then sn(u|m) = sin(phi),
 * and cn(u|m) = cos(phi).  Phi is called the amplitude of u.
 *
 * Computation is by means of the arithmetic-geometric mean
 * algorithm, except when m is within 1e-9 of 0 or 1.  In the
 * latter case with m close to 1, the approximation applies
 * only for phi < pi/2.
 *
 * ACCURACY:
 *
 * Tested at random points with u between 0 and 10, m between
 * 0 and 1.
 *
 *            Absolute error (* = relative error):
 * arithmetic   function   # trials      peak         rms
 *    DEC       sn           1800       4.5e-16     8.7e-17
 *    IEEE      phi         10000       9.2e-16*    1.4e-16*
 *    IEEE      sn          50000       4.1e-15     4.6e-16
 *    IEEE      cn          40000       3.6e-15     4.4e-16
 *    IEEE      dn          10000       1.3e-12     1.8e-14
 *
 *  Peak error observed in consistency check using addition
 * theorem for sn(u+v) was 4e-16 (absolute).  Also tested by
 * the above relation to the incomplete elliptic integral.
 * Accuracy deteriorates when u is large.
 *
 */

/*							ellpj.c		*/



int ellpj(double u, double m, double* sn, double* cn, double* dn, double* ph)
{
double ai, b, phi, t, twon;
double a[9], c[9];
int i;


/* Check for special cases */

if( m < 0.0 || m > 1.0 )
	{
	mtherr( "ellpj", DOMAIN );
	*sn = 0.0;
	*cn = 0.0;
	*ph = 0.0;
	*dn = 0.0;
	return(-1);
	}
if( m < 1.0e-9 )
	{
	t = sin(u);
	b = cos(u);
	ai = 0.25 * m * (u - t*b);
	*sn = t - ai*b;
	*cn = b + ai*t;
	*ph = u - ai;
	*dn = 1.0 - 0.5*m*t*t;
	return(0);
	}

if( m >= 0.9999999999 )
	{
	ai = 0.25 * (1.0-m);
	b = cosh(u);
	t = tanh(u);
	phi = 1.0/b;
	twon = b * sinh(u);
	*sn = t + ai * (twon - u)/(b*b);
	*ph = 2.0*atan(exp(u)) - PIO2 + ai*(twon - u)/b;
	ai *= t * phi;
	*cn = phi - ai * (twon - u);
	*dn = phi + ai * (twon + u);
	return(0);
	}


/*	A. G. M. scale		*/
a[0] = 1.0;
b = sqrt(1.0 - m);
c[0] = sqrt(m);
twon = 1.0;
i = 0;

while( fabs(c[i]/a[i]) > MACHEP )
	{
	if( i > 7 )
		{
		mtherr( "ellpj", OVERFLOW );
		goto done;
		}
	ai = a[i];
	++i;
	c[i] = ( ai - b )/2.0;
	t = sqrt( ai * b );
	a[i] = ( ai + b )/2.0;
	b = t;
	twon *= 2.0;
	}

done:

/* backward recurrence */
phi = twon * a[i] * u;
do
	{
	t = c[i] * sin(phi) / a[i];
	b = phi;
	phi = (asin(t) + phi)/2.0;
	}
while( --i );

*sn = sin(phi);
t = cos(phi);
*cn = t;
*dn = t/cos(phi-b);
*ph = phi;
return(0);
}



/* ========================================================================= */

/*							ndtr.c
 *
 *	Normal distribution function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, ndtr();
 *
 * y = ndtr( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the area under the Gaussian probability density
 * function, integrated from minus infinity to x:
 *
 *                            x
 *                             -
 *                   1        | |          2
 *    ndtr(x)  = ---------    |    exp( - t /2 ) dt
 *               sqrt(2pi)  | |
 *                           -
 *                          -inf.
 *
 *             =  ( 1 + erf(z) ) / 2
 *             =  erfc(z) / 2
 *
 * where z = x/sqrt(2). Computation is via the functions
 * erf and erfc with care to avoid error amplification in computing exp(-x^2).
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE     -13,0        30000       1.3e-15     2.2e-16
 *
 *
 * ERROR MESSAGES:
 *
 *   message         condition         value returned
 * erfc underflow    x > 37.519379347       0.0
 *
 */
/*							erf.c
 *
 *	Error function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, erf();
 *
 * y = erf( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * The integral is
 *
 *                           x 
 *                            -
 *                 2         | |          2
 *   erf(x)  =  --------     |    exp( - t  ) dt.
 *              sqrt(pi)   | |
 *                          -
 *                           0
 *
 * The magnitude of x is limited to 9.231948545 for DEC
 * arithmetic; 1 or -1 is returned outside this range.
 *
 * For 0 <= |x| < 1, erf(x) = x * P4(x**2)/Q5(x**2); otherwise
 * erf(x) = 1 - erfc(x).
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0,1         14000       4.7e-17     1.5e-17
 *    IEEE      0,1         30000       3.7e-16     1.0e-16
 *
 */
/*							erfc.c
 *
 *	Complementary error function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, erfc();
 *
 * y = erfc( x );
 *
 *
 *
 * DESCRIPTION:
 *
 *
 *  1 - erf(x) =
 *
 *                           inf. 
 *                             -
 *                  2         | |          2
 *   erfc(x)  =  --------     |    exp( - t  ) dt
 *               sqrt(pi)   | |
 *                           -
 *                            x
 *
 *
 * For small x, erfc(x) = 1 - erf(x); otherwise rational
 * approximations are computed.
 *
 * A special function expx2.c is used to suppress error amplification
 * in computing exp(-x^2).
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0,26.6417   30000       1.3e-15     2.2e-16
 *
 *
 * ERROR MESSAGES:
 *
 *   message         condition              value returned
 * erfc underflow    x > 9.231948545 (DEC)       0.0
 *
 *
 */




/* Define this macro to suppress error propagation in exp(x^2)
   by using the expx2 function.  The tradeoff is that doing so
   generates two calls to the exponential function instead of one.  */
#define USE_EXPXSQ 1

#ifdef UNK
static double PERF[] = {
 2.46196981473530512524E-10,
 5.64189564831068821977E-1,
 7.46321056442269912687E0,
 4.86371970985681366614E1,
 1.96520832956077098242E2,
 5.26445194995477358631E2,
 9.34528527171957607540E2,
 1.02755188689515710272E3,
 5.57535335369399327526E2
};
static double QERF[] = {
/* 1.00000000000000000000E0,*/
 1.32281951154744992508E1,
 8.67072140885989742329E1,
 3.54937778887819891062E2,
 9.75708501743205489753E2,
 1.82390916687909736289E3,
 2.24633760818710981792E3,
 1.65666309194161350182E3,
 5.57535340817727675546E2
};
static double RERF[] = {
 5.64189583547755073984E-1,
 1.27536670759978104416E0,
 5.01905042251180477414E0,
 6.16021097993053585195E0,
 7.40974269950448939160E0,
 2.97886665372100240670E0
};
static double SERF[] = {
/* 1.00000000000000000000E0,*/
 2.26052863220117276590E0,
 9.39603524938001434673E0,
 1.20489539808096656605E1,
 1.70814450747565897222E1,
 9.60896809063285878198E0,
 3.36907645100081516050E0
};
#ifndef HAVE_ERF
static double T[] = {
 9.60497373987051638749E0,
 9.00260197203842689217E1,
 2.23200534594684319226E3,
 7.00332514112805075473E3,
 5.55923013010394962768E4
};
static double U[] = {
/* 1.00000000000000000000E0,*/
 3.35617141647503099647E1,
 5.21357949780152679795E2,
 4.59432382970980127987E3,
 2.26290000613890934246E4,
 4.92673942608635921086E4
};
#endif

#define UTHRESH 37.519379347
#endif

#ifdef DEC
static unsigned short PERF[] = {
0030207,0054445,0011173,0021706,
0040020,0067272,0030661,0122075,
0040756,0151236,0173053,0067042,
0041502,0106175,0062555,0151457,
0042104,0102525,0047401,0003667,
0042403,0116176,0011446,0075303,
0042551,0120723,0061641,0123275,
0042600,0070651,0007264,0134516,
0042413,0061102,0167507,0176625
};
static unsigned short QERF[] = {
/*0040200,0000000,0000000,0000000,*/
0041123,0123257,0165741,0017142,
0041655,0065027,0173413,0115450,
0042261,0074011,0021573,0004150,
0042563,0166530,0013662,0007200,
0042743,0176427,0162443,0105214,
0043014,0062546,0153727,0123772,
0042717,0012470,0006227,0067424,
0042413,0061103,0003042,0013254
};
static unsigned short RERF[] = {
0040020,0067272,0101024,0155421,
0040243,0037467,0056706,0026462,
0040640,0116017,0120665,0034315,
0040705,0020162,0143350,0060137,
0040755,0016234,0134304,0130157,
0040476,0122700,0051070,0015473
};
static unsigned short SERF[] = {
/*0040200,0000000,0000000,0000000,*/
0040420,0126200,0044276,0070413,
0041026,0053051,0007302,0063746,
0041100,0144203,0174051,0061151,
0041210,0123314,0126343,0177646,
0041031,0137125,0051431,0033011,
0040527,0117362,0152661,0066201
};
#ifndef HAVE_ERF
static unsigned short T[] = {
0041031,0126770,0170672,0166101,
0041664,0006522,0072360,0031770,
0043013,0100025,0162641,0126671,
0043332,0155231,0161627,0076200,
0044131,0024115,0021020,0117343
};
static unsigned short U[] = {
/*0040200,0000000,0000000,0000000,*/
0041406,0037461,0177575,0032714,
0042402,0053350,0123061,0153557,
0043217,0111227,0032007,0164217,
0043660,0145000,0004013,0160114,
0044100,0071544,0167107,0125471
};
#endif
#define UTHRESH 14.0
#endif

#ifdef IBMPC
static unsigned short PERF[] = {
0x6479,0xa24f,0xeb24,0x3df0,
0x3488,0x4636,0x0dd7,0x3fe2,
0x6dc4,0xdec5,0xda53,0x401d,
0xba66,0xacad,0x518f,0x4048,
0x20f7,0xa9e0,0x90aa,0x4068,
0xcf58,0xc264,0x738f,0x4080,
0x34d8,0x6c74,0x343a,0x408d,
0x972a,0x21d6,0x0e35,0x4090,
0xffb3,0x5de8,0x6c48,0x4081
};
static unsigned short QERF[] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x23cc,0xfd7c,0x74d5,0x402a,
0x7365,0xfee1,0xad42,0x4055,
0x610d,0x246f,0x2f01,0x4076,
0x41d0,0x02f6,0x7dab,0x408e,
0x7151,0xfca4,0x7fa2,0x409c,
0xf4ff,0xdafa,0x8cac,0x40a1,
0xede2,0x0192,0xe2a7,0x4099,
0x42d6,0x60c4,0x6c48,0x4081
};
static unsigned short RERF[] = {
0x9b62,0x5042,0x0dd7,0x3fe2,
0xc5a6,0xebb8,0x67e6,0x3ff4,
0xa71a,0xf436,0x1381,0x4014,
0x0c0c,0x58dd,0xa40e,0x4018,
0x960e,0x9718,0xa393,0x401d,
0x0367,0x0a47,0xd4b8,0x4007
};
static unsigned short SERF[] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xce21,0x0917,0x1590,0x4002,
0x4cfd,0x21d8,0xcac5,0x4022,
0x2c4d,0x7f05,0x1910,0x4028,
0x7ff5,0x959c,0x14d9,0x4031,
0x26c1,0xaa63,0x37ca,0x4023,
0x2d90,0x5ab6,0xf3de,0x400a
};
#ifndef HAVE_ERF
static unsigned short T[] = {
0x5d88,0x1e37,0x35bf,0x4023,
0x067f,0x4e9e,0x81aa,0x4056,
0x35b7,0xbcb4,0x7002,0x40a1,
0xef90,0x3c72,0x5b53,0x40bb,
0x13dc,0xa442,0x2509,0x40eb
};
static unsigned short U[] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xa6ba,0x3fef,0xc7e6,0x4040,
0x3aee,0x14c6,0x4add,0x4080,
0xfd12,0xe680,0xf252,0x40b1,
0x7c0a,0x0101,0x1940,0x40d6,
0xf567,0x9dc8,0x0e6c,0x40e8
};
#endif
#define UTHRESH 37.519379347
#endif

#ifdef MIEEE
static unsigned short PERF[] = {
0x3df0,0xeb24,0xa24f,0x6479,
0x3fe2,0x0dd7,0x4636,0x3488,
0x401d,0xda53,0xdec5,0x6dc4,
0x4048,0x518f,0xacad,0xba66,
0x4068,0x90aa,0xa9e0,0x20f7,
0x4080,0x738f,0xc264,0xcf58,
0x408d,0x343a,0x6c74,0x34d8,
0x4090,0x0e35,0x21d6,0x972a,
0x4081,0x6c48,0x5de8,0xffb3
};
static unsigned short QERF[] = {
0x402a,0x74d5,0xfd7c,0x23cc,
0x4055,0xad42,0xfee1,0x7365,
0x4076,0x2f01,0x246f,0x610d,
0x408e,0x7dab,0x02f6,0x41d0,
0x409c,0x7fa2,0xfca4,0x7151,
0x40a1,0x8cac,0xdafa,0xf4ff,
0x4099,0xe2a7,0x0192,0xede2,
0x4081,0x6c48,0x60c4,0x42d6
};
static unsigned short RERF[] = {
0x3fe2,0x0dd7,0x5042,0x9b62,
0x3ff4,0x67e6,0xebb8,0xc5a6,
0x4014,0x1381,0xf436,0xa71a,
0x4018,0xa40e,0x58dd,0x0c0c,
0x401d,0xa393,0x9718,0x960e,
0x4007,0xd4b8,0x0a47,0x0367
};
static unsigned short SERF[] = {
0x4002,0x1590,0x0917,0xce21,
0x4022,0xcac5,0x21d8,0x4cfd,
0x4028,0x1910,0x7f05,0x2c4d,
0x4031,0x14d9,0x959c,0x7ff5,
0x4023,0x37ca,0xaa63,0x26c1,
0x400a,0xf3de,0x5ab6,0x2d90
};
#ifndef HAVE_ERF
static unsigned short T[] = {
0x4023,0x35bf,0x1e37,0x5d88,
0x4056,0x81aa,0x4e9e,0x067f,
0x40a1,0x7002,0xbcb4,0x35b7,
0x40bb,0x5b53,0x3c72,0xef90,
0x40eb,0x2509,0xa442,0x13dc
};
static unsigned short U[] = {
0x4040,0xc7e6,0x3fef,0xa6ba,
0x4080,0x4add,0x14c6,0x3aee,
0x40b1,0xf252,0xe680,0xfd12,
0x40d6,0x1940,0x0101,0x7c0a,
0x40e8,0x0e6c,0x9dc8,0xf567
};
#endif
#define UTHRESH 37.519379347
#endif

double ndtr(double a)
{
double x, y, z;

x = a * SQRTH;
z = fabs(x);

/* if( z < SQRTH ) */
if( z < 1.0 )
	y = 0.5 + 0.5 * erf(x);

else
	{
#ifdef USE_EXPXSQ
	/* See below for erfce. */
	y = 0.5 * erfce(z);
	/* Multiply by exp(-x^2 / 2)  */
	z = expx2(a, -1);
	y = y * sqrt(z);
#else
	y = 0.5 * erfc(z);
#endif
	if( x > 0 )
		y = 1.0 - y;
	}

return(y);
}

#ifndef HAVE_ERFC
double erfc(double a)
{
double p,q,x,y,z;


if( a < 0.0 )
	x = -a;
else
	x = a;

if( x < 1.0 )
	return( 1.0 - erf(a) );

z = -a * a;

if( z < -MAXLOG )
	{
under:
	mtherr( "erfc", UNDERFLOW );
	if( a < 0 )
		return( 2.0 );
	else
		return( 0.0 );
	}

#ifdef USE_EXPXSQ
/* Compute z = exp(z).  */
z = expx2(a, -1);
#else
z = exp(z);
#endif
if( x < 8.0 )
	{
	p = polevl( x, PERF, 8 );
	q = p1evl( x, QERF, 8 );
	}
else
	{
	p = polevl( x, RERF, 5 );
	q = p1evl( x, SERF, 6 );
	}
y = (z * p)/q;

if( a < 0 )
	y = 2.0 - y;

if( y == 0.0 )
	goto under;

return(y);
}
#endif


/* Exponentially scaled erfc function
   exp(x^2) erfc(x)
   valid for x > 1.
   Use with ndtr and expx2.  */
static double erfce(double x)
{
double p,q;

if( x < 8.0 )
	{
	p = polevl( x, PERF, 8 );
	q = p1evl( x, QERF, 8 );
	}
else
	{
	p = polevl( x, RERF, 5 );
	q = p1evl( x, SERF, 6 );
	}
return (p/q);
}



#ifndef HAVE_ERF
double erf(double x)
{
double y, z;

if( fabs(x) > 1.0 )
	return( 1.0 - erfc(x) );
z = x * x;
y = x * polevl( z, T, 4 ) / p1evl( z, U, 5 );
return( y );

}
#endif

/* ========================================================================= */

/*							dawsn.c
 *
 *	Dawson's Integral
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, dawsn();
 *
 * y = dawsn( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Approximates the integral
 *
 *                             x
 *                             -
 *                      2     | |        2
 *  dawsn(x)  =  exp( -x  )   |    exp( t  ) dt
 *                          | |
 *                           -
 *                           0
 *
 * Three different rational approximations are employed, for
 * the intervals 0 to 3.25; 3.25 to 6.25; and 6.25 up.
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0,10        10000       6.9e-16     1.0e-16
 *    DEC       0,10         6000       7.4e-17     1.4e-17
 *
 *
 */

/*							dawsn.c */


/* Dawson's integral, interval 0 to 3.25 */
#ifdef UNK
static double AN[10] = {
 1.13681498971755972054E-11,
 8.49262267667473811108E-10,
 1.94434204175553054283E-8,
 9.53151741254484363489E-7,
 3.07828309874913200438E-6,
 3.52513368520288738649E-4,
-8.50149846724410912031E-4,
 4.22618223005546594270E-2,
-9.17480371773452345351E-2,
 9.99999999999999994612E-1,
};
static double AD[11] = {
 2.40372073066762605484E-11,
 1.48864681368493396752E-9,
 5.21265281010541664570E-8,
 1.27258478273186970203E-6,
 2.32490249820789513991E-5,
 3.25524741826057911661E-4,
 3.48805814657162590916E-3,
 2.79448531198828973716E-2,
 1.58874241960120565368E-1,
 5.74918629489320327824E-1,
 1.00000000000000000539E0,
};
#endif
#ifdef DEC
static unsigned short AN[40] = {
0027107,0176630,0075752,0107612,
0030551,0070604,0166707,0127727,
0031647,0002210,0117120,0056376,
0033177,0156026,0141275,0140627,
0033516,0112200,0037035,0165515,
0035270,0150613,0016423,0105634,
0135536,0156227,0023515,0044413,
0037055,0015273,0105147,0064025,
0137273,0163145,0014460,0166465,
0040200,0000000,0000000,0000000,
};
static unsigned short AD[44] = {
0027323,0067372,0115566,0131320,
0030714,0114432,0074206,0006637,
0032137,0160671,0044203,0026344,
0033252,0146656,0020247,0100231,
0034303,0003346,0123260,0022433,
0035252,0125460,0173041,0155415,
0036144,0113747,0125203,0124617,
0036744,0166232,0143671,0133670,
0037442,0127755,0162625,0000100,
0040023,0026736,0003604,0106265,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short AN[40] = {
0x51f1,0x0f7d,0xffb3,0x3da8,
0xf5fb,0x9db8,0x2e30,0x3e0d,
0x0ba0,0x13ca,0xe091,0x3e54,
0xb833,0xd857,0xfb82,0x3eaf,
0xbd6a,0x07c3,0xd290,0x3ec9,
0x7174,0x63a2,0x1a31,0x3f37,
0xa921,0xe4e9,0xdb92,0xbf4b,
0xed03,0x714c,0xa357,0x3fa5,
0x1da7,0xa326,0x7ccc,0xbfb7,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short AD[44] = {
0xd65a,0x536e,0x6ddf,0x3dba,
0xc1b4,0x4f10,0x9323,0x3e19,
0x659c,0x2910,0xfc37,0x3e6b,
0xf013,0xc414,0x59b5,0x3eb5,
0x04a3,0xd4d6,0x60dc,0x3ef8,
0x3b62,0x1ec4,0x5566,0x3f35,
0x7532,0xf550,0x92fc,0x3f6c,
0x36f7,0x58f7,0x9d93,0x3f9c,
0xa008,0xbcb2,0x55fd,0x3fc4,
0x9197,0xc0f0,0x65bb,0x3fe2,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short AN[40] = {
0x3da8,0xffb3,0x0f7d,0x51f1,
0x3e0d,0x2e30,0x9db8,0xf5fb,
0x3e54,0xe091,0x13ca,0x0ba0,
0x3eaf,0xfb82,0xd857,0xb833,
0x3ec9,0xd290,0x07c3,0xbd6a,
0x3f37,0x1a31,0x63a2,0x7174,
0xbf4b,0xdb92,0xe4e9,0xa921,
0x3fa5,0xa357,0x714c,0xed03,
0xbfb7,0x7ccc,0xa326,0x1da7,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short AD[44] = {
0x3dba,0x6ddf,0x536e,0xd65a,
0x3e19,0x9323,0x4f10,0xc1b4,
0x3e6b,0xfc37,0x2910,0x659c,
0x3eb5,0x59b5,0xc414,0xf013,
0x3ef8,0x60dc,0xd4d6,0x04a3,
0x3f35,0x5566,0x1ec4,0x3b62,
0x3f6c,0x92fc,0xf550,0x7532,
0x3f9c,0x9d93,0x58f7,0x36f7,
0x3fc4,0x55fd,0xbcb2,0xa008,
0x3fe2,0x65bb,0xc0f0,0x9197,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif

/* interval 3.25 to 6.25 */
#ifdef UNK
static double BN[11] = {
 5.08955156417900903354E-1,
-2.44754418142697847934E-1,
 9.41512335303534411857E-2,
-2.18711255142039025206E-2,
 3.66207612329569181322E-3,
-4.23209114460388756528E-4,
 3.59641304793896631888E-5,
-2.14640351719968974225E-6,
 9.10010780076391431042E-8,
-2.40274520828250956942E-9,
 3.59233385440928410398E-11,
};
static double BD[10] = {
/*  1.00000000000000000000E0,*/
-6.31839869873368190192E-1,
 2.36706788228248691528E-1,
-5.31806367003223277662E-2,
 8.48041718586295374409E-3,
-9.47996768486665330168E-4,
 7.81025592944552338085E-5,
-4.55875153252442634831E-6,
 1.89100358111421846170E-7,
-4.91324691331920606875E-9,
 7.18466403235734541950E-11,
};
#endif
#ifdef DEC
static unsigned short BN[44] = {
0040002,0045342,0113762,0004360,
0137572,0120346,0172745,0144046,
0037300,0151134,0123440,0117047,
0136663,0025423,0014755,0046026,
0036157,0177561,0027535,0046744,
0135335,0161052,0071243,0146535,
0034426,0154060,0164506,0135625,
0133420,0005356,0100017,0151334,
0032303,0066137,0024013,0046212,
0131045,0016612,0066270,0047574,
0027435,0177025,0060625,0116363,
};
static unsigned short BD[40] = {
/*0040200,0000000,0000000,0000000,*/
0140041,0140101,0174552,0037073,
0037562,0061503,0124271,0160756,
0137131,0151760,0073210,0110534,
0036412,0170562,0117017,0155377,
0135570,0101374,0074056,0037276,
0034643,0145376,0001516,0060636,
0133630,0173540,0121344,0155231,
0032513,0005602,0134516,0007144,
0131250,0150540,0075747,0105341,
0027635,0177020,0012465,0125402,
};
#endif
#ifdef IBMPC
static unsigned short BN[44] = {
0x411e,0x52fe,0x495c,0x3fe0,
0xb905,0xdebc,0x541c,0xbfcf,
0x13c5,0x94e4,0x1a4b,0x3fb8,
0xa983,0x633d,0x6562,0xbf96,
0xa9bd,0x25eb,0xffee,0x3f6d,
0x79ac,0x4e54,0xbc45,0xbf3b,
0xd773,0x1d28,0xdb06,0x3f02,
0xfa5b,0xd001,0x015d,0xbec2,
0x6991,0xe501,0x6d8b,0x3e78,
0x09f0,0x4d97,0xa3b1,0xbe24,
0xb39e,0xac32,0xbfc2,0x3dc3,
};
static unsigned short BD[40] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x47c7,0x3f2d,0x3808,0xbfe4,
0x3c3e,0x7517,0x4c68,0x3fce,
0x122b,0x0ed1,0x3a7e,0xbfab,
0xfb60,0x53c1,0x5e2e,0x3f81,
0xc7d8,0x8f05,0x105f,0xbf4f,
0xcc34,0xc069,0x795f,0x3f14,
0x9b53,0x145c,0x1eec,0xbed3,
0xc1cd,0x5729,0x6170,0x3e89,
0xf15c,0x0f7c,0x1a2c,0xbe35,
0xb560,0x02a6,0xbfc2,0x3dd3,
};
#endif
#ifdef MIEEE
static unsigned short BN[44] = {
0x3fe0,0x495c,0x52fe,0x411e,
0xbfcf,0x541c,0xdebc,0xb905,
0x3fb8,0x1a4b,0x94e4,0x13c5,
0xbf96,0x6562,0x633d,0xa983,
0x3f6d,0xffee,0x25eb,0xa9bd,
0xbf3b,0xbc45,0x4e54,0x79ac,
0x3f02,0xdb06,0x1d28,0xd773,
0xbec2,0x015d,0xd001,0xfa5b,
0x3e78,0x6d8b,0xe501,0x6991,
0xbe24,0xa3b1,0x4d97,0x09f0,
0x3dc3,0xbfc2,0xac32,0xb39e,
};
static unsigned short BD[40] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0xbfe4,0x3808,0x3f2d,0x47c7,
0x3fce,0x4c68,0x7517,0x3c3e,
0xbfab,0x3a7e,0x0ed1,0x122b,
0x3f81,0x5e2e,0x53c1,0xfb60,
0xbf4f,0x105f,0x8f05,0xc7d8,
0x3f14,0x795f,0xc069,0xcc34,
0xbed3,0x1eec,0x145c,0x9b53,
0x3e89,0x6170,0x5729,0xc1cd,
0xbe35,0x1a2c,0x0f7c,0xf15c,
0x3dd3,0xbfc2,0x02a6,0xb560,
};
#endif

/* 6.25 to infinity */
#ifdef UNK
static double CN[5] = {
-5.90592860534773254987E-1,
 6.29235242724368800674E-1,
-1.72858975380388136411E-1,
 1.64837047825189632310E-2,
-4.86827613020462700845E-4,
};
static double CD[5] = {
/* 1.00000000000000000000E0,*/
-2.69820057197544900361E0,
 1.73270799045947845857E0,
-3.93708582281939493482E-1,
 3.44278924041233391079E-2,
-9.73655226040941223894E-4,
};
#endif
#ifdef DEC
static unsigned short CN[20] = {
0140027,0030427,0176477,0074402,
0040041,0012617,0112375,0162657,
0137461,0000761,0074120,0135160,
0036607,0004325,0117246,0115525,
0135377,0036345,0064750,0047732,
};
static unsigned short CD[20] = {
/*0040200,0000000,0000000,0000000,*/
0140454,0127521,0071653,0133415,
0040335,0144540,0016105,0045241,
0137711,0112053,0155034,0062237,
0037015,0002102,0177442,0074546,
0135577,0036345,0064750,0052152,
};
#endif
#ifdef IBMPC
static unsigned short CN[20] = {
0xef20,0xffa7,0xe622,0xbfe2,
0xbcb6,0xf29f,0x22b1,0x3fe4,
0x174e,0x2f0a,0x203e,0xbfc6,
0xd36b,0xb3d4,0xe11a,0x3f90,
0x09fb,0xad3d,0xe79c,0xbf3f,
};
static unsigned short CD[20] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x76e2,0x2e75,0x95ea,0xc005,
0xa954,0x0388,0xb92c,0x3ffb,
0x8c94,0x7b43,0x3285,0xbfd9,
0x4f2d,0x5fe4,0xa088,0x3fa1,
0x0a8d,0xad3d,0xe79c,0xbf4f,
};
#endif
#ifdef MIEEE
static unsigned short CN[20] = {
0xbfe2,0xe622,0xffa7,0xef20,
0x3fe4,0x22b1,0xf29f,0xbcb6,
0xbfc6,0x203e,0x2f0a,0x174e,
0x3f90,0xe11a,0xb3d4,0xd36b,
0xbf3f,0xe79c,0xad3d,0x09fb,
};
static unsigned short CD[20] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0xc005,0x95ea,0x2e75,0x76e2,
0x3ffb,0xb92c,0x0388,0xa954,
0xbfd9,0x3285,0x7b43,0x8c94,
0x3fa1,0xa088,0x5fe4,0x4f2d,
0xbf4f,0xe79c,0xad3d,0x0a8d,
};
#endif

double dawsn(double xx)
{
double x, y;
int sign;


sign = 1;
if( xx < 0.0 )
	{
	sign = -1;
	xx = -xx;
	}

if( xx < 3.25 )
{
x = xx*xx;
y = xx * polevl( x, AN, 9 )/polevl( x, AD, 10 );
return( sign * y );
}


x = 1.0/(xx*xx);

if( xx < 6.25 )
	{
	y = 1.0/xx + x * polevl( x, BN, 10) / (p1evl( x, BD, 10) * xx);
	return( sign * 0.5 * y );
	}


if( xx > 1.0e9 )
	return( (sign * 0.5)/xx );

/* 6.25 to infinity */
y = 1.0/xx + x * polevl( x, CN, 4) / (p1evl( x, CD, 5) * xx);
return( sign * 0.5 * y );
}

/* ========================================================================= */

/*							fresnl.c
 *
 *	Fresnel integral
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, S, C;
 * void fresnl();
 *
 * fresnl( x, _&S, _&C );
 *
 *
 * DESCRIPTION:
 *
 * Evaluates the Fresnel integrals
 *
 *           x
 *           -
 *          | |
 * C(x) =   |   cos(pi/2 t**2) dt,
 *        | |
 *         -
 *          0
 *
 *           x
 *           -
 *          | |
 * S(x) =   |   sin(pi/2 t**2) dt.
 *        | |
 *         -
 *          0
 *
 *
 * The integrals are evaluated by a power series for x < 1.
 * For x >= 1 auxiliary functions f(x) and g(x) are employed
 * such that
 *
 * C(x) = 0.5 + f(x) sin( pi/2 x**2 ) - g(x) cos( pi/2 x**2 )
 * S(x) = 0.5 - f(x) cos( pi/2 x**2 ) - g(x) sin( pi/2 x**2 )
 *
 *
 *
 * ACCURACY:
 *
 *  Relative error.
 *
 * Arithmetic  function   domain     # trials      peak         rms
 *   IEEE       S(x)      0, 10       10000       2.0e-15     3.2e-16
 *   IEEE       C(x)      0, 10       10000       1.8e-15     3.3e-16
 *   DEC        S(x)      0, 10        6000       2.2e-16     3.9e-17
 *   DEC        C(x)      0, 10        5000       2.3e-16     3.9e-17
 */



/* S(x) for small x */
#ifdef UNK
static double sn[6] = {
-2.99181919401019853726E3,
 7.08840045257738576863E5,
-6.29741486205862506537E7,
 2.54890880573376359104E9,
-4.42979518059697779103E10,
 3.18016297876567817986E11,
};
static double sd[6] = {
/* 1.00000000000000000000E0,*/
 2.81376268889994315696E2,
 4.55847810806532581675E4,
 5.17343888770096400730E6,
 4.19320245898111231129E8,
 2.24411795645340920940E10,
 6.07366389490084639049E11,
};
#endif
#ifdef DEC
static unsigned short sn[24] = {
0143072,0176433,0065455,0127034,
0045055,0007200,0134540,0026661,
0146560,0035061,0023667,0127545,
0050027,0166503,0002673,0153756,
0151045,0002721,0121737,0102066,
0051624,0013177,0033451,0021271,
};
static unsigned short sd[24] = {
/*0040200,0000000,0000000,0000000,*/
0042214,0130051,0112070,0101617,
0044062,0010307,0172346,0152510,
0045635,0160575,0143200,0136642,
0047307,0171215,0127457,0052361,
0050647,0031447,0032621,0013510,
0052015,0064733,0117362,0012653,
};
#endif
#ifdef IBMPC
static unsigned short sn[24] = {
0xb5c3,0x6d65,0x5fa3,0xc0a7,
0x05b6,0x172c,0xa1d0,0x4125,
0xf5ed,0x24f6,0x0746,0xc18e,
0x7afe,0x60b7,0xfda8,0x41e2,
0xf087,0x347b,0xa0ba,0xc224,
0x2457,0xe6e5,0x82cf,0x4252,
};
static unsigned short sd[24] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x1072,0x3287,0x9605,0x4071,
0xdaa9,0xfe9c,0x4218,0x40e6,
0x17b4,0xb8d0,0xbc2f,0x4153,
0xea9e,0xb5e5,0xfe51,0x41b8,
0x22e9,0xe6b2,0xe664,0x4214,
0x42b5,0x73de,0xad3b,0x4261,
};
#endif
#ifdef MIEEE
static unsigned short sn[24] = {
0xc0a7,0x5fa3,0x6d65,0xb5c3,
0x4125,0xa1d0,0x172c,0x05b6,
0xc18e,0x0746,0x24f6,0xf5ed,
0x41e2,0xfda8,0x60b7,0x7afe,
0xc224,0xa0ba,0x347b,0xf087,
0x4252,0x82cf,0xe6e5,0x2457,
};
static unsigned short sd[24] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4071,0x9605,0x3287,0x1072,
0x40e6,0x4218,0xfe9c,0xdaa9,
0x4153,0xbc2f,0xb8d0,0x17b4,
0x41b8,0xfe51,0xb5e5,0xea9e,
0x4214,0xe664,0xe6b2,0x22e9,
0x4261,0xad3b,0x73de,0x42b5,
};
#endif

/* C(x) for small x */
#ifdef UNK
static double cn[6] = {
-4.98843114573573548651E-8,
 9.50428062829859605134E-6,
-6.45191435683965050962E-4,
 1.88843319396703850064E-2,
-2.05525900955013891793E-1,
 9.99999999999999998822E-1,
};
static double cd[7] = {
 3.99982968972495980367E-12,
 9.15439215774657478799E-10,
 1.25001862479598821474E-7,
 1.22262789024179030997E-5,
 8.68029542941784300606E-4,
 4.12142090722199792936E-2,
 1.00000000000000000118E0,
};
#endif
#ifdef DEC
static unsigned short cn[24] = {
0132126,0040141,0063733,0013231,
0034037,0072223,0010200,0075637,
0135451,0021020,0073264,0036057,
0036632,0131520,0101316,0060233,
0137522,0072541,0136124,0132202,
0040200,0000000,0000000,0000000,
};
static unsigned short cd[28] = {
0026614,0135503,0051776,0032631,
0030573,0121116,0154033,0126712,
0032406,0034100,0012442,0106212,
0034115,0017567,0150520,0164623,
0035543,0106171,0177336,0146351,
0037050,0150073,0000607,0171635,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short cn[24] = {
0x62d3,0x2cfb,0xc80c,0xbe6a,
0x0f74,0x6210,0xee92,0x3ee3,
0x8786,0x0ed6,0x2442,0xbf45,
0xcc13,0x1059,0x566a,0x3f93,
0x9690,0x378a,0x4eac,0xbfca,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short cd[28] = {
0xc6b3,0x6a7f,0x9768,0x3d91,
0x75b9,0xdb03,0x7449,0x3e0f,
0x5191,0x02a4,0xc708,0x3e80,
0x1d32,0xfa2a,0xa3ee,0x3ee9,
0xd99d,0x3fdb,0x718f,0x3f4c,
0xfe74,0x6030,0x1a07,0x3fa5,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short cn[24] = {
0xbe6a,0xc80c,0x2cfb,0x62d3,
0x3ee3,0xee92,0x6210,0x0f74,
0xbf45,0x2442,0x0ed6,0x8786,
0x3f93,0x566a,0x1059,0xcc13,
0xbfca,0x4eac,0x378a,0x9690,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short cd[28] = {
0x3d91,0x9768,0x6a7f,0xc6b3,
0x3e0f,0x7449,0xdb03,0x75b9,
0x3e80,0xc708,0x02a4,0x5191,
0x3ee9,0xa3ee,0xfa2a,0x1d32,
0x3f4c,0x718f,0x3fdb,0xd99d,
0x3fa5,0x1a07,0x6030,0xfe74,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif

/* Auxiliary function f(x) */
#ifdef UNK
static double fn[10] = {
  4.21543555043677546506E-1,
  1.43407919780758885261E-1,
  1.15220955073585758835E-2,
  3.45017939782574027900E-4,
  4.63613749287867322088E-6,
  3.05568983790257605827E-8,
  1.02304514164907233465E-10,
  1.72010743268161828879E-13,
  1.34283276233062758925E-16,
  3.76329711269987889006E-20,
};
static double fd[10] = {
/*  1.00000000000000000000E0,*/
  7.51586398353378947175E-1,
  1.16888925859191382142E-1,
  6.44051526508858611005E-3,
  1.55934409164153020873E-4,
  1.84627567348930545870E-6,
  1.12699224763999035261E-8,
  3.60140029589371370404E-11,
  5.88754533621578410010E-14,
  4.52001434074129701496E-17,
  1.25443237090011264384E-20,
};
#endif
#ifdef DEC
static unsigned short fn[40] = {
0037727,0152216,0106601,0016214,
0037422,0154606,0112710,0071355,
0036474,0143453,0154253,0166545,
0035264,0161606,0022250,0073743,
0033633,0110036,0024653,0136246,
0032003,0036652,0041164,0036413,
0027740,0174122,0046305,0036726,
0025501,0125270,0121317,0167667,
0023032,0150555,0076175,0047443,
0020061,0133570,0070130,0027657,
};
static unsigned short fd[40] = {
/*0040200,0000000,0000000,0000000,*/
0040100,0063767,0054413,0151452,
0037357,0061566,0007243,0065754,
0036323,0005365,0033552,0133625,
0035043,0101123,0000275,0165402,
0033367,0146614,0110623,0023647,
0031501,0116644,0125222,0144263,
0027436,0062051,0117235,0001411,
0025204,0111543,0056370,0036201,
0022520,0071351,0015227,0122144,
0017554,0172240,0112713,0005006,
};
#endif
#ifdef IBMPC
static unsigned short fn[40] = {
0x2391,0xd1b0,0xfa91,0x3fda,
0x0e5e,0xd2b9,0x5b30,0x3fc2,
0x7dad,0x7b15,0x98e5,0x3f87,
0x0efc,0xc495,0x9c70,0x3f36,
0x7795,0xc535,0x7203,0x3ed3,
0x87a1,0x484e,0x67b5,0x3e60,
0xa7bb,0x4998,0x1f0a,0x3ddc,
0xfdf7,0x1459,0x3557,0x3d48,
0xa9e4,0xaf8f,0x5a2d,0x3ca3,
0x05f6,0x0e0b,0x36ef,0x3be6,
};
static unsigned short fd[40] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x7a65,0xeb21,0x0cfe,0x3fe8,
0x6d7d,0xc1d4,0xec6e,0x3fbd,
0x56f3,0xa6ed,0x615e,0x3f7a,
0xbd60,0x6017,0x704a,0x3f24,
0x64f5,0x9232,0xf9b1,0x3ebe,
0x5916,0x9552,0x33b4,0x3e48,
0xa061,0x33d3,0xcc85,0x3dc3,
0x0790,0x6b9f,0x926c,0x3d30,
0xf48d,0x2352,0x0e5d,0x3c8a,
0x6141,0x12b9,0x9e94,0x3bcd,
};
#endif
#ifdef MIEEE
static unsigned short fn[40] = {
0x3fda,0xfa91,0xd1b0,0x2391,
0x3fc2,0x5b30,0xd2b9,0x0e5e,
0x3f87,0x98e5,0x7b15,0x7dad,
0x3f36,0x9c70,0xc495,0x0efc,
0x3ed3,0x7203,0xc535,0x7795,
0x3e60,0x67b5,0x484e,0x87a1,
0x3ddc,0x1f0a,0x4998,0xa7bb,
0x3d48,0x3557,0x1459,0xfdf7,
0x3ca3,0x5a2d,0xaf8f,0xa9e4,
0x3be6,0x36ef,0x0e0b,0x05f6,
};
static unsigned short fd[40] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x3fe8,0x0cfe,0xeb21,0x7a65,
0x3fbd,0xec6e,0xc1d4,0x6d7d,
0x3f7a,0x615e,0xa6ed,0x56f3,
0x3f24,0x704a,0x6017,0xbd60,
0x3ebe,0xf9b1,0x9232,0x64f5,
0x3e48,0x33b4,0x9552,0x5916,
0x3dc3,0xcc85,0x33d3,0xa061,
0x3d30,0x926c,0x6b9f,0x0790,
0x3c8a,0x0e5d,0x2352,0xf48d,
0x3bcd,0x9e94,0x12b9,0x6141,
};
#endif


/* Auxiliary function g(x) */
#ifdef UNK
static double gn[11] = {
  5.04442073643383265887E-1,
  1.97102833525523411709E-1,
  1.87648584092575249293E-2,
  6.84079380915393090172E-4,
  1.15138826111884280931E-5,
  9.82852443688422223854E-8,
  4.45344415861750144738E-10,
  1.08268041139020870318E-12,
  1.37555460633261799868E-15,
  8.36354435630677421531E-19,
  1.86958710162783235106E-22,
};
static double gd[11] = {
/*  1.00000000000000000000E0,*/
  1.47495759925128324529E0,
  3.37748989120019970451E-1,
  2.53603741420338795122E-2,
  8.14679107184306179049E-4,
  1.27545075667729118702E-5,
  1.04314589657571990585E-7,
  4.60680728146520428211E-10,
  1.10273215066240270757E-12,
  1.38796531259578871258E-15,
  8.39158816283118707363E-19,
  1.86958710162783236342E-22,
};
#endif
#ifdef DEC
static unsigned short gn[44] = {
0040001,0021435,0120406,0053123,
0037511,0152523,0037703,0122011,
0036631,0134302,0122721,0110235,
0035463,0051712,0043215,0114732,
0034101,0025677,0147725,0057630,
0032323,0010342,0067523,0002206,
0030364,0152247,0110007,0054107,
0026230,0057654,0035464,0047124,
0023706,0036401,0167705,0045440,
0021166,0154447,0105632,0142461,
0016142,0002353,0011175,0170530,
};
static unsigned short gd[44] = {
/*0040200,0000000,0000000,0000000,*/
0040274,0145551,0016742,0127005,
0037654,0166557,0076416,0015165,
0036717,0140217,0030675,0050111,
0035525,0110060,0076405,0070502,
0034125,0176061,0060120,0031730,
0032340,0001615,0054343,0120501,
0030375,0041414,0070747,0107060,
0026233,0031034,0160757,0074526,
0023710,0003341,0137100,0144664,
0021167,0126414,0023774,0015435,
0016142,0002353,0011175,0170530,
};
#endif
#ifdef IBMPC
static unsigned short gn[44] = {
0xcaca,0xb420,0x2463,0x3fe0,
0x7481,0x67f8,0x3aaa,0x3fc9,
0x3214,0x54ba,0x3718,0x3f93,
0xb33b,0x48d1,0x6a79,0x3f46,
0xabf3,0xf9fa,0x2577,0x3ee8,
0x6091,0x4dea,0x621c,0x3e7a,
0xeb09,0xf200,0x9a94,0x3dfe,
0x89cb,0x8766,0x0bf5,0x3d73,
0xa964,0x3df8,0xc7a0,0x3cd8,
0x58a6,0xf173,0xdb24,0x3c2e,
0xbe2b,0x624f,0x409d,0x3b6c,
};
static unsigned short gd[44] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x55c1,0x23bc,0x996d,0x3ff7,
0xc34f,0xefa1,0x9dad,0x3fd5,
0xaa09,0xe637,0xf811,0x3f99,
0xae28,0x0fa0,0xb206,0x3f4a,
0x067b,0x2c0a,0xbf86,0x3eea,
0x7428,0xab1c,0x0071,0x3e7c,
0xf1c6,0x8e3c,0xa861,0x3dff,
0xef2b,0x9c3d,0x6643,0x3d73,
0x1936,0x37c8,0x00dc,0x3cd9,
0x8364,0x84ff,0xf5a1,0x3c2e,
0xbe2b,0x624f,0x409d,0x3b6c,
};
#endif
#ifdef MIEEE
static unsigned short gn[44] = {
0x3fe0,0x2463,0xb420,0xcaca,
0x3fc9,0x3aaa,0x67f8,0x7481,
0x3f93,0x3718,0x54ba,0x3214,
0x3f46,0x6a79,0x48d1,0xb33b,
0x3ee8,0x2577,0xf9fa,0xabf3,
0x3e7a,0x621c,0x4dea,0x6091,
0x3dfe,0x9a94,0xf200,0xeb09,
0x3d73,0x0bf5,0x8766,0x89cb,
0x3cd8,0xc7a0,0x3df8,0xa964,
0x3c2e,0xdb24,0xf173,0x58a6,
0x3b6c,0x409d,0x624f,0xbe2b,
};
static unsigned short gd[44] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x3ff7,0x996d,0x23bc,0x55c1,
0x3fd5,0x9dad,0xefa1,0xc34f,
0x3f99,0xf811,0xe637,0xaa09,
0x3f4a,0xb206,0x0fa0,0xae28,
0x3eea,0xbf86,0x2c0a,0x067b,
0x3e7c,0x0071,0xab1c,0x7428,
0x3dff,0xa861,0x8e3c,0xf1c6,
0x3d73,0x6643,0x9c3d,0xef2b,
0x3cd9,0x00dc,0x37c8,0x1936,
0x3c2e,0xf5a1,0x84ff,0x8364,
0x3b6c,0x409d,0x624f,0xbe2b,
};
#endif


int fresnl(double xxa, double* ssa, double* cca)
{
double f, g, cc, ss, c, s, t, u;
double x, x2;

x = fabs(xxa);
x2 = x * x;
if( x2 < 2.5625 )
	{
	t = x2 * x2;
	ss = x * x2 * polevl( t, sn, 5)/p1evl( t, sd, 6 );
	cc = x * polevl( t, cn, 5)/polevl(t, cd, 6 );
	goto done;
	}






if( x > 36974.0 )
	{
	cc = 0.5;
	ss = 0.5;
	goto done;
	}


/*		Asymptotic power series auxiliary functions
 *		for large argument
 */
	x2 = x * x;
	t = PI * x2;
	u = 1.0/(t * t);
	t = 1.0/t;
	f = 1.0 - u * polevl( u, fn, 9)/p1evl(u, fd, 10);
	g = t * polevl( u, gn, 10)/p1evl(u, gd, 11);

	t = PIO2 * x2;
	c = cos(t);
	s = sin(t);
	t = PI * x;
	cc = 0.5  +  (f * s  -  g * c)/t;
	ss = 0.5  -  (f * c  +  g * s)/t;

done:
if( xxa < 0.0 )
	{
	cc = -cc;
	ss = -ss;
	}

*cca = cc;
*ssa = ss;
return(0);
}

/* ========================================================================= */

/*							expx2.c
 *
 *	Exponential of squared argument
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, expx2();
 * int sign;
 *
 * y = expx2( x, sign );
 *
 *
 *
 * DESCRIPTION:
 *
 * Computes y = exp(x*x) while suppressing error amplification
 * that would ordinarily arise from the inexactness of the
 * exponential argument x*x.
 *
 * If sign < 0, the result is inverted; i.e., y = exp(-x*x) .
 * 
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic    domain     # trials      peak         rms
 *   IEEE      -26.6, 26.6    10^7       3.9e-16     8.9e-17
 *
 */



#ifdef DEC
#define M 32.0
#define MINV .03125
#else
#define M 128.0
#define MINV .0078125
#endif


double expx2 (double x, int sign)
{
  double u, u1, m, f;

  x = fabs (x);
  if (sign < 0)
    x = -x;

  /* Represent x as an exact multiple of M plus a residual.
     M is a power of 2 chosen so that exp(m * m) does not overflow
     or underflow and so that |x - m| is small.  */
  m = MINV * floor(M * x + 0.5);
  f = x - m;

  /* x^2 = m^2 + 2mf + f^2 */
  u = m * m;
  u1 = 2 * m * f  +  f * f;

  if (sign < 0)
    {
      u = -u;
      u1 = -u1;
    }

  if ((u+u1) > MAXLOG)
    return (CEPHESINFINITY);

  /* u is exact, u1 is small.  */
  u = exp(u) * exp(u1);
  return(u);
}



/* ========================================================================= */

/*							expn.c
 *
 *		Exponential integral En
 *
 *
 *
 * SYNOPSIS:
 *
 * int n;
 * double x, y, expn();
 *
 * y = expn( n, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Evaluates the exponential integral
 *
 *                 inf.
 *                   -
 *                  | |   -xt
 *                  |    e
 *      E (x)  =    |    ----  dt.
 *       n          |      n
 *                | |     t
 *                 -
 *                  1
 *
 *
 * Both n and x must be nonnegative.
 *
 * The routine employs either a power series, a continued
 * fraction, or an asymptotic formula depending on the
 * relative values of n and x.
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0, 30        5000       2.0e-16     4.6e-17
 *    IEEE      0, 30       10000       1.7e-15     3.6e-16
 *
 */

/*							expn.c	*/


double expn(int n, double x)
{
double ans, r, t, yk, xk;
double pk, pkm1, pkm2, qk, qkm1, qkm2;
double psi, z;
int i, k;
static double expnbig = BIG;

if( n < 0 )
	goto domerr;

if( x < 0 )
	{
domerr:	mtherr( "expn", DOMAIN );
	return( MAXNUM );
	}

if( x > MAXLOG )
	return( 0.0 );

if( x == 0.0 )
	{
	if( n < 2 )
		{
		mtherr( "expn", SING );
		return( MAXNUM );
		}
	else
		return( 1.0/(n-1.0) );
	}

if( n == 0 )
	return( exp(-x)/x );

/*							expn.c	*/
/*		Expansion for large n		*/

if( n > 5000 )
	{
	xk = x + n;
	yk = 1.0 / (xk * xk);
	t = n;
	ans = yk * t * (6.0 * x * x  -  8.0 * t * x  +  t * t);
	ans = yk * (ans + t * (t  -  2.0 * x));
	ans = yk * (ans + t);
	ans = (ans + 1.0) * exp( -x ) / xk;
	goto done;
	}

if( x > 1.0 )
	goto cfrac;

/*							expn.c	*/

/*		Power series expansion		*/

psi = -EUL - log(x);
for( i=1; i<n; i++ )
	psi = psi + 1.0/i;

z = -x;
xk = 0.0;
yk = 1.0;
pk = 1.0 - n;
if( n == 1 )
	ans = 0.0;
else
	ans = 1.0/pk;
do
	{
	xk += 1.0;
	yk *= z/xk;
	pk += 1.0;
	if( pk != 0.0 )
		{
		ans += yk/pk;
		}
	if( ans != 0.0 )
		t = fabs(yk/ans);
	else
		t = 1.0;
	}
while( t > MACHEP );
k = xk;
t = n;
r = n - 1;
ans = (pow(z, r) * psi / cephesgamma(t)) - ans;
goto done;

/*							expn.c	*/
/*		continued fraction		*/
cfrac:
k = 1;
pkm2 = 1.0;
qkm2 = x;
pkm1 = 1.0;
qkm1 = x + n;
ans = pkm1/qkm1;

do
	{
	k += 1;
	if( k & 1 )
		{
		yk = 1.0;
		xk = n + (k-1)/2;
		}
	else
		{
		yk = x;
		xk = k/2;
		}
	pk = pkm1 * yk  +  pkm2 * xk;
	qk = qkm1 * yk  +  qkm2 * xk;
	if( qk != 0 )
		{
		r = pk/qk;
		t = fabs( (ans - r)/r );
		ans = r;
		}
	else
		t = 1.0;
	pkm2 = pkm1;
	pkm1 = pk;
	qkm2 = qkm1;
	qkm1 = qk;
if( fabs(pk) > expnbig )
		{
		pkm2 /= expnbig;
		pkm1 /= expnbig;
		qkm2 /= expnbig;
		qkm1 /= expnbig;
		}
	}
while( t > MACHEP );

ans *= exp( -x );

done:
return( ans );
}

/* ========================================================================= */

/*							shichi.c
 *
 *	Hyperbolic sine and cosine integrals
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, Chi, Shi, shichi();
 *
 * shichi( x, &Chi, &Shi );
 *
 *
 * DESCRIPTION:
 *
 * Approximates the integrals
 *
 *                            x
 *                            -
 *                           | |   cosh t - 1
 *   Chi(x) = eul + ln x +   |    -----------  dt,
 *                         | |          t
 *                          -
 *                          0
 *
 *               x
 *               -
 *              | |  sinh t
 *   Shi(x) =   |    ------  dt
 *            | |       t
 *             -
 *             0
 *
 * where eul = 0.57721566490153286061 is Euler's constant.
 * The integrals are evaluated by power series for x < 8
 * and by Chebyshev expansions for x between 8 and 88.
 * For large x, both functions approach exp(x)/2x.
 * Arguments greater than 88 in magnitude return MAXNUM.
 *
 *
 * ACCURACY:
 *
 * Test interval 0 to 88.
 *                      Relative error:
 * arithmetic   function  # trials      peak         rms
 *    DEC          Shi       3000       9.1e-17
 *    IEEE         Shi      30000       6.9e-16     1.6e-16
 *        Absolute error, except relative when |Chi| > 1:
 *    DEC          Chi       2500       9.3e-17
 *    IEEE         Chi      30000       8.4e-16     1.4e-16
 */




#ifdef UNK
/* x exp(-x) shi(x), inverted interval 8 to 18 */
static double SHI1[] = {
 1.83889230173399459482E-17,
-9.55485532279655569575E-17,
 2.04326105980879882648E-16,
 1.09896949074905343022E-15,
-1.31313534344092599234E-14,
 5.93976226264314278932E-14,
-3.47197010497749154755E-14,
-1.40059764613117131000E-12,
 9.49044626224223543299E-12,
-1.61596181145435454033E-11,
-1.77899784436430310321E-10,
 1.35455469767246947469E-9,
-1.03257121792819495123E-9,
-3.56699611114982536845E-8,
 1.44818877384267342057E-7,
 7.82018215184051295296E-7,
-5.39919118403805073710E-6,
-3.12458202168959833422E-5,
 8.90136741950727517826E-5,
 2.02558474743846862168E-3,
 2.96064440855633256972E-2,
 1.11847751047257036625E0
};

/* x exp(-x) shi(x), inverted interval 18 to 88 */
static double SHI2[] = {
-1.05311574154850938805E-17,
 2.62446095596355225821E-17,
 8.82090135625368160657E-17,
-3.38459811878103047136E-16,
-8.30608026366935789136E-16,
 3.93397875437050071776E-15,
 1.01765565969729044505E-14,
-4.21128170307640802703E-14,
-1.60818204519802480035E-13,
 3.34714954175994481761E-13,
 2.72600352129153073807E-12,
 1.66894954752839083608E-12,
-3.49278141024730899554E-11,
-1.58580661666482709598E-10,
-1.79289437183355633342E-10,
 1.76281629144264523277E-9,
 1.69050228879421288846E-8,
 1.25391771228487041649E-7,
 1.16229947068677338732E-6,
 1.61038260117376323993E-5,
 3.49810375601053973070E-4,
 1.28478065259647610779E-2,
 1.03665722588798326712E0
};
#endif

#ifdef DEC
static unsigned short SHI1[] = {
0022251,0115635,0165120,0006574,
0122734,0050751,0020305,0101356,
0023153,0111154,0011103,0177462,
0023636,0060321,0060253,0124246,
0124554,0106655,0152525,0166400,
0025205,0140145,0171006,0106556,
0125034,0056427,0004205,0176022,
0126305,0016731,0025011,0134453,
0027046,0172453,0112604,0116235,
0127216,0022071,0116600,0137667,
0130103,0115126,0071104,0052535,
0030672,0025450,0010071,0141414,
0130615,0165136,0132137,0177737,
0132031,0031611,0074436,0175407,
0032433,0077602,0104345,0060076,
0033121,0165741,0167177,0172433,
0133665,0025262,0174621,0022612,
0134403,0006761,0124566,0145405,
0034672,0126332,0034737,0116744,
0036004,0137654,0037332,0131766,
0036762,0104466,0121445,0124326,
0040217,0025105,0062145,0042640
};

static unsigned short SHI2[] = {
0122102,0041774,0016051,0055137,
0022362,0010125,0007651,0015773,
0022713,0062551,0040227,0071645,
0123303,0015732,0025731,0146570,
0123557,0064016,0002067,0067711,
0024215,0136214,0132374,0124234,
0024467,0051425,0071066,0064210,
0125075,0124305,0135123,0024170,
0125465,0010261,0005560,0034232,
0025674,0066602,0030724,0174557,
0026477,0151520,0051510,0067250,
0026352,0161076,0113154,0116271,
0127431,0116470,0177465,0127274,
0130056,0056174,0170315,0013321,
0130105,0020575,0075327,0036710,
0030762,0043625,0113046,0125035,
0031621,0033211,0154354,0022077,
0032406,0121555,0074270,0041141,
0033234,0000116,0041611,0173743,
0034207,0013263,0174715,0115563,
0035267,0063300,0175753,0117266,
0036522,0077633,0033255,0136200,
0040204,0130457,0014454,0166254
};
#endif

#ifdef IBMPC
static unsigned short SHI1[] = {
0x01b0,0xbd4a,0x3373,0x3c75,
0xb05e,0x2418,0x8a3d,0xbc9b,
0x7fe6,0x8248,0x724d,0x3cad,
0x7515,0x2c15,0xcc1a,0x3cd3,
0xbda0,0xbaaa,0x91b5,0xbd0d,
0xd1ae,0xbe40,0xb80c,0x3d30,
0xbf82,0xe110,0x8ba2,0xbd23,
0x3725,0x2541,0xa3bb,0xbd78,
0x9394,0x72b0,0xdea5,0x3da4,
0x17f7,0x33b0,0xc487,0xbdb1,
0x8aac,0xce48,0x734a,0xbde8,
0x3862,0x0207,0x4565,0x3e17,
0xfffc,0xd68b,0xbd4b,0xbe11,
0xdf61,0x2f23,0x2671,0xbe63,
0xac08,0x511c,0x6ff0,0x3e83,
0xfea3,0x3dcf,0x3d7c,0x3eaa,
0x24b1,0x5f32,0xa556,0xbed6,
0xd961,0x352e,0x61be,0xbf00,
0xf3bd,0x473b,0x559b,0x3f17,
0x567f,0x87db,0x97f5,0x3f60,
0xb51b,0xd464,0x5126,0x3f9e,
0xa8b4,0xac8c,0xe548,0x3ff1
};

static unsigned short SHI2[] = {
0x2b4c,0x8385,0x487f,0xbc68,
0x237f,0xa1f5,0x420a,0x3c7e,
0xee75,0x2812,0x6cad,0x3c99,
0x39af,0x457b,0x637b,0xbcb8,
0xedf9,0xc086,0xed01,0xbccd,
0x9513,0x969f,0xb791,0x3cf1,
0xcd11,0xae46,0xea62,0x3d06,
0x650f,0xb74a,0xb518,0xbd27,
0x0713,0x216e,0xa216,0xbd46,
0x9f2e,0x463a,0x8db0,0x3d57,
0x0dd5,0x0a69,0xfa6a,0x3d87,
0x9397,0xd2cd,0x5c47,0x3d7d,
0xb5d8,0x1fe6,0x33a7,0xbdc3,
0xa2da,0x9e19,0xcb8f,0xbde5,
0xe7b9,0xaf5a,0xa42f,0xbde8,
0xd544,0xb2c4,0x48f2,0x3e1e,
0x8488,0x3b1d,0x26d1,0x3e52,
0x084c,0xaf17,0xd46d,0x3e80,
0x3efc,0xc871,0x8009,0x3eb3,
0xb36e,0x7f39,0xe2d6,0x3ef0,
0x73d7,0x1f7d,0xecd8,0x3f36,
0xb790,0x66d5,0x4ff3,0x3f8a,
0x9d96,0xe325,0x9625,0x3ff0
};
#endif

#ifdef MIEEE
static unsigned short SHI1[] = {
0x3c75,0x3373,0xbd4a,0x01b0,
0xbc9b,0x8a3d,0x2418,0xb05e,
0x3cad,0x724d,0x8248,0x7fe6,
0x3cd3,0xcc1a,0x2c15,0x7515,
0xbd0d,0x91b5,0xbaaa,0xbda0,
0x3d30,0xb80c,0xbe40,0xd1ae,
0xbd23,0x8ba2,0xe110,0xbf82,
0xbd78,0xa3bb,0x2541,0x3725,
0x3da4,0xdea5,0x72b0,0x9394,
0xbdb1,0xc487,0x33b0,0x17f7,
0xbde8,0x734a,0xce48,0x8aac,
0x3e17,0x4565,0x0207,0x3862,
0xbe11,0xbd4b,0xd68b,0xfffc,
0xbe63,0x2671,0x2f23,0xdf61,
0x3e83,0x6ff0,0x511c,0xac08,
0x3eaa,0x3d7c,0x3dcf,0xfea3,
0xbed6,0xa556,0x5f32,0x24b1,
0xbf00,0x61be,0x352e,0xd961,
0x3f17,0x559b,0x473b,0xf3bd,
0x3f60,0x97f5,0x87db,0x567f,
0x3f9e,0x5126,0xd464,0xb51b,
0x3ff1,0xe548,0xac8c,0xa8b4
};

static unsigned short SHI2[] = {
0xbc68,0x487f,0x8385,0x2b4c,
0x3c7e,0x420a,0xa1f5,0x237f,
0x3c99,0x6cad,0x2812,0xee75,
0xbcb8,0x637b,0x457b,0x39af,
0xbccd,0xed01,0xc086,0xedf9,
0x3cf1,0xb791,0x969f,0x9513,
0x3d06,0xea62,0xae46,0xcd11,
0xbd27,0xb518,0xb74a,0x650f,
0xbd46,0xa216,0x216e,0x0713,
0x3d57,0x8db0,0x463a,0x9f2e,
0x3d87,0xfa6a,0x0a69,0x0dd5,
0x3d7d,0x5c47,0xd2cd,0x9397,
0xbdc3,0x33a7,0x1fe6,0xb5d8,
0xbde5,0xcb8f,0x9e19,0xa2da,
0xbde8,0xa42f,0xaf5a,0xe7b9,
0x3e1e,0x48f2,0xb2c4,0xd544,
0x3e52,0x26d1,0x3b1d,0x8488,
0x3e80,0xd46d,0xaf17,0x084c,
0x3eb3,0x8009,0xc871,0x3efc,
0x3ef0,0xe2d6,0x7f39,0xb36e,
0x3f36,0xecd8,0x1f7d,0x73d7,
0x3f8a,0x4ff3,0x66d5,0xb790,
0x3ff0,0x9625,0xe325,0x9d96
};
#endif


#ifdef UNK
/* x exp(-x) chin(x), inverted interval 8 to 18 */
static double CHI1[] = {
-8.12435385225864036372E-18,
 2.17586413290339214377E-17,
 5.22624394924072204667E-17,
-9.48812110591690559363E-16,
 5.35546311647465209166E-15,
-1.21009970113732918701E-14,
-6.00865178553447437951E-14,
 7.16339649156028587775E-13,
-2.93496072607599856104E-12,
-1.40359438136491256904E-12,
 8.76302288609054966081E-11,
-4.40092476213282340617E-10,
-1.87992075640569295479E-10,
 1.31458150989474594064E-8,
-4.75513930924765465590E-8,
-2.21775018801848880741E-7,
 1.94635531373272490962E-6,
 4.33505889257316408893E-6,
-6.13387001076494349496E-5,
-3.13085477492997465138E-4,
 4.97164789823116062801E-4,
 2.64347496031374526641E-2,
 1.11446150876699213025E0
};

/* x exp(-x) chin(x), inverted interval 18 to 88 */
static double CHI2[] = {
 8.06913408255155572081E-18,
-2.08074168180148170312E-17,
-5.98111329658272336816E-17,
 2.68533951085945765591E-16,
 4.52313941698904694774E-16,
-3.10734917335299464535E-15,
-4.42823207332531972288E-15,
 3.49639695410806959872E-14,
 6.63406731718911586609E-14,
-3.71902448093119218395E-13,
-1.27135418132338309016E-12,
 2.74851141935315395333E-12,
 2.33781843985453438400E-11,
 2.71436006377612442764E-11,
-2.56600180000355990529E-10,
-1.61021375163803438552E-9,
-4.72543064876271773512E-9,
-3.00095178028681682282E-9,
 7.79387474390914922337E-8,
 1.06942765566401507066E-6,
 1.59503164802313196374E-5,
 3.49592575153777996871E-4,
 1.28475387530065247392E-2,
 1.03665693917934275131E0
};
#endif

#ifdef DEC
static unsigned short CHI1[] = {
0122025,0157055,0021702,0021427,
0022310,0130043,0123265,0022340,
0022561,0002231,0017746,0013043,
0123610,0136375,0002352,0024467,
0024300,0171555,0141300,0000446,
0124531,0176777,0126210,0035616,
0125207,0046604,0167760,0077132,
0026111,0120666,0026606,0064143,
0126516,0103615,0054127,0005436,
0126305,0104721,0025415,0004134,
0027700,0131556,0164725,0157553,
0130361,0170602,0077274,0055406,
0130116,0131420,0125472,0017231,
0031541,0153747,0177312,0056304,
0132114,0035517,0041545,0043151,
0132556,0020415,0110044,0172442,
0033402,0117041,0031152,0010364,
0033621,0072737,0050647,0013720,
0134600,0121366,0140010,0063265,
0135244,0022637,0013756,0044742,
0035402,0052052,0006523,0043564,
0036730,0106660,0020277,0162146,
0040216,0123254,0135147,0005724
};

static unsigned short CHI2[] = {
0022024,0154550,0104311,0144257,
0122277,0165037,0133443,0155601,
0122611,0165102,0157053,0055252,
0023232,0146235,0153511,0113222,
0023402,0057340,0145304,0010471,
0124137,0164171,0113071,0100002,
0124237,0105473,0056130,0022022,
0025035,0073266,0056746,0164433,
0025225,0061313,0055600,0165407,
0125721,0056312,0107613,0051215,
0126262,0166534,0115336,0066653,
0026501,0064307,0127442,0065573,
0027315,0121375,0142020,0045356,
0027356,0140764,0070641,0046570,
0130215,0010503,0146335,0177737,
0130735,0047134,0015215,0163665,
0131242,0056523,0155276,0050053,
0131116,0034515,0050707,0163512,
0032247,0057507,0107545,0032007,
0033217,0104501,0021706,0025047,
0034205,0146413,0033746,0076562,
0035267,0044605,0065355,0002772,
0036522,0077173,0130716,0170304,
0040204,0130454,0130571,0027270
};
#endif

#ifdef IBMPC
static unsigned short CHI1[] = {
0x4463,0xa478,0xbbc5,0xbc62,
0xa49c,0x74d6,0x1604,0x3c79,
0xc2c4,0x23fc,0x2093,0x3c8e,
0x4527,0xa09d,0x179f,0xbcd1,
0x0025,0xb858,0x1e6d,0x3cf8,
0x0772,0xf591,0x3fbf,0xbd0b,
0x0fcb,0x9dfe,0xe9b0,0xbd30,
0xcd0c,0xc5b0,0x3436,0x3d69,
0xe164,0xab0a,0xd0f1,0xbd89,
0xa10c,0x2561,0xb13a,0xbd78,
0xbbed,0xdd3a,0x166d,0x3dd8,
0x8b61,0x4fd7,0x3e30,0xbdfe,
0x43d3,0x1567,0xd662,0xbde9,
0x4b98,0xffd9,0x3afc,0x3e4c,
0xa8cd,0xe86c,0x8769,0xbe69,
0x9ea4,0xb204,0xc421,0xbe8d,
0x421f,0x264d,0x53c4,0x3ec0,
0xe2fa,0xea34,0x2ebb,0x3ed2,
0x0cd7,0xd801,0x145e,0xbf10,
0xc93c,0xe2fd,0x84b3,0xbf34,
0x68ef,0x41aa,0x4a85,0x3f40,
0xfc8d,0x0417,0x11b6,0x3f9b,
0xe17b,0x974c,0xd4d5,0x3ff1
};

static unsigned short CHI2[] = {
0x3916,0x1119,0x9b2d,0x3c62,
0x7b70,0xf6e4,0xfd43,0xbc77,
0x6b55,0x5bc5,0x3d48,0xbc91,
0x32d2,0xbae9,0x5993,0x3cb3,
0x8227,0x1958,0x4bdc,0x3cc0,
0x3000,0x32c7,0xfd0f,0xbceb,
0x0482,0x6b8b,0xf167,0xbcf3,
0xdd23,0xcbbc,0xaed6,0x3d23,
0x1d61,0x6b70,0xac59,0x3d32,
0x6a52,0x51f1,0x2b99,0xbd5a,
0xcdb5,0x935b,0x5dab,0xbd76,
0x4d6f,0xf5e4,0x2d18,0x3d88,
0x095e,0xb882,0xb45f,0x3db9,
0x29af,0x8e34,0xd83e,0x3dbd,
0xbffc,0x799b,0xa228,0xbdf1,
0xbcf7,0x8351,0xa9cb,0xbe1b,
0xca05,0x7b57,0x4baa,0xbe34,
0xfce9,0xaa38,0xc729,0xbe29,
0xa681,0xf1ec,0xebe8,0x3e74,
0xc545,0x2478,0xf128,0x3eb1,
0xcfae,0x66fc,0xb9a1,0x3ef0,
0xa0bf,0xad5d,0xe930,0x3f36,
0xde19,0x7639,0x4fcf,0x3f8a,
0x25d7,0x962f,0x9625,0x3ff0
};
#endif

#ifdef MIEEE
static unsigned short CHI1[] = {
0xbc62,0xbbc5,0xa478,0x4463,
0x3c79,0x1604,0x74d6,0xa49c,
0x3c8e,0x2093,0x23fc,0xc2c4,
0xbcd1,0x179f,0xa09d,0x4527,
0x3cf8,0x1e6d,0xb858,0x0025,
0xbd0b,0x3fbf,0xf591,0x0772,
0xbd30,0xe9b0,0x9dfe,0x0fcb,
0x3d69,0x3436,0xc5b0,0xcd0c,
0xbd89,0xd0f1,0xab0a,0xe164,
0xbd78,0xb13a,0x2561,0xa10c,
0x3dd8,0x166d,0xdd3a,0xbbed,
0xbdfe,0x3e30,0x4fd7,0x8b61,
0xbde9,0xd662,0x1567,0x43d3,
0x3e4c,0x3afc,0xffd9,0x4b98,
0xbe69,0x8769,0xe86c,0xa8cd,
0xbe8d,0xc421,0xb204,0x9ea4,
0x3ec0,0x53c4,0x264d,0x421f,
0x3ed2,0x2ebb,0xea34,0xe2fa,
0xbf10,0x145e,0xd801,0x0cd7,
0xbf34,0x84b3,0xe2fd,0xc93c,
0x3f40,0x4a85,0x41aa,0x68ef,
0x3f9b,0x11b6,0x0417,0xfc8d,
0x3ff1,0xd4d5,0x974c,0xe17b
};

static unsigned short CHI2[] = {
0x3c62,0x9b2d,0x1119,0x3916,
0xbc77,0xfd43,0xf6e4,0x7b70,
0xbc91,0x3d48,0x5bc5,0x6b55,
0x3cb3,0x5993,0xbae9,0x32d2,
0x3cc0,0x4bdc,0x1958,0x8227,
0xbceb,0xfd0f,0x32c7,0x3000,
0xbcf3,0xf167,0x6b8b,0x0482,
0x3d23,0xaed6,0xcbbc,0xdd23,
0x3d32,0xac59,0x6b70,0x1d61,
0xbd5a,0x2b99,0x51f1,0x6a52,
0xbd76,0x5dab,0x935b,0xcdb5,
0x3d88,0x2d18,0xf5e4,0x4d6f,
0x3db9,0xb45f,0xb882,0x095e,
0x3dbd,0xd83e,0x8e34,0x29af,
0xbdf1,0xa228,0x799b,0xbffc,
0xbe1b,0xa9cb,0x8351,0xbcf7,
0xbe34,0x4baa,0x7b57,0xca05,
0xbe29,0xc729,0xaa38,0xfce9,
0x3e74,0xebe8,0xf1ec,0xa681,
0x3eb1,0xf128,0x2478,0xc545,
0x3ef0,0xb9a1,0x66fc,0xcfae,
0x3f36,0xe930,0xad5d,0xa0bf,
0x3f8a,0x4fcf,0x7639,0xde19,
0x3ff0,0x9625,0x962f,0x25d7
};
#endif



/* Sine and cosine integrals */


int shichi(double x, double* si, double* ci)
{
double k, z, c, s, a;
short sign;

if( x < 0.0 )
	{
	sign = -1;
	x = -x;
	}
else
	sign = 0;


if( x == 0.0 )
	{
	*si = 0.0;
	*ci = -MAXNUM;
	return( 0 );
	}

if( x >= 8.0 )
	goto chb;

z = x * x;

/*	Direct power series expansion	*/

a = 1.0;
s = 1.0;
c = 0.0;
k = 2.0;

do
	{
	a *= z/k;
	c += a/k;
	k += 1.0;
	a /= k;
	s += a/k;
	k += 1.0;
	}
while( fabs(a/s) > MACHEP );

s *= x;
goto done;


chb:

if( x < 18.0 )
	{
	a = (576.0/x - 52.0)/10.0;
	k = exp(x) / x;
	s = k * chbevl( a, SHI1, 22 );
	c = k * chbevl( a, CHI1, 23 );
	goto done;
	}

if( x <= 88.0 )
	{
	a = (6336.0/x - 212.0)/70.0;
	k = exp(x) / x;
	s = k * chbevl( a, SHI2, 23 );
	c = k * chbevl( a, CHI2, 24 );
	goto done;
	}
else
	{
	if( sign )
		*si = -MAXNUM;
	else
		*si = MAXNUM;
	*ci = MAXNUM;
	return(0);
	}
done:
if( sign )
	s = -s;

*si = s;

*ci = EUL + log(x) + c;
return(0);
}

/* ========================================================================= */

/*							sici.c
 *
 *	Sine and cosine integrals
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, Ci, Si, sici();
 *
 * sici( x, &Si, &Ci );
 *
 *
 * DESCRIPTION:
 *
 * Evaluates the integrals
 *
 *                          x
 *                          -
 *                         |  cos t - 1
 *   Ci(x) = eul + ln x +  |  --------- dt,
 *                         |      t
 *                        -
 *                         0
 *             x
 *             -
 *            |  sin t
 *   Si(x) =  |  ----- dt
 *            |    t
 *           -
 *            0
 *
 * where eul = 0.57721566490153286061 is Euler's constant.
 * The integrals are approximated by rational functions.
 * For x > 8 auxiliary functions f(x) and g(x) are employed
 * such that
 *
 * Ci(x) = f(x) sin(x) - g(x) cos(x)
 * Si(x) = pi/2 - f(x) cos(x) - g(x) sin(x)
 *
 *
 * ACCURACY:
 *    Test interval = [0,50].
 * Absolute error, except relative when > 1:
 * arithmetic   function   # trials      peak         rms
 *    IEEE        Si        30000       4.4e-16     7.3e-17
 *    IEEE        Ci        30000       6.9e-16     5.1e-17
 *    DEC         Si         5000       4.4e-17     9.0e-18
 *    DEC         Ci         5300       7.9e-17     5.2e-18
 */


#ifdef UNK
static double SIN[] = {
-8.39167827910303881427E-11,
 4.62591714427012837309E-8,
-9.75759303843632795789E-6,
 9.76945438170435310816E-4,
-4.13470316229406538752E-2,
 1.00000000000000000302E0,
};
static double SID[] = {
  2.03269266195951942049E-12,
  1.27997891179943299903E-9,
  4.41827842801218905784E-7,
  9.96412122043875552487E-5,
  1.42085239326149893930E-2,
  9.99999999999999996984E-1,
};
#endif
#ifdef DEC
static unsigned short SIN[] = {
0127670,0104362,0167505,0035161,
0032106,0127177,0032131,0056461,
0134043,0132213,0000476,0172351,
0035600,0006331,0064761,0032665,
0137051,0055601,0044667,0017645,
0040200,0000000,0000000,0000000,
};
static unsigned short SID[] = {
0026417,0004674,0052064,0001573,
0030657,0165501,0014666,0131526,
0032755,0032133,0034147,0024124,
0034720,0173167,0166624,0154477,
0036550,0145336,0063534,0063220,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short SIN[] = {
0xa74e,0x5de8,0x111e,0xbdd7,
0x2ba6,0xe68b,0xd5cf,0x3e68,
0xde9d,0x6027,0x7691,0xbee4,
0x26b7,0x2d3e,0x019b,0x3f50,
0xe3f5,0x2936,0x2b70,0xbfa5,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short SID[] = {
0x806f,0x8a86,0xe137,0x3d81,
0xd66b,0x2336,0xfd68,0x3e15,
0xe50a,0x670c,0xa68b,0x3e9d,
0x9b28,0xfdb2,0x1ece,0x3f1a,
0x8cd2,0xcceb,0x195b,0x3f8d,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short SIN[] = {
0xbdd7,0x111e,0x5de8,0xa74e,
0x3e68,0xd5cf,0xe68b,0x2ba6,
0xbee4,0x7691,0x6027,0xde9d,
0x3f50,0x019b,0x2d3e,0x26b7,
0xbfa5,0x2b70,0x2936,0xe3f5,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short SID[] = {
0x3d81,0xe137,0x8a86,0x806f,
0x3e15,0xfd68,0x2336,0xd66b,
0x3e9d,0xa68b,0x670c,0xe50a,
0x3f1a,0x1ece,0xfdb2,0x9b28,
0x3f8d,0x195b,0xcceb,0x8cd2,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif
#ifdef UNK
static double CIN[] = {
 2.02524002389102268789E-11,
-1.35249504915790756375E-8,
 3.59325051419993077021E-6,
-4.74007206873407909465E-4,
 2.89159652607555242092E-2,
-1.00000000000000000080E0,
};
static double CID[] = {
  4.07746040061880559506E-12,
  3.06780997581887812692E-9,
  1.23210355685883423679E-6,
  3.17442024775032769882E-4,
  5.10028056236446052392E-2,
  4.00000000000000000080E0,
};
#endif
#ifdef DEC
static unsigned short CIN[] = {
0027262,0022131,0160257,0020166,
0131550,0055534,0077637,0000557,
0033561,0021622,0161463,0026575,
0135370,0102053,0116333,0000466,
0036754,0160454,0122022,0024622,
0140200,0000000,0000000,0000000,
};
static unsigned short CID[] = {
0026617,0073177,0107543,0104425,
0031122,0150573,0156453,0041517,
0033245,0057301,0077706,0110510,
0035246,0067130,0165424,0044543,
0037120,0164121,0061206,0053657,
0040600,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short CIN[] = {
0xe40f,0x3c15,0x448b,0x3db6,
0xe02e,0x8ff3,0x0b6b,0xbe4d,
0x65b0,0x5c66,0x2472,0x3ece,
0x6027,0x739b,0x1085,0xbf3f,
0x4532,0x9482,0x9c25,0x3f9d,
0x0000,0x0000,0x0000,0xbff0,
};
static unsigned short CID[] = {
0x7123,0xf1ec,0xeecf,0x3d91,
0x686a,0x7ba5,0x5a2f,0x3e2a,
0xd229,0x2ff8,0xabd8,0x3eb4,
0x892c,0x1d62,0xcdcb,0x3f34,
0xcaf6,0x2c50,0x1d0a,0x3faa,
0x0000,0x0000,0x0000,0x4010,
};
#endif
#ifdef MIEEE
static unsigned short CIN[] = {
0x3db6,0x448b,0x3c15,0xe40f,
0xbe4d,0x0b6b,0x8ff3,0xe02e,
0x3ece,0x2472,0x5c66,0x65b0,
0xbf3f,0x1085,0x739b,0x6027,
0x3f9d,0x9c25,0x9482,0x4532,
0xbff0,0x0000,0x0000,0x0000,
};
static unsigned short CID[] = {
0x3d91,0xeecf,0xf1ec,0x7123,
0x3e2a,0x5a2f,0x7ba5,0x686a,
0x3eb4,0xabd8,0x2ff8,0xd229,
0x3f34,0xcdcb,0x1d62,0x892c,
0x3faa,0x1d0a,0x2c50,0xcaf6,
0x4010,0x0000,0x0000,0x0000,
};
#endif


#ifdef UNK
static double FN4[] = {
  4.23612862892216586994E0,
  5.45937717161812843388E0,
  1.62083287701538329132E0,
  1.67006611831323023771E-1,
  6.81020132472518137426E-3,
  1.08936580650328664411E-4,
  5.48900223421373614008E-7,
};
static double FD4[] = {
/*  1.00000000000000000000E0,*/
  8.16496634205391016773E0,
  7.30828822505564552187E0,
  1.86792257950184183883E0,
  1.78792052963149907262E-1,
  7.01710668322789753610E-3,
  1.10034357153915731354E-4,
  5.48900252756255700982E-7,
};
#endif
#ifdef DEC
static unsigned short FN4[] = {
0040607,0107135,0120133,0153471,
0040656,0131467,0140424,0017567,
0040317,0073563,0121610,0002511,
0037453,0001710,0000040,0006334,
0036337,0024033,0176003,0171425,
0034744,0072341,0121657,0126035,
0033023,0054042,0154652,0000451,
};
static unsigned short FD4[] = {
/*0040200,0000000,0000000,0000000,*/
0041002,0121663,0137500,0177450,
0040751,0156577,0042213,0061552,
0040357,0014026,0045465,0147265,
0037467,0012503,0110413,0131772,
0036345,0167701,0155706,0160551,
0034746,0141076,0162250,0123547,
0033023,0054043,0056706,0151050,
};
#endif
#ifdef IBMPC
static unsigned short FN4[] = {
0x7ae7,0xb40b,0xf1cb,0x4010,
0x83ef,0xf822,0xd666,0x4015,
0x00a9,0x7471,0xeeee,0x3ff9,
0x019c,0x0004,0x6079,0x3fc5,
0x7e63,0x7f80,0xe503,0x3f7b,
0xf584,0x3475,0x8e9c,0x3f1c,
0x4025,0x5b35,0x6b04,0x3ea2,
};
static unsigned short FD4[] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x1fe5,0x77e8,0x5476,0x4020,
0x6c6d,0xe891,0x3baf,0x401d,
0xb9d7,0xc966,0xe302,0x3ffd,
0x767f,0x7221,0xe2a8,0x3fc6,
0xdc2d,0x3b78,0xbdf8,0x3f7c,
0x14ed,0xdc95,0xd847,0x3f1c,
0xda45,0x6bb8,0x6b04,0x3ea2,
};
#endif
#ifdef MIEEE
static unsigned short FN4[] = {
0x4010,0xf1cb,0xb40b,0x7ae7,
0x4015,0xd666,0xf822,0x83ef,
0x3ff9,0xeeee,0x7471,0x00a9,
0x3fc5,0x6079,0x0004,0x019c,
0x3f7b,0xe503,0x7f80,0x7e63,
0x3f1c,0x8e9c,0x3475,0xf584,
0x3ea2,0x6b04,0x5b35,0x4025,
};
static unsigned short FD4[] = {
/* 0x3ff0,0x0000,0x0000,0x0000,*/
0x4020,0x5476,0x77e8,0x1fe5,
0x401d,0x3baf,0xe891,0x6c6d,
0x3ffd,0xe302,0xc966,0xb9d7,
0x3fc6,0xe2a8,0x7221,0x767f,
0x3f7c,0xbdf8,0x3b78,0xdc2d,
0x3f1c,0xd847,0xdc95,0x14ed,
0x3ea2,0x6b04,0x6bb8,0xda45,
};
#endif

#ifdef UNK
static double FN8[] = {
  4.55880873470465315206E-1,
  7.13715274100146711374E-1,
  1.60300158222319456320E-1,
  1.16064229408124407915E-2,
  3.49556442447859055605E-4,
  4.86215430826454749482E-6,
  3.20092790091004902806E-8,
  9.41779576128512936592E-11,
  9.70507110881952024631E-14,
};
static double FD8[] = {
/*  1.00000000000000000000E0,*/
  9.17463611873684053703E-1,
  1.78685545332074536321E-1,
  1.22253594771971293032E-2,
  3.58696481881851580297E-4,
  4.92435064317881464393E-6,
  3.21956939101046018377E-8,
  9.43720590350276732376E-11,
  9.70507110881952025725E-14,
};
#endif
#ifdef DEC
static unsigned short FN8[] = {
0037751,0064467,0142332,0164573,
0040066,0133013,0050352,0071102,
0037444,0022671,0102157,0013535,
0036476,0024335,0136423,0146444,
0035267,0042253,0164110,0110460,
0033643,0022626,0062535,0060320,
0032011,0075223,0010110,0153413,
0027717,0014572,0011360,0014034,
0025332,0104755,0004563,0152354,
};
static unsigned short FD8[] = {
/*0040200,0000000,0000000,0000000,*/
0040152,0157345,0030104,0075616,
0037466,0174527,0172740,0071060,
0036510,0046337,0144272,0156552,
0035274,0007555,0042537,0015572,
0033645,0035731,0112465,0026474,
0032012,0043612,0030613,0030123,
0027717,0103277,0004564,0151000,
0025332,0104755,0004563,0152354,
};
#endif
#ifdef IBMPC
static unsigned short FN8[] = {
0x5d2f,0xf89b,0x2d26,0x3fdd,
0x4e48,0x6a1d,0xd6c1,0x3fe6,
0xe2ec,0x308d,0x84b7,0x3fc4,
0x79a4,0xb7a2,0xc51b,0x3f87,
0x1226,0x7d09,0xe895,0x3f36,
0xac1a,0xccab,0x64b2,0x3ed4,
0x1ae1,0x6209,0x2f52,0x3e61,
0x0304,0x425e,0xe32f,0x3dd9,
0x7a9d,0xa12e,0x513d,0x3d3b,
};
static unsigned short FD8[] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x8f72,0xa608,0x5bdc,0x3fed,
0x0e46,0xfebc,0xdf2a,0x3fc6,
0x5bad,0xf917,0x099b,0x3f89,
0xe36f,0xa8ab,0x81ed,0x3f37,
0xa5a8,0x32a6,0xa77b,0x3ed4,
0x660a,0x4631,0x48f1,0x3e61,
0x9a40,0xe12e,0xf0d7,0x3dd9,
0x7a9d,0xa12e,0x513d,0x3d3b,
};
#endif
#ifdef MIEEE
static unsigned short FN8[] = {
0x3fdd,0x2d26,0xf89b,0x5d2f,
0x3fe6,0xd6c1,0x6a1d,0x4e48,
0x3fc4,0x84b7,0x308d,0xe2ec,
0x3f87,0xc51b,0xb7a2,0x79a4,
0x3f36,0xe895,0x7d09,0x1226,
0x3ed4,0x64b2,0xccab,0xac1a,
0x3e61,0x2f52,0x6209,0x1ae1,
0x3dd9,0xe32f,0x425e,0x0304,
0x3d3b,0x513d,0xa12e,0x7a9d,
};
static unsigned short FD8[] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x3fed,0x5bdc,0xa608,0x8f72,
0x3fc6,0xdf2a,0xfebc,0x0e46,
0x3f89,0x099b,0xf917,0x5bad,
0x3f37,0x81ed,0xa8ab,0xe36f,
0x3ed4,0xa77b,0x32a6,0xa5a8,
0x3e61,0x48f1,0x4631,0x660a,
0x3dd9,0xf0d7,0xe12e,0x9a40,
0x3d3b,0x513d,0xa12e,0x7a9d,
};
#endif

#ifdef UNK
static double GN4[] = {
  8.71001698973114191777E-2,
  6.11379109952219284151E-1,
  3.97180296392337498885E-1,
  7.48527737628469092119E-2,
  5.38868681462177273157E-3,
  1.61999794598934024525E-4,
  1.97963874140963632189E-6,
  7.82579040744090311069E-9,
};
static double GD4[] = {
/*  1.00000000000000000000E0,*/
  1.64402202413355338886E0,
  6.66296701268987968381E-1,
  9.88771761277688796203E-2,
  6.22396345441768420760E-3,
  1.73221081474177119497E-4,
  2.02659182086343991969E-6,
  7.82579218933534490868E-9,
};
#endif
#ifdef DEC
static unsigned short GN4[] = {
0037262,0060622,0164572,0157515,
0040034,0101527,0061263,0147204,
0037713,0055467,0037475,0144512,
0037231,0046151,0035234,0045261,
0036260,0111624,0150617,0053536,
0035051,0157175,0016675,0155456,
0033404,0154757,0041211,0000055,
0031406,0071060,0130322,0033322,
};
static unsigned short GD4[] = {
/* 0040200,0000000,0000000,0000000,*/
0040322,0067520,0046707,0053275,
0040052,0111153,0126542,0005516,
0037312,0100035,0167121,0014552,
0036313,0171143,0137176,0014213,
0035065,0121256,0012033,0150603,
0033410,0000225,0013121,0071643,
0031406,0071062,0131152,0150454,
};
#endif
#ifdef IBMPC
static unsigned short GN4[] = {
0x5bea,0x5d2f,0x4c32,0x3fb6,
0x79d1,0xec56,0x906a,0x3fe3,
0xb929,0xe7e7,0x6b66,0x3fd9,
0x8956,0x2753,0x298d,0x3fb3,
0xeaec,0x9a31,0x1272,0x3f76,
0xbb66,0xa3b7,0x3bcf,0x3f25,
0x2006,0xe851,0x9b3d,0x3ec0,
0x46da,0x161a,0xce46,0x3e40,
};
static unsigned short GD4[] = {
/* 0x0000,0x0000,0x0000,0x3ff0,*/
0xead8,0x09b8,0x4dea,0x3ffa,
0x416a,0x75ac,0x524d,0x3fe5,
0x232d,0xbdca,0x5003,0x3fb9,
0xc311,0x77cf,0x7e4c,0x3f79,
0x7a30,0xc283,0xb455,0x3f26,
0x2e74,0xa2ca,0x0012,0x3ec1,
0x5a26,0x564d,0xce46,0x3e40,
};
#endif
#ifdef MIEEE
static unsigned short GN4[] = {
0x3fb6,0x4c32,0x5d2f,0x5bea,
0x3fe3,0x906a,0xec56,0x79d1,
0x3fd9,0x6b66,0xe7e7,0xb929,
0x3fb3,0x298d,0x2753,0x8956,
0x3f76,0x1272,0x9a31,0xeaec,
0x3f25,0x3bcf,0xa3b7,0xbb66,
0x3ec0,0x9b3d,0xe851,0x2006,
0x3e40,0xce46,0x161a,0x46da,
};
static unsigned short GD4[] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x3ffa,0x4dea,0x09b8,0xead8,
0x3fe5,0x524d,0x75ac,0x416a,
0x3fb9,0x5003,0xbdca,0x232d,
0x3f79,0x7e4c,0x77cf,0xc311,
0x3f26,0xb455,0xc283,0x7a30,
0x3ec1,0x0012,0xa2ca,0x2e74,
0x3e40,0xce46,0x564d,0x5a26,
};
#endif

#ifdef UNK
static double GN8[] = {
  6.97359953443276214934E-1,
  3.30410979305632063225E-1,
  3.84878767649974295920E-2,
  1.71718239052347903558E-3,
  3.48941165502279436777E-5,
  3.47131167084116673800E-7,
  1.70404452782044526189E-9,
  3.85945925430276600453E-12,
  3.14040098946363334640E-15,
};
static double GD8[] = {
/*  1.00000000000000000000E0,*/
  1.68548898811011640017E0,
  4.87852258695304967486E-1,
  4.67913194259625806320E-2,
  1.90284426674399523638E-3,
  3.68475504442561108162E-5,
  3.57043223443740838771E-7,
  1.72693748966316146736E-9,
  3.87830166023954706752E-12,
  3.14040098946363335242E-15,
};
#endif
#ifdef DEC
static unsigned short GN8[] = {
0040062,0103056,0110624,0033123,
0037651,0025640,0136266,0145647,
0037035,0122566,0137770,0061777,
0035741,0011424,0065311,0013370,
0034422,0055505,0134324,0016755,
0032672,0056530,0022565,0014747,
0030752,0031674,0114735,0013162,
0026607,0145353,0022020,0123625,
0024142,0045054,0060033,0016505,
};
static unsigned short GD8[] = {
/*0040200,0000000,0000000,0000000,*/
0040327,0137032,0064331,0136425,
0037771,0143705,0070300,0105711,
0037077,0124101,0025275,0035356,
0035771,0064333,0145103,0105357,
0034432,0106301,0105311,0010713,
0032677,0127645,0120034,0157551,
0030755,0054466,0010743,0105566,
0026610,0072242,0142530,0135744,
0024142,0045054,0060033,0016505,
};
#endif
#ifdef IBMPC
static unsigned short GN8[] = {
0x86ca,0xd232,0x50c5,0x3fe6,
0xd975,0x1796,0x2574,0x3fd5,
0x0c80,0xd7ff,0xb4ae,0x3fa3,
0x22df,0x8d59,0x2262,0x3f5c,
0x83be,0xb71a,0x4b68,0x3f02,
0xa33d,0x04ae,0x4bab,0x3e97,
0xa2ce,0x933b,0x4677,0x3e1d,
0x14f3,0x6482,0xf95d,0x3d90,
0x63a9,0x8c03,0x4945,0x3cec,
};
static unsigned short GD8[] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x37a3,0x4d1b,0xf7c3,0x3ffa,
0x1179,0xae18,0x38f8,0x3fdf,
0xa75e,0x2557,0xf508,0x3fa7,
0x715e,0x7948,0x2d1b,0x3f5f,
0x2239,0x3159,0x5198,0x3f03,
0x9bed,0xb403,0xf5f4,0x3e97,
0x716f,0xc23c,0xab26,0x3e1d,
0x177c,0x58ab,0x0e94,0x3d91,
0x63a9,0x8c03,0x4945,0x3cec,
};
#endif
#ifdef MIEEE
static unsigned short GN8[] = {
0x3fe6,0x50c5,0xd232,0x86ca,
0x3fd5,0x2574,0x1796,0xd975,
0x3fa3,0xb4ae,0xd7ff,0x0c80,
0x3f5c,0x2262,0x8d59,0x22df,
0x3f02,0x4b68,0xb71a,0x83be,
0x3e97,0x4bab,0x04ae,0xa33d,
0x3e1d,0x4677,0x933b,0xa2ce,
0x3d90,0xf95d,0x6482,0x14f3,
0x3cec,0x4945,0x8c03,0x63a9,
};
static unsigned short GD8[] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x3ffa,0xf7c3,0x4d1b,0x37a3,
0x3fdf,0x38f8,0xae18,0x1179,
0x3fa7,0xf508,0x2557,0xa75e,
0x3f5f,0x2d1b,0x7948,0x715e,
0x3f03,0x5198,0x3159,0x2239,
0x3e97,0xf5f4,0xb403,0x9bed,
0x3e1d,0xab26,0xc23c,0x716f,
0x3d91,0x0e94,0x58ab,0x177c,
0x3cec,0x4945,0x8c03,0x63a9,
};
#endif



int sici(double x, double* si, double* ci)
{
double z, c, s, f, g;
short sign;

if( x < 0.0 )
	{
	sign = -1;
	x = -x;
	}
else
	sign = 0;


if( x == 0.0 )
	{
	*si = 0.0;
	*ci = -MAXNUM;
	return( 0 );
	}


if( x > 1.0e9 )
	{
	*si = PIO2 - cos(x)/x;
	*ci = sin(x)/x;
	return( 0 );
	}



if( x > 4.0 )
	goto asympt;

z = x * x;
s = x * polevl( z, SIN, 5 ) / polevl( z, SID, 5 );
c = z * polevl( z, CIN, 5 ) / polevl( z, CID, 5 );

if( sign )
	s = -s;
*si = s;
*ci = EUL + log(x) + c;	/* real part if x < 0 */
return(0);



/* The auxiliary functions are:
 *
 *
 * *si = *si - PIO2;
 * c = cos(x);
 * s = sin(x);
 *
 * t = *ci * s - *si * c;
 * a = *ci * c + *si * s;
 *
 * *si = t;
 * *ci = -a;
 */


asympt:

s = sin(x);
c = cos(x);
z = 1.0/(x*x);
if( x < 8.0 )
	{
	f = polevl( z, FN4, 6 ) / (x * p1evl( z, FD4, 7 ));
	g = z * polevl( z, GN4, 7 ) / p1evl( z, GD4, 7 );
	}
else
	{
	f = polevl( z, FN8, 8 ) / (x * p1evl( z, FD8, 8 ));
	g = z * polevl( z, GN8, 8 ) / p1evl( z, GD8, 9 );
	}
*si = PIO2 - f * c - g * s;
if( sign )
	*si = -( *si );
*ci = f * s - g * c;

return(0);
}



/* ========================================================================= */

/*							beta.c
 *
 *	Beta function
 *
 *
 *
 * SYNOPSIS:
 *
 * double a, b, y, beta();
 *
 * y = beta( a, b );
 *
 *
 *
 * DESCRIPTION:
 *
 *                   -     -
 *                  | (a) | (b)
 * beta( a, b )  =  -----------.
 *                     -
 *                    | (a+b)
 *
 * For large arguments the logarithm of the function is
 * evaluated using lgam(), then exponentiated.
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC        0,30        1700       7.7e-15     1.5e-15
 *    IEEE       0,30       30000       8.1e-14     1.1e-14
 *
 * ERROR MESSAGES:
 *
 *   message         condition          value returned
 * beta overflow    log(beta) > MAXLOG       0.0
 *                  a or b <0 integer        0.0
 *
 */

/*							beta.c	*/



double beta(double a, double b)
{
double y;
int sign;

sign = 1;

if( a <= 0.0 )
	{
	if( a == floor(a) )
		goto over;
	}
if( b <= 0.0 )
	{
	if( b == floor(b) )
		goto over;
	}


y = a + b;
if( fabs(y) > MAXGAM )
	{
	y = lgamma(y);
	sign *= sgngam; /* keep track of the sign */
	y = lgamma(b) - y;
	sign *= sgngam;
	y = lgamma(a) + y;
	sign *= sgngam;
	if( y > MAXLOG )
		{
over:
		mtherr( "beta", OVERFLOW );
		return( sign * MAXNUM );
		}
	return( sign * exp(y) );
	}

y = cephesgamma(y);
if( y == 0.0 )
	goto over;

if( a > b )
	{
	y = cephesgamma(a)/y;
	y *= cephesgamma(b);
	}
else
	{
	y = cephesgamma(b)/y;
	y *= cephesgamma(a);
	}

return(y);
}



/* Natural log of |beta|.  Return the sign of beta in sgngam.  */

double lbeta(double a, double b)
{
double y;
int sign;

sign = 1;

if( a <= 0.0 )
	{
	if( a == floor(a) )
		goto over;
	}
if( b <= 0.0 )
	{
	if( b == floor(b) )
		goto over;
	}


y = a + b;
if( fabs(y) > MAXGAM )
	{
	y = lgamma(y);
	sign *= sgngam; /* keep track of the sign */
	y = lgamma(b) - y;
	sign *= sgngam;
	y = lgamma(a) + y;
	sign *= sgngam;
	sgngam = sign;
	return( y );
	}

y = cephesgamma(y);
if( y == 0.0 )
	{
over:
	mtherr( "lbeta", OVERFLOW );
	return( sign * MAXNUM );
	}

if( a > b )
	{
	y = cephesgamma(a)/y;
	y *= cephesgamma(b);
	}
else
	{
	y = cephesgamma(b)/y;
	y *= cephesgamma(a);
	}

if( y < 0 )
  {
    sgngam = -1;
    y = -y;
  }
else
  sgngam = 1;

return( log(y) );
}
/*							fac.c
 *
 *	Factorial function
 *
 *
 *
 * SYNOPSIS:
 *
 * double y, fac();
 * int i;
 *
 * y = fac( i );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns factorial of i  =  1 * 2 * 3 * ... * i.
 * fac(0) = 1.0.
 *
 * Due to machine arithmetic bounds the largest value of
 * i accepted is 33 in DEC arithmetic or 170 in IEEE
 * arithmetic.  Greater values, or negative ones,
 * produce an error message and return MAXNUM.
 *
 *
 *
 * ACCURACY:
 *
 * For i < 34 the values are simply tabulated, and have
 * full machine accuracy.  If i > 55, fac(i) = gamma(i+1);
 * see gamma.c.
 *
 *                      Relative error:
 * arithmetic   domain      peak
 *    IEEE      0, 170    1.4e-15
 *    DEC       0, 33      1.4e-17
 *
 */



/* Factorials of integers from 0 through 33 */
#ifdef UNK
static double factbl[] = {
  1.00000000000000000000E0,
  1.00000000000000000000E0,
  2.00000000000000000000E0,
  6.00000000000000000000E0,
  2.40000000000000000000E1,
  1.20000000000000000000E2,
  7.20000000000000000000E2,
  5.04000000000000000000E3,
  4.03200000000000000000E4,
  3.62880000000000000000E5,
  3.62880000000000000000E6,
  3.99168000000000000000E7,
  4.79001600000000000000E8,
  6.22702080000000000000E9,
  8.71782912000000000000E10,
  1.30767436800000000000E12,
  2.09227898880000000000E13,
  3.55687428096000000000E14,
  6.40237370572800000000E15,
  1.21645100408832000000E17,
  2.43290200817664000000E18,
  5.10909421717094400000E19,
  1.12400072777760768000E21,
  2.58520167388849766400E22,
  6.20448401733239439360E23,
  1.55112100433309859840E25,
  4.03291461126605635584E26,
  1.0888869450418352160768E28,
  3.04888344611713860501504E29,
  8.841761993739701954543616E30,
  2.6525285981219105863630848E32,
  8.22283865417792281772556288E33,
  2.6313083693369353016721801216E35,
  8.68331761881188649551819440128E36
};
#define MAXFAC 33
#endif

#ifdef DEC
static unsigned short factbl[] = {
0040200,0000000,0000000,0000000,
0040200,0000000,0000000,0000000,
0040400,0000000,0000000,0000000,
0040700,0000000,0000000,0000000,
0041300,0000000,0000000,0000000,
0041760,0000000,0000000,0000000,
0042464,0000000,0000000,0000000,
0043235,0100000,0000000,0000000,
0044035,0100000,0000000,0000000,
0044661,0030000,0000000,0000000,
0045535,0076000,0000000,0000000,
0046430,0042500,0000000,0000000,
0047344,0063740,0000000,0000000,
0050271,0112146,0000000,0000000,
0051242,0060731,0040000,0000000,
0052230,0035673,0126000,0000000,
0053230,0035673,0126000,0000000,
0054241,0137567,0063300,0000000,
0055265,0173546,0051630,0000000,
0056330,0012711,0101504,0100000,
0057407,0006635,0171012,0150000,
0060461,0040737,0046656,0030400,
0061563,0135223,0005317,0101540,
0062657,0027031,0127705,0023155,
0064003,0061223,0041723,0156322,
0065115,0045006,0014773,0004410,
0066246,0146044,0172433,0173526,
0067414,0136077,0027317,0114261,
0070566,0044556,0110753,0045465,
0071737,0031214,0032075,0036050,
0073121,0037543,0070371,0064146,
0074312,0132550,0052561,0116443,
0075512,0132550,0052561,0116443,
0076721,0005423,0114035,0025014
};
#define MAXFAC 33
#endif

#ifdef IBMPC
static unsigned short factbl[] = {
0x0000,0x0000,0x0000,0x3ff0,
0x0000,0x0000,0x0000,0x3ff0,
0x0000,0x0000,0x0000,0x4000,
0x0000,0x0000,0x0000,0x4018,
0x0000,0x0000,0x0000,0x4038,
0x0000,0x0000,0x0000,0x405e,
0x0000,0x0000,0x8000,0x4086,
0x0000,0x0000,0xb000,0x40b3,
0x0000,0x0000,0xb000,0x40e3,
0x0000,0x0000,0x2600,0x4116,
0x0000,0x0000,0xaf80,0x414b,
0x0000,0x0000,0x08a8,0x4183,
0x0000,0x0000,0x8cfc,0x41bc,
0x0000,0xc000,0x328c,0x41f7,
0x0000,0x2800,0x4c3b,0x4234,
0x0000,0x7580,0x0777,0x4273,
0x0000,0x7580,0x0777,0x42b3,
0x0000,0xecd8,0x37ee,0x42f4,
0x0000,0xca73,0xbeec,0x4336,
0x9000,0x3068,0x02b9,0x437b,
0x5a00,0xbe41,0xe1b3,0x43c0,
0xc620,0xe9b5,0x283b,0x4406,
0xf06c,0x6159,0x7752,0x444e,
0xa4ce,0x35f8,0xe5c3,0x4495,
0x7b9a,0x687a,0x6c52,0x44e0,
0x6121,0xc33f,0xa940,0x4529,
0x7eeb,0x9ea3,0xd984,0x4574,
0xf316,0xe5d9,0x9787,0x45c1,
0x6967,0xd23d,0xc92d,0x460e,
0xa785,0x8687,0xe651,0x465b,
0x2d0d,0x6e1f,0x27ec,0x46aa,
0x33a4,0x0aae,0x56ad,0x46f9,
0x33a4,0x0aae,0x56ad,0x4749,
0xa541,0x7303,0x2162,0x479a
};
#define MAXFAC 170
#endif

#ifdef MIEEE
static unsigned short factbl[] = {
0x3ff0,0x0000,0x0000,0x0000,
0x3ff0,0x0000,0x0000,0x0000,
0x4000,0x0000,0x0000,0x0000,
0x4018,0x0000,0x0000,0x0000,
0x4038,0x0000,0x0000,0x0000,
0x405e,0x0000,0x0000,0x0000,
0x4086,0x8000,0x0000,0x0000,
0x40b3,0xb000,0x0000,0x0000,
0x40e3,0xb000,0x0000,0x0000,
0x4116,0x2600,0x0000,0x0000,
0x414b,0xaf80,0x0000,0x0000,
0x4183,0x08a8,0x0000,0x0000,
0x41bc,0x8cfc,0x0000,0x0000,
0x41f7,0x328c,0xc000,0x0000,
0x4234,0x4c3b,0x2800,0x0000,
0x4273,0x0777,0x7580,0x0000,
0x42b3,0x0777,0x7580,0x0000,
0x42f4,0x37ee,0xecd8,0x0000,
0x4336,0xbeec,0xca73,0x0000,
0x437b,0x02b9,0x3068,0x9000,
0x43c0,0xe1b3,0xbe41,0x5a00,
0x4406,0x283b,0xe9b5,0xc620,
0x444e,0x7752,0x6159,0xf06c,
0x4495,0xe5c3,0x35f8,0xa4ce,
0x44e0,0x6c52,0x687a,0x7b9a,
0x4529,0xa940,0xc33f,0x6121,
0x4574,0xd984,0x9ea3,0x7eeb,
0x45c1,0x9787,0xe5d9,0xf316,
0x460e,0xc92d,0xd23d,0x6967,
0x465b,0xe651,0x8687,0xa785,
0x46aa,0x27ec,0x6e1f,0x2d0d,
0x46f9,0x56ad,0x0aae,0x33a4,
0x4749,0x56ad,0x0aae,0x33a4,
0x479a,0x2162,0x7303,0xa541
};
#define MAXFAC 170
#endif


double fac(int i)
{
double x, f, n;
int j;

if( i < 0 )
	{
	mtherr( "fac", SING );
	return( MAXNUM );
	}

if( i > MAXFAC )
	{
	mtherr( "fac", OVERFLOW );
	return( MAXNUM );
	}

/* Get answer from table for small i. */
if( i < 34 )
	{
#ifdef UNK
	return( factbl[i] );
#else
	return( *(double *)(&factbl[4*i]) );
#endif
	}
/* Use gamma function for large i. */
if( i > 55 )
	{
	x = i + 1;
	return( cephesgamma(x) );
	}
/* Compute directly for intermediate i. */
n = 34.0;
f = 34.0;
for( j=35; j<=i; j++ )
	{
	n += 1.0;
	f *= n;
	}
#ifdef UNK
	f *= factbl[33];
#else
	f *= *(double *)(&factbl[4*33]);
#endif
return( f );
}
/*							gamma.c
 *
 *	Gamma function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, gamma();
 * extern int sgngam;
 *
 * y = gamma( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns gamma function of the argument.  The result is
 * correctly signed, and the sign (+1 or -1) is also
 * returned in a global (extern) variable named sgngam.
 * This variable is also filled in by the logarithmic gamma
 * function lgam().
 *
 * Arguments |x| <= 34 are reduced by recurrence and the function
 * approximated by a rational function of degree 6/7 in the
 * interval (2,3).  Large arguments are handled by Stirling's
 * formula. Large negative arguments are made positive using
 * a reflection formula.  
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC      -34, 34      10000       1.3e-16     2.5e-17
 *    IEEE    -170,-33      20000       2.3e-15     3.3e-16
 *    IEEE     -33,  33     20000       9.4e-16     2.2e-16
 *    IEEE      33, 171.6   20000       2.3e-15     3.2e-16
 *
 * Error for arguments outside the test range will be larger
 * owing to error amplification by the exponential function.
 *
 */
/*							lgam()
 *
 *	Natural logarithm of gamma function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, lgam();
 * extern int sgngam;
 *
 * y = lgam( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the base e (2.718...) logarithm of the absolute
 * value of the gamma function of the argument.
 * The sign (+1 or -1) of the gamma function is returned in a
 * global (extern) variable named sgngam.
 *
 * For arguments greater than 13, the logarithm of the gamma
 * function is approximated by the logarithmic version of
 * Stirling's formula using a polynomial approximation of
 * degree 4. Arguments between -33 and +33 are reduced by
 * recurrence to the interval [2,3] of a rational approximation.
 * The cosecant reflection formula is employed for arguments
 * less than -33.
 *
 * Arguments greater than MAXLGM return MAXNUM and an error
 * message.  MAXLGM = 2.035093e36 for DEC
 * arithmetic or 2.556348e305 for IEEE arithmetic.
 *
 *
 *
 * ACCURACY:
 *
 *
 * arithmetic      domain        # trials     peak         rms
 *    DEC     0, 3                  7000     5.2e-17     1.3e-17
 *    DEC     2.718, 2.035e36       5000     3.9e-17     9.9e-18
 *    IEEE    0, 3                 28000     5.4e-16     1.1e-16
 *    IEEE    2.718, 2.556e305     40000     3.5e-16     8.3e-17
 * The error criterion was relative when the function magnitude
 * was greater than one but absolute when it was less than one.
 *
 * The following test used the relative error criterion, though
 * at certain points the relative error could be much higher than
 * indicated.
 *    IEEE    -200, -4             10000     4.8e-16     1.3e-16
 *
 */

/*							gamma.c	*/
/*	gamma function	*/



#ifndef HAVE_GAMMA
#ifdef UNK
static double P[] = {
  1.60119522476751861407E-4,
  1.19135147006586384913E-3,
  1.04213797561761569935E-2,
  4.76367800457137231464E-2,
  2.07448227648435975150E-1,
  4.94214826801497100753E-1,
  9.99999999999999996796E-1
};
static double Q[] = {
-2.31581873324120129819E-5,
 5.39605580493303397842E-4,
-4.45641913851797240494E-3,
 1.18139785222060435552E-2,
 3.58236398605498653373E-2,
-2.34591795718243348568E-1,
 7.14304917030273074085E-2,
 1.00000000000000000320E0
};
#endif

#ifdef DEC
static unsigned short P[] = {
0035047,0162701,0146301,0005234,
0035634,0023437,0032065,0176530,
0036452,0137157,0047330,0122574,
0037103,0017310,0143041,0017232,
0037524,0066516,0162563,0164605,
0037775,0004671,0146237,0014222,
0040200,0000000,0000000,0000000
};
static unsigned short Q[] = {
0134302,0041724,0020006,0116565,
0035415,0072121,0044251,0025634,
0136222,0003447,0035205,0121114,
0036501,0107552,0154335,0104271,
0037022,0135717,0014776,0171471,
0137560,0034324,0165024,0037021,
0037222,0045046,0047151,0161213,
0040200,0000000,0000000,0000000
};
#endif

#ifdef IBMPC
static unsigned short P[] = {
0x2153,0x3998,0xfcb8,0x3f24,
0xbfab,0xe686,0x84e3,0x3f53,
0x14b0,0xe9db,0x57cd,0x3f85,
0x23d3,0x18c4,0x63d9,0x3fa8,
0x7d31,0xdcae,0x8da9,0x3fca,
0xe312,0x3993,0xa137,0x3fdf,
0x0000,0x0000,0x0000,0x3ff0
};
static unsigned short Q[] = {
0xd3af,0x8400,0x487a,0xbef8,
0x2573,0x2915,0xae8a,0x3f41,
0xb44a,0xe750,0x40e4,0xbf72,
0xb117,0x5b1b,0x31ed,0x3f88,
0xde67,0xe33f,0x5779,0x3fa2,
0x87c2,0x9d42,0x071a,0xbfce,
0x3c51,0xc9cd,0x4944,0x3fb2,
0x0000,0x0000,0x0000,0x3ff0
};
#endif 

#ifdef MIEEE
static unsigned short P[] = {
0x3f24,0xfcb8,0x3998,0x2153,
0x3f53,0x84e3,0xe686,0xbfab,
0x3f85,0x57cd,0xe9db,0x14b0,
0x3fa8,0x63d9,0x18c4,0x23d3,
0x3fca,0x8da9,0xdcae,0x7d31,
0x3fdf,0xa137,0x3993,0xe312,
0x3ff0,0x0000,0x0000,0x0000
};
static unsigned short Q[] = {
0xbef8,0x487a,0x8400,0xd3af,
0x3f41,0xae8a,0x2915,0x2573,
0xbf72,0x40e4,0xe750,0xb44a,
0x3f88,0x31ed,0x5b1b,0xb117,
0x3fa2,0x5779,0xe33f,0xde67,
0xbfce,0x071a,0x9d42,0x87c2,
0x3fb2,0x4944,0xc9cd,0x3c51,
0x3ff0,0x0000,0x0000,0x0000
};
#endif 

/* Stirling's formula for the gamma function */
#if UNK
static double STIR[5] = {
 7.87311395793093628397E-4,
-2.29549961613378126380E-4,
-2.68132617805781232825E-3,
 3.47222221605458667310E-3,
 8.33333333333482257126E-2,
};
#define MAXSTIR 143.01608
static double SQTPI = 2.50662827463100050242E0;
#endif
#if DEC
static unsigned short STIR[20] = {
0035516,0061622,0144553,0112224,
0135160,0131531,0037460,0165740,
0136057,0134460,0037242,0077270,
0036143,0107070,0156306,0027751,
0037252,0125252,0125252,0146064,
};
#define MAXSTIR 26.77
static unsigned short SQT[4] = {
0040440,0066230,0177661,0034055,
};
#define SQTPI *(double *)SQT
#endif
#if IBMPC
static unsigned short STIR[20] = {
0x7293,0x592d,0xcc72,0x3f49,
0x1d7c,0x27e6,0x166b,0xbf2e,
0x4fd7,0x07d4,0xf726,0xbf65,
0xc5fd,0x1b98,0x71c7,0x3f6c,
0x5986,0x5555,0x5555,0x3fb5,
};
#define MAXSTIR 143.01608
static unsigned short SQT[4] = {
0x2706,0x1ff6,0x0d93,0x4004,
};
#define SQTPI *(double *)SQT
#endif
#if MIEEE
static unsigned short STIR[20] = {
0x3f49,0xcc72,0x592d,0x7293,
0xbf2e,0x166b,0x27e6,0x1d7c,
0xbf65,0xf726,0x07d4,0x4fd7,
0x3f6c,0x71c7,0x1b98,0xc5fd,
0x3fb5,0x5555,0x5555,0x5986,
};
#define MAXSTIR 143.01608
static unsigned short SQT[4] = {
0x4004,0x0d93,0x1ff6,0x2706,
};
#define SQTPI *(double *)SQT
#endif


/* Gamma function computed by Stirling's formula.
 * The polynomial STIR is valid for 33 <= x <= 172.
 */
static double stirf(double x)
{
double y, w, v;

w = 1.0/x;
w = 1.0 + w * polevl( w, STIR, 4 );
y = exp(x);
if( x > MAXSTIR )
	{ /* Avoid overflow in pow() */
	v = pow( x, 0.5 * x - 0.25 );
	y = v * (v / y);
	}
else
	{
	y = pow( x, x - 0.5 ) / y;
	}
y = SQTPI * y * w;
return( y );
}


double cephesgamma(double x)
{
double p, q, z;
int i;

sgngam = 1;
#ifdef NANS
if( isnan(x) )
	return(x);
#endif
#ifdef INFINITIES
#ifdef NANS
if( x == CEPHESINFINITY )
	return(x);
if( x == -CEPHESINFINITY )
	return(NAN);
#else
if( !isfinite(x) )
	return(x);
#endif
#endif
q = fabs(x);

if( q > 33.0 )
	{
	if( x < 0.0 )
		{
		p = floor(q);
		if( p == q )
			{
#ifdef NANS
gamnan:
			mtherr( "gamma", DOMAIN );
			return (NAN);
#else
			goto goverf;
#endif
			}
		i = p;
		if( (i & 1) == 0 )
			sgngam = -1;
		z = q - p;
		if( z > 0.5 )
			{
			p += 1.0;
			z = q - p;
			}
		z = q * sin( PI * z );
		if( z == 0.0 )
			{
#ifdef INFINITIES
			return( sgngam * CEPHESINFINITY);
#else
goverf:
			mtherr( "gamma", OVERFLOW );
			return( sgngam * MAXNUM);
#endif
			}
		z = fabs(z);
		z = PI/(z * stirf(q) );
		}
	else
		{
		z = stirf(x);
		}
	return( sgngam * z );
	}

z = 1.0;
while( x >= 3.0 )
	{
	x -= 1.0;
	z *= x;
	}

while( x < 0.0 )
	{
	if( x > -1.E-9 )
		goto small;
	z /= x;
	x += 1.0;
	}

while( x < 2.0 )
	{
	if( x < 1.e-9 )
		goto small;
	z /= x;
	x += 1.0;
	}

if( x == 2.0 )
	return(z);

x -= 2.0;
p = polevl( x, P, 6 );
q = polevl( x, Q, 7 );
return( z * p / q );

small:
if( x == 0.0 )
	{
#ifdef INFINITIES
#ifdef NANS
	  goto gamnan;
#else
	  return( CEPHESINFINITY );
#endif
#else
	mtherr( "gamma", SING );
	return( MAXNUM );
#endif
	}
else
	return( z/((1.0 + 0.5772156649015329 * x) * x) );
}
#endif

#ifndef HAVE_LGAMMA
double lgamma ( double );

/* A[]: Stirling's formula expansion of log gamma
 * B[], C[]: log gamma function between 2 and 3
 */
#ifdef UNK
static double A[] = {
 8.11614167470508450300E-4,
-5.95061904284301438324E-4,
 7.93650340457716943945E-4,
-2.77777777730099687205E-3,
 8.33333333333331927722E-2
};
static double B[] = {
-1.37825152569120859100E3,
-3.88016315134637840924E4,
-3.31612992738871184744E5,
-1.16237097492762307383E6,
-1.72173700820839662146E6,
-8.53555664245765465627E5
};
static double C[] = {
/* 1.00000000000000000000E0, */
-3.51815701436523470549E2,
-1.70642106651881159223E4,
-2.20528590553854454839E5,
-1.13933444367982507207E6,
-2.53252307177582951285E6,
-2.01889141433532773231E6
};
/* log( sqrt( 2*pi ) ) */
static double LS2PI  =  0.91893853320467274178;
#define MAXLGM 2.556348e305
static double LOGPI = 1.14472988584940017414;
#endif

#ifdef DEC
static unsigned short A[] = {
0035524,0141201,0034633,0031405,
0135433,0176755,0126007,0045030,
0035520,0006371,0003342,0172730,
0136066,0005540,0132605,0026407,
0037252,0125252,0125252,0125132
};
static unsigned short B[] = {
0142654,0044014,0077633,0035410,
0144027,0110641,0125335,0144760,
0144641,0165637,0142204,0047447,
0145215,0162027,0146246,0155211,
0145322,0026110,0010317,0110130,
0145120,0061472,0120300,0025363
};
static unsigned short C[] = {
/*0040200,0000000,0000000,0000000*/
0142257,0164150,0163630,0112622,
0143605,0050153,0156116,0135272,
0144527,0056045,0145642,0062332,
0145213,0012063,0106250,0001025,
0145432,0111254,0044577,0115142,
0145366,0071133,0050217,0005122
};
/* log( sqrt( 2*pi ) ) */
static unsigned short LS2P[] = {040153,037616,041445,0172645,};
#define LS2PI *(double *)LS2P
#define MAXLGM 2.035093e36
static unsigned short LPI[4] = {
0040222,0103202,0043475,0006750,
};
#define LOGPI *(double *)LPI
#endif

#ifdef IBMPC
static unsigned short A[] = {
0x6661,0x2733,0x9850,0x3f4a,
0xe943,0xb580,0x7fbd,0xbf43,
0x5ebb,0x20dc,0x019f,0x3f4a,
0xa5a1,0x16b0,0xc16c,0xbf66,
0x554b,0x5555,0x5555,0x3fb5
};
static unsigned short B[] = {
0x6761,0x8ff3,0x8901,0xc095,
0xb93e,0x355b,0xf234,0xc0e2,
0x89e5,0xf890,0x3d73,0xc114,
0xdb51,0xf994,0xbc82,0xc131,
0xf20b,0x0219,0x4589,0xc13a,
0x055e,0x5418,0x0c67,0xc12a
};
static unsigned short C[] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x12b2,0x1cf3,0xfd0d,0xc075,
0xd757,0x7b89,0xaa0d,0xc0d0,
0x4c9b,0xb974,0xeb84,0xc10a,
0x0043,0x7195,0x6286,0xc131,
0xf34c,0x892f,0x5255,0xc143,
0xe14a,0x6a11,0xce4b,0xc13e
};
/* log( sqrt( 2*pi ) ) */
static unsigned short LS2P[] = {
0xbeb5,0xc864,0x67f1,0x3fed
};
#define LS2PI *(double *)LS2P
#define MAXLGM 2.556348e305
static unsigned short LPI[4] = {
0xa1bd,0x48e7,0x50d0,0x3ff2,
};
#define LOGPI *(double *)LPI
#endif

#ifdef MIEEE
static unsigned short A[] = {
0x3f4a,0x9850,0x2733,0x6661,
0xbf43,0x7fbd,0xb580,0xe943,
0x3f4a,0x019f,0x20dc,0x5ebb,
0xbf66,0xc16c,0x16b0,0xa5a1,
0x3fb5,0x5555,0x5555,0x554b
};
static unsigned short B[] = {
0xc095,0x8901,0x8ff3,0x6761,
0xc0e2,0xf234,0x355b,0xb93e,
0xc114,0x3d73,0xf890,0x89e5,
0xc131,0xbc82,0xf994,0xdb51,
0xc13a,0x4589,0x0219,0xf20b,
0xc12a,0x0c67,0x5418,0x055e
};
static unsigned short C[] = {
0xc075,0xfd0d,0x1cf3,0x12b2,
0xc0d0,0xaa0d,0x7b89,0xd757,
0xc10a,0xeb84,0xb974,0x4c9b,
0xc131,0x6286,0x7195,0x0043,
0xc143,0x5255,0x892f,0xf34c,
0xc13e,0xce4b,0x6a11,0xe14a
};
/* log( sqrt( 2*pi ) ) */
static unsigned short LS2P[] = {
0x3fed,0x67f1,0xc864,0xbeb5
};
#define LS2PI *(double *)LS2P
#define MAXLGM 2.556348e305
static unsigned short LPI[4] = {
0x3ff2,0x50d0,0x48e7,0xa1bd,
};
#define LOGPI *(double *)LPI
#endif


/* Logarithm of gamma function */


double lgamma(double x)
{
double p, q, u, w, z;
int i;

sgngam = 1;
#ifdef NANS
if( isnan(x) )
	return(x);
#endif

#ifdef INFINITIES
if( !isfinite(x) )
	return(CEPHESINFINITY);
#endif

if( x < -34.0 )
	{
	q = -x;
	w = lgamma(q); /* note this modifies sgngam! */
	p = floor(q);
	if( p == q )
		{
lgsing:
#ifdef INFINITIES
		mtherr( "lgamma", SING );
		return (CEPHESINFINITY);
#else
		goto loverf;
#endif
		}
	i = p;
	if( (i & 1) == 0 )
		sgngam = -1;
	else
		sgngam = 1;
	z = q - p;
	if( z > 0.5 )
		{
		p += 1.0;
		z = p - q;
		}
	z = q * sin( PI * z );
	if( z == 0.0 )
		goto lgsing;
/*	z = log(PI) - log( z ) - w;*/
	z = LOGPI - log( z ) - w;
	return( z );
	}

if( x < 13.0 )
	{
	z = 1.0;
	p = 0.0;
	u = x;
	while( u >= 3.0 )
		{
		p -= 1.0;
		u = x + p;
		z *= u;
		}
	while( u < 2.0 )
		{
		if( u == 0.0 )
			goto lgsing;
		z /= u;
		p += 1.0;
		u = x + p;
		}
	if( z < 0.0 )
		{
		sgngam = -1;
		z = -z;
		}
	else
		sgngam = 1;
	if( u == 2.0 )
		return( log(z) );
	p -= 2.0;
	x = x + p;
	p = x * polevl( x, B, 5 ) / p1evl( x, C, 6);
	return( log(z) + p );
	}

if( x > MAXLGM )
	{
#ifdef INFINITIES
	return( sgngam * CEPHESINFINITY );
#else
loverf:
	mtherr( "lgamma", OVERFLOW );
	return( sgngam * MAXNUM );
#endif
	}

q = ( x - 0.5 ) * log(x) - x + LS2PI;
if( x > 1.0e8 )
	return( q );

p = 1.0/(x*x);
if( x >= 1000.0 )
	q += ((   7.9365079365079365079365e-4 * p
		- 2.7777777777777777777778e-3) *p
		+ 0.0833333333333333333333) / x;
else
	q += polevl( p, A, 4 ) / x;
return( q );
}
#endif
/*							incbet.c
 *
 *	Incomplete beta integral
 *
 *
 * SYNOPSIS:
 *
 * double a, b, x, y, incbet();
 *
 * y = incbet( a, b, x );
 *
 *
 * DESCRIPTION:
 *
 * Returns incomplete beta integral of the arguments, evaluated
 * from zero to x.  The function is defined as
 *
 *                  x
 *     -            -
 *    | (a+b)      | |  a-1     b-1
 *  -----------    |   t   (1-t)   dt.
 *   -     -     | |
 *  | (a) | (b)   -
 *                 0
 *
 * The domain of definition is 0 <= x <= 1.  In this
 * implementation a and b are restricted to positive values.
 * The integral from x to 1 may be obtained by the symmetry
 * relation
 *
 *    1 - incbet( a, b, x )  =  incbet( b, a, 1-x ).
 *
 * The integral is evaluated by a continued fraction expansion
 * or, when b*x is small, by a power series.
 *
 * ACCURACY:
 *
 * Tested at uniformly distributed random points (a,b,x) with a and b
 * in "domain" and x between 0 and 1.
 *                                        Relative error
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0,5         10000       6.9e-15     4.5e-16
 *    IEEE      0,85       250000       2.2e-13     1.7e-14
 *    IEEE      0,1000      30000       5.3e-12     6.3e-13
 *    IEEE      0,10000    250000       9.3e-11     7.1e-12
 *    IEEE      0,100000    10000       8.7e-10     4.8e-11
 * Outputs smaller than the IEEE gradual underflow threshold
 * were excluded from these statistics.
 *
 * ERROR MESSAGES:
 *   message         condition      value returned
 * incbet domain      x<0, x>1          0.0
 * incbet underflow                     0.0
 */



static double big = 4.503599627370496e15;
static double biginv =  2.22044604925031308085e-16;


double incbet(double aa, double bb, double xx)
{
double a, b, t, x, xc, w, y;
int flag;

if( aa <= 0.0 || bb <= 0.0 )
	goto domerr;

if( (xx <= 0.0) || ( xx >= 1.0) )
	{
	if( xx == 0.0 )
		return(0.0);
	if( xx == 1.0 )
		return( 1.0 );
domerr:
	mtherr( "incbet", DOMAIN );
	return( 0.0 );
	}

flag = 0;
if( (bb * xx) <= 1.0 && xx <= 0.95)
	{
	t = pseries(aa, bb, xx);
		goto done;
	}

w = 1.0 - xx;

/* Reverse a and b if x is greater than the mean. */
if( xx > (aa/(aa+bb)) )
	{
	flag = 1;
	a = bb;
	b = aa;
	xc = xx;
	x = w;
	}
else
	{
	a = aa;
	b = bb;
	xc = w;
	x = xx;
	}

if( flag == 1 && (b * x) <= 1.0 && x <= 0.95)
	{
	t = pseries(a, b, x);
	goto done;
	}

/* Choose expansion for better convergence. */
y = x * (a+b-2.0) - (a-1.0);
if( y < 0.0 )
	w = incbcf( a, b, x );
else
	w = incbd( a, b, x ) / xc;

/* Multiply w by the factor
     a      b   _             _     _
    x  (1-x)   | (a+b) / ( a | (a) | (b) ) .   */

y = a * log(x);
t = b * log(xc);
if( (a+b) < MAXGAM && fabs(y) < MAXLOG && fabs(t) < MAXLOG )
	{
	t = pow(xc,b);
	t *= pow(x,a);
	t /= a;
	t *= w;
	t *= cephesgamma(a+b) / (cephesgamma(a) * cephesgamma(b));
	goto done;
	}
/* Resort to logarithms.  */
y += t + lgamma(a+b) - lgamma(a) - lgamma(b);
y += log(w/a);
if( y < MINLOG )
	t = 0.0;
else
	t = exp(y);

done:

if( flag == 1 )
	{
	if( t <= MACHEP )
		t = 1.0 - MACHEP;
	else
		t = 1.0 - t;
	}
return( t );
}

/* Continued fraction expansion #1
 * for incomplete beta integral
 */

static double incbcf(double a, double b, double x)
{
double xk, pk, pkm1, pkm2, qk, qkm1, qkm2;
double k1, k2, k3, k4, k5, k6, k7, k8;
double r, t, ans, thresh;
int n;

k1 = a;
k2 = a + b;
k3 = a;
k4 = a + 1.0;
k5 = 1.0;
k6 = b - 1.0;
k7 = k4;
k8 = a + 2.0;

pkm2 = 0.0;
qkm2 = 1.0;
pkm1 = 1.0;
qkm1 = 1.0;
ans = 1.0;
r = 1.0;
n = 0;
thresh = 3.0 * MACHEP;
do
	{
	
	xk = -( x * k1 * k2 )/( k3 * k4 );
	pk = pkm1 +  pkm2 * xk;
	qk = qkm1 +  qkm2 * xk;
	pkm2 = pkm1;
	pkm1 = pk;
	qkm2 = qkm1;
	qkm1 = qk;

	xk = ( x * k5 * k6 )/( k7 * k8 );
	pk = pkm1 +  pkm2 * xk;
	qk = qkm1 +  qkm2 * xk;
	pkm2 = pkm1;
	pkm1 = pk;
	qkm2 = qkm1;
	qkm1 = qk;

	if( qk != 0 )
		r = pk/qk;
	if( r != 0 )
		{
		t = fabs( (ans - r)/r );
		ans = r;
		}
	else
		t = 1.0;

	if( t < thresh )
		goto cdone;

	k1 += 1.0;
	k2 += 1.0;
	k3 += 2.0;
	k4 += 2.0;
	k5 += 1.0;
	k6 -= 1.0;
	k7 += 2.0;
	k8 += 2.0;

	if( (fabs(qk) + fabs(pk)) > big )
		{
		pkm2 *= biginv;
		pkm1 *= biginv;
		qkm2 *= biginv;
		qkm1 *= biginv;
		}
	if( (fabs(qk) < biginv) || (fabs(pk) < biginv) )
		{
		pkm2 *= big;
		pkm1 *= big;
		qkm2 *= big;
		qkm1 *= big;
		}
	}
while( ++n < 300 );

cdone:
return(ans);
}


/* Continued fraction expansion #2
 * for incomplete beta integral
 */

static double incbd(double a, double b, double x)
{
double xk, pk, pkm1, pkm2, qk, qkm1, qkm2;
double k1, k2, k3, k4, k5, k6, k7, k8;
double r, t, ans, z, thresh;
int n;

k1 = a;
k2 = b - 1.0;
k3 = a;
k4 = a + 1.0;
k5 = 1.0;
k6 = a + b;
k7 = a + 1.0;;
k8 = a + 2.0;

pkm2 = 0.0;
qkm2 = 1.0;
pkm1 = 1.0;
qkm1 = 1.0;
z = x / (1.0-x);
ans = 1.0;
r = 1.0;
n = 0;
thresh = 3.0 * MACHEP;
do
	{
	
	xk = -( z * k1 * k2 )/( k3 * k4 );
	pk = pkm1 +  pkm2 * xk;
	qk = qkm1 +  qkm2 * xk;
	pkm2 = pkm1;
	pkm1 = pk;
	qkm2 = qkm1;
	qkm1 = qk;

	xk = ( z * k5 * k6 )/( k7 * k8 );
	pk = pkm1 +  pkm2 * xk;
	qk = qkm1 +  qkm2 * xk;
	pkm2 = pkm1;
	pkm1 = pk;
	qkm2 = qkm1;
	qkm1 = qk;

	if( qk != 0 )
		r = pk/qk;
	if( r != 0 )
		{
		t = fabs( (ans - r)/r );
		ans = r;
		}
	else
		t = 1.0;

	if( t < thresh )
		goto cdone;

	k1 += 1.0;
	k2 -= 1.0;
	k3 += 2.0;
	k4 += 2.0;
	k5 += 1.0;
	k6 += 1.0;
	k7 += 2.0;
	k8 += 2.0;

	if( (fabs(qk) + fabs(pk)) > big )
		{
		pkm2 *= biginv;
		pkm1 *= biginv;
		qkm2 *= biginv;
		qkm1 *= biginv;
		}
	if( (fabs(qk) < biginv) || (fabs(pk) < biginv) )
		{
		pkm2 *= big;
		pkm1 *= big;
		qkm2 *= big;
		qkm1 *= big;
		}
	}
while( ++n < 300 );
cdone:
return(ans);
}

/* Power series for incomplete beta integral.
   Use when b*x is small and x not too close to 1.  */

static double pseries(double a, double b, double x)
{
double s, t, u, v, n, t1, z, ai;

ai = 1.0 / a;
u = (1.0 - b) * x;
v = u / (a + 1.0);
t1 = v;
t = u;
n = 2.0;
s = 0.0;
z = MACHEP * ai;
while( fabs(v) > z )
	{
	u = (n - b) * x / n;
	t *= u;
	v = t / (a + n);
	s += v; 
	n += 1.0;
	}
s += t1;
s += ai;

u = a * log(x);
if( (a+b) < MAXGAM && fabs(u) < MAXLOG )
	{
	t = cephesgamma(a+b)/(cephesgamma(a)*cephesgamma(b));
	s = s * t * pow(x,a);
	}
else
	{
	t = lgamma(a+b) - lgamma(a) - lgamma(b) + u + log(s);
	if( t < MINLOG )
		s = 0.0;
	else
	s = exp(t);
	}
return(s);
}
/*							incbi()
 *
 *      Inverse of imcomplete beta integral
 *
 *
 *
 * SYNOPSIS:
 *
 * double a, b, x, y, incbi();
 *
 * x = incbi( a, b, y );
 *
 *
 *
 * DESCRIPTION:
 *
 * Given y, the function finds x such that
 *
 *  incbet( a, b, x ) = y .
 *
 * The routine performs interval halving or Newton iterations to find the
 * root of incbet(a,b,x) - y = 0.
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 *                x     a,b
 * arithmetic   domain  domain  # trials    peak       rms
 *    IEEE      0,1    .5,10000   50000    5.8e-12   1.3e-13
 *    IEEE      0,1   .25,100    100000    1.8e-13   3.9e-15
 *    IEEE      0,1     0,5       50000    1.1e-12   5.5e-15
 *    VAX       0,1    .5,100     25000    3.5e-14   1.1e-15
 * With a and b constrained to half-integer or integer values:
 *    IEEE      0,1    .5,10000   50000    5.8e-12   1.1e-13
 *    IEEE      0,1    .5,100    100000    1.7e-14   7.9e-16
 * With a = .5, b constrained to half-integer or integer values:
 *    IEEE      0,1    .5,10000   10000    8.3e-11   1.0e-11
 */




double incbi(double aa, double bb, double yy0)
{
double a, b, y0, d, y, x, x0, x1, lgm, yp, di, dithresh, yl, yh, xt;
int i, rflg, dir, nflg;


i = 0;
if( yy0 <= 0 )
	return(0.0);
if( yy0 >= 1.0 )
	return(1.0);
x0 = 0.0;
yl = 0.0;
x1 = 1.0;
yh = 1.0;
nflg = 0;

if( aa <= 1.0 || bb <= 1.0 )
	{
	dithresh = 1.0e-6;
	rflg = 0;
	a = aa;
	b = bb;
	y0 = yy0;
	x = a/(a+b);
	y = incbet( a, b, x );
	goto ihalve;
	}
else
	{
	dithresh = 1.0e-4;
	}
/* approximation to inverse function */

yp = -ndtri(yy0);

if( yy0 > 0.5 )
	{
	rflg = 1;
	a = bb;
	b = aa;
	y0 = 1.0 - yy0;
	yp = -yp;
	}
else
	{
	rflg = 0;
	a = aa;
	b = bb;
	y0 = yy0;
	}

lgm = (yp * yp - 3.0)/6.0;
x = 2.0/( 1.0/(2.0*a-1.0)  +  1.0/(2.0*b-1.0) );
d = yp * sqrt( x + lgm ) / x
	- ( 1.0/(2.0*b-1.0) - 1.0/(2.0*a-1.0) )
	* (lgm + 5.0/6.0 - 2.0/(3.0*x));
d = 2.0 * d;
if( d < MINLOG )
	{
	x = 1.0;
	goto under;
	}
x = a/( a + b * exp(d) );
y = incbet( a, b, x );
yp = (y - y0)/y0;
if( fabs(yp) < 0.2 )
	goto newt;

/* Resort to interval halving if not close enough. */
ihalve:

dir = 0;
di = 0.5;
for( i=0; i<100; i++ )
	{
	if( i != 0 )
		{
		x = x0  +  di * (x1 - x0);
		if( x == 1.0 )
			x = 1.0 - MACHEP;
		if( x == 0.0 )
			{
			di = 0.5;
			x = x0  +  di * (x1 - x0);
			if( x == 0.0 )
				goto under;
			}
		y = incbet( a, b, x );
		yp = (x1 - x0)/(x1 + x0);
		if( fabs(yp) < dithresh )
			goto newt;
		yp = (y-y0)/y0;
		if( fabs(yp) < dithresh )
			goto newt;
		}
	if( y < y0 )
		{
		x0 = x;
		yl = y;
		if( dir < 0 )
			{
			dir = 0;
			di = 0.5;
			}
		else if( dir > 3 )
			di = 1.0 - (1.0 - di) * (1.0 - di);
		else if( dir > 1 )
			di = 0.5 * di + 0.5; 
		else
			di = (y0 - y)/(yh - yl);
		dir += 1;
		if( x0 > 0.75 )
			{
			if( rflg == 1 )
				{
				rflg = 0;
				a = aa;
				b = bb;
				y0 = yy0;
				}
			else
				{
				rflg = 1;
				a = bb;
				b = aa;
				y0 = 1.0 - yy0;
				}
			x = 1.0 - x;
			y = incbet( a, b, x );
			x0 = 0.0;
			yl = 0.0;
			x1 = 1.0;
			yh = 1.0;
			goto ihalve;
			}
		}
	else
		{
		x1 = x;
		if( rflg == 1 && x1 < MACHEP )
			{
			x = 0.0;
			goto done;
			}
		yh = y;
		if( dir > 0 )
			{
			dir = 0;
			di = 0.5;
			}
		else if( dir < -3 )
			di = di * di;
		else if( dir < -1 )
			di = 0.5 * di;
		else
			di = (y - y0)/(yh - yl);
		dir -= 1;
		}
	}
mtherr( "incbi", PLOSS );
if( x0 >= 1.0 )
	{
	x = 1.0 - MACHEP;
	goto done;
	}
if( x <= 0.0 )
	{
under:
	mtherr( "incbi", UNDERFLOW );
	x = 0.0;
	goto done;
	}

newt:

if( nflg )
	goto done;
nflg = 1;
lgm = lgamma(a+b) - lgamma(a) - lgamma(b);

for( i=0; i<8; i++ )
	{
	/* Compute the function at this point. */
	if( i != 0 )
		y = incbet(a,b,x);
	if( y < yl )
		{
		x = x0;
		y = yl;
		}
	else if( y > yh )
		{
		x = x1;
		y = yh;
		}
	else if( y < y0 )
		{
		x0 = x;
		yl = y;
		}
	else
		{
		x1 = x;
		yh = y;
		}
	if( x == 1.0 || x == 0.0 )
		break;
	/* Compute the derivative of the function at this point. */
	d = (a - 1.0) * log(x) + (b - 1.0) * log(1.0-x) + lgm;
	if( d < MINLOG )
		goto done;
	if( d > MAXLOG )
		break;
	d = exp(d);
	/* Compute the step to the next approximation of x. */
	d = (y - y0)/d;
	xt = x - d;
	if( xt <= x0 )
		{
		y = (x - x0) / (x1 - x0);
		xt = x0 + 0.5 * y * (x - x0);
		if( xt <= 0.0 )
			break;
		}
	if( xt >= x1 )
		{
		y = (x1 - x) / (x1 - x0);
		xt = x1 - 0.5 * y * (x1 - x);
		if( xt >= 1.0 )
			break;
		}
	x = xt;
	if( fabs(d/x) < 128.0 * MACHEP )
		goto done;
	}
/* Did not converge.  */
dithresh = 256.0 * MACHEP;
goto ihalve;

done:

if( rflg )
	{
	if( x <= MACHEP )
		x = 1.0 - MACHEP;
	else
		x = 1.0 - x;
	}
return( x );
}
/*							igam.c
 *
 *	Incomplete gamma integral
 *
 *
 *
 * SYNOPSIS:
 *
 * double a, x, y, igam();
 *
 * y = igam( a, x );
 *
 * DESCRIPTION:
 *
 * The function is defined by
 *
 *                           x
 *                            -
 *                   1       | |  -t  a-1
 *  igam(a,x)  =   -----     |   e   t   dt.
 *                  -      | |
 *                 | (a)    -
 *                           0
 *
 *
 * In this implementation both arguments must be positive.
 * The integral is evaluated by either a power series or
 * continued fraction expansion, depending on the relative
 * values of a and x.
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0,30       200000       3.6e-14     2.9e-15
 *    IEEE      0,100      300000       9.9e-14     1.5e-14
 */
/*							igamc()
 *
 *	Complemented incomplete gamma integral
 *
 *
 *
 * SYNOPSIS:
 *
 * double a, x, y, igamc();
 *
 * y = igamc( a, x );
 *
 * DESCRIPTION:
 *
 * The function is defined by
 *
 *
 *  igamc(a,x)   =   1 - igam(a,x)
 *
 *                            inf.
 *                              -
 *                     1       | |  -t  a-1
 *               =   -----     |   e   t   dt.
 *                    -      | |
 *                   | (a)    -
 *                             x
 *
 *
 * In this implementation both arguments must be positive.
 * The integral is evaluated by either a power series or
 * continued fraction expansion, depending on the relative
 * values of a and x.
 *
 * ACCURACY:
 *
 * Tested at random a, x.
 *                a         x                      Relative error:
 * arithmetic   domain   domain     # trials      peak         rms
 *    IEEE     0.5,100   0,100      200000       1.9e-14     1.7e-15
 *    IEEE     0.01,0.5  0,100      200000       1.4e-13     1.6e-15
 */


double igamc(double a, double x)
{
double ans, ax, c, yc, r, t, y, z;
double pk, pkm1, pkm2, qk, qkm1, qkm2;

if( (x <= 0) || ( a <= 0) )
	return( 1.0 );

if( (x < 1.0) || (x < a) )
	return( 1.0 - igam(a,x) );

ax = a * log(x) - x - lgamma(a);
if( ax < -MAXLOG )
	{
	mtherr( "igamc", UNDERFLOW );
	return( 0.0 );
	}
ax = exp(ax);

/* continued fraction */
y = 1.0 - a;
z = x + y + 1.0;
c = 0.0;
pkm2 = 1.0;
qkm2 = x;
pkm1 = x + 1.0;
qkm1 = z * x;
ans = pkm1/qkm1;

do
	{
	c += 1.0;
	y += 1.0;
	z += 2.0;
	yc = y * c;
	pk = pkm1 * z  -  pkm2 * yc;
	qk = qkm1 * z  -  qkm2 * yc;
	if( qk != 0 )
		{
		r = pk/qk;
		t = fabs( (ans - r)/r );
		ans = r;
		}
	else
		t = 1.0;
	pkm2 = pkm1;
	pkm1 = pk;
	qkm2 = qkm1;
	qkm1 = qk;
	if( fabs(pk) > big )
		{
		pkm2 *= biginv;
		pkm1 *= biginv;
		qkm2 *= biginv;
		qkm1 *= biginv;
		}
	}
while( t > MACHEP );

return( ans * ax );
}



/* left tail of incomplete gamma function:
 *
 *          inf.      k
 *   a  -x   -       x
 *  x  e     >   ----------
 *           -     -
 *          k=0   | (a+k+1)
 *
 */

double igam(double a, double x)
{
double ans, ax, c, r;

if( (x <= 0) || ( a <= 0) )
	return( 0.0 );

if( (x > 1.0) && (x > a ) )
	return( 1.0 - igamc(a,x) );

/* Compute  x**a * exp(-x) / gamma(a)  */
ax = a * log(x) - x - lgamma(a);
if( ax < -MAXLOG )
	{
	mtherr( "igam", UNDERFLOW );
	return( 0.0 );
	}
ax = exp(ax);

/* power series */
r = a;
c = 1.0;
ans = 1.0;

do
	{
	r += 1.0;
	c *= x/r;
	ans += c;
	}
while( c/ans > MACHEP );

return( ans * ax/a );
}
/*							igami()
 *
 *      Inverse of complemented imcomplete gamma integral
 *
 *
 *
 * SYNOPSIS:
 *
 * double a, x, p, igami();
 *
 * x = igami( a, p );
 *
 * DESCRIPTION:
 *
 * Given p, the function finds x such that
 *
 *  igamc( a, x ) = p.
 *
 * Starting with the approximate value
 *
 *         3
 *  x = a t
 *
 *  where
 *
 *  t = 1 - d - ndtri(p) sqrt(d)
 * 
 * and
 *
 *  d = 1/9a,
 *
 * the routine performs up to 10 Newton iterations to find the
 * root of igamc(a,x) - p = 0.
 *
 * ACCURACY:
 *
 * Tested at random a, p in the intervals indicated.
 *
 *                a        p                      Relative error:
 * arithmetic   domain   domain     # trials      peak         rms
 *    IEEE     0.5,100   0,0.5       100000       1.0e-14     1.7e-15
 *    IEEE     0.01,0.5  0,0.5       100000       9.0e-14     3.4e-15
 *    IEEE    0.5,10000  0,0.5        20000       2.3e-13     3.8e-14
 */




double igami(double a, double y0)
{
double x0, x1, x, yl, yh, y, d, lgm, dithresh;
int i, dir;

/* bound the solution */
x0 = MAXNUM;
yl = 0;
x1 = 0;
yh = 1.0;
dithresh = 5.0 * MACHEP;

/* approximation to inverse function */
d = 1.0/(9.0*a);
y = ( 1.0 - d - ndtri(y0) * sqrt(d) );
x = a * y * y * y;

lgm = lgamma(a);

for( i=0; i<10; i++ )
	{
	if( x > x0 || x < x1 )
		goto ihalve;
	y = igamc(a,x);
	if( y < yl || y > yh )
		goto ihalve;
	if( y < y0 )
		{
		x0 = x;
		yl = y;
		}
	else
		{
		x1 = x;
		yh = y;
		}
/* compute the derivative of the function at this point */
	d = (a - 1.0) * log(x) - x - lgm;
	if( d < -MAXLOG )
		goto ihalve;
	d = -exp(d);
/* compute the step to the next approximation of x */
	d = (y - y0)/d;
	if( fabs(d/x) < MACHEP )
		goto done;
	x = x - d;
	}

/* Resort to interval halving if Newton iteration did not converge. */
ihalve:

d = 0.0625;
if( x0 == MAXNUM )
	{
	if( x <= 0.0 )
		x = 1.0;
	while( x0 == MAXNUM )
		{
		x = (1.0 + d) * x;
		y = igamc( a, x );
		if( y < y0 )
			{
			x0 = x;
			yl = y;
			break;
			}
		d = d + d;
		}
	}
d = 0.5;
dir = 0;

for( i=0; i<400; i++ )
	{
	x = x1  +  d * (x0 - x1);
	y = igamc( a, x );
	lgm = (x0 - x1)/(x1 + x0);
	if( fabs(lgm) < dithresh )
		break;
	lgm = (y - y0)/y0;
	if( fabs(lgm) < dithresh )
		break;
	if( x <= 0.0 )
		break;
	if( y >= y0 )
		{
		x1 = x;
		yh = y;
		if( dir < 0 )
			{
			dir = 0;
			d = 0.5;
			}
		else if( dir > 1 )
			d = 0.5 * d + 0.5; 
		else
			d = (y0 - yl)/(yh - yl);
		dir += 1;
		}
	else
		{
		x0 = x;
		yl = y;
		if( dir > 0 )
			{
			dir = 0;
			d = 0.5;
			}
		else if( dir < -1 )
			d = 0.5 * d;
		else
			d = (y0 - yl)/(yh - yl);
		dir -= 1;
		}
	}
if( x == 0.0 )
	mtherr( "igami", UNDERFLOW );

done:
return( x );
}

/* ========================================================================= */

/*							psi.c
 *
 *	Psi (digamma) function
 *
 *
 * SYNOPSIS:
 *
 * double x, y, psi();
 *
 * y = psi( x );
 *
 *
 * DESCRIPTION:
 *
 *              d      -
 *   psi(x)  =  -- ln | (x)
 *              dx
 *
 * is the logarithmic derivative of the gamma function.
 * For integer x,
 *                   n-1
 *                    -
 * psi(n) = -EUL  +   >  1/k.
 *                    -
 *                   k=1
 *
 * This formula is used for 0 < n <= 10.  If x is negative, it
 * is transformed to a positive argument by the reflection
 * formula  psi(1-x) = psi(x) + pi cot(pi x).
 * For general positive x, the argument is made greater than 10
 * using the recurrence  psi(x+1) = psi(x) + 1/x.
 * Then the following asymptotic expansion is applied:
 *
 *                           inf.   B
 *                            -      2k
 * psi(x) = log(x) - 1/2x -   >   -------
 *                            -        2k
 *                           k=1   2k x
 *
 * where the B2k are Bernoulli numbers.
 *
 * ACCURACY:
 *    Relative error (except absolute when |psi| < 1):
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0,30         2500       1.7e-16     2.0e-17
 *    IEEE      0,30        30000       1.3e-15     1.4e-16
 *    IEEE      -30,0       40000       1.5e-15     2.2e-16
 *
 * ERROR MESSAGES:
 *     message         condition      value returned
 * psi singularity    x integer <=0      MAXNUM
 */



#ifdef UNK
static double APSI[] = {
 8.33333333333333333333E-2,
-2.10927960927960927961E-2,
 7.57575757575757575758E-3,
-4.16666666666666666667E-3,
 3.96825396825396825397E-3,
-8.33333333333333333333E-3,
 8.33333333333333333333E-2
};
#endif

#ifdef DEC
static unsigned short APSI[] = {
0037252,0125252,0125252,0125253,
0136654,0145314,0126312,0146255,
0036370,0037017,0101740,0174076,
0136210,0104210,0104210,0104211,
0036202,0004040,0101010,0020202,
0136410,0104210,0104210,0104211,
0037252,0125252,0125252,0125253
};
#endif

#ifdef IBMPC
static unsigned short APSI[] = {
0x5555,0x5555,0x5555,0x3fb5,
0x5996,0x9599,0x9959,0xbf95,
0x1f08,0xf07c,0x07c1,0x3f7f,
0x1111,0x1111,0x1111,0xbf71,
0x0410,0x1041,0x4104,0x3f70,
0x1111,0x1111,0x1111,0xbf81,
0x5555,0x5555,0x5555,0x3fb5
};
#endif

#ifdef MIEEE
static unsigned short APSI[] = {
0x3fb5,0x5555,0x5555,0x5555,
0xbf95,0x9959,0x9599,0x5996,
0x3f7f,0x07c1,0xf07c,0x1f08,
0xbf71,0x1111,0x1111,0x1111,
0x3f70,0x4104,0x1041,0x0410,
0xbf81,0x1111,0x1111,0x1111,
0x3fb5,0x5555,0x5555,0x5555
};
#endif

double psi(double x)
{
double p, q, nz, s, w, y, z;
int i, n, negative;

negative = 0;
nz = 0.0;

if( x <= 0.0 )
	{
	negative = 1;
	q = x;
	p = floor(q);
	if( p == q )
		{
		mtherr( "psi", SING );
		return( MAXNUM );
		}
/* Remove the zeros of tan(PI x)
 * by subtracting the nearest integer from x
 */
	nz = q - p;
	if( nz != 0.5 )
		{
		if( nz > 0.5 )
			{
			p += 1.0;
			nz = q - p;
			}
		nz = PI/tan(PI*nz);
		}
	else
		{
		nz = 0.0;
		}
	x = 1.0 - x;
	}

/* check for positive integer up to 10 */
if( (x <= 10.0) && (x == floor(x)) )
	{
	y = 0.0;
	n = x;
	for( i=1; i<n; i++ )
		{
		w = i;
		y += 1.0/w;
		}
	y -= EUL;
	goto done;
	}

s = x;
w = 0.0;
while( s < 10.0 )
	{
	w += 1.0/s;
	s += 1.0;
	}

if( s < 1.0e17 )
	{
	z = 1.0/(s * s);
	y = z * polevl( z, APSI, 6 );
	}
else
	y = 0.0;

y = log(s)  -  (0.5/s)  -  y  -  w;

done:

if( negative )
	{
	y -= nz;
	}

return(y);
}
/*						rgamma.c
 *
 *	Reciprocal gamma function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, rgamma();
 *
 * y = rgamma( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns one divided by the gamma function of the argument.
 *
 * The function is approximated by a Chebyshev expansion in
 * the interval [0,1].  Range reduction is by recurrence
 * for arguments between -34.034 and +34.84425627277176174.
 * 1/MAXNUM is returned for positive arguments outside this
 * range.  For arguments less than -34.034 the cosecant
 * reflection formula is applied; lograrithms are employed
 * to avoid unnecessary overflow.
 *
 * The reciprocal gamma function has no singularities,
 * but overflow and underflow may occur for large arguments.
 * These conditions return either MAXNUM or 1/MAXNUM with
 * appropriate sign.
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC      -30,+30       4000       1.2e-16     1.8e-17
 *    IEEE     -30,+30      30000       1.1e-15     2.0e-16
 * For arguments less than -34.034 the peak error is on the
 * order of 5e-15 (DEC), excepting overflow or underflow.
 */



/* Chebyshev coefficients for reciprocal gamma function
 * in interval 0 to 1.  Function is 1/(x gamma(x)) - 1
 */

#ifdef UNK
static double R[] = {
 3.13173458231230000000E-17,
-6.70718606477908000000E-16,
 2.20039078172259550000E-15,
 2.47691630348254132600E-13,
-6.60074100411295197440E-12,
 5.13850186324226978840E-11,
 1.08965386454418662084E-9,
-3.33964630686836942556E-8,
 2.68975996440595483619E-7,
 2.96001177518801696639E-6,
-8.04814124978471142852E-5,
 4.16609138709688864714E-4,
 5.06579864028608725080E-3,
-6.41925436109158228810E-2,
-4.98558728684003594785E-3,
 1.27546015610523951063E-1
};
#endif

#ifdef DEC
static unsigned short R[] = {
0022420,0066376,0176751,0071636,
0123501,0051114,0042104,0131153,
0024036,0107013,0126504,0033361,
0025613,0070040,0035174,0162316,
0126750,0037060,0077775,0122202,
0027541,0177143,0037675,0105150,
0030625,0141311,0075005,0115436,
0132017,0067714,0125033,0014721,
0032620,0063707,0105256,0152643,
0033506,0122235,0072757,0170053,
0134650,0144041,0015617,0016143,
0035332,0066125,0000776,0006215,
0036245,0177377,0137173,0131432,
0137203,0073541,0055645,0141150,
0136243,0057043,0026226,0017362,
0037402,0115554,0033441,0012310
};
#endif

#ifdef IBMPC
static unsigned short R[] = {
0x2e74,0xdfbd,0x0d9f,0x3c82,
0x964d,0x8888,0x2a49,0xbcc8,
0x86de,0x75a8,0xd1c1,0x3ce3,
0x9c9a,0x074f,0x6e04,0x3d51,
0xb490,0x0fff,0x07c6,0xbd9d,
0xb14d,0x67f7,0x3fcc,0x3dcc,
0xb364,0x2f40,0xb859,0x3e12,
0x633a,0x9543,0xedf9,0xbe61,
0xdab4,0xf155,0x0cf8,0x3e92,
0xfe05,0xaebd,0xd493,0x3ec8,
0xe38c,0x2371,0x1904,0xbf15,
0xc192,0xa03f,0x4d8a,0x3f3b,
0x7663,0xf7cf,0xbfdf,0x3f74,
0xb84d,0x2b74,0x6eec,0xbfb0,
0xc3de,0x6592,0x6bc4,0xbf74,
0x2299,0x86e4,0x536d,0x3fc0
};
#endif

#ifdef MIEEE
static unsigned short R[] = {
0x3c82,0x0d9f,0xdfbd,0x2e74,
0xbcc8,0x2a49,0x8888,0x964d,
0x3ce3,0xd1c1,0x75a8,0x86de,
0x3d51,0x6e04,0x074f,0x9c9a,
0xbd9d,0x07c6,0x0fff,0xb490,
0x3dcc,0x3fcc,0x67f7,0xb14d,
0x3e12,0xb859,0x2f40,0xb364,
0xbe61,0xedf9,0x9543,0x633a,
0x3e92,0x0cf8,0xf155,0xdab4,
0x3ec8,0xd493,0xaebd,0xfe05,
0xbf15,0x1904,0x2371,0xe38c,
0x3f3b,0x4d8a,0xa03f,0xc192,
0x3f74,0xbfdf,0xf7cf,0x7663,
0xbfb0,0x6eec,0x2b74,0xb84d,
0xbf74,0x6bc4,0x6592,0xc3de,
0x3fc0,0x536d,0x86e4,0x2299
};
#endif

static char name[] = "rgamma";



double rgamma(double x)
{
double w, y, z;
int sign;

if( x > 34.84425627277176174)
	{
	mtherr( name, UNDERFLOW );
	return(1.0/MAXNUM);
	}
if( x < -34.034 )
	{
	w = -x;
	z = sin( PI*w );
	if( z == 0.0 )
		return(0.0);
	if( z < 0.0 )
		{
		sign = 1;
		z = -z;
		}
	else
		sign = -1;

	y = log( w * z ) - log(PI) + lgamma(w);
	if( y < -MAXLOG )
		{
		mtherr( name, UNDERFLOW );
		return( sign * 1.0 / MAXNUM );
		}
	if( y > MAXLOG )
		{
		mtherr( name, OVERFLOW );
		return( sign * MAXNUM );
		}
	return( sign * exp(y));
	}
z = 1.0;
w = x;

while( w > 1.0 )	/* Downward recurrence */
	{
	w -= 1.0;
	z *= w;
	}
while( w < 0.0 )	/* Upward recurrence */
	{
	z /= w;
	w += 1.0;
	}
if( w == 0.0 )		/* Nonpositive integer */
	return(0.0);
if( w == 1.0 )		/* Other integer */
	return( 1.0/z );

y = w * ( 1.0 + chbevl( 4.0*w-2.0, R, 16 ) ) / z;
return(y);
}

/* ========================================================================= */

/*							airy.c
 *
 *	Airy function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, ai, aip, bi, bip;
 * int airy();
 *
 * airy( x, _&ai, _&aip, _&bi, _&bip );
 *
 *
 *
 * DESCRIPTION:
 *
 * Solution of the differential equation
 *
 *	y"(x) = xy.
 *
 * The function returns the two independent solutions Ai, Bi
 * and their first derivatives Ai'(x), Bi'(x).
 *
 * Evaluation is by power series summation for small x,
 * by rational minimax approximations for large x.
 *
 *
 *
 * ACCURACY:
 * Error criterion is absolute when function <= 1, relative
 * when function > 1, except * denotes relative error criterion.
 * For large negative x, the absolute error increases as x^1.5.
 * For large positive x, the relative error increases as x^1.5.
 *
 * Arithmetic  domain   function  # trials      peak         rms
 * IEEE        -10, 0     Ai        10000       1.6e-15     2.7e-16
 * IEEE          0, 10    Ai        10000       2.3e-14*    1.8e-15*
 * IEEE        -10, 0     Ai'       10000       4.6e-15     7.6e-16
 * IEEE          0, 10    Ai'       10000       1.8e-14*    1.5e-15*
 * IEEE        -10, 10    Bi        30000       4.2e-15     5.3e-16
 * IEEE        -10, 10    Bi'       30000       4.9e-15     7.3e-16
 * DEC         -10, 0     Ai         5000       1.7e-16     2.8e-17
 * DEC           0, 10    Ai         5000       2.1e-15*    1.7e-16*
 * DEC         -10, 0     Ai'        5000       4.7e-16     7.8e-17
 * DEC           0, 10    Ai'       12000       1.8e-15*    1.5e-16*
 * DEC         -10, 10    Bi        10000       5.5e-16     6.8e-17
 * DEC         -10, 10    Bi'        7000       5.3e-16     8.7e-17
 *
 */
/*							airy.c */

static double c1 = 0.35502805388781723926;
static double c2 = 0.258819403792806798405;
static double sqrt3 = 1.732050807568877293527;
static double sqpii = 5.64189583547756286948E-1;

#ifdef UNK
#define MAXAIRY 25.77
#endif
#ifdef DEC
#define MAXAIRY 25.77
#endif
#ifdef IBMPC
#define MAXAIRY 103.892
#endif
#ifdef MIEEE
#define MAXAIRY 103.892
#endif


#ifdef UNK
static double ANAIRY[8] = {
  3.46538101525629032477E-1,
  1.20075952739645805542E1,
  7.62796053615234516538E1,
  1.68089224934630576269E2,
  1.59756391350164413639E2,
  7.05360906840444183113E1,
  1.40264691163389668864E1,
  9.99999999999999995305E-1,
};
static double ADAIRY[8] = {
  5.67594532638770212846E-1,
  1.47562562584847203173E1,
  8.45138970141474626562E1,
  1.77318088145400459522E2,
  1.64234692871529701831E2,
  7.14778400825575695274E1,
  1.40959135607834029598E1,
  1.00000000000000000470E0,
};
#endif
#ifdef DEC
static unsigned short ANAIRY[32] = {
0037661,0066561,0024675,0131301,
0041100,0017434,0034324,0101466,
0041630,0107450,0067427,0007430,
0042050,0013327,0071000,0034737,
0042037,0140642,0156417,0167366,
0041615,0011172,0075147,0051165,
0041140,0066152,0160520,0075146,
0040200,0000000,0000000,0000000,
};
static unsigned short ADAIRY[32] = {
0040021,0046740,0011422,0064606,
0041154,0014640,0024631,0062450,
0041651,0003435,0101152,0106401,
0042061,0050556,0034605,0136602,
0042044,0036024,0152377,0151414,
0041616,0172247,0072216,0115374,
0041141,0104334,0124154,0166007,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short ANAIRY[32] = {
0xb658,0x2537,0x2dae,0x3fd6,
0x9067,0x871a,0x03e3,0x4028,
0xe1e3,0x0de2,0x11e5,0x4053,
0x073c,0xee40,0x02da,0x4065,
0xfddf,0x5ba1,0xf834,0x4063,
0xea4f,0x4f4c,0xa24f,0x4051,
0x0f4d,0x5c2a,0x0d8d,0x402c,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short ADAIRY[32] = {
0x4d31,0x0262,0x29bc,0x3fe2,
0x2ca5,0x0533,0x8334,0x402d,
0x51a0,0xb04d,0x20e3,0x4055,
0xb7b0,0xc730,0x2a2d,0x4066,
0xfa61,0x9a9f,0x8782,0x4064,
0xd35f,0xee91,0xde94,0x4051,
0x9d81,0x950d,0x311b,0x402c,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short ANAIRY[32] = {
0x3fd6,0x2dae,0x2537,0xb658,
0x4028,0x03e3,0x871a,0x9067,
0x4053,0x11e5,0x0de2,0xe1e3,
0x4065,0x02da,0xee40,0x073c,
0x4063,0xf834,0x5ba1,0xfddf,
0x4051,0xa24f,0x4f4c,0xea4f,
0x402c,0x0d8d,0x5c2a,0x0f4d,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short ADAIRY[32] = {
0x3fe2,0x29bc,0x0262,0x4d31,
0x402d,0x8334,0x0533,0x2ca5,
0x4055,0x20e3,0xb04d,0x51a0,
0x4066,0x2a2d,0xc730,0xb7b0,
0x4064,0x8782,0x9a9f,0xfa61,
0x4051,0xde94,0xee91,0xd35f,
0x402c,0x311b,0x950d,0x9d81,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif

#ifdef UNK
static double APN[8] = {
  6.13759184814035759225E-1,
  1.47454670787755323881E1,
  8.20584123476060982430E1,
  1.71184781360976385540E2,
  1.59317847137141783523E2,
  6.99778599330103016170E1,
  1.39470856980481566958E1,
  1.00000000000000000550E0,
};
static double APD[8] = {
  3.34203677749736953049E-1,
  1.11810297306158156705E1,
  7.11727352147859965283E1,
  1.58778084372838313640E2,
  1.53206427475809220834E2,
  6.86752304592780337944E1,
  1.38498634758259442477E1,
  9.99999999999999994502E-1,
};
#endif
#ifdef DEC
static unsigned short APN[32] = {
0040035,0017522,0065145,0054755,
0041153,0166556,0161471,0057174,
0041644,0016750,0034445,0046462,
0042053,0027515,0152316,0046717,
0042037,0050536,0067023,0023264,
0041613,0172252,0007240,0131055,
0041137,0023503,0052472,0002305,
0040200,0000000,0000000,0000000,
};
static unsigned short APD[32] = {
0037653,0016276,0112106,0126625,
0041062,0162577,0067111,0111761,
0041616,0054160,0140004,0137455,
0042036,0143460,0104626,0157206,
0042031,0032330,0067131,0114260,
0041611,0054667,0147207,0134564,
0041135,0114412,0070653,0146015,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short APN[32] = {
0xab3e,0x4d4c,0xa3ea,0x3fe3,
0x2bcf,0xdc67,0x7dad,0x402d,
0xa9a6,0x0724,0x83bd,0x4054,
0xc9ba,0xba99,0x65e9,0x4065,
0x64d7,0xcdc2,0xea2b,0x4063,
0x1646,0x41d4,0x7e95,0x4051,
0x4099,0x6aa7,0xe4e8,0x402b,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short APD[32] = {
0xd5b3,0xd288,0x6397,0x3fd5,
0x327e,0xedc9,0x5caf,0x4026,
0x97e6,0x1800,0xcb0e,0x4051,
0xdbd1,0x1132,0xd8e6,0x4063,
0x3316,0x0dcb,0x269b,0x4063,
0xf72f,0xf9d0,0x2b36,0x4051,
0x7982,0x4e35,0xb321,0x402b,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short APN[32] = {
0x3fe3,0xa3ea,0x4d4c,0xab3e,
0x402d,0x7dad,0xdc67,0x2bcf,
0x4054,0x83bd,0x0724,0xa9a6,
0x4065,0x65e9,0xba99,0xc9ba,
0x4063,0xea2b,0xcdc2,0x64d7,
0x4051,0x7e95,0x41d4,0x1646,
0x402b,0xe4e8,0x6aa7,0x4099,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short APD[32] = {
0x3fd5,0x6397,0xd288,0xd5b3,
0x4026,0x5caf,0xedc9,0x327e,
0x4051,0xcb0e,0x1800,0x97e6,
0x4063,0xd8e6,0x1132,0xdbd1,
0x4063,0x269b,0x0dcb,0x3316,
0x4051,0x2b36,0xf9d0,0xf72f,
0x402b,0xb321,0x4e35,0x7982,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif

#ifdef UNK
static double BN16[5] = {
-2.53240795869364152689E-1,
 5.75285167332467384228E-1,
-3.29907036873225371650E-1,
 6.44404068948199951727E-2,
-3.82519546641336734394E-3,
};
static double BD16[5] = {
/* 1.00000000000000000000E0,*/
-7.15685095054035237902E0,
 1.06039580715664694291E1,
-5.23246636471251500874E0,
 9.57395864378383833152E-1,
-5.50828147163549611107E-2,
};
#endif
#ifdef DEC
static unsigned short BN16[20] = {
0137601,0124307,0010213,0035210,
0040023,0042743,0101621,0016031,
0137650,0164623,0036056,0074511,
0037203,0174525,0000473,0142474,
0136172,0130041,0066726,0064324,
};
static unsigned short BD16[20] = {
/*0040200,0000000,0000000,0000000,*/
0140745,0002354,0044335,0055276,
0041051,0124717,0170130,0104013,
0140647,0070135,0046473,0103501,
0040165,0013745,0033324,0127766,
0137141,0117204,0076164,0033107,
};
#endif
#ifdef IBMPC
static unsigned short BN16[20] = {
0x6751,0xe211,0x3518,0xbfd0,
0x2383,0x7072,0x68bc,0x3fe2,
0xcf29,0x6785,0x1d32,0xbfd5,
0x78a8,0xa027,0x7f2a,0x3fb0,
0xcd1b,0x2dba,0x5604,0xbf6f,
};
static unsigned short BD16[20] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xab58,0x891b,0xa09d,0xc01c,
0x1101,0xfe0b,0x3539,0x4025,
0x70e8,0xa9a7,0xee0b,0xc014,
0x95ff,0xa6da,0xa2fc,0x3fee,
0x86c9,0x8f8e,0x33d0,0xbfac,
};
#endif
#ifdef MIEEE
static unsigned short BN16[20] = {
0xbfd0,0x3518,0xe211,0x6751,
0x3fe2,0x68bc,0x7072,0x2383,
0xbfd5,0x1d32,0x6785,0xcf29,
0x3fb0,0x7f2a,0xa027,0x78a8,
0xbf6f,0x5604,0x2dba,0xcd1b,
};
static unsigned short BD16[20] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0xc01c,0xa09d,0x891b,0xab58,
0x4025,0x3539,0xfe0b,0x1101,
0xc014,0xee0b,0xa9a7,0x70e8,
0x3fee,0xa2fc,0xa6da,0x95ff,
0xbfac,0x33d0,0x8f8e,0x86c9,
};
#endif

#ifdef UNK
static double BPPN[5] = {
 4.65461162774651610328E-1,
-1.08992173800493920734E0,
 6.38800117371827987759E-1,
-1.26844349553102907034E-1,
 7.62487844342109852105E-3,
};
static double BPPD[5] = {
/* 1.00000000000000000000E0,*/
-8.70622787633159124240E0,
 1.38993162704553213172E1,
-7.14116144616431159572E0,
 1.34008595960680518666E0,
-7.84273211323341930448E-2,
};
#endif
#ifdef DEC
static unsigned short BPPN[20] = {
0037756,0050354,0167531,0135731,
0140213,0101216,0032767,0020375,
0040043,0104147,0106312,0177632,
0137401,0161574,0032015,0043714,
0036371,0155035,0143165,0142262,
};
static unsigned short BPPD[20] = {
/*0040200,0000000,0000000,0000000,*/
0141013,0046265,0115005,0161053,
0041136,0061631,0072445,0156131,
0140744,0102145,0001127,0065304,
0040253,0103757,0146453,0102513,
0137240,0117200,0155402,0113500,
};
#endif
#ifdef IBMPC
static unsigned short BPPN[20] = {
0x377b,0x9deb,0xca1d,0x3fdd,
0xe420,0xc6be,0x7051,0xbff1,
0x5ff3,0xf199,0x710c,0x3fe4,
0xa8fa,0x8681,0x3c6f,0xbfc0,
0xb896,0xb8ce,0x3b43,0x3f7f,
};
static unsigned short BPPD[20] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xbc45,0xb340,0x6996,0xc021,
0xbb8b,0x2ea4,0xcc73,0x402b,
0xed59,0xa04a,0x908c,0xc01c,
0x70a9,0xf9a5,0x70fd,0x3ff5,
0x52e8,0x1b60,0x13d0,0xbfb4,
};
#endif
#ifdef MIEEE
static unsigned short BPPN[20] = {
0x3fdd,0xca1d,0x9deb,0x377b,
0xbff1,0x7051,0xc6be,0xe420,
0x3fe4,0x710c,0xf199,0x5ff3,
0xbfc0,0x3c6f,0x8681,0xa8fa,
0x3f7f,0x3b43,0xb8ce,0xb896,
};
static unsigned short BPPD[20] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0xc021,0x6996,0xb340,0xbc45,
0x402b,0xcc73,0x2ea4,0xbb8b,
0xc01c,0x908c,0xa04a,0xed59,
0x3ff5,0x70fd,0xf9a5,0x70a9,
0xbfb4,0x13d0,0x1b60,0x52e8,
};
#endif

#ifdef UNK
static double AFN[9] = {
-1.31696323418331795333E-1,
-6.26456544431912369773E-1,
-6.93158036036933542233E-1,
-2.79779981545119124951E-1,
-4.91900132609500318020E-2,
-4.06265923594885404393E-3,
-1.59276496239262096340E-4,
-2.77649108155232920844E-6,
-1.67787698489114633780E-8,
};
static double AFD[9] = {
/* 1.00000000000000000000E0,*/
 1.33560420706553243746E1,
 3.26825032795224613948E1,
 2.67367040941499554804E1,
 9.18707402907259625840E0,
 1.47529146771666414581E0,
 1.15687173795188044134E-1,
 4.40291641615211203805E-3,
 7.54720348287414296618E-5,
 4.51850092970580378464E-7,
};
#endif
#ifdef DEC
static unsigned short AFN[36] = {
0137406,0155546,0124127,0033732,
0140040,0057564,0141263,0041222,
0140061,0071316,0013674,0175754,
0137617,0037522,0056637,0120130,
0137111,0075567,0121755,0166122,
0136205,0020016,0043317,0002201,
0135047,0001565,0075130,0002334,
0133472,0051700,0165021,0131551,
0131620,0020347,0132165,0013215,
};
static unsigned short AFD[36] = {
/*0040200,0000000,0000000,0000000,*/
0041125,0131131,0025627,0067623,
0041402,0135342,0021703,0154315,
0041325,0162305,0016671,0120175,
0041022,0177101,0053114,0141632,
0040274,0153131,0147364,0114306,
0037354,0166545,0120042,0150530,
0036220,0043127,0000727,0130273,
0034636,0043275,0075667,0034733,
0032762,0112715,0146250,0142474,
};
#endif
#ifdef IBMPC
static unsigned short AFN[36] = {
0xe6fb,0xd50a,0xdb6c,0xbfc0,
0x6852,0x9856,0x0bee,0xbfe4,
0x9f7d,0xc2f7,0x2e59,0xbfe6,
0xf40b,0x4bb3,0xe7ea,0xbfd1,
0xbd8a,0xf47d,0x2f6e,0xbfa9,
0xe090,0xc8d9,0xa401,0xbf70,
0x009c,0xaf4b,0xe06e,0xbf24,
0x366d,0x1d42,0x4a78,0xbec7,
0xa2d2,0xf68e,0x041c,0xbe52,
};
static unsigned short AFD[36] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xedf2,0x2572,0xb64b,0x402a,
0x7b1a,0x4478,0x575c,0x4040,
0x3410,0xa3b7,0xbc98,0x403a,
0x9873,0x2ac9,0x5fc8,0x4022,
0x9319,0x39de,0x9acb,0x3ff7,
0x5a2b,0xb404,0x9dac,0x3fbd,
0xf617,0xe03a,0x08ca,0x3f72,
0xe73b,0xaf76,0xc8d7,0x3f13,
0x18a7,0xb995,0x52b9,0x3e9e,
};
#endif
#ifdef MIEEE
static unsigned short AFN[36] = {
0xbfc0,0xdb6c,0xd50a,0xe6fb,
0xbfe4,0x0bee,0x9856,0x6852,
0xbfe6,0x2e59,0xc2f7,0x9f7d,
0xbfd1,0xe7ea,0x4bb3,0xf40b,
0xbfa9,0x2f6e,0xf47d,0xbd8a,
0xbf70,0xa401,0xc8d9,0xe090,
0xbf24,0xe06e,0xaf4b,0x009c,
0xbec7,0x4a78,0x1d42,0x366d,
0xbe52,0x041c,0xf68e,0xa2d2,
};
static unsigned short AFD[36] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x402a,0xb64b,0x2572,0xedf2,
0x4040,0x575c,0x4478,0x7b1a,
0x403a,0xbc98,0xa3b7,0x3410,
0x4022,0x5fc8,0x2ac9,0x9873,
0x3ff7,0x9acb,0x39de,0x9319,
0x3fbd,0x9dac,0xb404,0x5a2b,
0x3f72,0x08ca,0xe03a,0xf617,
0x3f13,0xc8d7,0xaf76,0xe73b,
0x3e9e,0x52b9,0xb995,0x18a7,
};
#endif

#ifdef UNK
static double AGN[11] = {
  1.97339932091685679179E-2,
  3.91103029615688277255E-1,
  1.06579897599595591108E0,
  9.39169229816650230044E-1,
  3.51465656105547619242E-1,
  6.33888919628925490927E-2,
  5.85804113048388458567E-3,
  2.82851600836737019778E-4,
  6.98793669997260967291E-6,
  8.11789239554389293311E-8,
  3.41551784765923618484E-10,
};
static double AGD[10] = {
/*  1.00000000000000000000E0,*/
  9.30892908077441974853E0,
  1.98352928718312140417E1,
  1.55646628932864612953E1,
  5.47686069422975497931E0,
  9.54293611618961883998E-1,
  8.64580826352392193095E-2,
  4.12656523824222607191E-3,
  1.01259085116509135510E-4,
  1.17166733214413521882E-6,
  4.91834570062930015649E-9,
};
#endif
#ifdef DEC
static unsigned short AGN[44] = {
0036641,0124456,0167175,0157354,
0037710,0037250,0001441,0136671,
0040210,0066031,0150401,0123532,
0040160,0066545,0003570,0153133,
0037663,0171516,0072507,0170345,
0037201,0151011,0007510,0045702,
0036277,0172317,0104572,0101030,
0035224,0045663,0000160,0136422,
0033752,0074753,0047702,0135160,
0032256,0052225,0156550,0107103,
0030273,0142443,0166277,0071720,
};
static unsigned short AGD[40] = {
/*0040200,0000000,0000000,0000000,*/
0041024,0170537,0117253,0055003,
0041236,0127256,0003570,0143240,
0041171,0004333,0172476,0160645,
0040657,0041161,0055716,0157161,
0040164,0046226,0006257,0063431,
0037261,0010357,0065445,0047563,
0036207,0034043,0057434,0116732,
0034724,0055416,0130035,0026377,
0033235,0041056,0154071,0023502,
0031250,0177071,0167254,0047242,
};
#endif
#ifdef IBMPC
static unsigned short AGN[44] = {
0xbbde,0xddcf,0x3525,0x3f94,
0x37b7,0x0064,0x07d5,0x3fd9,
0x34eb,0x3a20,0x0d83,0x3ff1,
0x1acb,0xa0ef,0x0dac,0x3fee,
0xfe1d,0xcea8,0x7e69,0x3fd6,
0x0978,0x21e9,0x3a41,0x3fb0,
0x5043,0xf12f,0xfe99,0x3f77,
0x17a2,0x600e,0x8976,0x3f32,
0x574e,0x69f8,0x4f3d,0x3edd,
0x11c8,0xbbad,0xca92,0x3e75,
0xee7a,0x7d97,0x78a4,0x3df7,
};
static unsigned short AGD[40] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x6b40,0xf3d5,0x9e2b,0x4022,
0x18d4,0xc0ef,0xd5d5,0x4033,
0xdc35,0x7ea7,0x211b,0x402f,
0xdbce,0x2b79,0xe84e,0x4015,
0xece3,0xc195,0x8992,0x3fee,
0xa9ee,0xed64,0x221d,0x3fb6,
0x93bb,0x6be3,0xe704,0x3f70,
0xa5a0,0xd603,0x8b61,0x3f1a,
0x24e8,0xdb07,0xa845,0x3eb3,
0x89d4,0x3dd5,0x1fc7,0x3e35,
};
#endif
#ifdef MIEEE
static unsigned short AGN[44] = {
0x3f94,0x3525,0xddcf,0xbbde,
0x3fd9,0x07d5,0x0064,0x37b7,
0x3ff1,0x0d83,0x3a20,0x34eb,
0x3fee,0x0dac,0xa0ef,0x1acb,
0x3fd6,0x7e69,0xcea8,0xfe1d,
0x3fb0,0x3a41,0x21e9,0x0978,
0x3f77,0xfe99,0xf12f,0x5043,
0x3f32,0x8976,0x600e,0x17a2,
0x3edd,0x4f3d,0x69f8,0x574e,
0x3e75,0xca92,0xbbad,0x11c8,
0x3df7,0x78a4,0x7d97,0xee7a,
};
static unsigned short AGD[40] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4022,0x9e2b,0xf3d5,0x6b40,
0x4033,0xd5d5,0xc0ef,0x18d4,
0x402f,0x211b,0x7ea7,0xdc35,
0x4015,0xe84e,0x2b79,0xdbce,
0x3fee,0x8992,0xc195,0xece3,
0x3fb6,0x221d,0xed64,0xa9ee,
0x3f70,0xe704,0x6be3,0x93bb,
0x3f1a,0x8b61,0xd603,0xa5a0,
0x3eb3,0xa845,0xdb07,0x24e8,
0x3e35,0x1fc7,0x3dd5,0x89d4,
};
#endif

#ifdef UNK
static double APFN[9] = {
  1.85365624022535566142E-1,
  8.86712188052584095637E-1,
  9.87391981747398547272E-1,
  4.01241082318003734092E-1,
  7.10304926289631174579E-2,
  5.90618657995661810071E-3,
  2.33051409401776799569E-4,
  4.08718778289035454598E-6,
  2.48379932900442457853E-8,
};
static double APFD[9] = {
/*  1.00000000000000000000E0,*/
  1.47345854687502542552E1,
  3.75423933435489594466E1,
  3.14657751203046424330E1,
  1.09969125207298778536E1,
  1.78885054766999417817E0,
  1.41733275753662636873E-1,
  5.44066067017226003627E-3,
  9.39421290654511171663E-5,
  5.65978713036027009243E-7,
};
#endif
#ifdef DEC
static unsigned short APFN[36] = {
0037475,0150174,0071752,0166651,
0040142,0177621,0164246,0101757,
0040174,0142670,0106760,0006573,
0037715,0067570,0116274,0022404,
0037221,0074157,0053341,0117207,
0036301,0104257,0015075,0004777,
0035164,0057502,0164034,0001313,
0033611,0022254,0176000,0112565,
0031725,0055523,0025153,0166057,
};
static unsigned short APFD[36] = {
/*0040200,0000000,0000000,0000000,*/
0041153,0140334,0130506,0061402,
0041426,0025551,0024440,0070611,
0041373,0134750,0047147,0176702,
0041057,0171532,0105430,0017674,
0040344,0174416,0001726,0047754,
0037421,0021207,0020167,0136264,
0036262,0043621,0151321,0124324,
0034705,0001313,0163733,0016407,
0033027,0166702,0150440,0170561,
};
#endif
#ifdef IBMPC
static unsigned short APFN[36] = {
0x5db5,0x8e7d,0xba0f,0x3fc7,
0xd07e,0x3d14,0x5ff2,0x3fec,
0x01af,0x11be,0x98b7,0x3fef,
0x84a1,0x1397,0xadef,0x3fd9,
0x33d1,0xeadc,0x2f0d,0x3fb2,
0xa140,0xe347,0x3115,0x3f78,
0x8059,0x5d03,0x8be8,0x3f2e,
0x12af,0x9f80,0x2495,0x3ed1,
0x7d86,0x654d,0xab6a,0x3e5a,
};
static unsigned short APFD[36] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xcc60,0x9628,0x781b,0x402d,
0x0e31,0x2524,0xc56d,0x4042,
0xffb8,0x09cc,0x773d,0x403f,
0x03f7,0x5163,0xfe6b,0x4025,
0xc9fd,0xc07a,0x9f21,0x3ffc,
0xf796,0xe40e,0x2450,0x3fc2,
0x351a,0x3a5a,0x48f2,0x3f76,
0x63a1,0x7cfb,0xa059,0x3f18,
0x1e2e,0x5a24,0xfdb8,0x3ea2,
};
#endif
#ifdef MIEEE
static unsigned short APFN[36] = {
0x3fc7,0xba0f,0x8e7d,0x5db5,
0x3fec,0x5ff2,0x3d14,0xd07e,
0x3fef,0x98b7,0x11be,0x01af,
0x3fd9,0xadef,0x1397,0x84a1,
0x3fb2,0x2f0d,0xeadc,0x33d1,
0x3f78,0x3115,0xe347,0xa140,
0x3f2e,0x8be8,0x5d03,0x8059,
0x3ed1,0x2495,0x9f80,0x12af,
0x3e5a,0xab6a,0x654d,0x7d86,
};
static unsigned short APFD[36] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x402d,0x781b,0x9628,0xcc60,
0x4042,0xc56d,0x2524,0x0e31,
0x403f,0x773d,0x09cc,0xffb8,
0x4025,0xfe6b,0x5163,0x03f7,
0x3ffc,0x9f21,0xc07a,0xc9fd,
0x3fc2,0x2450,0xe40e,0xf796,
0x3f76,0x48f2,0x3a5a,0x351a,
0x3f18,0xa059,0x7cfb,0x63a1,
0x3ea2,0xfdb8,0x5a24,0x1e2e,
};
#endif

#ifdef UNK
static double APGN[11] = {
-3.55615429033082288335E-2,
-6.37311518129435504426E-1,
-1.70856738884312371053E0,
-1.50221872117316635393E0,
-5.63606665822102676611E-1,
-1.02101031120216891789E-1,
-9.48396695961445269093E-3,
-4.60325307486780994357E-4,
-1.14300836484517375919E-5,
-1.33415518685547420648E-7,
-5.63803833958893494476E-10,
};
static double APGD[11] = {
/*  1.00000000000000000000E0,*/
  9.85865801696130355144E0,
  2.16401867356585941885E1,
  1.73130776389749389525E1,
  6.17872175280828766327E0,
  1.08848694396321495475E0,
  9.95005543440888479402E-2,
  4.78468199683886610842E-3,
  1.18159633322838625562E-4,
  1.37480673554219441465E-6,
  5.79912514929147598821E-9,
};
#endif
#ifdef DEC
static unsigned short APGN[44] = {
0137021,0124372,0176075,0075331,
0140043,0023330,0177672,0161655,
0140332,0131126,0010413,0171112,
0140300,0044263,0175560,0054070,
0140020,0044206,0142603,0073324,
0137321,0015130,0066144,0144033,
0136433,0061243,0175542,0103373,
0135361,0053721,0020441,0053203,
0134077,0141725,0160277,0130612,
0132417,0040372,0100363,0060200,
0130432,0175052,0171064,0034147,
};
static unsigned short APGD[40] = {
/*0040200,0000000,0000000,0000000,*/
0041035,0136420,0030124,0140220,
0041255,0017432,0034447,0162256,
0041212,0100456,0154544,0006321,
0040705,0134026,0127154,0123414,
0040213,0051612,0044470,0172607,
0037313,0143362,0053273,0157051,
0036234,0144322,0054536,0007264,
0034767,0146170,0054265,0170342,
0033270,0102777,0167362,0073631,
0031307,0040644,0167103,0021763,
};
#endif
#ifdef IBMPC
static unsigned short APGN[44] = {
0xaf5b,0x5f87,0x351f,0xbfa2,
0x5c76,0x1ff7,0x64db,0xbfe4,
0x7e49,0xc221,0x564a,0xbffb,
0x0b07,0x7f6e,0x0916,0xbff8,
0x6edb,0xd8b0,0x0910,0xbfe2,
0x9903,0x0d8c,0x234b,0xbfba,
0x50df,0x7f6c,0x6c54,0xbf83,
0x2ad0,0x2424,0x2afa,0xbf3e,
0xf631,0xbc17,0xf87a,0xbee7,
0x6c10,0x501e,0xe81f,0xbe81,
0x870d,0x5e46,0x5f45,0xbe03,
};
static unsigned short APGD[40] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x9812,0x060a,0xb7a2,0x4023,
0xfc96,0x4724,0xa3e3,0x4035,
0x819a,0xdb2c,0x5025,0x4031,
0x94e2,0xd5cd,0xb702,0x4018,
0x1eb1,0x4927,0x6a71,0x3ff1,
0x7bc5,0x4ad7,0x78de,0x3fb9,
0xc1d7,0x4b2b,0x991a,0x3f73,
0xbe1c,0x0b16,0xf98f,0x3f1e,
0x4ef3,0xfdde,0x10bf,0x3eb7,
0x647e,0x9dc8,0xe834,0x3e38,
};
#endif
#ifdef MIEEE
static unsigned short APGN[44] = {
0xbfa2,0x351f,0x5f87,0xaf5b,
0xbfe4,0x64db,0x1ff7,0x5c76,
0xbffb,0x564a,0xc221,0x7e49,
0xbff8,0x0916,0x7f6e,0x0b07,
0xbfe2,0x0910,0xd8b0,0x6edb,
0xbfba,0x234b,0x0d8c,0x9903,
0xbf83,0x6c54,0x7f6c,0x50df,
0xbf3e,0x2afa,0x2424,0x2ad0,
0xbee7,0xf87a,0xbc17,0xf631,
0xbe81,0xe81f,0x501e,0x6c10,
0xbe03,0x5f45,0x5e46,0x870d,
};
static unsigned short APGD[40] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4023,0xb7a2,0x060a,0x9812,
0x4035,0xa3e3,0x4724,0xfc96,
0x4031,0x5025,0xdb2c,0x819a,
0x4018,0xb702,0xd5cd,0x94e2,
0x3ff1,0x6a71,0x4927,0x1eb1,
0x3fb9,0x78de,0x4ad7,0x7bc5,
0x3f73,0x991a,0x4b2b,0xc1d7,
0x3f1e,0xf98f,0x0b16,0xbe1c,
0x3eb7,0x10bf,0xfdde,0x4ef3,
0x3e38,0xe834,0x9dc8,0x647e,
};
#endif

int airy(double x, double* ai, double* aip, double* bi, double* bip )
{
double z, zz, t, f, g, uf, ug, k, zeta, theta;
int domflg;

domflg = 0;
if( x > MAXAIRY )
	{
	*ai = 0;
	*aip = 0;
	*bi = MAXNUM;
	*bip = MAXNUM;
	return(-1);
	}

if( x < -2.09 )
	{
	domflg = 15;
	t = sqrt(-x);
	zeta = -2.0 * x * t / 3.0;
	t = sqrt(t);
	k = sqpii / t;
	z = 1.0/zeta;
	zz = z * z;
	uf = 1.0 + zz * polevl( zz, AFN, 8 ) / p1evl( zz, AFD, 9 );
	ug = z * polevl( zz, AGN, 10 ) / p1evl( zz, AGD, 10 );
	theta = zeta + 0.25 * PI;
	f = sin( theta );
	g = cos( theta );
	*ai = k * (f * uf - g * ug);
	*bi = k * (g * uf + f * ug);
	uf = 1.0 + zz * polevl( zz, APFN, 8 ) / p1evl( zz, APFD, 9 );
	ug = z * polevl( zz, APGN, 10 ) / p1evl( zz, APGD, 10 );
	k = sqpii * t;
	*aip = -k * (g * uf + f * ug);
	*bip = k * (f * uf - g * ug);
	return(0);
	}

if( x >= 2.09 )	/* cbrt(9) */
	{
	domflg = 5;
	t = sqrt(x);
	zeta = 2.0 * x * t / 3.0;
	g = exp( zeta );
	t = sqrt(t);
	k = 2.0 * t * g;
	z = 1.0/zeta;
	f = polevl( z, ANAIRY, 7 ) / polevl( z, ADAIRY, 7 );
	*ai = sqpii * f / k;
	k = -0.5 * sqpii * t / g;
	f = polevl( z, APN, 7 ) / polevl( z, APD, 7 );
	*aip = f * k;

	if( x > 8.3203353 )	/* zeta > 16 */
		{
		f = z * polevl( z, BN16, 4 ) / p1evl( z, BD16, 5 );
		k = sqpii * g;
		*bi = k * (1.0 + f) / t;
		f = z * polevl( z, BPPN, 4 ) / p1evl( z, BPPD, 5 );
		*bip = k * t * (1.0 + f);
		return(0);
		}
	}

f = 1.0;
g = x;
t = 1.0;
uf = 1.0;
ug = x;
k = 1.0;
z = x * x * x;
while( t > MACHEP )
	{
	uf *= z;
	k += 1.0;
	uf /=k;
	ug *= z;
	k += 1.0;
	ug /=k;
	uf /=k;
	f += uf;
	k += 1.0;
	ug /=k;
	g += ug;
	t = fabs(uf/f);
	}
uf = c1 * f;
ug = c2 * g;
if( (domflg & 1) == 0 )
	*ai = uf - ug;
if( (domflg & 2) == 0 )
	*bi = sqrt3 * (uf + ug);

/* the deriviative of ai */
k = 4.0;
uf = x * x/2.0;
ug = z/3.0;
f = uf;
g = 1.0 + ug;
uf /= 3.0;
t = 1.0;

while( t > MACHEP )
	{
	uf *= z;
	ug /=k;
	k += 1.0;
	ug *= z;
	uf /=k;
	f += uf;
	k += 1.0;
	ug /=k;
	uf /=k;
	g += ug;
	k += 1.0;
	t = fabs(ug/g);
	}

uf = c1 * f;
ug = c2 * g;
if( (domflg & 4) == 0 )
	*aip = uf - ug;
if( (domflg & 8) == 0 )
	*bip = sqrt3 * (uf + ug);
return(0);
}

/* ========================================================================= */

/*							j0.c
 *
 *	Bessel function of order zero
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, j0();
 *
 * y = j0( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns Bessel function of order zero of the argument.
 *
 * The domain is divided into the intervals [0, 5] and
 * (5, infinity). In the first interval the following rational
 * approximation is used:
 *
 *
 *        2         2
 * (w - r  ) (w - r  ) P (w) / Q (w)
 *       1         2    3       8
 *
 *            2
 * where w = x  and the two r's are zeros of the function.
 *
 * In the second interval, the Hankel asymptotic expansion
 * is employed with two rational functions of degree 6/6
 * and 7/7.
 *
 *
 *
 * ACCURACY:
 *
 *                      Absolute error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0, 30       10000       4.4e-17     6.3e-18
 *    IEEE      0, 30       60000       4.2e-16     1.1e-16
 *
 */
/*							y0.c
 *
 *	Bessel function of the second kind, order zero
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, y0();
 *
 * y = y0( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns Bessel function of the second kind, of order
 * zero, of the argument.
 *
 * The domain is divided into the intervals [0, 5] and
 * (5, infinity). In the first interval a rational approximation
 * R(x) is employed to compute
 *   y0(x)  = R(x)  +   2 * log(x) * j0(x) / PI.
 * Thus a call to j0() is required.
 *
 * In the second interval, the Hankel asymptotic expansion
 * is employed with two rational functions of degree 6/6
 * and 7/7.
 *
 *
 *
 * ACCURACY:
 *
 *  Absolute error, when y0(x) < 1; else relative error:
 *
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0, 30        9400       7.0e-17     7.9e-18
 *    IEEE      0, 30       30000       1.3e-15     1.6e-16
 *
 */


/* Note: all coefficients satisfy the relative error criterion
 * except YP, YQ which are designed for absolute error. */

#if ((!defined(HAVE_J0)) || (!defined(HAVE_Y0)))
#ifdef UNK
static double PP[7] = {
  7.96936729297347051624E-4,
  8.28352392107440799803E-2,
  1.23953371646414299388E0,
  5.44725003058768775090E0,
  8.74716500199817011941E0,
  5.30324038235394892183E0,
  9.99999999999999997821E-1,
};
static double PQ[7] = {
  9.24408810558863637013E-4,
  8.56288474354474431428E-2,
  1.25352743901058953537E0,
  5.47097740330417105182E0,
  8.76190883237069594232E0,
  5.30605288235394617618E0,
  1.00000000000000000218E0,
};
#endif
#ifdef DEC
static unsigned short PP[28] = {
0035520,0164604,0140733,0054470,
0037251,0122605,0115356,0107170,
0040236,0124412,0071500,0056303,
0040656,0047737,0045720,0045263,
0041013,0172143,0045004,0142103,
0040651,0132045,0026241,0026406,
0040200,0000000,0000000,0000000,
};
static unsigned short PQ[28] = {
0035562,0052006,0070034,0134666,
0037257,0057055,0055242,0123424,
0040240,0071626,0046630,0032371,
0040657,0011077,0032013,0012731,
0041014,0030307,0050331,0006414,
0040651,0145457,0065021,0150304,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short PP[28] = {
0x6b27,0x983b,0x1d30,0x3f4a,
0xd1cf,0xb35d,0x34b0,0x3fb5,
0x0b98,0x4e68,0xd521,0x3ff3,
0x0956,0xe97a,0xc9fb,0x4015,
0x9888,0x6940,0x7e8c,0x4021,
0x25a1,0xa594,0x3684,0x4015,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short PQ[28] = {
0x9737,0xce03,0x4a80,0x3f4e,
0x54e3,0xab54,0xebc5,0x3fb5,
0x069f,0xc9b3,0x0e72,0x3ff4,
0x62bb,0xe681,0xe247,0x4015,
0x21a1,0xea1b,0x8618,0x4021,
0x3a19,0xed42,0x3965,0x4015,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short PP[28] = {
0x3f4a,0x1d30,0x983b,0x6b27,
0x3fb5,0x34b0,0xb35d,0xd1cf,
0x3ff3,0xd521,0x4e68,0x0b98,
0x4015,0xc9fb,0xe97a,0x0956,
0x4021,0x7e8c,0x6940,0x9888,
0x4015,0x3684,0xa594,0x25a1,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short PQ[28] = {
0x3f4e,0x4a80,0xce03,0x9737,
0x3fb5,0xebc5,0xab54,0x54e3,
0x3ff4,0x0e72,0xc9b3,0x069f,
0x4015,0xe247,0xe681,0x62bb,
0x4021,0x8618,0xea1b,0x21a1,
0x4015,0x3965,0xed42,0x3a19,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif

#ifdef UNK
static double QP[8] = {
-1.13663838898469149931E-2,
-1.28252718670509318512E0,
-1.95539544257735972385E1,
-9.32060152123768231369E1,
-1.77681167980488050595E2,
-1.47077505154951170175E2,
-5.14105326766599330220E1,
-6.05014350600728481186E0,
};
static double QQ[7] = {
/*  1.00000000000000000000E0,*/
  6.43178256118178023184E1,
  8.56430025976980587198E2,
  3.88240183605401609683E3,
  7.24046774195652478189E3,
  5.93072701187316984827E3,
  2.06209331660327847417E3,
  2.42005740240291393179E2,
};
#endif
#ifdef DEC
static unsigned short QP[32] = {
0136472,0035021,0142451,0141115,
0140244,0024731,0150620,0105642,
0141234,0067177,0124161,0060141,
0141672,0064572,0151557,0043036,
0142061,0127141,0003127,0043517,
0142023,0011727,0060271,0144544,
0141515,0122142,0126620,0143150,
0140701,0115306,0106715,0007344,
};
static unsigned short QQ[28] = {
/*0040200,0000000,0000000,0000000,*/
0041600,0121272,0004741,0026544,
0042526,0015605,0105654,0161771,
0043162,0123155,0165644,0062645,
0043342,0041675,0167576,0130756,
0043271,0052720,0165631,0154214,
0043000,0160576,0034614,0172024,
0042162,0000570,0030500,0051235,
};
#endif
#ifdef IBMPC
static unsigned short QP[32] = {
0x384a,0x38a5,0x4742,0xbf87,
0x1174,0x3a32,0x853b,0xbff4,
0x2c0c,0xf50e,0x8dcf,0xc033,
0xe8c4,0x5a6d,0x4d2f,0xc057,
0xe8ea,0x20ca,0x35cc,0xc066,
0x392d,0xec17,0x627a,0xc062,
0x18cd,0x55b2,0xb48c,0xc049,
0xa1dd,0xd1b9,0x3358,0xc018,
};
static unsigned short QQ[28] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x25ac,0x413c,0x1457,0x4050,
0x9c7f,0xb175,0xc370,0x408a,
0x8cb5,0xbd74,0x54cd,0x40ae,
0xd63e,0xbdef,0x4877,0x40bc,
0x3b11,0x1d73,0x2aba,0x40b7,
0x9e82,0xc731,0x1c2f,0x40a0,
0x0a54,0x0628,0x402f,0x406e,
};
#endif
#ifdef MIEEE
static unsigned short QP[32] = {
0xbf87,0x4742,0x38a5,0x384a,
0xbff4,0x853b,0x3a32,0x1174,
0xc033,0x8dcf,0xf50e,0x2c0c,
0xc057,0x4d2f,0x5a6d,0xe8c4,
0xc066,0x35cc,0x20ca,0xe8ea,
0xc062,0x627a,0xec17,0x392d,
0xc049,0xb48c,0x55b2,0x18cd,
0xc018,0x3358,0xd1b9,0xa1dd,
};
static unsigned short QQ[28] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4050,0x1457,0x413c,0x25ac,
0x408a,0xc370,0xb175,0x9c7f,
0x40ae,0x54cd,0xbd74,0x8cb5,
0x40bc,0x4877,0xbdef,0xd63e,
0x40b7,0x2aba,0x1d73,0x3b11,
0x40a0,0x1c2f,0xc731,0x9e82,
0x406e,0x402f,0x0628,0x0a54,
};
#endif
#endif


#ifndef HAVE_Y0
#ifdef UNK
static double YP[8] = {
 1.55924367855235737965E4,
-1.46639295903971606143E7,
 5.43526477051876500413E9,
-9.82136065717911466409E11,
 8.75906394395366999549E13,
-3.46628303384729719441E15,
 4.42733268572569800351E16,
-1.84950800436986690637E16,
};
static double YQ[7] = {
/* 1.00000000000000000000E0,*/
 1.04128353664259848412E3,
 6.26107330137134956842E5,
 2.68919633393814121987E8,
 8.64002487103935000337E10,
 2.02979612750105546709E13,
 3.17157752842975028269E15,
 2.50596256172653059228E17,
};
#endif
#ifdef DEC
static unsigned short YP[32] = {
0043563,0120677,0042264,0046166,
0146137,0140371,0113444,0042260,
0050241,0175707,0100502,0063344,
0152144,0125737,0007265,0164526,
0053637,0051621,0163035,0060546,
0155105,0004416,0107306,0060023,
0056035,0045133,0030132,0000024,
0155603,0065132,0144061,0131732,
};
static unsigned short YQ[28] = {
/*0040200,0000000,0000000,0000000,*/
0042602,0024422,0135557,0162663,
0045030,0155665,0044075,0160135,
0047200,0035432,0105446,0104005,
0051240,0167331,0056063,0022743,
0053223,0127746,0025764,0012160,
0055064,0044206,0177532,0145545,
0056536,0111375,0163715,0127201,
};
#endif
#ifdef IBMPC
static unsigned short YP[32] = {
0x898f,0xe896,0x7437,0x40ce,
0x8896,0x32e4,0xf81f,0xc16b,
0x4cdd,0xf028,0x3f78,0x41f4,
0xbd2b,0xe1d6,0x957b,0xc26c,
0xac2d,0x3cc3,0xea72,0x42d3,
0xcc02,0xd1d8,0xa121,0xc328,
0x4003,0x660b,0xa94b,0x4363,
0x367b,0x5906,0x6d4b,0xc350,
};
static unsigned short YQ[28] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xfcb6,0x576d,0x4522,0x4090,
0xbc0c,0xa907,0x1b76,0x4123,
0xd101,0x5164,0x0763,0x41b0,
0x64bc,0x2b86,0x1ddb,0x4234,
0x828e,0xc57e,0x75fc,0x42b2,
0x596d,0xdfeb,0x8910,0x4326,
0xb5d0,0xbcf9,0xd25f,0x438b,
};
#endif
#ifdef MIEEE
static unsigned short YP[32] = {
0x40ce,0x7437,0xe896,0x898f,
0xc16b,0xf81f,0x32e4,0x8896,
0x41f4,0x3f78,0xf028,0x4cdd,
0xc26c,0x957b,0xe1d6,0xbd2b,
0x42d3,0xea72,0x3cc3,0xac2d,
0xc328,0xa121,0xd1d8,0xcc02,
0x4363,0xa94b,0x660b,0x4003,
0xc350,0x6d4b,0x5906,0x367b,
};
static unsigned short YQ[28] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4090,0x4522,0x576d,0xfcb6,
0x4123,0x1b76,0xa907,0xbc0c,
0x41b0,0x0763,0x5164,0xd101,
0x4234,0x1ddb,0x2b86,0x64bc,
0x42b2,0x75fc,0xc57e,0x828e,
0x4326,0x8910,0xdfeb,0x596d,
0x438b,0xd25f,0xbcf9,0xb5d0,
};
#endif
#endif

#ifndef HAVE_J0
#ifdef UNK
/*  5.783185962946784521175995758455807035071 */
static double DR1 = 5.78318596294678452118E0;
/* 30.47126234366208639907816317502275584842 */
static double DR2 = 3.04712623436620863991E1;
#endif

#ifdef DEC
static unsigned short R1[] = {0040671,0007734,0001061,0056734};
#define DR1 *(double *)R1
static unsigned short R2[] = {0041363,0142445,0030416,0165567};
#define DR2 *(double *)R2
#endif

#ifdef IBMPC
static unsigned short R1[] = {0x2bbb,0x8046,0x21fb,0x4017};
#define DR1 *(double *)R1
static unsigned short R2[] = {0xdd6f,0xa621,0x78a4,0x403e};
#define DR2 *(double *)R2
#endif

#ifdef MIEEE
static unsigned short R1[] = {0x4017,0x21fb,0x8046,0x2bbb};
#define DR1 *(double *)R1
static unsigned short R2[] = {0x403e,0x78a4,0xa621,0xdd6f};
#define DR2 *(double *)R2
#endif

#ifdef UNK
static double RP[4] = {
-4.79443220978201773821E9,
 1.95617491946556577543E12,
-2.49248344360967716204E14,
 9.70862251047306323952E15,
};
static double RQ[8] = {
/* 1.00000000000000000000E0,*/
 4.99563147152651017219E2,
 1.73785401676374683123E5,
 4.84409658339962045305E7,
 1.11855537045356834862E10,
 2.11277520115489217587E12,
 3.10518229857422583814E14,
 3.18121955943204943306E16,
 1.71086294081043136091E18,
};
#endif
#ifdef DEC
static unsigned short RP[16] = {
0150216,0161235,0064344,0014450,
0052343,0135216,0035624,0144153,
0154142,0130247,0003310,0003667,
0055411,0173703,0047772,0176635,
};
static unsigned short RQ[32] = {
/*0040200,0000000,0000000,0000000,*/
0042371,0144025,0032265,0136137,
0044451,0133131,0132420,0151466,
0046470,0144641,0072540,0030636,
0050446,0126600,0045042,0044243,
0052365,0172633,0110301,0071063,
0054215,0032424,0062272,0043513,
0055742,0005013,0171731,0072335,
0057275,0170646,0036663,0013134,
};
#endif
#ifdef IBMPC
static unsigned short RP[16] = {
0x8325,0xad1c,0xdc53,0xc1f1,
0x990d,0xc772,0x7751,0x427c,
0x00f7,0xe0d9,0x5614,0xc2ec,
0x5fb4,0x69ff,0x3ef8,0x4341,
};
static unsigned short RQ[32] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xb78c,0xa696,0x3902,0x407f,
0x1a67,0x36a2,0x36cb,0x4105,
0x0634,0x2eac,0x1934,0x4187,
0x4914,0x0944,0xd5b0,0x4204,
0x2e46,0x7218,0xbeb3,0x427e,
0x48e9,0x8c97,0xa6a2,0x42f1,
0x2e9c,0x7e7b,0x4141,0x435c,
0x62cc,0xc7b6,0xbe34,0x43b7,
};
#endif
#ifdef MIEEE
static unsigned short RP[16] = {
0xc1f1,0xdc53,0xad1c,0x8325,
0x427c,0x7751,0xc772,0x990d,
0xc2ec,0x5614,0xe0d9,0x00f7,
0x4341,0x3ef8,0x69ff,0x5fb4,
};
static unsigned short RQ[32] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x407f,0x3902,0xa696,0xb78c,
0x4105,0x36cb,0x36a2,0x1a67,
0x4187,0x1934,0x2eac,0x0634,
0x4204,0xd5b0,0x0944,0x4914,
0x427e,0xbeb3,0x7218,0x2e46,
0x42f1,0xa6a2,0x8c97,0x48e9,
0x435c,0x4141,0x7e7b,0x2e9c,
0x43b7,0xbe34,0xc7b6,0x62cc,
};
#endif
#endif

#ifndef HAVE_J0
double j0(double x)
{
double w, z, p, q, xn;

if( x < 0 )
	x = -x;

if( x <= 5.0 )
	{
	z = x * x;
	if( x < 1.0e-5 )
		return( 1.0 - z/4.0 );

	p = (z - DR1) * (z - DR2);
	p = p * polevl( z, RP, 3)/p1evl( z, RQ, 8 );
	return( p );
	}

w = 5.0/x;
q = 25.0/(x*x);
p = polevl( q, PP, 6)/polevl( q, PQ, 6 );
q = polevl( q, QP, 7)/p1evl( q, QQ, 7 );
xn = x - PIO4;
p = p * cos(xn) - w * q * sin(xn);
return( p * SQ2OPI / sqrt(x) );
}
#endif


/*							y0() 2	*/
/* Bessel function of second kind, order zero	*/

/* Rational approximation coefficients YP[], YQ[] are used here.
 * The function computed is  y0(x)  -  2 * log(x) * j0(x) / PI,
 * whose value at x = 0 is  2 * ( log(0.5) + EUL ) / PI
 * = 0.073804295108687225.
 */

#ifndef HAVE_Y0
double y0(double x)
{
double w, z, p, q, xn;

if( x <= 5.0 )
	{
	if( x <= 0.0 )
		{
		mtherr( "y0", DOMAIN );
		return( -MAXNUM );
		}
	z = x * x;
	w = polevl( z, YP, 7) / p1evl( z, YQ, 7 );
	w += TWOOPI * log(x) * j0(x);
	return( w );
	}

w = 5.0/x;
z = 25.0 / (x * x);
p = polevl( z, PP, 6)/polevl( z, PQ, 6 );
q = polevl( z, QP, 7)/p1evl( z, QQ, 7 );
xn = x - PIO4;
p = p * sin(xn) + w * q * cos(xn);
return( p * SQ2OPI / sqrt(x) );
}
#endif

/* ========================================================================= */

/*							j1.c
 *
 *	Bessel function of order one
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, j1();
 *
 * y = j1( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns Bessel function of order one of the argument.
 *
 * The domain is divided into the intervals [0, 8] and
 * (8, infinity). In the first interval a 24 term Chebyshev
 * expansion is used. In the second, the asymptotic
 * trigonometric representation is employed using two
 * rational functions of degree 5/5.
 *
 *
 *
 * ACCURACY:
 *
 *                      Absolute error:
 * arithmetic   domain      # trials      peak         rms
 *    DEC       0, 30       10000       4.0e-17     1.1e-17
 *    IEEE      0, 30       30000       2.6e-16     1.1e-16
 *
 *
 */
/*							y1.c
 *
 *	Bessel function of second kind of order one
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, y1();
 *
 * y = y1( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns Bessel function of the second kind of order one
 * of the argument.
 *
 * The domain is divided into the intervals [0, 8] and
 * (8, infinity). In the first interval a 25 term Chebyshev
 * expansion is used, and a call to j1() is required.
 * In the second, the asymptotic trigonometric representation
 * is employed using two rational functions of degree 5/5.
 *
 *
 *
 * ACCURACY:
 *
 *                      Absolute error:
 * arithmetic   domain      # trials      peak         rms
 *    DEC       0, 30       10000       8.6e-17     1.3e-17
 *    IEEE      0, 30       30000       1.0e-15     1.3e-16
 *
 * (error criterion relative when |y1| > 1).
 *
 */


#ifndef HAVE_J1
#ifdef UNK
static double RP1[4] = {
-8.99971225705559398224E8,
 4.52228297998194034323E11,
-7.27494245221818276015E13,
 3.68295732863852883286E15,
};
static double RQ1[8] = {
/* 1.00000000000000000000E0,*/
 6.20836478118054335476E2,
 2.56987256757748830383E5,
 8.35146791431949253037E7,
 2.21511595479792499675E10,
 4.74914122079991414898E12,
 7.84369607876235854894E14,
 8.95222336184627338078E16,
 5.32278620332680085395E18,
};
#endif
#ifdef DEC
static unsigned short RP1[16] = {
0147526,0110742,0063322,0077052,
0051722,0112720,0065034,0061530,
0153604,0052227,0033147,0105650,
0055121,0055025,0032276,0022015,
};
static unsigned short RQ1[32] = {
/*0040200,0000000,0000000,0000000,*/
0042433,0032610,0155604,0033473,
0044572,0173320,0067270,0006616,
0046637,0045246,0162225,0006606,
0050645,0004773,0157577,0053004,
0052612,0033734,0001667,0176501,
0054462,0054121,0173147,0121367,
0056237,0002777,0121451,0176007,
0057623,0136253,0131601,0044710,
};
#endif
#ifdef IBMPC
static unsigned short RP1[16] = {
0x4fc5,0x4cda,0xd23c,0xc1ca,
0x8c6b,0x0d43,0x52ba,0x425a,
0xf175,0xe6cc,0x8a92,0xc2d0,
0xc482,0xa697,0x2b42,0x432a,
};
static unsigned short RQ1[32] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x86e7,0x1b70,0x66b1,0x4083,
0x01b2,0x0dd7,0x5eda,0x410f,
0xa1b1,0xdc92,0xe954,0x4193,
0xeac1,0x7bef,0xa13f,0x4214,
0xffa8,0x8076,0x46fb,0x4291,
0xf45f,0x3ecc,0x4b0a,0x4306,
0x3f81,0xf465,0xe0bf,0x4373,
0x2939,0x7670,0x7795,0x43d2,
};
#endif
#ifdef MIEEE
static unsigned short RP1[16] = {
0xc1ca,0xd23c,0x4cda,0x4fc5,
0x425a,0x52ba,0x0d43,0x8c6b,
0xc2d0,0x8a92,0xe6cc,0xf175,
0x432a,0x2b42,0xa697,0xc482,
};
static unsigned short RQ1[32] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4083,0x66b1,0x1b70,0x86e7,
0x410f,0x5eda,0x0dd7,0x01b2,
0x4193,0xe954,0xdc92,0xa1b1,
0x4214,0xa13f,0x7bef,0xeac1,
0x4291,0x46fb,0x8076,0xffa8,
0x4306,0x4b0a,0x3ecc,0xf45f,
0x4373,0xe0bf,0xf465,0x3f81,
0x43d2,0x7795,0x7670,0x2939,
};
#endif
#endif

#if ((!defined(HAVE_J1)) || (!defined(HAVE_Y1)))
#ifdef UNK
static double PP1[7] = {
 7.62125616208173112003E-4,
 7.31397056940917570436E-2,
 1.12719608129684925192E0,
 5.11207951146807644818E0,
 8.42404590141772420927E0,
 5.21451598682361504063E0,
 1.00000000000000000254E0,
};
static double PQ1[7] = {
 5.71323128072548699714E-4,
 6.88455908754495404082E-2,
 1.10514232634061696926E0,
 5.07386386128601488557E0,
 8.39985554327604159757E0,
 5.20982848682361821619E0,
 9.99999999999999997461E-1,
};
#endif
#ifdef DEC
static unsigned short PP1[28] = {
0035507,0144542,0061543,0024326,
0037225,0145105,0017766,0022661,
0040220,0043766,0010254,0133255,
0040643,0113047,0142611,0151521,
0041006,0144344,0055351,0074261,
0040646,0156520,0120574,0006416,
0040200,0000000,0000000,0000000,
};
static unsigned short PQ1[28] = {
0035425,0142330,0115041,0165514,
0037214,0177352,0145105,0052026,
0040215,0072515,0141207,0073255,
0040642,0056427,0137222,0106405,
0041006,0062716,0166427,0165450,
0040646,0133352,0035425,0123304,
0040200,0000000,0000000,0000000,
};
#endif
#ifdef IBMPC
static unsigned short PP1[28] = {
0x651b,0x4c6c,0xf92c,0x3f48,
0xc4b6,0xa3fe,0xb948,0x3fb2,
0x96d6,0xc215,0x08fe,0x3ff2,
0x3a6a,0xf8b1,0x72c4,0x4014,
0x2f16,0x8b5d,0xd91c,0x4020,
0x81a2,0x142f,0xdbaa,0x4014,
0x0000,0x0000,0x0000,0x3ff0,
};
static unsigned short PQ1[28] = {
0x3d69,0x1344,0xb89b,0x3f42,
0xaa83,0x5948,0x9fdd,0x3fb1,
0xeed6,0xb850,0xaea9,0x3ff1,
0x51a1,0xf7d2,0x4ba2,0x4014,
0xfd65,0xdda2,0xccb9,0x4020,
0xb4d9,0x4762,0xd6dd,0x4014,
0x0000,0x0000,0x0000,0x3ff0,
};
#endif
#ifdef MIEEE
static unsigned short PP1[28] = {
0x3f48,0xf92c,0x4c6c,0x651b,
0x3fb2,0xb948,0xa3fe,0xc4b6,
0x3ff2,0x08fe,0xc215,0x96d6,
0x4014,0x72c4,0xf8b1,0x3a6a,
0x4020,0xd91c,0x8b5d,0x2f16,
0x4014,0xdbaa,0x142f,0x81a2,
0x3ff0,0x0000,0x0000,0x0000,
};
static unsigned short PQ1[28] = {
0x3f42,0xb89b,0x1344,0x3d69,
0x3fb1,0x9fdd,0x5948,0xaa83,
0x3ff1,0xaea9,0xb850,0xeed6,
0x4014,0x4ba2,0xf7d2,0x51a1,
0x4020,0xccb9,0xdda2,0xfd65,
0x4014,0xd6dd,0x4762,0xb4d9,
0x3ff0,0x0000,0x0000,0x0000,
};
#endif

#ifdef UNK
static double QP1[8] = {
 5.10862594750176621635E-2,
 4.98213872951233449420E0,
 7.58238284132545283818E1,
 3.66779609360150777800E2,
 7.10856304998926107277E2,
 5.97489612400613639965E2,
 2.11688757100572135698E2,
 2.52070205858023719784E1,
};
static double QQ1[7] = {
/* 1.00000000000000000000E0,*/
 7.42373277035675149943E1,
 1.05644886038262816351E3,
 4.98641058337653607651E3,
 9.56231892404756170795E3,
 7.99704160447350683650E3,
 2.82619278517639096600E3,
 3.36093607810698293419E2,
};
#endif
#ifdef DEC
static unsigned short QP1[32] = {
0037121,0037723,0055605,0151004,
0040637,0066656,0031554,0077264,
0041627,0122714,0153170,0161466,
0042267,0061712,0036520,0140145,
0042461,0133315,0131573,0071176,
0042425,0057525,0147500,0013201,
0042123,0130122,0061245,0154131,
0041311,0123772,0064254,0172650,
};
static unsigned short QQ1[28] = {
/*0040200,0000000,0000000,0000000,*/
0041624,0074603,0002112,0101670,
0042604,0007135,0010162,0175565,
0043233,0151510,0157757,0172010,
0043425,0064506,0112006,0104276,
0043371,0164125,0032271,0164242,
0043060,0121425,0122750,0136013,
0042250,0005773,0053472,0146267,
};
#endif
#ifdef IBMPC
static unsigned short QP1[32] = {
0xba40,0x6b70,0x27fa,0x3faa,
0x8fd6,0xc66d,0xedb5,0x4013,
0x1c67,0x9acf,0xf4b9,0x4052,
0x180d,0x47aa,0xec79,0x4076,
0x6e50,0xb66f,0x36d9,0x4086,
0x02d0,0xb9e8,0xabea,0x4082,
0xbb0b,0x4c54,0x760a,0x406a,
0x9eb5,0x4d15,0x34ff,0x4039,
};
static unsigned short QQ1[28] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x5077,0x6089,0x8f30,0x4052,
0x5f6f,0xa20e,0x81cb,0x4090,
0xfe81,0x1bfd,0x7a69,0x40b3,
0xd118,0xd280,0xad28,0x40c2,
0x3d14,0xa697,0x3d0a,0x40bf,
0x1781,0xb4bd,0x1462,0x40a6,
0x5997,0x6ae7,0x017f,0x4075,
};
#endif
#ifdef MIEEE
static unsigned short QP1[32] = {
0x3faa,0x27fa,0x6b70,0xba40,
0x4013,0xedb5,0xc66d,0x8fd6,
0x4052,0xf4b9,0x9acf,0x1c67,
0x4076,0xec79,0x47aa,0x180d,
0x4086,0x36d9,0xb66f,0x6e50,
0x4082,0xabea,0xb9e8,0x02d0,
0x406a,0x760a,0x4c54,0xbb0b,
0x4039,0x34ff,0x4d15,0x9eb5,
};
static unsigned short QQ1[28] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4052,0x8f30,0x6089,0x5077,
0x4090,0x81cb,0xa20e,0x5f6f,
0x40b3,0x7a69,0x1bfd,0xfe81,
0x40c2,0xad28,0xd280,0xd118,
0x40bf,0x3d0a,0xa697,0x3d14,
0x40a6,0x1462,0xb4bd,0x1781,
0x4075,0x017f,0x6ae7,0x5997,
};
#endif
#endif

#ifndef HAVE_Y1
#ifdef UNK
static double YP1[6] = {
 1.26320474790178026440E9,
-6.47355876379160291031E11,
 1.14509511541823727583E14,
-8.12770255501325109621E15,
 2.02439475713594898196E17,
-7.78877196265950026825E17,
};
static double YQ1[8] = {
/* 1.00000000000000000000E0,*/
 5.94301592346128195359E2,
 2.35564092943068577943E5,
 7.34811944459721705660E7,
 1.87601316108706159478E10,
 3.88231277496238566008E12,
 6.20557727146953693363E14,
 6.87141087355300489866E16,
 3.97270608116560655612E18,
};
#endif
#ifdef DEC
static unsigned short YP1[24] = {
0047626,0112763,0013715,0133045,
0152026,0134552,0142033,0024411,
0053720,0045245,0102210,0077565,
0155347,0000321,0136415,0102031,
0056463,0146550,0055633,0032605,
0157054,0171012,0167361,0054265,
};
static unsigned short YQ1[32] = {
/*0040200,0000000,0000000,0000000,*/
0042424,0111515,0044773,0153014,
0044546,0005405,0171307,0075774,
0046614,0023575,0047105,0063556,
0050613,0143034,0101533,0156026,
0052541,0175367,0166514,0114257,
0054415,0014466,0134350,0171154,
0056164,0017436,0025075,0022101,
0057534,0103614,0103663,0121772,
};
#endif
#ifdef IBMPC
static unsigned short YP1[24] = {
0xb6c5,0x62f9,0xd2be,0x41d2,
0x6521,0x5883,0xd72d,0xc262,
0x0fef,0xb091,0x0954,0x42da,
0xb083,0x37a1,0xe01a,0xc33c,
0x66b1,0x0b73,0x79ad,0x4386,
0x2b17,0x5dde,0x9e41,0xc3a5,
};
static unsigned short YQ1[32] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x7ac2,0xa93f,0x9269,0x4082,
0xef7f,0xbe58,0xc160,0x410c,
0xacee,0xa9c8,0x84ef,0x4191,
0x7b83,0x906b,0x78c3,0x4211,
0x9316,0xfda9,0x3f5e,0x428c,
0x1e4e,0xd71d,0xa326,0x4301,
0xa488,0xc547,0x83e3,0x436e,
0x747f,0x90f6,0x90f1,0x43cb,
};
#endif
#ifdef MIEEE
static unsigned short YP1[24] = {
0x41d2,0xd2be,0x62f9,0xb6c5,
0xc262,0xd72d,0x5883,0x6521,
0x42da,0x0954,0xb091,0x0fef,
0xc33c,0xe01a,0x37a1,0xb083,
0x4386,0x79ad,0x0b73,0x66b1,
0xc3a5,0x9e41,0x5dde,0x2b17,
};
static unsigned short YQ1[32] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4082,0x9269,0xa93f,0x7ac2,
0x410c,0xc160,0xbe58,0xef7f,
0x4191,0x84ef,0xa9c8,0xacee,
0x4211,0x78c3,0x906b,0x7b83,
0x428c,0x3f5e,0xfda9,0x9316,
0x4301,0xa326,0xd71d,0x1e4e,
0x436e,0x83e3,0xc547,0xa488,
0x43cb,0x90f1,0x90f6,0x747f,
};
#endif
#endif


#ifndef HAVE_J1
#ifdef UNK
static double Z1 = 1.46819706421238932572E1;
static double Z2 = 4.92184563216946036703E1;
#endif

#ifdef DEC
static unsigned short DZ1[] = {0041152,0164532,0006114,0010540};
static unsigned short DZ2[] = {0041504,0157663,0001625,0020621};
#define Z1 (*(double *)DZ1)
#define Z2 (*(double *)DZ2)
#endif

#ifdef IBMPC
static unsigned short DZ1[] = {0x822c,0x4189,0x5d2b,0x402d};
static unsigned short DZ2[] = {0xa432,0x6072,0x9bf6,0x4048};
#define Z1 (*(double *)DZ1)
#define Z2 (*(double *)DZ2)
#endif

#ifdef MIEEE
static unsigned short DZ1[] = {0x402d,0x5d2b,0x4189,0x822c};
static unsigned short DZ2[] = {0x4048,0x9bf6,0x6072,0xa432};
#define Z1 (*(double *)DZ1)
#define Z2 (*(double *)DZ2)
#endif
#endif

#ifndef HAVE_J1
double j1(double x)
{
double w, z, p, q, xn;

w = x;
if( x < 0 )
	w = -x;

if( w <= 5.0 )
	{
	z = x * x;	
	w = polevl( z, RP1, 3 ) / p1evl( z, RQ1, 8 );
	w = w * x * (z - Z1) * (z - Z2);
	return( w );
	}

w = 5.0/x;
z = w * w;
p = polevl( z, PP1, 6)/polevl( z, PQ1, 6 );
q = polevl( z, QP1, 7)/p1evl( z, QQ1, 7 );
xn = x - THPIO4;
p = p * cos(xn) - w * q * sin(xn);
return( p * SQ2OPI / sqrt(x) );
}
#endif


#ifndef HAVE_Y1
double y1(x)
double x;
{
double w, z, p, q, xn;

if( x <= 5.0 )
	{
	if( x <= 0.0 )
		{
		mtherr( "y1", DOMAIN );
		return( -MAXNUM );
		}
	z = x * x;
	w = x * (polevl( z, YP1, 5 ) / p1evl( z, YQ1, 8 ));
	w += TWOOPI * ( j1(x) * log(x)  -  1.0/x );
	return( w );
	}

w = 5.0/x;
z = w * w;
p = polevl( z, PP1, 6)/polevl( z, PQ1, 6 );
q = polevl( z, QP1, 7)/p1evl( z, QQ1, 7 );
xn = x - THPIO4;
p = p * sin(xn) + w * q * cos(xn);
return( p * SQ2OPI / sqrt(x) );
}
#endif

/* ========================================================================= */

/*							jn.c
 *
 *	Bessel function of integer order
 *
 *
 *
 * SYNOPSIS:
 *
 * int n;
 * double x, y, jn();
 *
 * y = jn( n, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns Bessel function of order n, where n is a
 * (possibly negative) integer.
 *
 * The ratio of jn(x) to j0(x) is computed by backward
 * recurrence.  First the ratio jn/jn-1 is found by a
 * continued fraction expansion.  Then the recurrence
 * relating successive orders is applied until j0 or j1 is
 * reached.
 *
 * If n = 0 or 1 the routine for j0 or j1 is called
 * directly.
 *
 *
 *
 * ACCURACY:
 *
 *                      Absolute error:
 * arithmetic   range      # trials      peak         rms
 *    DEC       0, 30        5500       6.9e-17     9.3e-18
 *    IEEE      0, 30        5000       4.4e-16     7.9e-17
 *
 *
 * Not suitable for large n or x. Use jv() instead.
 *
 */


#ifndef HAVE_JN
double jn(int n, double x)
{
double pkm2, pkm1, pk, xk, r, ans;
int k, sign;

if( n < 0 )
	{
	n = -n;
	if( (n & 1) == 0 )	/* -1**n */
		sign = 1;
	else
		sign = -1;
	}
else
	sign = 1;

if( x < 0.0 )
	{
	if( n & 1 )
		sign = -sign;
	x = -x;
	}

if( n == 0 )
	return( sign * j0(x) );
if( n == 1 )
	return( sign * j1(x) );
if( n == 2 )
	return( sign * (2.0 * j1(x) / x  -  j0(x)) );

if( x < MACHEP )
	return( 0.0 );

/* continued fraction */
#ifdef DEC
k = 56;
#else
k = 53;
#endif

pk = 2 * (n + k);
ans = pk;
xk = x * x;

do
	{
	pk -= 2.0;
	ans = pk - (xk/ans);
	}
while( --k > 0 );
ans = x/ans;

/* backward recurrence */

pk = 1.0;
pkm1 = 1.0/ans;
k = n-1;
r = 2 * k;

do
	{
	pkm2 = (pkm1 * r  -  pk * x) / x;
	pk = pkm1;
	pkm1 = pkm2;
	r -= 2.0;
	}
while( --k > 0 );

if( fabs(pk) > fabs(pkm1) )
	ans = j1(x)/pk;
else
	ans = j0(x)/pkm1;
return( sign * ans );
}
#endif

/* ========================================================================= */

/*							jv.c
 *
 *	Bessel function of noninteger order
 *
 *
 *
 * SYNOPSIS:
 *
 * double v, x, y, jv();
 *
 * y = jv( v, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns Bessel function of order v of the argument,
 * where v is real.  Negative x is allowed if v is an integer.
 *
 * Several expansions are included: the ascending power
 * series, the Hankel expansion, and two transitional
 * expansions for large v.  If v is not too large, it
 * is reduced by recurrence to a region of best accuracy.
 * The transitional expansions give 12D accuracy for v > 500.
 *
 *
 *
 * ACCURACY:
 * Results for integer v are indicated by *, where x and v
 * both vary from -125 to +125.  Otherwise,
 * x ranges from 0 to 125, v ranges as indicated by "domain."
 * Error criterion is absolute, except relative when |jv()| > 1.
 *
 * arithmetic  v domain  x domain    # trials      peak       rms
 *    IEEE      0,125     0,125      100000      4.6e-15    2.2e-16
 *    IEEE   -125,0       0,125       40000      5.4e-11    3.7e-13
 *    IEEE      0,500     0,500       20000      4.4e-15    4.0e-16
 * Integer v:
 *    IEEE   -125,125   -125,125      50000      3.5e-15*   1.9e-16*
 *
 */





double jv(double n, double x)
{
double k, q, t, y, an;
int i, sign, nint;

nint = 0;	/* Flag for integer n */
sign = 1;	/* Flag for sign inversion */
an = fabs( n );
y = floor( an );
if( y == an )
	{
	nint = 1;
	i = an - 16384.0 * floor( an/16384.0 );
	if( n < 0.0 )
		{
		if( i & 1 )
			sign = -sign;
		n = an;
		}
	if( x < 0.0 )
		{
		if( i & 1 )
			sign = -sign;
		x = -x;
		}
	if( n == 0.0 )
		return( j0(x) );
	if( n == 1.0 )
		return( sign * j1(x) );
	}

if( (x < 0.0) && (y != an) )
	{
	mtherr( "Jv", DOMAIN );
	y = 0.0;
	goto done;
 	}

y = fabs(x);

if( y < MACHEP )
	goto underf;

k = 3.6 * sqrt(y);
t = 3.6 * sqrt(an);
if( (y < t) && (an > 21.0) )
	return( sign * jvs(n,x) );
if( (an < k) && (y > 21.0) )
	return( sign * hankel(n,x) );

if( an < 500.0 )
	{
/* Note: if x is too large, the continued
 * fraction will fail; but then the
 * Hankel expansion can be used.
 */
	if( nint != 0 )
		{
		k = 0.0;
		q = recur( &n, x, &k, 1 );
		if( k == 0.0 )
			{
			y = j0(x)/q;
			goto done;
			}
		if( k == 1.0 )
			{
			y = j1(x)/q;
			goto done;
			}
		}

if( an > 2.0 * y )
	goto rlarger;

	if( (n >= 0.0) && (n < 20.0)
		&& (y > 6.0) && (y < 20.0) )
		{
/* Recur backwards from a larger value of n
 */
rlarger:
		k = n;

		y = y + an + 1.0;
		if( y < 30.0 )
			y = 30.0;
		y = n + floor(y-n);
		q = recur( &y, x, &k, 0 );
		y = jvs(y,x) * q;
		goto done;
		}

	if( k <= 30.0 )
		{
		k = 2.0;
		}
	else if( k < 90.0 )
		{
		k = (3*k)/4;
		}
	if( an > (k + 3.0) )
		{
		if( n < 0.0 )
			k = -k;
		q = n - floor(n);
		k = floor(k) + q;
		if( n > 0.0 )
			q = recur( &n, x, &k, 1 );
		else
			{
			t = k;
			k = n;
			q = recur( &t, x, &k, 1 );
			k = t;
			}
		if( q == 0.0 )
			{
underf:
			y = 0.0;
			goto done;
			}
		}
	else
		{
		k = n;
		q = 1.0;
		}

/* boundary between convergence of
 * power series and Hankel expansion
 */
	y = fabs(k);
	if( y < 26.0 )
		t = (0.0083*y + 0.09)*y + 12.9;
	else
		t = 0.9 * y;

	if( x > t )
		y = hankel(k,x);
	else
		y = jvs(k,x);
#if DEBUG
printf( "y = %.16e, recur q = %.16e\n", y, q );
#endif
	if( n > 0.0 )
		y /= q;
	else
		y *= q;
	}

else
	{
/* For large n, use the uniform expansion
 * or the transitional expansion.
 * But if x is of the order of n**2,
 * these may blow up, whereas the
 * Hankel expansion will then work.
 */
	if( n < 0.0 )
		{
		mtherr( "Jv", TLOSS );
		y = 0.0;
		goto done;
		}
	t = x/n;
	t /= n;
	if( t > 0.3 )
		y = hankel(n,x);
	else
		y = jnx(n,x);
	}

done:	return( sign * y);
}

/* Reduce the order by backward recurrence.
 * AMS55 #9.1.27 and 9.1.73.
 */

static double recur(double* n, double x, double* newn, int cancel)
{
double pkm2, pkm1, pk, qkm2, qkm1;
/* double pkp1; */
double k, ans, qk, xk, yk, r, t, kf;
static double recurbig = BIG;
int nflag, ctr;

/* continued fraction for Jn(x)/Jn-1(x)  */
if( *n < 0.0 )
	nflag = 1;
else
	nflag = 0;

fstart:

#if DEBUG
printf( "recur: n = %.6e, newn = %.6e, cfrac = ", *n, *newn );
#endif

pkm2 = 0.0;
qkm2 = 1.0;
pkm1 = x;
qkm1 = *n + *n;
xk = -x * x;
yk = qkm1;
ans = 1.0;
ctr = 0;
do
	{
	yk += 2.0;
	pk = pkm1 * yk +  pkm2 * xk;
	qk = qkm1 * yk +  qkm2 * xk;
	pkm2 = pkm1;
	pkm1 = pk;
	qkm2 = qkm1;
	qkm1 = qk;
	if( qk != 0 )
		r = pk/qk;
	else
		r = 0.0;
	if( r != 0 )
		{
		t = fabs( (ans - r)/r );
		ans = r;
		}
	else
		t = 1.0;

	if( ++ctr > 1000 )
		{
		mtherr( "jv", UNDERFLOW );
		goto done;
		}
	if( t < MACHEP )
		goto done;

	if( fabs(pk) > recurbig )
		{
		pkm2 /= recurbig;
		pkm1 /= recurbig;
		qkm2 /= recurbig;
		qkm1 /= recurbig;
		}
	}
while( t > MACHEP );

done:

#if DEBUG
printf( "%.6e\n", ans );
#endif

/* Change n to n-1 if n < 0 and the continued fraction is small
 */
if( nflag > 0 )
	{
	if( fabs(ans) < 0.125 )
		{
		nflag = -1;
		*n = *n - 1.0;
		goto fstart;
		}
	}


kf = *newn;

/* backward recurrence
 *              2k
 *  J   (x)  =  --- J (x)  -  J   (x)
 *   k-1         x   k         k+1
 */

pk = 1.0;
pkm1 = 1.0/ans;
k = *n - 1.0;
r = 2 * k;
do
	{
	pkm2 = (pkm1 * r  -  pk * x) / x;
	/*	pkp1 = pk; */
	pk = pkm1;
	pkm1 = pkm2;
	r -= 2.0;
/*
	t = fabs(pkp1) + fabs(pk);
	if( (k > (kf + 2.5)) && (fabs(pkm1) < 0.25*t) )
		{
		k -= 1.0;
		t = x*x;
		pkm2 = ( (r*(r+2.0)-t)*pk - r*x*pkp1 )/t;
		pkp1 = pk;
		pk = pkm1;
		pkm1 = pkm2;
		r -= 2.0;
		}
*/
	k -= 1.0;
	}
while( k > (kf + 0.5) );

/* Take the larger of the last two iterates
 * on the theory that it may have less cancellation error.
 */

if( cancel )
	{
	if( (kf >= 0.0) && (fabs(pk) > fabs(pkm1)) )
		{
		k += 1.0;
		pkm2 = pk;
		}
	}
*newn = k;
#if DEBUG
printf( "newn %.6e rans %.6e\n", k, pkm2 );
#endif
return( pkm2 );
}



/* Ascending power series for Jv(x).
 * AMS55 #9.1.10.
 */

extern int sgngam;

static double jvs(double n, double x)
{
double t, u, y, z, k;
int ex;

z = -x * x / 4.0;
u = 1.0;
y = u;
k = 1.0;
t = 1.0;

while( t > MACHEP )
	{
	u *= z / (k * (n+k));
	y += u;
	k += 1.0;
	if( y != 0 )
		t = fabs( u/y );
	}
#if DEBUG
printf( "power series=%.5e ", y );
#endif
t = frexp( 0.5*x, &ex );
ex = ex * n;
if(  (ex > -1023)
  && (ex < 1023) 
  && (n > 0.0)
  && (n < (MAXGAM-1.0)) )
	{
	t = pow( 0.5*x, n ) / cephesgamma( n + 1.0 );
#if DEBUG
printf( "pow(.5*x, %.4e)/cephesgamma(n+1)=%.5e\n", n, t );
#endif
	y *= t;
	}
else
	{
#if DEBUG
	z = n * log(0.5*x);
	k = lgamma( n+1.0 );
	t = z - k;
	printf( "log pow=%.5e, lgamma(%.4e)=%.5e\n", z, n+1.0, k );
#else
	t = n * log(0.5*x) - lgamma(n + 1.0);
#endif
	if( y < 0 )
		{
		sgngam = -sgngam;
		y = -y;
		}
	t += log(y);
#if DEBUG
printf( "log y=%.5e\n", log(y) );
#endif
	if( t < -MAXLOG )
		{
		return( 0.0 );
		}
	if( t > MAXLOG )
		{
		mtherr( "Jv", OVERFLOW );
		return( MAXNUM );
		}
	y = sgngam * exp( t );
	}
return(y);
}

/* Hankel's asymptotic expansion
 * for large x.
 * AMS55 #9.2.5.
 */

static double hankel(double n, double x)
{
double t, u, z, k, sign, conv;
double p, q, j, m, pp, qq;
int flag;

m = 4.0*n*n;
j = 1.0;
z = 8.0 * x;
k = 1.0;
p = 1.0;
u = (m - 1.0)/z;
q = u;
sign = 1.0;
conv = 1.0;
flag = 0;
t = 1.0;
pp = 1.0e38;
qq = 1.0e38;

while( t > MACHEP )
	{
	k += 2.0;
	j += 1.0;
	sign = -sign;
	u *= (m - k * k)/(j * z);
	p += sign * u;
	k += 2.0;
	j += 1.0;
	u *= (m - k * k)/(j * z);
	q += sign * u;
	t = fabs(u/p);
	if( t < conv )
		{
		conv = t;
		qq = q;
		pp = p;
		flag = 1;
		}
/* stop if the terms start getting larger */
	if( (flag != 0) && (t > conv) )
		{
#if DEBUG
		printf( "Hankel: convergence to %.4E\n", conv );
#endif
		goto hank1;
		}
	}	

hank1:
u = x - (0.5*n + 0.25) * PI;
t = sqrt( 2.0/(PI*x) ) * ( pp * cos(u) - qq * sin(u) );
#if DEBUG
printf( "hank: %.6e\n", t );
#endif
return( t );
}


/* Asymptotic expansion for large n.
 * AMS55 #9.3.35.
 */

static double lambda[] = {
  1.0,
  1.041666666666666666666667E-1,
  8.355034722222222222222222E-2,
  1.282265745563271604938272E-1,
  2.918490264641404642489712E-1,
  8.816272674437576524187671E-1,
  3.321408281862767544702647E+0,
  1.499576298686255465867237E+1,
  7.892301301158651813848139E+1,
  4.744515388682643231611949E+2,
  3.207490090890661934704328E+3
};
static double mu[] = {
  1.0,
 -1.458333333333333333333333E-1,
 -9.874131944444444444444444E-2,
 -1.433120539158950617283951E-1,
 -3.172272026784135480967078E-1,
 -9.424291479571202491373028E-1,
 -3.511203040826354261542798E+0,
 -1.572726362036804512982712E+1,
 -8.228143909718594444224656E+1,
 -4.923553705236705240352022E+2,
 -3.316218568547972508762102E+3
};
static double P1[] = {
 -2.083333333333333333333333E-1,
  1.250000000000000000000000E-1
};
static double P2[] = {
  3.342013888888888888888889E-1,
 -4.010416666666666666666667E-1,
  7.031250000000000000000000E-2
};
static double P3[] = {
 -1.025812596450617283950617E+0,
  1.846462673611111111111111E+0,
 -8.912109375000000000000000E-1,
  7.324218750000000000000000E-2
};
static double P4[] = {
  4.669584423426247427983539E+0,
 -1.120700261622299382716049E+1,
  8.789123535156250000000000E+0,
 -2.364086914062500000000000E+0,
  1.121520996093750000000000E-1
};
static double P5[] = {
 -2.8212072558200244877E1,
  8.4636217674600734632E1,
 -9.1818241543240017361E1,
  4.2534998745388454861E1,
 -7.3687943594796316964E0,
  2.27108001708984375E-1
};
static double P6[] = {
  2.1257013003921712286E2,
 -7.6525246814118164230E2,
  1.0599904525279998779E3,
 -6.9957962737613254123E2,
  2.1819051174421159048E2,
 -2.6491430486951555525E1,
  5.7250142097473144531E-1
};
static double P7[] = {
 -1.9194576623184069963E3,
  8.0617221817373093845E3,
 -1.3586550006434137439E4,
  1.1655393336864533248E4,
 -5.3056469786134031084E3,
  1.2009029132163524628E3,
 -1.0809091978839465550E2,
  1.7277275025844573975E0
};


static double jnx(double n, double x)
{
double zeta, sqz, zz, zp, np;
double cbn, n23, t, z, sz;
double pp, qq, z32i, zzi;
double ak, bk, akl, bkl;
int sign, doa, dob, nflg, k, s, tk, tkp1, m;
static double u[8];
static double ai, aip, bi, bip;

/* Test for x very close to n.
 * Use expansion for transition region if so.
 */
cbn = cbrt(n);
z = (x - n)/cbn;
if( fabs(z) <= 0.7 )
	return( jnt(n,x) );

z = x/n;
zz = 1.0 - z*z;
if( zz == 0.0 )
	return(0.0);

if( zz > 0.0 )
	{
	sz = sqrt( zz );
	t = 1.5 * (log( (1.0+sz)/z ) - sz );	/* zeta ** 3/2		*/
	zeta = cbrt( t * t );
	nflg = 1;
	}
else
	{
	sz = sqrt(-zz);
	t = 1.5 * (sz - acos(1.0/z));
	zeta = -cbrt( t * t );
	nflg = -1;
	}
z32i = fabs(1.0/t);
sqz = cbrt(t);

/* Airy function */
n23 = cbrt( n * n );
t = n23 * zeta;

#if DEBUG
printf("zeta %.5E, Airy(%.5E)\n", zeta, t );
#endif
airy( t, &ai, &aip, &bi, &bip );

/* polynomials in expansion */
u[0] = 1.0;
zzi = 1.0/zz;
u[1] = polevl( zzi, P1, 1 )/sz;
u[2] = polevl( zzi, P2, 2 )/zz;
u[3] = polevl( zzi, P3, 3 )/(sz*zz);
pp = zz*zz;
u[4] = polevl( zzi, P4, 4 )/pp;
u[5] = polevl( zzi, P5, 5 )/(pp*sz);
pp *= zz;
u[6] = polevl( zzi, P6, 6 )/pp;
u[7] = polevl( zzi, P7, 7 )/(pp*sz);

#if DEBUG
for( k=0; k<=7; k++ )
	printf( "u[%d] = %.5E\n", k, u[k] );
#endif

pp = 0.0;
qq = 0.0;
np = 1.0;
/* flags to stop when terms get larger */
doa = 1;
dob = 1;
akl = MAXNUM;
bkl = MAXNUM;

for( k=0; k<=3; k++ )
	{
	tk = 2 * k;
	tkp1 = tk + 1;
	zp = 1.0;
	ak = 0.0;
	bk = 0.0;
	for( s=0; s<=tk; s++ )
		{
		if( doa )
			{
			if( (s & 3) > 1 )
				sign = nflg;
			else
				sign = 1;
			ak += sign * mu[s] * zp * u[tk-s];
			}

		if( dob )
			{
			m = tkp1 - s;
			if( ((m+1) & 3) > 1 )
				sign = nflg;
			else
				sign = 1;
			bk += sign * lambda[s] * zp * u[m];
			}
		zp *= z32i;
		}

	if( doa )
		{
		ak *= np;
		t = fabs(ak);
		if( t < akl )
			{
			akl = t;
			pp += ak;
			}
		else
			doa = 0;
		}

	if( dob )
		{
		bk += lambda[tkp1] * zp * u[0];
		bk *= -np/sqz;
		t = fabs(bk);
		if( t < bkl )
			{
			bkl = t;
			qq += bk;
			}
		else
			dob = 0;
		}
#if DEBUG
	printf("a[%d] %.5E, b[%d] %.5E\n", k, ak, k, bk );
#endif
	if( np < MACHEP )
		break;
	np /= n*n;
	}

/* normalizing factor ( 4*zeta/(1 - z**2) )**1/4	*/
t = 4.0 * zeta/zz;
t = sqrt( sqrt(t) );

t *= ai*pp/cbrt(n)  +  aip*qq/(n23*n);
return(t);
}

/* Asymptotic expansion for transition region,
 * n large and x close to n.
 * AMS55 #9.3.23.
 */

static double PF2[] = {
 -9.0000000000000000000e-2,
  8.5714285714285714286e-2
};
static double PF3[] = {
  1.3671428571428571429e-1,
 -5.4920634920634920635e-2,
 -4.4444444444444444444e-3
};
static double PF4[] = {
  1.3500000000000000000e-3,
 -1.6036054421768707483e-1,
  4.2590187590187590188e-2,
  2.7330447330447330447e-3
};
static double PG1[] = {
 -2.4285714285714285714e-1,
  1.4285714285714285714e-2
};
static double PG2[] = {
 -9.0000000000000000000e-3,
  1.9396825396825396825e-1,
 -1.1746031746031746032e-2
};
static double PG3[] = {
  1.9607142857142857143e-2,
 -1.5983694083694083694e-1,
  6.3838383838383838384e-3
};


static double jnt(double n, double x)
{
double z, zz, z3;
double cbn, n23, cbtwo;
double ai, aip, bi, bip;	/* Airy functions */
double nk, fk, gk, pp, qq;
double F[5], G[4];
int k;

cbn = cbrt(n);
z = (x - n)/cbn;
cbtwo = cbrt( 2.0 );

/* Airy function */
zz = -cbtwo * z;
airy( zz, &ai, &aip, &bi, &bip );

/* polynomials in expansion */
zz = z * z;
z3 = zz * z;
F[0] = 1.0;
F[1] = -z/5.0;
F[2] = polevl( z3, PF2, 1 ) * zz;
F[3] = polevl( z3, PF3, 2 );
F[4] = polevl( z3, PF4, 3 ) * z;
G[0] = 0.3 * zz;
G[1] = polevl( z3, PG1, 1 );
G[2] = polevl( z3, PG2, 2 ) * z;
G[3] = polevl( z3, PG3, 2 ) * zz;
#if DEBUG
for( k=0; k<=4; k++ )
	printf( "F[%d] = %.5E\n", k, F[k] );
for( k=0; k<=3; k++ )
	printf( "G[%d] = %.5E\n", k, G[k] );
#endif
pp = 0.0;
qq = 0.0;
nk = 1.0;
n23 = cbrt( n * n );

for( k=0; k<=4; k++ )
	{
	fk = F[k]*nk;
	pp += fk;
	if( k != 4 )
		{
		gk = G[k]*nk;
		qq += gk;
		}
#if DEBUG
	printf("fk[%d] %.5E, gk[%d] %.5E\n", k, fk, k, gk );
#endif
	nk /= n23;
	}

fk = cbtwo * ai * pp/cbn  +  cbrt(4.0) * aip * qq/n;
return(fk);
}

/* ========================================================================= */

/*							yn.c
 *
 *	Bessel function of second kind of integer order
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, yn();
 * int n;
 *
 * y = yn( n, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns Bessel function of order n, where n is a
 * (possibly negative) integer.
 *
 * The function is evaluated by forward recurrence on
 * n, starting with values computed by the routines
 * y0() and y1().
 *
 * If n = 0 or 1 the routine for y0 or y1 is called
 * directly.
 *
 *
 *
 * ACCURACY:
 *
 *
 *                      Absolute error, except relative
 *                      when y > 1:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0, 30        2200       2.9e-16     5.3e-17
 *    IEEE      0, 30       30000       3.4e-15     4.3e-16
 *
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * yn singularity   x = 0              MAXNUM
 * yn overflow                         MAXNUM
 *
 * Spot checked against tables for x, n between 0 and 100.
 *
 */


#ifndef HAVE_YN
double yn(int n, double x)
{
double an, anm1, anm2, r;
int k, sign;

if( n < 0 )
	{
	n = -n;
	if( (n & 1) == 0 )	/* -1**n */
		sign = 1;
	else
		sign = -1;
	}
else
	sign = 1;


if( n == 0 )
	return( sign * y0(x) );
if( n == 1 )
	return( sign * y1(x) );

/* test for overflow */
if( x <= 0.0 )
	{
	mtherr( "yn", SING );
	return( -MAXNUM );
	}

/* forward recurrence on n */

anm2 = y0(x);
anm1 = y1(x);
k = 1;
r = 2 * k;
do
	{
	an = r * anm1 / x  -  anm2;
	anm2 = anm1;
	anm1 = an;
	r += 2.0;
	++k;
	}
while( k < n );


return( sign * an );
}
#endif

/* ========================================================================= */

/*							i0.c
 *
 *	Modified Bessel function of order zero
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, i0();
 *
 * y = i0( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns modified Bessel function of order zero of the
 * argument.
 *
 * The function is defined as i0(x) = j0( ix ).
 *
 * The range is partitioned into the two intervals [0,8] and
 * (8, infinity).  Chebyshev polynomial expansions are employed
 * in each interval.
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0,30         6000       8.2e-17     1.9e-17
 *    IEEE      0,30        30000       5.8e-16     1.4e-16
 *
 */
/*							i0e.c
 *
 *	Modified Bessel function of order zero,
 *	exponentially scaled
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, i0e();
 *
 * y = i0e( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns exponentially scaled modified Bessel function
 * of order zero of the argument.
 *
 * The function is defined as i0e(x) = exp(-|x|) j0( ix ).
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0,30        30000       5.4e-16     1.2e-16
 * See i0().
 *
 */

/*							i0.c		*/


/* Chebyshev coefficients for exp(-x) I0(x)
 * in the interval [0,8].
 *
 * lim(x->0){ exp(-x) I0(x) } = 1.
 */

#ifdef UNK
static double AI0[] =
{
-4.41534164647933937950E-18,
 3.33079451882223809783E-17,
-2.43127984654795469359E-16,
 1.71539128555513303061E-15,
-1.16853328779934516808E-14,
 7.67618549860493561688E-14,
-4.85644678311192946090E-13,
 2.95505266312963983461E-12,
-1.72682629144155570723E-11,
 9.67580903537323691224E-11,
-5.18979560163526290666E-10,
 2.65982372468238665035E-9,
-1.30002500998624804212E-8,
 6.04699502254191894932E-8,
-2.67079385394061173391E-7,
 1.11738753912010371815E-6,
-4.41673835845875056359E-6,
 1.64484480707288970893E-5,
-5.75419501008210370398E-5,
 1.88502885095841655729E-4,
-5.76375574538582365885E-4,
 1.63947561694133579842E-3,
-4.32430999505057594430E-3,
 1.05464603945949983183E-2,
-2.37374148058994688156E-2,
 4.93052842396707084878E-2,
-9.49010970480476444210E-2,
 1.71620901522208775349E-1,
-3.04682672343198398683E-1,
 6.76795274409476084995E-1
};
#endif

#ifdef DEC
static unsigned short AI0[] = {
0121642,0162671,0004646,0103567,
0022431,0115424,0135755,0026104,
0123214,0023533,0110365,0156635,
0023767,0033304,0117662,0172716,
0124522,0100426,0012277,0157531,
0025254,0155062,0054461,0030465,
0126010,0131143,0013560,0153604,
0026517,0170577,0006336,0114437,
0127227,0162253,0152243,0052734,
0027724,0142766,0061641,0160200,
0130416,0123760,0116564,0125262,
0031066,0144035,0021246,0054641,
0131537,0053664,0060131,0102530,
0032201,0155664,0165153,0020652,
0132617,0061434,0074423,0176145,
0033225,0174444,0136147,0122542,
0133624,0031576,0056453,0020470,
0034211,0175305,0172321,0041314,
0134561,0054462,0147040,0165315,
0035105,0124333,0120203,0162532,
0135427,0013750,0174257,0055221,
0035726,0161654,0050220,0100162,
0136215,0131361,0000325,0041110,
0036454,0145417,0117357,0017352,
0136702,0072367,0104415,0133574,
0037111,0172126,0072505,0014544,
0137302,0055601,0120550,0033523,
0037457,0136543,0136544,0043002,
0137633,0177536,0001276,0066150,
0040055,0041164,0100655,0010521
};
#endif

#ifdef IBMPC
static unsigned short AI0[] = {
0xd0ef,0x2134,0x5cb7,0xbc54,
0xa589,0x977d,0x3362,0x3c83,
0xbbb4,0x721e,0x84eb,0xbcb1,
0x5eba,0x93f6,0xe6d8,0x3cde,
0xfbeb,0xc297,0x5022,0xbd0a,
0x2627,0x4b26,0x9b46,0x3d35,
0x1af0,0x62ee,0x164c,0xbd61,
0xd324,0xe19b,0xfe2f,0x3d89,
0x6abc,0x7a94,0xfc95,0xbdb2,
0x3c10,0xcc74,0x98be,0x3dda,
0x9556,0x13ae,0xd4fe,0xbe01,
0xcb34,0xa454,0xd903,0x3e26,
0x30ab,0x8c0b,0xeaf6,0xbe4b,
0x6435,0x9d4d,0x3b76,0x3e70,
0x7f8d,0x8f22,0xec63,0xbe91,
0xf4ac,0x978c,0xbf24,0x3eb2,
0x6427,0xcba5,0x866f,0xbed2,
0x2859,0xbe9a,0x3f58,0x3ef1,
0x1d5a,0x59c4,0x2b26,0xbf0e,
0x7cab,0x7410,0xb51b,0x3f28,
0xeb52,0x1f15,0xe2fd,0xbf42,
0x100e,0x8a12,0xdc75,0x3f5a,
0xa849,0x201a,0xb65e,0xbf71,
0xe3dd,0xf3dd,0x9961,0x3f85,
0xb6f0,0xf121,0x4e9e,0xbf98,
0xa32d,0xcea8,0x3e8a,0x3fa9,
0x06ea,0x342d,0x4b70,0xbfb8,
0x88c0,0x77ac,0xf7ac,0x3fc5,
0xcd8d,0xc057,0x7feb,0xbfd3,
0xa22a,0x9035,0xa84e,0x3fe5,
};
#endif

#ifdef MIEEE
static unsigned short AI0[] = {
0xbc54,0x5cb7,0x2134,0xd0ef,
0x3c83,0x3362,0x977d,0xa589,
0xbcb1,0x84eb,0x721e,0xbbb4,
0x3cde,0xe6d8,0x93f6,0x5eba,
0xbd0a,0x5022,0xc297,0xfbeb,
0x3d35,0x9b46,0x4b26,0x2627,
0xbd61,0x164c,0x62ee,0x1af0,
0x3d89,0xfe2f,0xe19b,0xd324,
0xbdb2,0xfc95,0x7a94,0x6abc,
0x3dda,0x98be,0xcc74,0x3c10,
0xbe01,0xd4fe,0x13ae,0x9556,
0x3e26,0xd903,0xa454,0xcb34,
0xbe4b,0xeaf6,0x8c0b,0x30ab,
0x3e70,0x3b76,0x9d4d,0x6435,
0xbe91,0xec63,0x8f22,0x7f8d,
0x3eb2,0xbf24,0x978c,0xf4ac,
0xbed2,0x866f,0xcba5,0x6427,
0x3ef1,0x3f58,0xbe9a,0x2859,
0xbf0e,0x2b26,0x59c4,0x1d5a,
0x3f28,0xb51b,0x7410,0x7cab,
0xbf42,0xe2fd,0x1f15,0xeb52,
0x3f5a,0xdc75,0x8a12,0x100e,
0xbf71,0xb65e,0x201a,0xa849,
0x3f85,0x9961,0xf3dd,0xe3dd,
0xbf98,0x4e9e,0xf121,0xb6f0,
0x3fa9,0x3e8a,0xcea8,0xa32d,
0xbfb8,0x4b70,0x342d,0x06ea,
0x3fc5,0xf7ac,0x77ac,0x88c0,
0xbfd3,0x7feb,0xc057,0xcd8d,
0x3fe5,0xa84e,0x9035,0xa22a
};
#endif


/* Chebyshev coefficients for exp(-x) sqrt(x) I0(x)
 * in the inverted interval [8,infinity].
 *
 * lim(x->inf){ exp(-x) sqrt(x) I0(x) } = 1/sqrt(2pi).
 */

#ifdef UNK
static double BI0[] =
{
-7.23318048787475395456E-18,
-4.83050448594418207126E-18,
 4.46562142029675999901E-17,
 3.46122286769746109310E-17,
-2.82762398051658348494E-16,
-3.42548561967721913462E-16,
 1.77256013305652638360E-15,
 3.81168066935262242075E-15,
-9.55484669882830764870E-15,
-4.15056934728722208663E-14,
 1.54008621752140982691E-14,
 3.85277838274214270114E-13,
 7.18012445138366623367E-13,
-1.79417853150680611778E-12,
-1.32158118404477131188E-11,
-3.14991652796324136454E-11,
 1.18891471078464383424E-11,
 4.94060238822496958910E-10,
 3.39623202570838634515E-9,
 2.26666899049817806459E-8,
 2.04891858946906374183E-7,
 2.89137052083475648297E-6,
 6.88975834691682398426E-5,
 3.36911647825569408990E-3,
 8.04490411014108831608E-1
};
#endif

#ifdef DEC
static unsigned short BI0[] = {
0122005,0066672,0123124,0054311,
0121662,0033323,0030214,0104602,
0022515,0170300,0113314,0020413,
0022437,0117350,0035402,0007146,
0123243,0000135,0057220,0177435,
0123305,0073476,0144106,0170702,
0023777,0071755,0017527,0154373,
0024211,0052214,0102247,0033270,
0124454,0017763,0171453,0012322,
0125072,0166316,0075505,0154616,
0024612,0133770,0065376,0025045,
0025730,0162143,0056036,0001632,
0026112,0015077,0150464,0063542,
0126374,0101030,0014274,0065457,
0127150,0077271,0125763,0157617,
0127412,0104350,0040713,0120445,
0027121,0023765,0057500,0001165,
0030407,0147146,0003643,0075644,
0031151,0061445,0044422,0156065,
0031702,0132224,0003266,0125551,
0032534,0000076,0147153,0005555,
0033502,0004536,0004016,0026055,
0034620,0076433,0142314,0171215,
0036134,0146145,0013454,0101104,
0040115,0171425,0062500,0047133
};
#endif

#ifdef IBMPC
static unsigned short BI0[] = {
0x8b19,0x54ca,0xadb7,0xbc60,
0x9130,0x6611,0x46da,0xbc56,
0x8421,0x12d9,0xbe18,0x3c89,
0x41cd,0x0760,0xf3dd,0x3c83,
0x1fe4,0xabd2,0x600b,0xbcb4,
0xde38,0xd908,0xaee7,0xbcb8,
0xfb1f,0xa3ea,0xee7d,0x3cdf,
0xe6d7,0x9094,0x2a91,0x3cf1,
0x629a,0x7e65,0x83fe,0xbd05,
0xbb32,0xcf68,0x5d99,0xbd27,
0xc545,0x0d5f,0x56ff,0x3d11,
0xc073,0x6b83,0x1c8c,0x3d5b,
0x8cec,0xfa26,0x4347,0x3d69,
0x8d66,0x0317,0x9043,0xbd7f,
0x7bf2,0x357e,0x0fd7,0xbdad,
0x7425,0x0839,0x511d,0xbdc1,
0x004f,0xabe8,0x24fe,0x3daa,
0x6f75,0xc0f4,0xf9cc,0x3e00,
0x5b87,0xa922,0x2c64,0x3e2d,
0xd56d,0x80d6,0x5692,0x3e58,
0x616e,0xd9cd,0x8007,0x3e8b,
0xc586,0xc101,0x412b,0x3ec8,
0x9e52,0x7899,0x0fa3,0x3f12,
0x9049,0xa2e5,0x998c,0x3f6b,
0x09cb,0xaca8,0xbe62,0x3fe9
};
#endif

#ifdef MIEEE
static unsigned short BI0[] = {
0xbc60,0xadb7,0x54ca,0x8b19,
0xbc56,0x46da,0x6611,0x9130,
0x3c89,0xbe18,0x12d9,0x8421,
0x3c83,0xf3dd,0x0760,0x41cd,
0xbcb4,0x600b,0xabd2,0x1fe4,
0xbcb8,0xaee7,0xd908,0xde38,
0x3cdf,0xee7d,0xa3ea,0xfb1f,
0x3cf1,0x2a91,0x9094,0xe6d7,
0xbd05,0x83fe,0x7e65,0x629a,
0xbd27,0x5d99,0xcf68,0xbb32,
0x3d11,0x56ff,0x0d5f,0xc545,
0x3d5b,0x1c8c,0x6b83,0xc073,
0x3d69,0x4347,0xfa26,0x8cec,
0xbd7f,0x9043,0x0317,0x8d66,
0xbdad,0x0fd7,0x357e,0x7bf2,
0xbdc1,0x511d,0x0839,0x7425,
0x3daa,0x24fe,0xabe8,0x004f,
0x3e00,0xf9cc,0xc0f4,0x6f75,
0x3e2d,0x2c64,0xa922,0x5b87,
0x3e58,0x5692,0x80d6,0xd56d,
0x3e8b,0x8007,0xd9cd,0x616e,
0x3ec8,0x412b,0xc101,0xc586,
0x3f12,0x0fa3,0x7899,0x9e52,
0x3f6b,0x998c,0xa2e5,0x9049,
0x3fe9,0xbe62,0xaca8,0x09cb
};
#endif

double i0(double x)
{
double y;

if( x < 0 )
	x = -x;
if( x <= 8.0 )
	{
	y = (x/2.0) - 2.0;
	return( exp(x) * chbevl( y, AI0, 30 ) );
	}

return(  exp(x) * chbevl( 32.0/x - 2.0, BI0, 25 ) / sqrt(x) );

}




double i0e(double x)
{
double y;

if( x < 0 )
	x = -x;
if( x <= 8.0 )
	{
	y = (x/2.0) - 2.0;
	return( chbevl( y, AI0, 30 ) );
	}

return(  chbevl( 32.0/x - 2.0, BI0, 25 ) / sqrt(x) );

}

/* ========================================================================= */

/*							i1.c
 *
 *	Modified Bessel function of order one
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, i1();
 *
 * y = i1( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns modified Bessel function of order one of the
 * argument.
 *
 * The function is defined as i1(x) = -i j1( ix ).
 *
 * The range is partitioned into the two intervals [0,8] and
 * (8, infinity).  Chebyshev polynomial expansions are employed
 * in each interval.
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0, 30        3400       1.2e-16     2.3e-17
 *    IEEE      0, 30       30000       1.9e-15     2.1e-16
 *
 *
 */
/*							i1e.c
 *
 *	Modified Bessel function of order one,
 *	exponentially scaled
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, i1e();
 *
 * y = i1e( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns exponentially scaled modified Bessel function
 * of order one of the argument.
 *
 * The function is defined as i1(x) = -i exp(-|x|) j1( ix ).
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0, 30       30000       2.0e-15     2.0e-16
 * See i1().
 *
 */

/*							i1.c 2		*/


/* Chebyshev coefficients for exp(-x) I1(x) / x
 * in the interval [0,8].
 *
 * lim(x->0){ exp(-x) I1(x) / x } = 1/2.
 */

#ifdef UNK
static double AI1[] =
{
 2.77791411276104639959E-18,
-2.11142121435816608115E-17,
 1.55363195773620046921E-16,
-1.10559694773538630805E-15,
 7.60068429473540693410E-15,
-5.04218550472791168711E-14,
 3.22379336594557470981E-13,
-1.98397439776494371520E-12,
 1.17361862988909016308E-11,
-6.66348972350202774223E-11,
 3.62559028155211703701E-10,
-1.88724975172282928790E-9,
 9.38153738649577178388E-9,
-4.44505912879632808065E-8,
 2.00329475355213526229E-7,
-8.56872026469545474066E-7,
 3.47025130813767847674E-6,
-1.32731636560394358279E-5,
 4.78156510755005422638E-5,
-1.61760815825896745588E-4,
 5.12285956168575772895E-4,
-1.51357245063125314899E-3,
 4.15642294431288815669E-3,
-1.05640848946261981558E-2,
 2.47264490306265168283E-2,
-5.29459812080949914269E-2,
 1.02643658689847095384E-1,
-1.76416518357834055153E-1,
 2.52587186443633654823E-1
};
#endif

#ifdef DEC
static unsigned short AI1[] = {
0021514,0174520,0060742,0000241,
0122302,0137206,0016120,0025663,
0023063,0017437,0026235,0176536,
0123637,0052523,0170150,0125632,
0024410,0165770,0030251,0044134,
0125143,0012160,0162170,0054727,
0025665,0075702,0035716,0145247,
0126413,0116032,0176670,0015462,
0027116,0073425,0110351,0105242,
0127622,0104034,0137530,0037364,
0030307,0050645,0120776,0175535,
0131001,0130331,0043523,0037455,
0031441,0026160,0010712,0100174,
0132076,0164761,0022706,0017500,
0032527,0015045,0115076,0104076,
0133146,0001714,0015434,0144520,
0033550,0161166,0124215,0077050,
0134136,0127715,0143365,0157170,
0034510,0106652,0013070,0064130,
0135051,0117126,0117264,0123761,
0035406,0045355,0133066,0175751,
0135706,0061420,0054746,0122440,
0036210,0031232,0047235,0006640,
0136455,0012373,0144235,0011523,
0036712,0107437,0036731,0015111,
0137130,0156742,0115744,0172743,
0037322,0033326,0124667,0124740,
0137464,0123210,0021510,0144556,
0037601,0051433,0111123,0177721
};
#endif

#ifdef IBMPC
static unsigned short AI1[] = {
0x4014,0x0c3c,0x9f2a,0x3c49,
0x0576,0xc38a,0x57d0,0xbc78,
0xbfac,0xe593,0x63e3,0x3ca6,
0x1573,0x7e0d,0xeaaa,0xbcd3,
0x290c,0x0615,0x1d7f,0x3d01,
0x0b3b,0x1c8f,0x628e,0xbd2c,
0xd955,0x4779,0xaf78,0x3d56,
0x0366,0x5fb7,0x7383,0xbd81,
0x3154,0xb21d,0xcee2,0x3da9,
0x07de,0x97eb,0x5103,0xbdd2,
0xdf6c,0xb43f,0xea34,0x3df8,
0x67e6,0x28ea,0x361b,0xbe20,
0x5010,0x0239,0x258e,0x3e44,
0xc3e8,0x24b8,0xdd3e,0xbe67,
0xd108,0xb347,0xe344,0x3e8a,
0x992a,0x8363,0xc079,0xbeac,
0xafc5,0xd511,0x1c4e,0x3ecd,
0xbbcf,0xb8de,0xd5f9,0xbeeb,
0x0d0b,0x42c7,0x11b5,0x3f09,
0x94fe,0xd3d6,0x33ca,0xbf25,
0xdf7d,0xb6c6,0xc95d,0x3f40,
0xd4a4,0x0b3c,0xcc62,0xbf58,
0xa1b4,0x49d3,0x0653,0x3f71,
0xa26a,0x7913,0xa29f,0xbf85,
0x2349,0xe7bb,0x51e3,0x3f99,
0x9ebc,0x537c,0x1bbc,0xbfab,
0xf53c,0xd536,0x46da,0x3fba,
0x192e,0x0469,0x94d1,0xbfc6,
0x7ffa,0x724a,0x2a63,0x3fd0
};
#endif

#ifdef MIEEE
static unsigned short AI1[] = {
0x3c49,0x9f2a,0x0c3c,0x4014,
0xbc78,0x57d0,0xc38a,0x0576,
0x3ca6,0x63e3,0xe593,0xbfac,
0xbcd3,0xeaaa,0x7e0d,0x1573,
0x3d01,0x1d7f,0x0615,0x290c,
0xbd2c,0x628e,0x1c8f,0x0b3b,
0x3d56,0xaf78,0x4779,0xd955,
0xbd81,0x7383,0x5fb7,0x0366,
0x3da9,0xcee2,0xb21d,0x3154,
0xbdd2,0x5103,0x97eb,0x07de,
0x3df8,0xea34,0xb43f,0xdf6c,
0xbe20,0x361b,0x28ea,0x67e6,
0x3e44,0x258e,0x0239,0x5010,
0xbe67,0xdd3e,0x24b8,0xc3e8,
0x3e8a,0xe344,0xb347,0xd108,
0xbeac,0xc079,0x8363,0x992a,
0x3ecd,0x1c4e,0xd511,0xafc5,
0xbeeb,0xd5f9,0xb8de,0xbbcf,
0x3f09,0x11b5,0x42c7,0x0d0b,
0xbf25,0x33ca,0xd3d6,0x94fe,
0x3f40,0xc95d,0xb6c6,0xdf7d,
0xbf58,0xcc62,0x0b3c,0xd4a4,
0x3f71,0x0653,0x49d3,0xa1b4,
0xbf85,0xa29f,0x7913,0xa26a,
0x3f99,0x51e3,0xe7bb,0x2349,
0xbfab,0x1bbc,0x537c,0x9ebc,
0x3fba,0x46da,0xd536,0xf53c,
0xbfc6,0x94d1,0x0469,0x192e,
0x3fd0,0x2a63,0x724a,0x7ffa
};
#endif

/*							i1.c	*/

/* Chebyshev coefficients for exp(-x) sqrt(x) I1(x)
 * in the inverted interval [8,infinity].
 *
 * lim(x->inf){ exp(-x) sqrt(x) I1(x) } = 1/sqrt(2pi).
 */

#ifdef UNK
static double BI1[] =
{
 7.51729631084210481353E-18,
 4.41434832307170791151E-18,
-4.65030536848935832153E-17,
-3.20952592199342395980E-17,
 2.96262899764595013876E-16,
 3.30820231092092828324E-16,
-1.88035477551078244854E-15,
-3.81440307243700780478E-15,
 1.04202769841288027642E-14,
 4.27244001671195135429E-14,
-2.10154184277266431302E-14,
-4.08355111109219731823E-13,
-7.19855177624590851209E-13,
 2.03562854414708950722E-12,
 1.41258074366137813316E-11,
 3.25260358301548823856E-11,
-1.89749581235054123450E-11,
-5.58974346219658380687E-10,
-3.83538038596423702205E-9,
-2.63146884688951950684E-8,
-2.51223623787020892529E-7,
-3.88256480887769039346E-6,
-1.10588938762623716291E-4,
-9.76109749136146840777E-3,
 7.78576235018280120474E-1
};
#endif

#ifdef DEC
static unsigned short BI1[] = {
0022012,0125555,0115227,0043456,
0021642,0156127,0052075,0145203,
0122526,0072435,0111231,0011664,
0122424,0001544,0161671,0114403,
0023252,0144257,0163532,0142121,
0023276,0132162,0174045,0013204,
0124007,0077154,0057046,0110517,
0124211,0066650,0116127,0157073,
0024473,0133413,0130551,0107504,
0025100,0064741,0032631,0040364,
0124675,0045101,0071551,0012400,
0125745,0161054,0071637,0011247,
0126112,0117410,0035525,0122231,
0026417,0037237,0131034,0176427,
0027170,0100373,0024742,0025725,
0027417,0006417,0105303,0141446,
0127246,0163716,0121202,0060137,
0130431,0123122,0120436,0166000,
0131203,0144134,0153251,0124500,
0131742,0005234,0122732,0033006,
0132606,0157751,0072362,0121031,
0133602,0043372,0047120,0015626,
0134747,0165774,0001125,0046462,
0136437,0166402,0117746,0155137,
0040107,0050305,0125330,0124241
};
#endif

#ifdef IBMPC
static unsigned short BI1[] = {
0xe8e6,0xb352,0x556d,0x3c61,
0xb950,0xea87,0x5b8a,0x3c54,
0x2277,0xb253,0xcea3,0xbc8a,
0x3320,0x9c77,0x806c,0xbc82,
0x588a,0xfceb,0x5915,0x3cb5,
0xa2d1,0x5f04,0xd68e,0x3cb7,
0xd22a,0x8bc4,0xefcd,0xbce0,
0xfbc7,0x138a,0x2db5,0xbcf1,
0x31e8,0x762d,0x76e1,0x3d07,
0x281e,0x26b3,0x0d3c,0x3d28,
0x22a0,0x2e6d,0xa948,0xbd17,
0xe255,0x8e73,0xbc45,0xbd5c,
0xb493,0x076a,0x53e1,0xbd69,
0x9fa3,0xf643,0xe7d3,0x3d81,
0x457b,0x653c,0x101f,0x3daf,
0x7865,0xf158,0xe1a1,0x3dc1,
0x4c0c,0xd450,0xdcf9,0xbdb4,
0xdd80,0x5423,0x34ca,0xbe03,
0x3528,0x9ad5,0x790b,0xbe30,
0x46c1,0x94bb,0x4153,0xbe5c,
0x5443,0x2e9e,0xdbfd,0xbe90,
0x0373,0x49ca,0x48df,0xbed0,
0xa9a6,0x804a,0xfd7f,0xbf1c,
0xdb4c,0x53fc,0xfda0,0xbf83,
0x1514,0xb55b,0xea18,0x3fe8
};
#endif

#ifdef MIEEE
static unsigned short BI1[] = {
0x3c61,0x556d,0xb352,0xe8e6,
0x3c54,0x5b8a,0xea87,0xb950,
0xbc8a,0xcea3,0xb253,0x2277,
0xbc82,0x806c,0x9c77,0x3320,
0x3cb5,0x5915,0xfceb,0x588a,
0x3cb7,0xd68e,0x5f04,0xa2d1,
0xbce0,0xefcd,0x8bc4,0xd22a,
0xbcf1,0x2db5,0x138a,0xfbc7,
0x3d07,0x76e1,0x762d,0x31e8,
0x3d28,0x0d3c,0x26b3,0x281e,
0xbd17,0xa948,0x2e6d,0x22a0,
0xbd5c,0xbc45,0x8e73,0xe255,
0xbd69,0x53e1,0x076a,0xb493,
0x3d81,0xe7d3,0xf643,0x9fa3,
0x3daf,0x101f,0x653c,0x457b,
0x3dc1,0xe1a1,0xf158,0x7865,
0xbdb4,0xdcf9,0xd450,0x4c0c,
0xbe03,0x34ca,0x5423,0xdd80,
0xbe30,0x790b,0x9ad5,0x3528,
0xbe5c,0x4153,0x94bb,0x46c1,
0xbe90,0xdbfd,0x2e9e,0x5443,
0xbed0,0x48df,0x49ca,0x0373,
0xbf1c,0xfd7f,0x804a,0xa9a6,
0xbf83,0xfda0,0x53fc,0xdb4c,
0x3fe8,0xea18,0xb55b,0x1514
};
#endif

/*							i1.c	*/
double i1(double x)
{ 
double y, z;

z = fabs(x);
if( z <= 8.0 )
	{
	y = (z/2.0) - 2.0;
	z = chbevl( y, AI1, 29 ) * z * exp(z);
	}
else
	{
	z = exp(z) * chbevl( 32.0/z - 2.0, BI1, 25 ) / sqrt(z);
	}
if( x < 0.0 )
	z = -z;
return( z );
}

/*							i1e()	*/

double i1e(double x)
{ 
double y, z;

z = fabs(x);
if( z <= 8.0 )
	{
	y = (z/2.0) - 2.0;
	z = chbevl( y, AI1, 29 ) * z;
	}
else
	{
	z = chbevl( 32.0/z - 2.0, BI1, 25 ) / sqrt(z);
	}
if( x < 0.0 )
	z = -z;
return( z );
}

/* ========================================================================= */

/*							iv.c
 *
 *	Modified Bessel function of noninteger order
 *
 *
 *
 * SYNOPSIS:
 *
 * double v, x, y, iv();
 *
 * y = iv( v, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns modified Bessel function of order v of the
 * argument.  If x is negative, v must be integer valued.
 *
 * The function is defined as Iv(x) = Jv( ix ).  It is
 * here computed in terms of the confluent hypergeometric
 * function, according to the formula
 *
 *              v  -x
 * Iv(x) = (x/2)  e   hyperg( v+0.5, 2v+1, 2x ) / gamma(v+1)
 *
 * If v is a negative integer, then v is replaced by -v.
 *
 *
 * ACCURACY:
 *
 * Tested at random points (v, x), with v between 0 and
 * 30, x between 0 and 28.
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0,30          2000      3.1e-15     5.4e-16
 *    IEEE      0,30         10000      1.7e-14     2.7e-15
 *
 * Accuracy is diminished if v is near a negative integer.
 *
 * See also hyperg.c.
 *
 */
/*							iv.c	*/
/*	Modified Bessel function of noninteger order		*/
/* If x < 0, then v must be an integer. */



double iv(double v, double x)
{
int sign;
double t, ax;

/* If v is a negative integer, invoke symmetry */
t = floor(v);
if( v < 0.0 )
	{
	if( t == v )
		{
		v = -v;	/* symmetry */
		t = -t;
		}
	}
/* If x is negative, require v to be an integer */
sign = 1;
if( x < 0.0 )
	{
	if( t != v )
		{
		mtherr( "iv", DOMAIN );
		return( 0.0 );
		}
	if( v != 2.0 * floor(v/2.0) )
		sign = -1;
	}

/* Avoid logarithm singularity */
if( x == 0.0 )
	{
	if( v == 0.0 )
		return( 1.0 );
	if( v < 0.0 )
		{
		mtherr( "iv", OVERFLOW );
		return( MAXNUM );
		}
	else
		return( 0.0 );
	}

ax = fabs(x);
t = v * log( 0.5 * ax )  -  x;
t = sign * exp(t) / cephesgamma( v + 1.0 );
ax = v + 0.5;
return( t * hyperg( ax,  2.0 * ax,  2.0 * x ) );
}

/* ========================================================================= */

/*							k0.c
 *
 *	Modified Bessel function, third kind, order zero
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, k0();
 *
 * y = k0( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns modified Bessel function of the third kind
 * of order zero of the argument.
 *
 * The range is partitioned into the two intervals [0,8] and
 * (8, infinity).  Chebyshev polynomial expansions are employed
 * in each interval.
 *
 *
 *
 * ACCURACY:
 *
 * Tested at 2000 random points between 0 and 8.  Peak absolute
 * error (relative when K0 > 1) was 1.46e-14; rms, 4.26e-15.
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0, 30        3100       1.3e-16     2.1e-17
 *    IEEE      0, 30       30000       1.2e-15     1.6e-16
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 *  K0 domain          x <= 0          MAXNUM
 *
 */
/*							k0e()
 *
 *	Modified Bessel function, third kind, order zero,
 *	exponentially scaled
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, k0e();
 *
 * y = k0e( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns exponentially scaled modified Bessel function
 * of the third kind of order zero of the argument.
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0, 30       30000       1.4e-15     1.4e-16
 * See k0().
 *
 */


/* Chebyshev coefficients for K0(x) + log(x/2) I0(x)
 * in the interval [0,2].  The odd order coefficients are all
 * zero; only the even order coefficients are listed.
 * 
 * lim(x->0){ K0(x) + log(x/2) I0(x) } = -EUL.
 */

#ifdef UNK
static double AK0[] =
{
 1.37446543561352307156E-16,
 4.25981614279661018399E-14,
 1.03496952576338420167E-11,
 1.90451637722020886025E-9,
 2.53479107902614945675E-7,
 2.28621210311945178607E-5,
 1.26461541144692592338E-3,
 3.59799365153615016266E-2,
 3.44289899924628486886E-1,
-5.35327393233902768720E-1
};
#endif

#ifdef DEC
static unsigned short AK0[] = {
0023036,0073417,0032477,0165673,
0025077,0154126,0016046,0012517,
0027066,0011342,0035211,0005041,
0031002,0160233,0037454,0050224,
0032610,0012747,0037712,0173741,
0034277,0144007,0172147,0162375,
0035645,0140563,0125431,0165626,
0037023,0057662,0125124,0102051,
0037660,0043304,0004411,0166707,
0140011,0005467,0047227,0130370
};
#endif

#ifdef IBMPC
static unsigned short AK0[] = {
0xfd77,0xe6a7,0xcee1,0x3ca3,
0xc2aa,0xc384,0xfb0a,0x3d27,
0x2144,0x4751,0xc25c,0x3da6,
0x8a13,0x67e5,0x5c13,0x3e20,
0x5efc,0xe7f9,0x02bc,0x3e91,
0xfca0,0xfe8c,0xf900,0x3ef7,
0x3d73,0x7563,0xb82e,0x3f54,
0x9085,0x554a,0x6bf6,0x3fa2,
0x3db9,0x8121,0x08d8,0x3fd6,
0xf61f,0xe9d2,0x2166,0xbfe1
};
#endif

#ifdef MIEEE
static unsigned short AK0[] = {
0x3ca3,0xcee1,0xe6a7,0xfd77,
0x3d27,0xfb0a,0xc384,0xc2aa,
0x3da6,0xc25c,0x4751,0x2144,
0x3e20,0x5c13,0x67e5,0x8a13,
0x3e91,0x02bc,0xe7f9,0x5efc,
0x3ef7,0xf900,0xfe8c,0xfca0,
0x3f54,0xb82e,0x7563,0x3d73,
0x3fa2,0x6bf6,0x554a,0x9085,
0x3fd6,0x08d8,0x8121,0x3db9,
0xbfe1,0x2166,0xe9d2,0xf61f
};
#endif



/* Chebyshev coefficients for exp(x) sqrt(x) K0(x)
 * in the inverted interval [2,infinity].
 * 
 * lim(x->inf){ exp(x) sqrt(x) K0(x) } = sqrt(pi/2).
 */

#ifdef UNK
static double BK0[] = {
 5.30043377268626276149E-18,
-1.64758043015242134646E-17,
 5.21039150503902756861E-17,
-1.67823109680541210385E-16,
 5.51205597852431940784E-16,
-1.84859337734377901440E-15,
 6.34007647740507060557E-15,
-2.22751332699166985548E-14,
 8.03289077536357521100E-14,
-2.98009692317273043925E-13,
 1.14034058820847496303E-12,
-4.51459788337394416547E-12,
 1.85594911495471785253E-11,
-7.95748924447710747776E-11,
 3.57739728140030116597E-10,
-1.69753450938905987466E-9,
 8.57403401741422608519E-9,
-4.66048989768794782956E-8,
 2.76681363944501510342E-7,
-1.83175552271911948767E-6,
 1.39498137188764993662E-5,
-1.28495495816278026384E-4,
 1.56988388573005337491E-3,
-3.14481013119645005427E-2,
 2.44030308206595545468E0
};
#endif

#ifdef DEC
static unsigned short BK0[] = {
0021703,0106456,0076144,0173406,
0122227,0173144,0116011,0030033,
0022560,0044562,0006506,0067642,
0123101,0076243,0123273,0131013,
0023436,0157713,0056243,0141331,
0124005,0032207,0063726,0164664,
0024344,0066342,0051756,0162300,
0124710,0121365,0154053,0077022,
0025264,0161166,0066246,0077420,
0125647,0141671,0006443,0103212,
0026240,0076431,0077147,0160445,
0126636,0153741,0174002,0105031,
0027243,0040102,0035375,0163073,
0127656,0176256,0113476,0044653,
0030304,0125544,0006377,0130104,
0130751,0047257,0110537,0127324,
0031423,0046400,0014772,0012164,
0132110,0025240,0155247,0112570,
0032624,0105314,0007437,0021574,
0133365,0155243,0174306,0116506,
0034152,0004776,0061643,0102504,
0135006,0136277,0036104,0175023,
0035715,0142217,0162474,0115022,
0137000,0147671,0065177,0134356,
0040434,0026754,0175163,0044070
};
#endif

#ifdef IBMPC
static unsigned short BK0[] = {
0x9ee1,0xcf8c,0x71a5,0x3c58,
0x2603,0x9381,0xfecc,0xbc72,
0xcdf4,0x41a8,0x092e,0x3c8e,
0x7641,0x74d7,0x2f94,0xbca8,
0x785b,0x6b94,0xdbf9,0x3cc3,
0xdd36,0xecfa,0xa690,0xbce0,
0xdc98,0x4a7d,0x8d9c,0x3cfc,
0x6fc2,0xbb05,0x145e,0xbd19,
0xcfe2,0xcd94,0x9c4e,0x3d36,
0x70d1,0x21a4,0xf877,0xbd54,
0xfc25,0x2fcc,0x0fa3,0x3d74,
0x5143,0x3f00,0xdafc,0xbd93,
0xbcc7,0x475f,0x6808,0x3db4,
0xc935,0xd2e7,0xdf95,0xbdd5,
0xf608,0x819f,0x956c,0x3df8,
0xf5db,0xf22b,0x29d5,0xbe1d,
0x428e,0x033f,0x69a0,0x3e42,
0xf2af,0x1b54,0x0554,0xbe69,
0xe46f,0x81e3,0x9159,0x3e92,
0xd3a9,0x7f18,0xbb54,0xbebe,
0x70a9,0xcc74,0x413f,0x3eed,
0x9f42,0xe788,0xd797,0xbf20,
0x9342,0xfca7,0xb891,0x3f59,
0xf71e,0x2d4f,0x19f7,0xbfa0,
0x6907,0x9f4e,0x85bd,0x4003
};
#endif

#ifdef MIEEE
static unsigned short BK0[] = {
0x3c58,0x71a5,0xcf8c,0x9ee1,
0xbc72,0xfecc,0x9381,0x2603,
0x3c8e,0x092e,0x41a8,0xcdf4,
0xbca8,0x2f94,0x74d7,0x7641,
0x3cc3,0xdbf9,0x6b94,0x785b,
0xbce0,0xa690,0xecfa,0xdd36,
0x3cfc,0x8d9c,0x4a7d,0xdc98,
0xbd19,0x145e,0xbb05,0x6fc2,
0x3d36,0x9c4e,0xcd94,0xcfe2,
0xbd54,0xf877,0x21a4,0x70d1,
0x3d74,0x0fa3,0x2fcc,0xfc25,
0xbd93,0xdafc,0x3f00,0x5143,
0x3db4,0x6808,0x475f,0xbcc7,
0xbdd5,0xdf95,0xd2e7,0xc935,
0x3df8,0x956c,0x819f,0xf608,
0xbe1d,0x29d5,0xf22b,0xf5db,
0x3e42,0x69a0,0x033f,0x428e,
0xbe69,0x0554,0x1b54,0xf2af,
0x3e92,0x9159,0x81e3,0xe46f,
0xbebe,0xbb54,0x7f18,0xd3a9,
0x3eed,0x413f,0xcc74,0x70a9,
0xbf20,0xd797,0xe788,0x9f42,
0x3f59,0xb891,0xfca7,0x9342,
0xbfa0,0x19f7,0x2d4f,0xf71e,
0x4003,0x85bd,0x9f4e,0x6907
};
#endif

/*							k0.c	*/

double k0(double x)
{
double y, z;

if( x <= 0.0 )
	{
	mtherr( "k0", DOMAIN );
	return( MAXNUM );
	}

if( x <= 2.0 )
	{
	y = x * x - 2.0;
	y = chbevl( y, AK0, 10 ) - log( 0.5 * x ) * i0(x);
	return( y );
	}
z = 8.0/x - 2.0;
y = exp(-x) * chbevl( z, BK0, 25 ) / sqrt(x);
return(y);
}




double k0e(double x)
{
double y;

if( x <= 0.0 )
	{
	mtherr( "k0e", DOMAIN );
	return( MAXNUM );
	}

if( x <= 2.0 )
	{
	y = x * x - 2.0;
	y = chbevl( y, AK0, 10 ) - log( 0.5 * x ) * i0(x);
	return( y * exp(x) );
	}

y = chbevl( 8.0/x - 2.0, BK0, 25 ) / sqrt(x);
return(y);
}

/* ========================================================================= */

/*							k1.c
 *
 *	Modified Bessel function, third kind, order one
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, k1();
 *
 * y = k1( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Computes the modified Bessel function of the third kind
 * of order one of the argument.
 *
 * The range is partitioned into the two intervals [0,2] and
 * (2, infinity).  Chebyshev polynomial expansions are employed
 * in each interval.
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0, 30        3300       8.9e-17     2.2e-17
 *    IEEE      0, 30       30000       1.2e-15     1.6e-16
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * k1 domain          x <= 0          MAXNUM
 *
 */
/*							k1e.c
 *
 *	Modified Bessel function, third kind, order one,
 *	exponentially scaled
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, k1e();
 *
 * y = k1e( x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns exponentially scaled modified Bessel function
 * of the third kind of order one of the argument:
 *
 *      k1e(x) = exp(x) * k1(x).
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      0, 30       30000       7.8e-16     1.2e-16
 * See k1().
 *
 */


/* Chebyshev coefficients for x(K1(x) - log(x/2) I1(x))
 * in the interval [0,2].
 * 
 * lim(x->0){ x(K1(x) - log(x/2) I1(x)) } = 1.
 */

#ifdef UNK
static double AK1[] =
{
-7.02386347938628759343E-18,
-2.42744985051936593393E-15,
-6.66690169419932900609E-13,
-1.41148839263352776110E-10,
-2.21338763073472585583E-8,
-2.43340614156596823496E-6,
-1.73028895751305206302E-4,
-6.97572385963986435018E-3,
-1.22611180822657148235E-1,
-3.53155960776544875667E-1,
 1.52530022733894777053E0
};
#endif

#ifdef DEC
static unsigned short AK1[] = {
0122001,0110501,0164746,0151255,
0124056,0165213,0150034,0147377,
0126073,0124026,0167207,0001044,
0130033,0030735,0141061,0033116,
0131676,0020350,0121341,0107175,
0133443,0046631,0062031,0070716,
0135065,0067427,0026435,0164022,
0136344,0112234,0165752,0006222,
0137373,0015622,0017016,0155636,
0137664,0150333,0125730,0067240,
0040303,0036411,0130200,0043120
};
#endif

#ifdef IBMPC
static unsigned short AK1[] = {
0xda56,0x3d3c,0x3228,0xbc60,
0x99e0,0x7a03,0xdd51,0xbce5,
0xe045,0xddd0,0x7502,0xbd67,
0x26ca,0xb846,0x663b,0xbde3,
0x31d0,0x145c,0xc41d,0xbe57,
0x2e3a,0x2c83,0x69b3,0xbec4,
0xbd02,0xe5a3,0xade2,0xbf26,
0x4192,0x9d7d,0x9293,0xbf7c,
0xdb74,0x43c1,0x6372,0xbfbf,
0x0dd4,0x757b,0x9a1b,0xbfd6,
0x08ca,0x3610,0x67a1,0x3ff8
};
#endif

#ifdef MIEEE
static unsigned short AK1[] = {
0xbc60,0x3228,0x3d3c,0xda56,
0xbce5,0xdd51,0x7a03,0x99e0,
0xbd67,0x7502,0xddd0,0xe045,
0xbde3,0x663b,0xb846,0x26ca,
0xbe57,0xc41d,0x145c,0x31d0,
0xbec4,0x69b3,0x2c83,0x2e3a,
0xbf26,0xade2,0xe5a3,0xbd02,
0xbf7c,0x9293,0x9d7d,0x4192,
0xbfbf,0x6372,0x43c1,0xdb74,
0xbfd6,0x9a1b,0x757b,0x0dd4,
0x3ff8,0x67a1,0x3610,0x08ca
};
#endif



/* Chebyshev coefficients for exp(x) sqrt(x) K1(x)
 * in the interval [2,infinity].
 *
 * lim(x->inf){ exp(x) sqrt(x) K1(x) } = sqrt(pi/2).
 */

#ifdef UNK
static double BK1[] =
{
-5.75674448366501715755E-18,
 1.79405087314755922667E-17,
-5.68946255844285935196E-17,
 1.83809354436663880070E-16,
-6.05704724837331885336E-16,
 2.03870316562433424052E-15,
-7.01983709041831346144E-15,
 2.47715442448130437068E-14,
-8.97670518232499435011E-14,
 3.34841966607842919884E-13,
-1.28917396095102890680E-12,
 5.13963967348173025100E-12,
-2.12996783842756842877E-11,
 9.21831518760500529508E-11,
-4.19035475934189648750E-10,
 2.01504975519703286596E-9,
-1.03457624656780970260E-8,
 5.74108412545004946722E-8,
-3.50196060308781257119E-7,
 2.40648494783721712015E-6,
-1.93619797416608296024E-5,
 1.95215518471351631108E-4,
-2.85781685962277938680E-3,
 1.03923736576817238437E-1,
 2.72062619048444266945E0
};
#endif

#ifdef DEC
static unsigned short BK1[] = {
0121724,0061352,0013041,0150076,
0022245,0074324,0016172,0173232,
0122603,0030250,0135670,0165221,
0023123,0165362,0023561,0060124,
0123456,0112436,0141654,0073623,
0024022,0163557,0077564,0006753,
0124374,0165221,0131014,0026524,
0024737,0017512,0144250,0175451,
0125312,0021456,0123136,0076633,
0025674,0077720,0020125,0102607,
0126265,0067543,0007744,0043701,
0026664,0152702,0033002,0074202,
0127273,0055234,0120016,0071733,
0027712,0133200,0042441,0075515,
0130346,0057000,0015456,0074470,
0031012,0074441,0051636,0111155,
0131461,0136444,0177417,0002101,
0032166,0111743,0032176,0021410,
0132674,0001224,0076555,0027060,
0033441,0077430,0135226,0106663,
0134242,0065610,0167155,0113447,
0035114,0131304,0043664,0102163,
0136073,0045065,0171465,0122123,
0037324,0152767,0147401,0017732,
0040456,0017275,0050061,0062120,
};
#endif

#ifdef IBMPC
static unsigned short BK1[] = {
0x3a08,0x42c4,0x8c5d,0xbc5a,
0x5ed3,0x838f,0xaf1a,0x3c74,
0x1d52,0x1777,0x6615,0xbc90,
0x2c0b,0x44ee,0x7d5e,0x3caa,
0x8ef2,0xd875,0xd2a3,0xbcc5,
0x81bd,0xefee,0x5ced,0x3ce2,
0x85ab,0x3641,0x9d52,0xbcff,
0x1f65,0x5915,0xe3e9,0x3d1b,
0xcfb3,0xd4cb,0x4465,0xbd39,
0xb0b1,0x040a,0x8ffa,0x3d57,
0x88f8,0x61fc,0xadec,0xbd76,
0x4f10,0x46c0,0x9ab8,0x3d96,
0xce7b,0x9401,0x6b53,0xbdb7,
0x2f6a,0x08a4,0x56d0,0x3dd9,
0xcf27,0x0365,0xcbc0,0xbdfc,
0xd24e,0x2a73,0x4f24,0x3e21,
0xe088,0x9fe1,0x37a4,0xbe46,
0xc461,0x668f,0xd27c,0x3e6e,
0xa5c6,0x8fad,0x8052,0xbe97,
0xd1b6,0x1752,0x2fe3,0x3ec4,
0xb2e5,0x1dcd,0x4d71,0xbef4,
0x908e,0x88f6,0x9658,0x3f29,
0xb48a,0xbe66,0x6946,0xbf67,
0x23fb,0xf9e0,0x9abe,0x3fba,
0x2c8a,0xaa06,0xc3d7,0x4005
};
#endif

#ifdef MIEEE
static unsigned short BK1[] = {
0xbc5a,0x8c5d,0x42c4,0x3a08,
0x3c74,0xaf1a,0x838f,0x5ed3,
0xbc90,0x6615,0x1777,0x1d52,
0x3caa,0x7d5e,0x44ee,0x2c0b,
0xbcc5,0xd2a3,0xd875,0x8ef2,
0x3ce2,0x5ced,0xefee,0x81bd,
0xbcff,0x9d52,0x3641,0x85ab,
0x3d1b,0xe3e9,0x5915,0x1f65,
0xbd39,0x4465,0xd4cb,0xcfb3,
0x3d57,0x8ffa,0x040a,0xb0b1,
0xbd76,0xadec,0x61fc,0x88f8,
0x3d96,0x9ab8,0x46c0,0x4f10,
0xbdb7,0x6b53,0x9401,0xce7b,
0x3dd9,0x56d0,0x08a4,0x2f6a,
0xbdfc,0xcbc0,0x0365,0xcf27,
0x3e21,0x4f24,0x2a73,0xd24e,
0xbe46,0x37a4,0x9fe1,0xe088,
0x3e6e,0xd27c,0x668f,0xc461,
0xbe97,0x8052,0x8fad,0xa5c6,
0x3ec4,0x2fe3,0x1752,0xd1b6,
0xbef4,0x4d71,0x1dcd,0xb2e5,
0x3f29,0x9658,0x88f6,0x908e,
0xbf67,0x6946,0xbe66,0xb48a,
0x3fba,0x9abe,0xf9e0,0x23fb,
0x4005,0xc3d7,0xaa06,0x2c8a
};
#endif

double k1(double x)
{
double y, z;

z = 0.5 * x;
if( z <= 0.0 )
	{
	mtherr( "k1", DOMAIN );
	return( MAXNUM );
	}

if( x <= 2.0 )
	{
	y = x * x - 2.0;
	y =  log(z) * i1(x)  +  chbevl( y, AK1, 11 ) / x;
	return( y );
	}

return(  exp(-x) * chbevl( 8.0/x - 2.0, BK1, 25 ) / sqrt(x) );
}




double k1e(double x)
{
double y;

if( x <= 0.0 )
	{
	mtherr( "k1e", DOMAIN );
	return( MAXNUM );
	}

if( x <= 2.0 )
	{
	y = x * x - 2.0;
	y =  log( 0.5 * x ) * i1(x)  +  chbevl( y, AK1, 11 ) / x;
	return( y * exp(x) );
	}

return(  chbevl( 8.0/x - 2.0, BK1, 25 ) / sqrt(x) );
}

/* ========================================================================= */

/*							kn.c
 *
 *	Modified Bessel function, third kind, integer order
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, kn();
 * int n;
 *
 * y = kn( n, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns modified Bessel function of the third kind
 * of order n of the argument.
 *
 * The range is partitioned into the two intervals [0,9.55] and
 * (9.55, infinity).  An ascending power series is used in the
 * low range, and an asymptotic expansion in the high range.
 *
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0,30         3000       1.3e-9      5.8e-11
 *    IEEE      0,30        90000       1.8e-8      3.0e-10
 *
 *  Error is high only near the crossover point x = 9.55
 * between the two expansions used.
 */



/*
Algorithm for Kn.
                       n-1 
                   -n   -  (n-k-1)!    2   k
K (x)  =  0.5 (x/2)     >  -------- (-x /4)
 n                      -     k!
                       k=0

                    inf.                                   2   k
       n         n   -                                   (x /4)
 + (-1)  0.5(x/2)    >  {p(k+1) + p(n+k+1) - 2log(x/2)} ---------
                     -                                  k! (n+k)!
                    k=0

where  p(m) is the psi function: p(1) = -EUL and

                      m-1
                       -
      p(m)  =  -EUL +  >  1/k
                       -
                      k=1

For large x,
                                         2        2     2
                                      u-1     (u-1 )(u-3 )
K (z)  =  sqrt(pi/2z) exp(-z) { 1 + ------- + ------------ + ...}
 v                                        1            2
                                    1! (8z)     2! (8z)
asymptotically, where

           2
    u = 4 v .

*/


#define KNMAXFAC 31

double kn(int nn, double x)
{
double k, kf, nk1f, nkf, zn, t, s, z0, z;
double ans, fn, pn, pk, zmn, tlg, tox;
int i, n;

if( nn < 0 )
	n = -nn;
else
	n = nn;

if( n > KNMAXFAC )
	{
overf:
	mtherr( "kn", OVERFLOW );
	return( MAXNUM );
	}

if( x <= 0.0 )
	{
	if( x < 0.0 )
		mtherr( "kn", DOMAIN );
	else
		mtherr( "kn", SING );
	return( MAXNUM );
	}


if( x > 9.55 )
	goto asymp;

ans = 0.0;
z0 = 0.25 * x * x;
fn = 1.0;
pn = 0.0;
zmn = 1.0;
tox = 2.0/x;

if( n > 0 )
	{
	/* compute factorial of n and psi(n) */
	pn = -EUL;
	k = 1.0;
	for( i=1; i<n; i++ )
		{
		pn += 1.0/k;
		k += 1.0;
		fn *= k;
		}

	zmn = tox;

	if( n == 1 )
		{
		ans = 1.0/x;
		}
	else
		{
		nk1f = fn/n;
		kf = 1.0;
		s = nk1f;
		z = -z0;
		zn = 1.0;
		for( i=1; i<n; i++ )
			{
			nk1f = nk1f/(n-i);
			kf = kf * i;
			zn *= z;
			t = nk1f * zn / kf;
			s += t;   
			if( (MAXNUM - fabs(t)) < fabs(s) )
				goto overf;
			if( (tox > 1.0) && ((MAXNUM/tox) < zmn) )
				goto overf;
			zmn *= tox;
			}
		s *= 0.5;
		t = fabs(s);
		if( (zmn > 1.0) && ((MAXNUM/zmn) < t) )
			goto overf;
		if( (t > 1.0) && ((MAXNUM/t) < zmn) )
			goto overf;
		ans = s * zmn;
		}
	}


tlg = 2.0 * log( 0.5 * x );
pk = -EUL;
if( n == 0 )
	{
	pn = pk;
	t = 1.0;
	}
else
	{
	pn = pn + 1.0/n;
	t = 1.0/fn;
	}
s = (pk+pn-tlg)*t;
k = 1.0;
do
	{
	t *= z0 / (k * (k+n));
	pk += 1.0/k;
	pn += 1.0/(k+n);
	s += (pk+pn-tlg)*t;
	k += 1.0;
	}
while( fabs(t/s) > MACHEP );

s = 0.5 * s / zmn;
if( n & 1 )
	s = -s;
ans += s;

return(ans);



/* Asymptotic expansion for Kn(x) */
/* Converges to 1.4e-17 for x > 18.4 */

asymp:

if( x > MAXLOG )
	{
	mtherr( "kn", UNDERFLOW );
	return(0.0);
	}
k = n;
pn = 4.0 * k * k;
pk = 1.0;
z0 = 8.0 * x;
fn = 1.0;
t = 1.0;
s = t;
nkf = MAXNUM;
i = 0;
do
	{
	z = pn - pk * pk;
	t = t * z /(fn * z0);
	nk1f = fabs(t);
	if( (i >= n) && (nk1f > nkf) )
		{
		goto adone;
		}
	nkf = nk1f;
	s += t;
	fn += 1.0;
	pk += 2.0;
	i += 1;
	}
while( fabs(t/s) > MACHEP );

adone:
ans = exp(-x) * sqrt( PI/(2.0*x) ) * s;
return(ans);
}

/* ========================================================================= */

/*							hyperg.c
 *
 *	Confluent hypergeometric function
 *
 *
 *
 * SYNOPSIS:
 *
 * double a, b, x, y, hyperg();
 *
 * y = hyperg( a, b, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Computes the confluent hypergeometric function
 *
 *                          1           2
 *                       a x    a(a+1) x
 *   F ( a,b;x )  =  1 + ---- + --------- + ...
 *  1 1                  b 1!   b(b+1) 2!
 *
 * Many higher transcendental functions are special cases of
 * this power series.
 *
 * As is evident from the formula, b must not be a negative
 * integer or zero unless a is an integer with 0 >= a > b.
 *
 * The routine attempts both a direct summation of the series
 * and an asymptotic expansion.  In each case error due to
 * roundoff, cancellation, and nonconvergence is estimated.
 * The result with smaller estimated error is returned.
 *
 *
 *
 * ACCURACY:
 *
 * Tested at random points (a, b, x), all three variables
 * ranging from 0 to 30.
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    DEC       0,30         2000       1.2e-15     1.3e-16
 qtst1:
 21800   max =  1.4200E-14   rms =  1.0841E-15  ave = -5.3640E-17 
 ltstd:
 25500   max = 1.2759e-14   rms = 3.7155e-16  ave = 1.5384e-18 
 *    IEEE      0,30        30000       1.8e-14     1.1e-15
 *
 * Larger errors can be observed when b is near a negative
 * integer or zero.  Certain combinations of arguments yield
 * serious cancellation error in the power series summation
 * and also are not in the region of near convergence of the
 * asymptotic series.  An error message is printed if the
 * self-estimated relative error is greater than 1.0e-12.
 *
 */

/*							hyperg.c */




double hyperg(double a, double b, double x)
{
double asum, psum, acanc, pcanc=0.0, temp;

/* See if a Kummer transformation will help */
temp = b - a;
if( fabs(temp) < 0.001 * fabs(a) )
	return( exp(x) * hyperg( temp, b, -x )  );


psum = hy1f1p( a, b, x, &pcanc );
if( pcanc < 1.0e-15 )
	goto done;


/* try asymptotic series */

asum = hy1f1a( a, b, x, &acanc );


/* Pick the result with less estimated error */

if( acanc < pcanc )
	{
	pcanc = acanc;
	psum = asum;
	}

done:
if( pcanc > 1.0e-12 )
	mtherr( "hyperg", PLOSS );

return( psum );
}




/* Power series summation for confluent hypergeometric function		*/


static double hy1f1p(double a, double b, double x, double* err)
{
double n, a0, sum, t, u, temp;
double an, bn, maxt, pcanc;


/* set up for power series summation */
an = a;
bn = b;
a0 = 1.0;
sum = 1.0;
n = 1.0;
t = 1.0;
maxt = 0.0;


while( t > MACHEP )
	{
	if( bn == 0 )			/* check bn first since if both	*/
		{
		mtherr( "hyperg", SING );
		return( MAXNUM );	/* an and bn are zero it is	*/
		}
	if( an == 0 )			/* a singularity		*/
		return( sum );
	if( n > 200 )
		goto pdone;
	u = x * ( an / (bn * n) );

	/* check for blowup */
	temp = fabs(u);
	if( (temp > 1.0 ) && (maxt > (MAXNUM/temp)) )
		{
		pcanc = 1.0;	/* estimate 100% error */
		goto blowup;
		}

	a0 *= u;
	sum += a0;
	t = fabs(a0);
	if( t > maxt )
		maxt = t;
/*
	if( (maxt/fabs(sum)) > 1.0e17 )
		{
		pcanc = 1.0;
		goto blowup;
		}
*/
	an += 1.0;
	bn += 1.0;
	n += 1.0;
	}

pdone:

/* estimate error due to roundoff and cancellation */
if( sum != 0.0 )
	maxt /= fabs(sum);
maxt *= MACHEP; 	/* this way avoids multiply overflow */
pcanc = fabs( MACHEP * n  +  maxt );

blowup:

*err = pcanc;

return( sum );
}


/*							hy1f1a()	*/
/* asymptotic formula for hypergeometric function:
 *
 *        (    -a                         
 *  --    ( |z|                           
 * |  (b) ( -------- 2f0( a, 1+a-b, -1/x )
 *        (  --                           
 *        ( |  (b-a)                      
 *
 *
 *                                x    a-b                     )
 *                               e  |x|                        )
 *                             + -------- 2f0( b-a, 1-a, 1/x ) )
 *                                --                           )
 *                               |  (a)                        )
 */

static double hy1f1a(double a, double b, double x, double* err)
{
double h1, h2, t, u, temp, acanc, asum, err1, err2;

if( x == 0 )
	{
	acanc = 1.0;
	asum = MAXNUM;
	goto adone;
	}
temp = log( fabs(x) );
t = x + temp * (a-b);
u = -temp * a;

if( b > 0 )
	{
	temp = lgamma(b);
	t += temp;
	u += temp;
	}

h1 = hyp2f0( a, a-b+1, -1.0/x, 1, &err1 );

temp = exp(u) / cephesgamma(b-a);
h1 *= temp;
err1 *= temp;

h2 = hyp2f0( b-a, 1.0-a, 1.0/x, 2, &err2 );

if( a < 0 )
	temp = exp(t) / cephesgamma(a);
else
	temp = exp( t - lgamma(a) );

h2 *= temp;
err2 *= temp;

if( x < 0.0 )
	asum = h1;
else
	asum = h2;

acanc = fabs(err1) + fabs(err2);


if( b < 0 )
	{
	temp = cephesgamma(b);
	asum *= temp;
	acanc *= fabs(temp);
	}


if( asum != 0.0 )
	acanc /= fabs(asum);

acanc *= 30.0;	/* fudge factor, since error of asymptotic formula
		 * often seems this much larger than advertised */

adone:


*err = acanc;
return( asum );
}

/*							hyp2f0()	*/

double hyp2f0(double a, double b, double x, int type, double* err)
/* The argument 'type' determines what converging factor to use */
{
double a0, alast, t, tlast, maxt;
double n, an, bn, u, sum, temp;

an = a;
bn = b;
a0 = 1.0e0;
alast = 1.0e0;
sum = 0.0;
n = 1.0e0;
t = 1.0e0;
tlast = 1.0e9;
maxt = 0.0;

do
	{
	if( an == 0 )
		goto pdone;
	if( bn == 0 )
		goto pdone;

	u = an * (bn * x / n);

	/* check for blowup */
	temp = fabs(u);
	if( (temp > 1.0 ) && (maxt > (MAXNUM/temp)) )
		goto error;

	a0 *= u;
	t = fabs(a0);

	/* terminating condition for asymptotic series */
	if( t > tlast )
		goto ndone;

	tlast = t;
	sum += alast;	/* the sum is one term behind */
	alast = a0;

	if( n > 200 )
		goto ndone;

	an += 1.0e0;
	bn += 1.0e0;
	n += 1.0e0;
	if( t > maxt )
		maxt = t;
	}
while( t > MACHEP );


pdone:	/* series converged! */

/* estimate error due to roundoff and cancellation */
*err = fabs(  MACHEP * (n + maxt)  );

alast = a0;
goto done;

ndone:	/* series did not converge */

/* The following "Converging factors" are supposed to improve accuracy,
 * but do not actually seem to accomplish very much. */

n -= 1.0;
x = 1.0/x;

switch( type )	/* "type" given as subroutine argument */
{
case 1:
	alast *= ( 0.5 + (0.125 + 0.25*b - 0.5*a + 0.25*x - 0.25*n)/x );
	break;

case 2:
	alast *= 2.0/3.0 - b + 2.0*a + x - n;
	break;

default:
	;
}

/* estimate error due to roundoff, cancellation, and nonconvergence */
*err = MACHEP * (n + maxt)  +  fabs ( a0 );


done:
sum += alast;
return( sum );

/* series blew up: */
error:
*err = MAXNUM;
mtherr( "hyperg", TLOSS );
return( sum );
}

/* ========================================================================= */

/*							hyp2f1.c
 *
 *	Gauss hypergeometric function   F
 *	                               2 1
 *
 *
 * SYNOPSIS:
 *
 * double a, b, c, x, y, hyp2f1();
 *
 * y = hyp2f1( a, b, c, x );
 *
 *
 * DESCRIPTION:
 *
 *
 *  hyp2f1( a, b, c, x )  =   F ( a, b; c; x )
 *                           2 1
 *
 *           inf.
 *            -   a(a+1)...(a+k) b(b+1)...(b+k)   k+1
 *   =  1 +   >   -----------------------------  x   .
 *            -         c(c+1)...(c+k) (k+1)!
 *          k = 0
 *
 *  Cases addressed are
 *	Tests and escapes for negative integer a, b, or c
 *	Linear transformation if c - a or c - b negative integer
 *	Special case c = a or c = b
 *	Linear transformation for  x near +1
 *	Transformation for x < -0.5
 *	Psi function expansion if x > 0.5 and c - a - b integer
 *      Conditionally, a recurrence on c to make c-a-b > 0
 *
 * |x| > 1 is rejected.
 *
 * The parameters a, b, c are considered to be integer
 * valued if they are within 1.0e-14 of the nearest integer
 * (1.0e-13 for IEEE arithmetic).
 *
 * ACCURACY:
 *
 *
 *               Relative error (-1 < x < 1):
 * arithmetic   domain     # trials      peak         rms
 *    IEEE      -1,7        230000      1.2e-11     5.2e-14
 *
 * Several special cases also tested with a, b, c in
 * the range -7 to 7.
 *
 * ERROR MESSAGES:
 *
 * A "partial loss of precision" message is printed if
 * the internally estimated relative error exceeds 1^-12.
 * A "singularity" message is printed on overflow or
 * in cases not addressed (such as x < -1).
 */

/*							hyp2f1	*/




#ifdef DEC
#define EPS 1.0e-14
#define EPS2 1.0e-11
#endif

#ifdef IBMPC
#define EPS 1.0e-13
#define EPS2 1.0e-10
#endif

#ifdef MIEEE
#define EPS 1.0e-13
#define EPS2 1.0e-10
#endif

#ifdef UNK
#define EPS 1.0e-13
#define EPS2 1.0e-10
#endif

#define ETHRESH 1.0e-12


double hyp2f1(double a, double b, double c, double x)
{
double d, d1, d2, e;
double p, q, r, s, y, ax;
double ia, ib, ic, id, err;
int flag, i, aid;

err = 0.0;
ax = fabs(x);
s = 1.0 - x;
flag = 0;
ia = round(a); /* nearest integer to a */
ib = round(b);

if( a <= 0 )
	{
	if( fabs(a-ia) < EPS )		/* a is a negative integer */
		flag |= 1;
	}

if( b <= 0 )
	{
	if( fabs(b-ib) < EPS )		/* b is a negative integer */
		flag |= 2;
	}

if( ax < 1.0 )
	{
	if( fabs(b-c) < EPS )		/* b = c */
		{
		y = pow( s, -a );	/* s to the -a power */
		goto hypdon;
		}
	if( fabs(a-c) < EPS )		/* a = c */
		{
		y = pow( s, -b );	/* s to the -b power */
		goto hypdon;
		}
	}



if( c <= 0.0 )
	{
	ic = round(c); 	/* nearest integer to c */
	if( fabs(c-ic) < EPS )		/* c is a negative integer */
		{
		/* check if termination before explosion */
		if( (flag & 1) && (ia > ic) )
			goto hypok;
		if( (flag & 2) && (ib > ic) )
			goto hypok;
		goto hypdiv;
		}
	}

if( flag )			/* function is a polynomial */
	goto hypok;

if( ax > 1.0 )			/* series diverges	*/
	goto hypdiv;

p = c - a;
ia = round(p); /* nearest integer to c-a */
if( (ia <= 0.0) && (fabs(p-ia) < EPS) )	/* negative int c - a */
	flag |= 4;

r = c - b;
ib = round(r); /* nearest integer to c-b */
if( (ib <= 0.0) && (fabs(r-ib) < EPS) )	/* negative int c - b */
	flag |= 8;

d = c - a - b;
id = round(d); /* nearest integer to d */
q = fabs(d-id);

/* Thanks to Christian Burger <BURGER@DMRHRZ11.HRZ.Uni-Marburg.DE>
 * for reporting a bug here.  */
if( fabs(ax-1.0) < EPS )			/* |x| == 1.0	*/
	{
	if( x > 0.0 )
		{
		if( flag & 12 ) /* negative int c-a or c-b */
			{
			if( d >= 0.0 )
				goto hypf;
			else
				goto hypdiv;
			}
		if( d <= 0.0 )
			goto hypdiv;
		y = cephesgamma(c)*cephesgamma(d)/(cephesgamma(p)*cephesgamma(r));
		goto hypdon;
		}

	if( d <= -1.0 )
		goto hypdiv;

	}

/* Conditionally make d > 0 by recurrence on c
 * AMS55 #15.2.27
 */
if( d < 0.0 )
	{
/* Try the power series first */
	y = hyt2f1( a, b, c, x, &err );
	if( err < ETHRESH )
		goto hypdon;
/* Apply the recurrence if power series fails */
	err = 0.0;
	aid = 2 - id;
	e = c + aid;
	d2 = hyp2f1(a,b,e,x);
	d1 = hyp2f1(a,b,e+1.0,x);
	q = a + b + 1.0;
	for( i=0; i<aid; i++ )
		{
		r = e - 1.0;
		y = (e*(r-(2.0*e-q)*x)*d2 + (e-a)*(e-b)*x*d1)/(e*r*s);
		e = r;
		d1 = d2;
		d2 = y;
		}
	goto hypdon;
	}


if( flag & 12 )
	goto hypf; /* negative integer c-a or c-b */

hypok:
y = hyt2f1( a, b, c, x, &err );


hypdon:
if( err > ETHRESH )
	{
	mtherr( "hyp2f1", PLOSS );
/*	printf( "Estimated err = %.2e\n", err ); */
	}
return(y);

/* The transformation for c-a or c-b negative integer
 * AMS55 #15.3.3
 */
hypf:
y = pow( s, d ) * hys2f1( c-a, c-b, c, x, &err );
goto hypdon;

/* The alarm exit */
hypdiv:
mtherr( "hyp2f1", OVERFLOW );
return( MAXNUM );
}






/* Apply transformations for |x| near 1
 * then call the power series
 */
static double hyt2f1(double a, double b, double c, double x, double* loss)
{
double p, q, r, s, t, y, d, err, err1;
double ax, id, d1, d2, e, y1;
int i, aid;

err = 0.0;
s = 1.0 - x;
if( x < -0.5 )
	{
	if( b > a )
		y = pow( s, -a ) * hys2f1( a, c-b, c, -x/s, &err );

	else
		y = pow( s, -b ) * hys2f1( c-a, b, c, -x/s, &err );

	goto done;
	}

d = c - a - b;
id = round(d);	/* nearest integer to d */

if( x > 0.9 )
{
if( fabs(d-id) > EPS ) /* test for integer c-a-b */
	{
/* Try the power series first */
	y = hys2f1( a, b, c, x, &err );
	if( err < ETHRESH )
		goto done;
/* If power series fails, then apply AMS55 #15.3.6 */
	q = hys2f1( a, b, 1.0-d, s, &err );	
	q *= cephesgamma(d) /(cephesgamma(c-a) * cephesgamma(c-b));
	r = pow(s,d) * hys2f1( c-a, c-b, d+1.0, s, &err1 );
	r *= cephesgamma(-d)/(cephesgamma(a) * cephesgamma(b));
	y = q + r;

	q = fabs(q); /* estimate cancellation error */
	r = fabs(r);
	if( q > r )
		r = q;
	err += err1 + (MACHEP*r)/y;

	y *= cephesgamma(c);
	goto done;
	}
else
	{
/* Psi function expansion, AMS55 #15.3.10, #15.3.11, #15.3.12 */
	if( id >= 0.0 )
		{
		e = d;
		d1 = d;
		d2 = 0.0;
		aid = id;
		}
	else
		{
		e = -d;
		d1 = 0.0;
		d2 = d;
		aid = -id;
		}

	ax = log(s);

	/* sum for t = 0 */
	y = psi(1.0) + psi(1.0+e) - psi(a+d1) - psi(b+d1) - ax;
	y /= cephesgamma(e+1.0);

	p = (a+d1) * (b+d1) * s / cephesgamma(e+2.0);	/* Poch for t=1 */
	t = 1.0;
	do
		{
		r = psi(1.0+t) + psi(1.0+t+e) - psi(a+t+d1)
			- psi(b+t+d1) - ax;
		q = p * r;
		y += q;
		p *= s * (a+t+d1) / (t+1.0);
		p *= (b+t+d1) / (t+1.0+e);
		t += 1.0;
		}
	while( fabs(q/y) > EPS );


	if( id == 0.0 )
		{
		y *= cephesgamma(c)/(cephesgamma(a)*cephesgamma(b));
		goto psidon;
		}

	y1 = 1.0;

	if( aid == 1 )
		goto nosum;

	t = 0.0;
	p = 1.0;
	for( i=1; i<aid; i++ )
		{
		r = 1.0-e+t;
		p *= s * (a+t+d2) * (b+t+d2) / r;
		t += 1.0;
		p /= t;
		y1 += p;
		}
nosum:
	p = cephesgamma(c);
	y1 *= cephesgamma(e) * p / (cephesgamma(a+d1) * cephesgamma(b+d1));

	y *= p / (cephesgamma(a+d2) * cephesgamma(b+d2));
	if( (aid & 1) != 0 )
		y = -y;

	q = pow( s, id );	/* s to the id power */
	if( id > 0.0 )
		y *= q;
	else
		y1 *= q;

	y += y1;
psidon:
	goto done;
	}

}

/* Use defining power series if no special cases */
y = hys2f1( a, b, c, x, &err );

done:
*loss = err;
return(y);
}





/* Defining power series expansion of Gauss hypergeometric function */

static double hys2f1(double a, double b, double c, double x, double* loss)
{
double f, g, h, k, m, s, u, umax;
int i;

i = 0;
umax = 0.0;
f = a;
g = b;
h = c;
s = 1.0;
u = 1.0;
k = 0.0;
do
	{
	if( fabs(h) < EPS )
		{
		*loss = 1.0;
		return( MAXNUM );
		}
	m = k + 1.0;
	u = u * ((f+k) * (g+k) * x / ((h+k) * m));
	s += u;
	k = fabs(u);  /* remember largest term summed */
	if( k > umax )
		umax = k;
	k = m;
	if( ++i > 10000 ) /* should never happen */
		{
		*loss = 1.0;
		return(s);
		}
	}
while( fabs(u/s) > MACHEP );

/* return estimated relative error */
*loss = (MACHEP*umax)/fabs(s) + (MACHEP*i);

return(s);
}



/* ========================================================================= */

/*							bdtr.c
 *
 *	Binomial distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k, n;
 * double p, y, bdtr();
 *
 * y = bdtr( k, n, p );
 *
 * DESCRIPTION:
 *
 * Returns the sum of the terms 0 through k of the Binomial
 * probability density:
 *
 *   k
 *   --  ( n )   j      n-j
 *   >   (   )  p  (1-p)
 *   --  ( j )
 *  j=0
 *
 * The terms are not summed directly; instead the incomplete
 * beta integral is employed, according to the formula
 *
 * y = bdtr( k, n, p ) = incbet( n-k, k+1, 1-p ).
 *
 * The arguments must be positive, with p ranging from 0 to 1.
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,p), with p between 0 and 1.
 *
 *               a,b                     Relative error:
 * arithmetic  domain     # trials      peak         rms
 *  For p between 0.001 and 1:
 *    IEEE     0,100       100000      4.3e-15     2.6e-16
 * See also incbet.c.
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * bdtr domain         k < 0            0.0
 *                     n < k
 *                     x < 0, x > 1
 */
/*							bdtrc()
 *
 *	Complemented binomial distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k, n;
 * double p, y, bdtrc();
 *
 * y = bdtrc( k, n, p );
 *
 * DESCRIPTION:
 *
 * Returns the sum of the terms k+1 through n of the Binomial
 * probability density:
 *
 *   n
 *   --  ( n )   j      n-j
 *   >   (   )  p  (1-p)
 *   --  ( j )
 *  j=k+1
 *
 * The terms are not summed directly; instead the incomplete
 * beta integral is employed, according to the formula
 *
 * y = bdtrc( k, n, p ) = incbet( k+1, n-k, p ).
 *
 * The arguments must be positive, with p ranging from 0 to 1.
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,p).
 *
 *               a,b                     Relative error:
 * arithmetic  domain     # trials      peak         rms
 *  For p between 0.001 and 1:
 *    IEEE     0,100       100000      6.7e-15     8.2e-16
 *  For p between 0 and .001:
 *    IEEE     0,100       100000      1.5e-13     2.7e-15
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * bdtrc domain      x<0, x>1, n<k       0.0
 */
/*							bdtri()
 *
 *	Inverse binomial distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k, n;
 * double p, y, bdtri();
 *
 * p = bdtr( k, n, y );
 *
 * DESCRIPTION:
 *
 * Finds the event probability p such that the sum of the
 * terms 0 through k of the Binomial probability density
 * is equal to the given cumulative probability y.
 *
 * This is accomplished using the inverse beta integral
 * function and the relation
 *
 * 1 - p = incbi( n-k, k+1, y ).
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,p).
 *
 *               a,b                     Relative error:
 * arithmetic  domain     # trials      peak         rms
 *  For p between 0.001 and 1:
 *    IEEE     0,100       100000      2.3e-14     6.4e-16
 *    IEEE     0,10000     100000      6.6e-12     1.2e-13
 *  For p between 10^-6 and 0.001:
 *    IEEE     0,100       100000      2.0e-12     1.3e-14
 *    IEEE     0,10000     100000      1.5e-12     3.2e-14
 * See also incbi.c.
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * bdtri domain     k < 0, n <= k         0.0
 *                  x < 0, x > 1
 */

/*								bdtr() */



double bdtrc(int k, int n, double p)
{
double dk, dn;

if( (p < 0.0) || (p > 1.0) )
	goto domerr;
if( k < 0 )
	return( 1.0 );

if( n < k )
	{
domerr:
	mtherr( "bdtrc", DOMAIN );
	return( 0.0 );
	}

if( k == n )
	return( 0.0 );
dn = n - k;
if( k == 0 )
	{
	if( p < .01 )
		dk = -expm1( dn * log1p(-p) );
	else
		dk = 1.0 - pow( 1.0-p, dn );
	}
else
	{
	dk = k + 1;
	dk = incbet( dk, dn, p );
	}
return( dk );
}



double bdtr(int k, int n, double p)
{
double dk, dn;

if( (p < 0.0) || (p > 1.0) )
	goto domerr;
if( (k < 0) || (n < k) )
	{
domerr:
	mtherr( "bdtr", DOMAIN );
	return( 0.0 );
	}

if( k == n )
	return( 1.0 );

dn = n - k;
if( k == 0 )
	{
	dk = pow( 1.0-p, dn );
	}
else
	{
	dk = k + 1;
	dk = incbet( dn, dk, 1.0 - p );
	}
return( dk );
}


double bdtri(int k, int n, double y)
{
double dk, dn, p;

if( (y < 0.0) || (y > 1.0) )
	goto domerr;
if( (k < 0) || (n <= k) )
	{
domerr:
	mtherr( "bdtri", DOMAIN );
	return( 0.0 );
	}

dn = n - k;
if( k == 0 )
	{
	if( y > 0.8 )
		p = -expm1( log1p(y-1.0) / dn );
	else
		p = 1.0 - pow( y, 1.0/dn );
	}
else
	{
	dk = k + 1;
	p = incbet( dn, dk, 0.5 );
	if( p > 0.5 )
		p = incbi( dk, dn, 1.0-y );
	else
		p = 1.0 - incbi( dn, dk, y );
	}
return( p );
}

/* ========================================================================= */

/*							chdtr.c
 *
 *	Chi-square distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * double df, x, y, chdtr();
 *
 * y = chdtr( df, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the area under the left hand tail (from 0 to x)
 * of the Chi square probability density function with
 * v degrees of freedom.
 *
 *
 *                                  inf.
 *                                    -
 *                        1          | |  v/2-1  -t/2
 *  P( x | v )   =   -----------     |   t      e     dt
 *                    v/2  -       | |
 *                   2    | (v/2)   -
 *                                   x
 *
 * where x is the Chi-square variable.
 *
 * The incomplete gamma integral is used, according to the
 * formula
 *
 *	y = chdtr( v, x ) = igam( v/2.0, x/2.0 ).
 *
 *
 * The arguments must both be positive.
 *
 *
 *
 * ACCURACY:
 *
 * See igam().
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * chdtr domain   x < 0 or v < 1        0.0
 */
/*							chdtrc()
 *
 *	Complemented Chi-square distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * double v, x, y, chdtrc();
 *
 * y = chdtrc( v, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the area under the right hand tail (from x to
 * infinity) of the Chi square probability density function
 * with v degrees of freedom:
 *
 *
 *                                  inf.
 *                                    -
 *                        1          | |  v/2-1  -t/2
 *  P( x | v )   =   -----------     |   t      e     dt
 *                    v/2  -       | |
 *                   2    | (v/2)   -
 *                                   x
 *
 * where x is the Chi-square variable.
 *
 * The incomplete gamma integral is used, according to the
 * formula
 *
 *	y = chdtr( v, x ) = igamc( v/2.0, x/2.0 ).
 *
 *
 * The arguments must both be positive.
 *
 *
 *
 * ACCURACY:
 *
 * See igamc().
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * chdtrc domain  x < 0 or v < 1        0.0
 */
/*							chdtri()
 *
 *	Inverse of complemented Chi-square distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * double df, x, y, chdtri();
 *
 * x = chdtri( df, y );
 *
 *
 *
 *
 * DESCRIPTION:
 *
 * Finds the Chi-square argument x such that the integral
 * from x to infinity of the Chi-square density is equal
 * to the given cumulative probability y.
 *
 * This is accomplished using the inverse gamma integral
 * function and the relation
 *
 *    x/2 = igami( df/2, y );
 *
 *
 *
 *
 * ACCURACY:
 *
 * See igami.c.
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * chdtri domain   y < 0 or y > 1        0.0
 *                     v < 1
 *
 */

/*								chdtr() */


double chdtrc(double df, double x)
{
if( (x < 0.0) || (df < 1.0) )
	{
	mtherr( "chdtrc", DOMAIN );
	return(0.0);
	}
return( igamc( df/2.0, x/2.0 ) );
}



double chdtr(double df, double x)
{
if( (x < 0.0) || (df < 1.0) )
	{
	mtherr( "chdtr", DOMAIN );
	return(0.0);
	}
return( igam( df/2.0, x/2.0 ) );
}



double chdtri(double df, double y)
{
double x;

if( (y < 0.0) || (y > 1.0) || (df < 1.0) )
	{
	mtherr( "chdtri", DOMAIN );
	return(0.0);
	}

x = igami( 0.5 * df, y );
return( 2.0 * x );
}

/* ========================================================================= */

/*							fdtr.c
 *
 *	F distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int df1, df2;
 * double x, y, fdtr();
 *
 * y = fdtr( df1, df2, x );
 *
 * DESCRIPTION:
 *
 * Returns the area from zero to x under the F density
 * function (also known as Snedcor's density or the
 * variance ratio density).  This is the density
 * of x = (u1/df1)/(u2/df2), where u1 and u2 are random
 * variables having Chi square distributions with df1
 * and df2 degrees of freedom, respectively.
 *
 * The incomplete beta integral is used, according to the
 * formula
 *
 *	P(x) = incbet( df1/2, df2/2, (df1*x/(df2 + df1*x) ).
 *
 *
 * The arguments a and b are greater than zero, and x is
 * nonnegative.
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,x).
 *
 *                x     a,b                     Relative error:
 * arithmetic  domain  domain     # trials      peak         rms
 *    IEEE      0,1    0,100       100000      9.8e-15     1.7e-15
 *    IEEE      1,5    0,100       100000      6.5e-15     3.5e-16
 *    IEEE      0,1    1,10000     100000      2.2e-11     3.3e-12
 *    IEEE      1,5    1,10000     100000      1.1e-11     1.7e-13
 * See also incbet.c.
 *
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * fdtr domain     a<0, b<0, x<0         0.0
 *
 */
/*							fdtrc()
 *
 *	Complemented F distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int df1, df2;
 * double x, y, fdtrc();
 *
 * y = fdtrc( df1, df2, x );
 *
 * DESCRIPTION:
 *
 * Returns the area from x to infinity under the F density
 * function (also known as Snedcor's density or the
 * variance ratio density).
 *
 *
 *                      inf.
 *                       -
 *              1       | |  a-1      b-1
 * 1-P(x)  =  ------    |   t    (1-t)    dt
 *            B(a,b)  | |
 *                     -
 *                      x
 *
 *
 * The incomplete beta integral is used, according to the
 * formula
 *
 *	P(x) = incbet( df2/2, df1/2, (df2/(df2 + df1*x) ).
 *
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,x) in the indicated intervals.
 *                x     a,b                     Relative error:
 * arithmetic  domain  domain     # trials      peak         rms
 *    IEEE      0,1    1,100       100000      3.7e-14     5.9e-16
 *    IEEE      1,5    1,100       100000      8.0e-15     1.6e-15
 *    IEEE      0,1    1,10000     100000      1.8e-11     3.5e-13
 *    IEEE      1,5    1,10000     100000      2.0e-11     3.0e-12
 * See also incbet.c.
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * fdtrc domain    a<0, b<0, x<0         0.0
 *
 */
/*							fdtri()
 *
 *	Inverse of complemented F distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int df1, df2;
 * double x, p, fdtri();
 *
 * x = fdtri( df1, df2, p );
 *
 * DESCRIPTION:
 *
 * Finds the F density argument x such that the integral
 * from x to infinity of the F density is equal to the
 * given probability p.
 *
 * This is accomplished using the inverse beta integral
 * function and the relations
 *
 *      z = incbi( df2/2, df1/2, p )
 *      x = df2 (1-z) / (df1 z).
 *
 * Note: the following relations hold for the inverse of
 * the uncomplemented F distribution:
 *
 *      z = incbi( df1/2, df2/2, p )
 *      x = df2 z / (df1 (1-z)).
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,p).
 *
 *              a,b                     Relative error:
 * arithmetic  domain     # trials      peak         rms
 *  For p between .001 and 1:
 *    IEEE     1,100       100000      8.3e-15     4.7e-16
 *    IEEE     1,10000     100000      2.1e-11     1.4e-13
 *  For p between 10^-6 and 10^-3:
 *    IEEE     1,100        50000      1.3e-12     8.4e-15
 *    IEEE     1,10000      50000      3.0e-12     4.8e-14
 * See also fdtrc.c.
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * fdtri domain   p <= 0 or p > 1       0.0
 *                     v < 1
 *
 */



double fdtrc(int ia, int ib, double x)
{
double a, b, w;

if( (ia < 1) || (ib < 1) || (x < 0.0) )
	{
	mtherr( "fdtrc", DOMAIN );
	return( 0.0 );
	}
a = ia;
b = ib;
w = b / (b + a * x);
return( incbet( 0.5*b, 0.5*a, w ) );
}



double fdtr(int ia, int ib, double x)
{
double a, b, w;

if( (ia < 1) || (ib < 1) || (x < 0.0) )
	{
	mtherr( "fdtr", DOMAIN );
	return( 0.0 );
	}
a = ia;
b = ib;
w = a * x;
w = w / (b + w);
return( incbet(0.5*a, 0.5*b, w) );
}


double fdtri(int ia, int ib, double y)
{
double a, b, w, x;

if( (ia < 1) || (ib < 1) || (y <= 0.0) || (y > 1.0) )
	{
	mtherr( "fdtri", DOMAIN );
	return( 0.0 );
	}
a = ia;
b = ib;
/* Compute probability for x = 0.5.  */
w = incbet( 0.5*b, 0.5*a, 0.5 );
/* If that is greater than y, then the solution w < .5.
   Otherwise, solve at 1-y to remove cancellation in (b - b*w).  */
if( w > y || y < 0.001)
	{
	w = incbi( 0.5*b, 0.5*a, y );
	x = (b - b*w)/(a*w);
	}
else
	{
	w = incbi( 0.5*a, 0.5*b, 1.0-y );
	x = b*w/(a*(1.0-w));
	}
return(x);
}

/* ========================================================================= */

/*							gdtr.c
 *
 *	Gamma distribution function
 *
 *
 *
 * SYNOPSIS:
 *
 * double a, b, x, y, gdtr();
 *
 * y = gdtr( a, b, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the integral from zero to x of the gamma probability
 * density function:
 *
 *
 *                x
 *        b       -
 *       a       | |   b-1  -at
 * y =  -----    |    t    e    dt
 *       -     | |
 *      | (b)   -
 *               0
 *
 *  The incomplete gamma integral is used, according to the
 * relation
 *
 * y = igam( b, ax ).
 *
 *
 * ACCURACY:
 *
 * See igam().
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * gdtr domain         x < 0            0.0
 *
 */
/*							gdtrc.c
 *
 *	Complemented gamma distribution function
 *
 *
 *
 * SYNOPSIS:
 *
 * double a, b, x, y, gdtrc();
 *
 * y = gdtrc( a, b, x );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the integral from x to infinity of the gamma
 * probability density function:
 *
 *
 *               inf.
 *        b       -
 *       a       | |   b-1  -at
 * y =  -----    |    t    e    dt
 *       -     | |
 *      | (b)   -
 *               x
 *
 *  The incomplete gamma integral is used, according to the
 * relation
 *
 * y = igamc( b, ax ).
 *
 *
 * ACCURACY:
 *
 * See igamc().
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * gdtrc domain         x < 0            0.0
 *
 */

/*							gdtr()  */


double gdtr(double a, double b, double x)
{

if( x < 0.0 )
	{
	mtherr( "gdtr", DOMAIN );
	return( 0.0 );
	}
return(  igam( b, a * x )  );
}



double gdtrc(double a, double b, double x)
{

if( x < 0.0 )
	{
	mtherr( "gdtrc", DOMAIN );
	return( 0.0 );
	}
return(  igamc( b, a * x )  );
}

/* ========================================================================= */

/*							nbdtr.c
 *
 *	Negative binomial distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k, n;
 * double p, y, nbdtr();
 *
 * y = nbdtr( k, n, p );
 *
 * DESCRIPTION:
 *
 * Returns the sum of the terms 0 through k of the negative
 * binomial distribution:
 *
 *   k
 *   --  ( n+j-1 )   n      j
 *   >   (       )  p  (1-p)
 *   --  (   j   )
 *  j=0
 *
 * In a sequence of Bernoulli trials, this is the probability
 * that k or fewer failures precede the nth success.
 *
 * The terms are not computed individually; instead the incomplete
 * beta integral is employed, according to the formula
 *
 * y = nbdtr( k, n, p ) = incbet( n, k+1, p ).
 *
 * The arguments must be positive, with p ranging from 0 to 1.
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,p), with p between 0 and 1.
 *
 *               a,b                     Relative error:
 * arithmetic  domain     # trials      peak         rms
 *    IEEE     0,100       100000      1.7e-13     8.8e-15
 * See also incbet.c.
 *
 */
/*							nbdtr.c
 *
 *	Complemented negative binomial distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k, n;
 * double p, y, nbdtrc();
 *
 * y = nbdtrc( k, n, p );
 *
 * DESCRIPTION:
 *
 * Returns the sum of the terms k+1 to infinity of the negative
 * binomial distribution:
 *
 *   inf
 *   --  ( n+j-1 )   n      j
 *   >   (       )  p  (1-p)
 *   --  (   j   )
 *  j=k+1
 *
 * The terms are not computed individually; instead the incomplete
 * beta integral is employed, according to the formula
 *
 * y = nbdtrc( k, n, p ) = incbet( k+1, n, 1-p ).
 *
 * The arguments must be positive, with p ranging from 0 to 1.
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,p), with p between 0 and 1.
 *
 *               a,b                     Relative error:
 * arithmetic  domain     # trials      peak         rms
 *    IEEE     0,100       100000      1.7e-13     8.8e-15
 * See also incbet.c.
 */
/*							nbdtr.c
 *
 *	Functional inverse of negative binomial distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k, n;
 * double p, y, nbdtri();
 *
 * p = nbdtri( k, n, y );
 *
 * DESCRIPTION:
 *
 * Finds the argument p such that nbdtr(k,n,p) is equal to y.
 *
 * ACCURACY:
 *
 * Tested at random points (a,b,y), with y between 0 and 1.
 *
 *               a,b                     Relative error:
 * arithmetic  domain     # trials      peak         rms
 *    IEEE     0,100       100000      1.5e-14     8.5e-16
 * See also incbi.c.
 */


double nbdtrc(int k, int n, double p)
{
double dk, dn;

if( (p < 0.0) || (p > 1.0) )
	goto domerr;
if( k < 0 )
	{
domerr:
	mtherr( "nbdtr", DOMAIN );
	return( 0.0 );
	}

dk = k+1;
dn = n;
return( incbet( dk, dn, 1.0 - p ) );
}



double nbdtr(int k, int n, double p)
{
double dk, dn;

if( (p < 0.0) || (p > 1.0) )
	goto domerr;
if( k < 0 )
	{
domerr:
	mtherr( "nbdtr", DOMAIN );
	return( 0.0 );
	}
dk = k+1;
dn = n;
return( incbet( dn, dk, p ) );
}



double nbdtri(int k, int n, double p)
{
double dk, dn, w;

if( (p < 0.0) || (p > 1.0) )
	goto domerr;
if( k < 0 )
	{
domerr:
	mtherr( "nbdtri", DOMAIN );
	return( 0.0 );
	}
dk = k+1;
dn = n;
w = incbi( dn, dk, p );
return( w );
}

/* ========================================================================= */

/*							ndtri.c
 *
 *	Inverse of Normal distribution function
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, ndtri();
 *
 * x = ndtri( y );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the argument, x, for which the area under the
 * Gaussian probability density function (integrated from
 * minus infinity to x) is equal to y.
 *
 *
 * For small arguments 0 < y < exp(-2), the program computes
 * z = sqrt( -2.0 * log(y) );  then the approximation is
 * x = z - log(z)/z  - (1/z) P(1/z) / Q(1/z).
 * There are two rational functions P/Q, one for 0 < y < exp(-32)
 * and the other for y up to exp(-2).  For larger arguments,
 * w = y - 0.5, and  x/sqrt(2pi) = w + w**3 R(w**2)/S(w**2)).
 *
 *
 * ACCURACY:
 *
 *                      Relative error:
 * arithmetic   domain        # trials      peak         rms
 *    DEC      0.125, 1         5500       9.5e-17     2.1e-17
 *    DEC      6e-39, 0.135     3500       5.7e-17     1.3e-17
 *    IEEE     0.125, 1        20000       7.2e-16     1.3e-16
 *    IEEE     3e-308, 0.135   50000       4.6e-16     9.8e-17
 *
 *
 * ERROR MESSAGES:
 *
 *   message         condition    value returned
 * ndtri domain       x <= 0        -MAXNUM
 * ndtri domain       x >= 1         MAXNUM
 *
 */



#ifdef UNK
/* sqrt(2pi) */
static double s2pi = 2.50662827463100050242E0;
#endif

#ifdef DEC
static unsigned short s2p[] = {0040440,0066230,0177661,0034055};
#define s2pi *(double *)s2p
#endif

#ifdef IBMPC
static unsigned short s2p[] = {0x2706,0x1ff6,0x0d93,0x4004};
#define s2pi *(double *)s2p
#endif

#ifdef MIEEE
static unsigned short s2p[] = {
0x4004,0x0d93,0x1ff6,0x2706
};
#define s2pi *(double *)s2p
#endif

/* approximation for 0 <= |y - 0.5| <= 3/8 */
#ifdef UNK
static double NP0[5] = {
-5.99633501014107895267E1,
 9.80010754185999661536E1,
-5.66762857469070293439E1,
 1.39312609387279679503E1,
-1.23916583867381258016E0,
};
static double NQ0[8] = {
/* 1.00000000000000000000E0,*/
 1.95448858338141759834E0,
 4.67627912898881538453E0,
 8.63602421390890590575E1,
-2.25462687854119370527E2,
 2.00260212380060660359E2,
-8.20372256168333339912E1,
 1.59056225126211695515E1,
-1.18331621121330003142E0,
};
#endif
#ifdef DEC
static unsigned short NP0[20] = {
0141557,0155170,0071360,0120550,
0041704,0000214,0172417,0067307,
0141542,0132204,0040066,0156723,
0041136,0163161,0157276,0007747,
0140236,0116374,0073666,0051764,
};
static unsigned short NQ0[32] = {
/*0040200,0000000,0000000,0000000,*/
0040372,0026256,0110403,0123707,
0040625,0122024,0020277,0026661,
0041654,0134161,0124134,0007244,
0142141,0073162,0133021,0131371,
0042110,0041235,0043516,0057767,
0141644,0011417,0036155,0137305,
0041176,0076556,0004043,0125430,
0140227,0073347,0152776,0067251,
};
#endif
#ifdef IBMPC
static unsigned short NP0[20] = {
0x142d,0x0e5e,0xfb4f,0xc04d,
0xedd9,0x9ea1,0x8011,0x4058,
0xdbba,0x8806,0x5690,0xc04c,
0xc1fd,0x3bd7,0xdcce,0x402b,
0xca7e,0x8ef6,0xd39f,0xbff3,
};
static unsigned short NQ0[36] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0x74f9,0xd220,0x4595,0x3fff,
0xe5b6,0x8417,0xb482,0x4012,
0x81d4,0x350b,0x970e,0x4055,
0x365f,0x56c2,0x2ece,0xc06c,
0xcbff,0xa8e9,0x0853,0x4069,
0xb7d9,0xe78d,0x8261,0xc054,
0x7563,0xc104,0xcfad,0x402f,
0xcdd5,0xfabf,0xeedc,0xbff2,
};
#endif
#ifdef MIEEE
static unsigned short NP0[20] = {
0xc04d,0xfb4f,0x0e5e,0x142d,
0x4058,0x8011,0x9ea1,0xedd9,
0xc04c,0x5690,0x8806,0xdbba,
0x402b,0xdcce,0x3bd7,0xc1fd,
0xbff3,0xd39f,0x8ef6,0xca7e,
};
static unsigned short NQ0[32] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x3fff,0x4595,0xd220,0x74f9,
0x4012,0xb482,0x8417,0xe5b6,
0x4055,0x970e,0x350b,0x81d4,
0xc06c,0x2ece,0x56c2,0x365f,
0x4069,0x0853,0xa8e9,0xcbff,
0xc054,0x8261,0xe78d,0xb7d9,
0x402f,0xcfad,0xc104,0x7563,
0xbff2,0xeedc,0xfabf,0xcdd5,
};
#endif


/* Approximation for interval z = sqrt(-2 log y ) between 2 and 8
 * i.e., y between exp(-2) = .135 and exp(-32) = 1.27e-14.
 */
#ifdef UNK
static double NP1[9] = {
 4.05544892305962419923E0,
 3.15251094599893866154E1,
 5.71628192246421288162E1,
 4.40805073893200834700E1,
 1.46849561928858024014E1,
 2.18663306850790267539E0,
-1.40256079171354495875E-1,
-3.50424626827848203418E-2,
-8.57456785154685413611E-4,
};
static double NQ1[8] = {
/*  1.00000000000000000000E0,*/
 1.57799883256466749731E1,
 4.53907635128879210584E1,
 4.13172038254672030440E1,
 1.50425385692907503408E1,
 2.50464946208309415979E0,
-1.42182922854787788574E-1,
-3.80806407691578277194E-2,
-9.33259480895457427372E-4,
};
#endif
#ifdef DEC
static unsigned short NP1[36] = {
0040601,0143074,0150744,0073326,
0041374,0031554,0113253,0146016,
0041544,0123272,0012463,0176771,
0041460,0051160,0103560,0156511,
0041152,0172624,0117772,0030755,
0040413,0170713,0151545,0176413,
0137417,0117512,0022154,0131671,
0137017,0104257,0071432,0007072,
0135540,0143363,0063137,0036166,
};
static unsigned short NQ1[32] = {
/*0040200,0000000,0000000,0000000,*/
0041174,0075325,0004736,0120326,
0041465,0110044,0047561,0045567,
0041445,0042321,0012142,0030340,
0041160,0127074,0166076,0141051,
0040440,0046055,0040745,0150400,
0137421,0114146,0067330,0010621,
0137033,0175162,0025555,0114351,
0135564,0122773,0145750,0030357,
};
#endif
#ifdef IBMPC
static unsigned short NP1[36] = {
0x8edb,0x9a3c,0x38c7,0x4010,
0x7982,0x92d5,0x866d,0x403f,
0x7fbf,0x42a6,0x94d7,0x404c,
0x1ba9,0x10ee,0x0a4e,0x4046,
0x463e,0x93ff,0x5eb2,0x402d,
0xbfa1,0x7a6c,0x7e39,0x4001,
0x9677,0x448d,0xf3e9,0xbfc1,
0x41c7,0xee63,0xf115,0xbfa1,
0xe78f,0x6ccb,0x18de,0xbf4c,
};
static unsigned short NQ1[32] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xd41b,0xa13b,0x8f5a,0x402f,
0x296f,0x89ee,0xb204,0x4046,
0x461c,0x228c,0xa89a,0x4044,
0xd845,0x9d87,0x15c7,0x402e,
0xba20,0xa83c,0x0985,0x4004,
0x0232,0xcddb,0x330c,0xbfc2,
0xb31d,0x456d,0x7f4e,0xbfa3,
0x061e,0x797d,0x94bf,0xbf4e,
};
#endif
#ifdef MIEEE
static unsigned short NP1[36] = {
0x4010,0x38c7,0x9a3c,0x8edb,
0x403f,0x866d,0x92d5,0x7982,
0x404c,0x94d7,0x42a6,0x7fbf,
0x4046,0x0a4e,0x10ee,0x1ba9,
0x402d,0x5eb2,0x93ff,0x463e,
0x4001,0x7e39,0x7a6c,0xbfa1,
0xbfc1,0xf3e9,0x448d,0x9677,
0xbfa1,0xf115,0xee63,0x41c7,
0xbf4c,0x18de,0x6ccb,0xe78f,
};
static unsigned short NQ1[32] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x402f,0x8f5a,0xa13b,0xd41b,
0x4046,0xb204,0x89ee,0x296f,
0x4044,0xa89a,0x228c,0x461c,
0x402e,0x15c7,0x9d87,0xd845,
0x4004,0x0985,0xa83c,0xba20,
0xbfc2,0x330c,0xcddb,0x0232,
0xbfa3,0x7f4e,0x456d,0xb31d,
0xbf4e,0x94bf,0x797d,0x061e,
};
#endif

/* Approximation for interval z = sqrt(-2 log y ) between 8 and 64
 * i.e., y between exp(-32) = 1.27e-14 and exp(-2048) = 3.67e-890.
 */

#ifdef UNK
static double NP2[9] = {
  3.23774891776946035970E0,
  6.91522889068984211695E0,
  3.93881025292474443415E0,
  1.33303460815807542389E0,
  2.01485389549179081538E-1,
  1.23716634817820021358E-2,
  3.01581553508235416007E-4,
  2.65806974686737550832E-6,
  6.23974539184983293730E-9,
};
static double NQ2[8] = {
/*  1.00000000000000000000E0,*/
  6.02427039364742014255E0,
  3.67983563856160859403E0,
  1.37702099489081330271E0,
  2.16236993594496635890E-1,
  1.34204006088543189037E-2,
  3.28014464682127739104E-4,
  2.89247864745380683936E-6,
  6.79019408009981274425E-9,
};
#endif
#ifdef DEC
static unsigned short NP2[36] = {
0040517,0033507,0036236,0125641,
0040735,0044616,0014473,0140133,
0040574,0012567,0114535,0102541,
0040252,0120340,0143474,0150135,
0037516,0051057,0115361,0031211,
0036512,0131204,0101511,0125144,
0035236,0016627,0043160,0140216,
0033462,0060512,0060141,0010641,
0031326,0062541,0101304,0077706,
};
static unsigned short NQ2[32] = {
/*0040200,0000000,0000000,0000000,*/
0040700,0143322,0132137,0040501,
0040553,0101155,0053221,0140257,
0040260,0041071,0052573,0010004,
0037535,0066472,0177261,0162330,
0036533,0160475,0066666,0036132,
0035253,0174533,0027771,0044027,
0033502,0016147,0117666,0063671,
0031351,0047455,0141663,0054751,
};
#endif
#ifdef IBMPC
static unsigned short NP2[36] = {
0xd574,0xe793,0xe6e8,0x4009,
0x780b,0xc327,0xa931,0x401b,
0xb0ac,0xf32b,0x82ae,0x400f,
0x9a0c,0x18e7,0x541c,0x3ff5,
0x2651,0xf35e,0xca45,0x3fc9,
0x354d,0x9069,0x5650,0x3f89,
0x1812,0xe8ce,0xc3b2,0x3f33,
0x2234,0x4c0c,0x4c29,0x3ec6,
0x8ff9,0x3058,0xccac,0x3e3a,
};
static unsigned short NQ2[32] = {
/*0x0000,0x0000,0x0000,0x3ff0,*/
0xe828,0x568b,0x18da,0x4018,
0x3816,0xaad2,0x704d,0x400d,
0x6200,0x2aaf,0x0847,0x3ff6,
0x3c9b,0x5fd6,0xada7,0x3fcb,
0xc78b,0xadb6,0x7c27,0x3f8b,
0x2903,0x65ff,0x7f2b,0x3f35,
0xccf7,0xf3f6,0x438c,0x3ec8,
0x6b3d,0xb876,0x29e5,0x3e3d,
};
#endif
#ifdef MIEEE
static unsigned short NP2[36] = {
0x4009,0xe6e8,0xe793,0xd574,
0x401b,0xa931,0xc327,0x780b,
0x400f,0x82ae,0xf32b,0xb0ac,
0x3ff5,0x541c,0x18e7,0x9a0c,
0x3fc9,0xca45,0xf35e,0x2651,
0x3f89,0x5650,0x9069,0x354d,
0x3f33,0xc3b2,0xe8ce,0x1812,
0x3ec6,0x4c29,0x4c0c,0x2234,
0x3e3a,0xccac,0x3058,0x8ff9,
};
static unsigned short NQ2[32] = {
/*0x3ff0,0x0000,0x0000,0x0000,*/
0x4018,0x18da,0x568b,0xe828,
0x400d,0x704d,0xaad2,0x3816,
0x3ff6,0x0847,0x2aaf,0x6200,
0x3fcb,0xada7,0x5fd6,0x3c9b,
0x3f8b,0x7c27,0xadb6,0xc78b,
0x3f35,0x7f2b,0x65ff,0x2903,
0x3ec8,0x438c,0xf3f6,0xccf7,
0x3e3d,0x29e5,0xb876,0x6b3d,
};
#endif


double ndtri(double y0)
{
double x, y, z, y2, x0, x1;
int code;

if( y0 <= 0.0 )
	{
	mtherr( "ndtri", DOMAIN );
	return( -MAXNUM );
	}
if( y0 >= 1.0 )
	{
	mtherr( "ndtri", DOMAIN );
	return( MAXNUM );
	}
code = 1;
y = y0;
if( y > (1.0 - 0.13533528323661269189) ) /* 0.135... = exp(-2) */
	{
	y = 1.0 - y;
	code = 0;
	}

if( y > 0.13533528323661269189 )
	{
	y = y - 0.5;
	y2 = y * y;
	x = y + y * (y2 * polevl( y2, NP0, 4)/p1evl( y2, NQ0, 8 ));
	x = x * s2pi; 
	return(x);
	}

x = sqrt( -2.0 * log(y) );
x0 = x - log(x)/x;

z = 1.0/x;
if( x < 8.0 ) /* y > exp(-32) = 1.2664165549e-14 */
	x1 = z * polevl( z, NP1, 8 )/p1evl( z, NQ1, 8 );
else
	x1 = z * polevl( z, NP2, 8 )/p1evl( z, NQ2, 8 );
x = x0 - x1;
if( code != 0 )
	x = -x;
return( x );
}

/* ========================================================================= */

/*							pdtr.c
 *
 *	Poisson distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k;
 * double m, y, pdtr();
 *
 * y = pdtr( k, m );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the sum of the first k terms of the Poisson
 * distribution:
 *
 *   k         j
 *   --   -m  m
 *   >   e    --
 *   --       j!
 *  j=0
 *
 * The terms are not summed directly; instead the incomplete
 * gamma integral is employed, according to the relation
 *
 * y = pdtr( k, m ) = igamc( k+1, m ).
 *
 * The arguments must both be positive.
 *
 *
 *
 * ACCURACY:
 *
 * See igamc().
 *
 */
/*							pdtrc()
 *
 *	Complemented poisson distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k;
 * double m, y, pdtrc();
 *
 * y = pdtrc( k, m );
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the sum of the terms k+1 to infinity of the Poisson
 * distribution:
 *
 *  inf.       j
 *   --   -m  m
 *   >   e    --
 *   --       j!
 *  j=k+1
 *
 * The terms are not summed directly; instead the incomplete
 * gamma integral is employed, according to the formula
 *
 * y = pdtrc( k, m ) = igam( k+1, m ).
 *
 * The arguments must both be positive.
 *
 *
 *
 * ACCURACY:
 *
 * See igam.c.
 *
 */
/*							pdtri()
 *
 *	Inverse Poisson distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * int k;
 * double m, y, pdtr();
 *
 * m = pdtri( k, y );
 *
 *
 *
 *
 * DESCRIPTION:
 *
 * Finds the Poisson variable x such that the integral
 * from 0 to x of the Poisson density is equal to the
 * given probability y.
 *
 * This is accomplished using the inverse gamma integral
 * function and the relation
 *
 *    m = igami( k+1, y ).
 *
 *
 *
 *
 * ACCURACY:
 *
 * See igami.c.
 *
 * ERROR MESSAGES:
 *
 *   message         condition      value returned
 * pdtri domain    y < 0 or y >= 1       0.0
 *                     k < 0
 *
 */


double pdtrc(int k, double m)
{
double v;

if( (k < 0) || (m <= 0.0) )
	{
	mtherr( "pdtrc", DOMAIN );
	return( 0.0 );
	}
v = k+1;
return( igam( v, m ) );
}



double pdtr(int k, double m)
{
double v;

if( (k < 0) || (m <= 0.0) )
	{
	mtherr( "pdtr", DOMAIN );
	return( 0.0 );
	}
v = k+1;
return( igamc( v, m ) );
}


double pdtri(int k, double y)
{
double v;

if( (k < 0) || (y < 0.0) || (y >= 1.0) )
	{
	mtherr( "pdtri", DOMAIN );
	return( 0.0 );
	}
v = k+1;
v = igami( v, y );
return( v );
}

/* ========================================================================= */

/*							stdtr.c
 *
 *	Student's t distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * double t, stdtr();
 * short k;
 *
 * y = stdtr( k, t );
 *
 *
 * DESCRIPTION:
 *
 * Computes the integral from minus infinity to t of the Student
 * t distribution with integer k > 0 degrees of freedom:
 *
 *                                      t
 *                                      -
 *                                     | |
 *              -                      |         2   -(k+1)/2
 *             | ( (k+1)/2 )           |  (     x   )
 *       ----------------------        |  ( 1 + --- )        dx
 *                     -               |  (      k  )
 *       sqrt( k pi ) | ( k/2 )        |
 *                                   | |
 *                                    -
 *                                   -inf.
 * 
 * Relation to incomplete beta integral:
 *
 *        1 - stdtr(k,t) = 0.5 * incbet( k/2, 1/2, z )
 * where
 *        z = k/(k + t**2).
 *
 * For t < -2, this is the method of computation.  For higher t,
 * a direct method is derived from integration by parts.
 * Since the function is symmetric about t=0, the area under the
 * right tail of the density is found by calling the function
 * with -t instead of t.
 * 
 * ACCURACY:
 *
 * Tested at random 1 <= k <= 25.  The "domain" refers to t.
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE     -100,-2      50000       5.9e-15     1.4e-15
 *    IEEE     -2,100      500000       2.7e-15     4.9e-17
 */

/*							stdtri.c
 *
 *	Functional inverse of Student's t distribution
 *
 *
 *
 * SYNOPSIS:
 *
 * double p, t, stdtri();
 * int k;
 *
 * t = stdtri( k, p );
 *
 *
 * DESCRIPTION:
 *
 * Given probability p, finds the argument t such that stdtr(k,t)
 * is equal to p.
 * 
 * ACCURACY:
 *
 * Tested at random 1 <= k <= 100.  The "domain" refers to p:
 *                      Relative error:
 * arithmetic   domain     # trials      peak         rms
 *    IEEE    .001,.999     25000       5.7e-15     8.0e-16
 *    IEEE    10^-6,.001    25000       2.0e-12     2.9e-14
 */



double stdtr(int k, double t)
{
double x, rk, z, f, tz, p, xsqk;
int j;

if( k <= 0 )
	{
	mtherr( "stdtr", DOMAIN );
	return(0.0);
	}

if( t == 0 )
	return( 0.5 );

if( t < -2.0 )
	{
	rk = k;
	z = rk / (rk + t * t);
	p = 0.5 * incbet( 0.5*rk, 0.5, z );
	return( p );
	}

/*	compute integral from -t to + t */

if( t < 0 )
	x = -t;
else
	x = t;

rk = k;	/* degrees of freedom */
z = 1.0 + ( x * x )/rk;

/* test if k is odd or even */
if( (k & 1) != 0)
	{

	/*	computation for odd k	*/

	xsqk = x/sqrt(rk);
	p = atan( xsqk );
	if( k > 1 )
		{
		f = 1.0;
		tz = 1.0;
		j = 3;
		while(  (j<=(k-2)) && ( (tz/f) > MACHEP )  )
			{
			tz *= (j-1)/( z * j );
			f += tz;
			j += 2;
			}
		p += f * xsqk/z;
		}
	p *= 2.0/PI;
	}


else
	{

	/*	computation for even k	*/

	f = 1.0;
	tz = 1.0;
	j = 2;

	while(  ( j <= (k-2) ) && ( (tz/f) > MACHEP )  )
		{
		tz *= (j - 1)/( z * j );
		f += tz;
		j += 2;
		}
	p = f * x/sqrt(z*rk);
	}

/*	common exit	*/


if( t < 0 )
	p = -p;	/* note destruction of relative accuracy */

	p = 0.5 + 0.5 * p;
return(p);
}

double stdtri(int k, double p)
{
double t, rk, z;
int rflg;

if( k <= 0 || p <= 0.0 || p >= 1.0 )
	{
	mtherr( "stdtri", DOMAIN );
	return(0.0);
	}

rk = k;

if( p > 0.25 && p < 0.75 )
	{
	if( p == 0.5 )
		return( 0.0 );
	z = 1.0 - 2.0 * p;
	z = incbi( 0.5, 0.5*rk, fabs(z) );
	t = sqrt( rk*z/(1.0-z) );
	if( p < 0.5 )
		t = -t;
	return( t );
	}
rflg = -1;
if( p >= 0.5)
	{
	p = 1.0 - p;
	rflg = 1;
	}
z = incbi( 0.5*rk, 0.5, 2.0*p );

if( MAXNUM * z < rk )
	return(rflg* MAXNUM);
t = sqrt( rk/z - rk );
return( rflg * t );
}

/* ========================================================================= */

/*							unity.c
 *
 * Relative error approximations for function arguments near
 * unity.
 *
 *    log1p(x) = log(1+x)
 *    expm1(x) = exp(x) - 1
 *    cosm1(x) = cos(x) - 1
 *
 */


#ifndef HAVE_LOG1P
/* log1p(x) = log(1 + x)  */

/* Coefficients for log(1+x) = x - x**2/2 + x**3 P(x)/Q(x)
 * 1/sqrt(2) <= x < sqrt(2)
 * Theoretical peak relative error = 2.32e-20
 */
static double LP[] = {
 4.5270000862445199635215E-5,
 4.9854102823193375972212E-1,
 6.5787325942061044846969E0,
 2.9911919328553073277375E1,
 6.0949667980987787057556E1,
 5.7112963590585538103336E1,
 2.0039553499201281259648E1,
};
static double LQ[] = {
/* 1.0000000000000000000000E0,*/
 1.5062909083469192043167E1,
 8.3047565967967209469434E1,
 2.2176239823732856465394E2,
 3.0909872225312059774938E2,
 2.1642788614495947685003E2,
 6.0118660497603843919306E1,
};

#define SQRTH 0.70710678118654752440
#define SQRT2 1.41421356237309504880

double log1p(double x)
{
double z;

z = 1.0 + x;
if( (z < SQRTH) || (z > SQRT2) )
	return( log(z) );
z = x*x;
z = -0.5 * z + x * ( z * polevl( x, LP, 6 ) / p1evl( x, LQ, 6 ) );
return (x + z);
}
#endif


#ifndef HAVE_EXPM1
/* expm1(x) = exp(x) - 1  */

/*  e^x =  1 + 2x P(x^2)/( Q(x^2) - P(x^2) )
 * -0.5 <= x <= 0.5
 */

static double EP[3] = {
 1.2617719307481059087798E-4,
 3.0299440770744196129956E-2,
 9.9999999999999999991025E-1,
};
static double EQ[4] = {
 3.0019850513866445504159E-6,
 2.5244834034968410419224E-3,
 2.2726554820815502876593E-1,
 2.0000000000000000000897E0,
};

double expm1(double x)
{
double r, xx;

#ifdef NANS
if( isnan(x) )
	return(x);
#endif
#ifdef INFINITIES
if( x == CEPHESINFINITY )
	return(CEPHESINFINITY);
if( x == -CEPHESINFINITY )
	return(-1.0);
#endif
if( (x < -0.5) || (x > 0.5) )
	return( exp(x) - 1.0 );
xx = x * x;
r = x * polevl( xx, EP, 2 );
r = r/( polevl( xx, EQ, 3 ) - r );
return (r + r);
}
#endif



/* cosm1(x) = cos(x) - 1  */

static double coscof[7] = {
 4.7377507964246204691685E-14,
-1.1470284843425359765671E-11,
 2.0876754287081521758361E-9,
-2.7557319214999787979814E-7,
 2.4801587301570552304991E-5,
-1.3888888888888872993737E-3,
 4.1666666666666666609054E-2,
};

double cosm1(double x)
{
double xx;

if( (x < -PIO4) || (x > PIO4) )
	return( cos(x) - 1.0 );
xx = x * x;
xx = -0.5*xx + xx * xx * polevl( xx, coscof, 6 );
return xx;
}

/* ========================================================================= */

/*							round.c
 *
 *	Round double to nearest or even integer valued double
 *
 *
 *
 * SYNOPSIS:
 *
 * double x, y, round();
 *
 * y = round(x);
 *
 *
 *
 * DESCRIPTION:
 *
 * Returns the nearest integer to x as a double precision
 * floating point result.  If x ends in 0.5 exactly, the
 * nearest even integer is chosen.
 * 
 *
 *
 * ACCURACY:
 *
 * If x is greater than 1/(2*MACHEP), its closest machine
 * representation is already an integer, so rounding does
 * not change it.
 */


#ifndef HAVE_ROUND
double round(double x)
{
double y, r;

/* Largest integer <= x */
y = floor(x);

/* Fractional part */
r = x - y;

/* Round up to nearest. */
if( r > 0.5 )
	goto rndup;

/* Round to even */
if( r == 0.5 )
	{
	r = y - 2.0 * floor( 0.5 * y );
	if( r == 1.0 )
		{
rndup:
		y += 1.0;
		}
	}

/* Else round down. */
return(y);
}
#endif
