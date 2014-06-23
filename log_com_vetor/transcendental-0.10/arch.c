/* This program determines if the computer architecture is consistent with
 * the ANSI/IEEE 754 standard, the Motorola-type IEEE architecture, or the
 * DEC architecture by checking the interpretation of individual bits in a
 * C double. Compile with
 * gcc arch.c -DIBMPC
 * gcc arch.c -DMIEEE
 * gcc arch.c -DDEC
 * and run each executable. If the correct architecture was chosen, the
 * executable returns 0. Otherwise, it returns 1. For IBMPC and MIEEE, you
 * should also add -DHAVE_DECL_ISNAN if the function isnan to check for
 * NaNs is available on your system.
 * This program is compiled and run automatically from the setup.py script
 * when you execute "python setup.py config".
 *
 * Michiel de Hoon, University of Tokyo, Human Genome Center.
 * mdehoon@ims.u-tokyo.ac.jp
 */

/* Test results:
Windows 2000			Intel Xeon CPU 1700 MHz			IBMPC
Windows 2000 running Cygwin	Intel Xeon CPU 1700 MHz			IBMPC
Mac OS X version 10.3.2		PowerPC G4 800 MHz			MIEEE
Redhat Linux 9			Intel Pentium III			IBMPC
SunOS 5.8			Sun Fire 15K				MIEEE
HP Tru64 Unix 5.1b(JAVA)	DS20L 2@833MHz(ev68)	IBMPC; fails denormals
HP Tru64 Unix 5.1b(JAVA)	DS20E 2@667MHz (ev67)	IBMPC; fails denormals
HP Tru64 Unix 5.1b(JAVA)	ES40 4@833MHz (ev67)	IBMPC; fails denormals
HP Tru64 Unix 5.1b(JAVA)	ES45 4@1GHz (ev68)	IBMPC; fails denormals
HP Tru64 Unix 5.1b(JAVA)	ES47 2@1GHz (ev7)	IBMPC; fails denormals
HP OpenVMS 7.3-2		DS10-L 1@466MHz (ev6)			DEC
HP OpenVMS 7.3-2		DS20 2@500MHz (ev6)			DEC
HP OpenVMS 8.1			rx2600 2@900MHz (Itanium II)		other
HP-UX 11i 11.22			rx2600 2@900MHz (Itanium II)		MIEEE
HP-UX 11i 11.23			rx2600 2@900MHz (Itanium II)		MIEEE
HP-UX 11i 11.23			rx2600 2@1.5GHz (Itanium II)		MIEEE
HP-UX 11i 11.11			rp2470 2@750MHz (PA-RISC)		MIEEE
HP-UX 11i 11.11			rp2470 2@750MHz (PA-RISC)		MIEEE
Debian GNU/Linux 3.0 on Intel	ProLiant DL360 G2 1.4GHz (P3)		IBMPC
Debian GNU/Linux 3.0 on Intel	rx2600 2@900MHz (Itanium II)		IBMPC
Debian GNU/Linux 3.0r2 on Intel   rx2600 2@1.5GHz (Itanium II)		IBMPC
Debian GNU/Linux 3.0 on Alpha     XP1000a 1@667MHz (ev6)		other
Debian GNU/Linux 3.0 on Alpha     DS20 2@500MHz (ev6)			other
Debian GNU/Linux 3.0 on PA-RISC   rp5470 1@550MHz (PA-RISC)		MIEEE
Mandrake Linux 9.2 on Intel       ProLiant DL360 2@1.2GHz (P3)		IBMPC
Red Hat Ent Linux ES 2.1 on Intel ProLiant ML530 2@1.0GHz (P3)		IBMPC
Red Hat Ent Linux AS 2.1 on Intel ProLiant DL360 2@800MHz (P3) 		IBMPC
Red Hat Ent Linux AS 2.1 on Intel rx2600 2@900MHz (ItaniumII)		IBMPC
Red Hat Ent Linux AS 2.1 on Intel rx2600 2@900MHz (ItaniumII)		IBMPC
Red Hat Ent Linux AS 2.1 on Intel Intel 4@1.4GHz (Itanium II)		IBMPC
Red Hat Linux 7.2 on Alpha        DS20 2@500MHz (ev6)			other
Red Hat Linux 7.2 on Alpha        ES40 4@667MHz (ev67)			other
Slackware Linux 9.1 on Intel      ProLiant ML530 2@800MHz (P3)		IBMPC
SuSE Linux Ent Svr 8.0 on Intel   ProLiant DL360 2@1.4GHz (P3)		IBMPC
FreeBSD 4.9 on Intel              ProLiant DL360 2@1.4GHz (P3)		IBMPC
FreeBSD 5.1 on Alpha              XP1000a 1@667MHz (ev6)		other
NetBSD 1.6 on Intel               ProLiant DL360 2@1.2GHz (P3)		IBMPC
Beowulf BrickWall Cluster         DS10 & DS10-L(8) 466MHz (ev6)		other
HP TruCluster Server 5.1b(JAVA)   ES40 883Mhz & DS20E 667Mhz		other
Red Hat Advanced Server Cluster   ProLiant DL360x2 2@800MHz (P3)	IBMPC
*/

#ifdef DEC

/* For sprintf */
#include <stdio.h>

/* We need signal to be able to ignore SIGFPE when checking NaN */
#include <signal.h>

static int dec_isnan(double x)
/* The usual method to check for NaN (x==x) doesn't seem to work on DEC.
 * We use this kludge instead. */
{ char buffer[32];
  sprintf (buffer, "%f", x);
  if ((buffer[0]=='N' || buffer[0]=='n') &&
      (buffer[1]=='a' || buffer[1]=='a') &&
      (buffer[2]=='N' || buffer[1]=='n') &&
       buffer[3]=='\0') return 1;
  else return 0;
}

#else

#include <math.h>
/* For exp when checking for infinity. */

#ifndef HAVE_DECL_ISNAN
#define isnan(x) ((x)!=(x))
/* This usually works (but it didn't work for DEC, so beware!). The function
 * isnan is used for IBMPC and MIEEE only. */
#endif

#endif

#ifdef DEC
int main(void)
{ int i, j;
  unsigned short p[4];
  double* x = (double*)p;
  double y;
  const unsigned short pc[7] =
    {0x4080,0x4100,0x4200,0x4400,0x4800,0x5000,0x6000};
  const unsigned short nc[8] =
    {0x4000,0x3f80,0x3f00,0x3e00,0x3c00,0x3800,0x3000,0x2000};
  const int px[7] = {1, 2, 4, 8, 16, 32, 64};
  const int nx[8] = {0, 1, 2, 4, 8, 16, 32, 64};
  /* Switch off signalling so that we can check NaNs. */
  signal(SIGFPE, SIG_IGN);
  /* Sign is 1, exponent is 0 yields NaN */
  p[0] = 0x8000;
  p[1] = 0x0000;
  p[2] = 0x0000;
  p[3] = 0x0000;
  if (!dec_isnan(*x)) return 1;
  p[0] = 0x8040;
  if (!dec_isnan(*x)) return 1;
  p[0] = 0x8020;
  if (!dec_isnan(*x)) return 1;
  p[0] = 0x8010;
  if (!dec_isnan(*x)) return 1;
  p[0] = 0x8008;
  if (!dec_isnan(*x)) return 1;
  p[0] = 0x8004;
  if (!dec_isnan(*x)) return 1;
  p[0] = 0x8002;
  if (!dec_isnan(*x)) return 1;
  p[0] = 0x8001;
  if (!dec_isnan(*x)) return 1;
  p[0] = 0x8000;
  p[1] = 0x8000;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x4000;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x2000;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x1000;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0800;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0400;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0200;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0100;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0080;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0040;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0020;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0010;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0008;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0004;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0002;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0001;
  if (!dec_isnan(*x)) return 1;
  p[1] = 0x0000;
  p[2] = 0x8000;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x4000;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x2000;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x1000;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0800;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0400;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0200;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0100;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0080;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0040;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0020;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0010;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0008;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0004;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0002;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0001;
  if (!dec_isnan(*x)) return 1;
  p[2] = 0x0000;
  p[3] = 0x8000;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x4000;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x2000;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x1000;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0800;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0400;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0200;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0100;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0080;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0040;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0020;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0010;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0008;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0004;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0002;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0001;
  if (!dec_isnan(*x)) return 1;
  p[3] = 0x0000;
  if (!dec_isnan(*x)) return 1;
  /* Zero is defined as a zero sign and zero biased exponent, independent of
   * the significand. However, since a non-zero significand causes an error
   * on Alpha machines, only a zero significand is being checked here. */
  p[0] = 0x0000;
  p[1] = 0x0000;
  p[2] = 0x0000;
  p[3] = 0x0000;
  if ((*x)!=0.0) return 1;
  /* Unity */
  p[0] = 0x4080;
  if ((*x)!=1.0) return 1;
  /* Minus unity */
  p[0] = 0xc080;
  if ((*x)!=-1.0) return 1;
  /* Test the bits in the exponent */
  y = 0.5;
  j = 0;
  for (i = 0; i < 7; i++)
  { p[0] = pc[i];
    for (; j < px[i]; j++) y *= 2.0;
    if (*x != y) return 1;
  }
  y = 0.5;
  j = 0;
  for (i = 0; i < 8; i ++)
  { p[0] = nc[i];
    for (; j < nx[i]; j++) y /= 2.0;
    if (*x != y) return 1;
  }
  /* Test the bits in the significand */
  p[0] = 0x40c0;
  y = 0.5;
  if ((*x) != 1+y) return 1;
  p[0] = 0x40a0;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[0] = 0x4090;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[0] = 0x4088;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[0] = 0x4084;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[0] = 0x4082;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[0] = 0x4081;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[0] = 0x4080;
  p[1] = 0x8000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x4000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x2000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x1000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0800;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0400;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0200;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0100;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0080;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0040;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0020;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0010;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0008;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0004;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0002;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0001;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[1] = 0x0000;
  p[2] = 0x8000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x4000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x2000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x1000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0800;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0400;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0200;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0100;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0080;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0040;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0020;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0010;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0008;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0004;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0002;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0001;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[2] = 0x0000;
  p[3] = 0x8000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x4000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x2000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x1000;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0800;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0400;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0200;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0100;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0080;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0040;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0020;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0010;
  y /= 2;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0008;
  y /= 2;
  if (((*x)) != 1+y) return 1;
  if ((*x) != 1+y) return 1;
  p[3] = 0x0004;
  y /= 2;
  if (((*x)) != 1+y) return 1;
  p[3] = 0x0002;
  y /= 2;
  if (((*x)) != 1+y) return 1;
  p[3] = 0x0001;
  y /= 2;
  if (((*x)) != 1+y) return 1;
  /* No errors */
  return 0;
}
#endif

#ifdef IBMPC
int main(void)
{ int i, j;
  char c[8];
  double* x = (double*)c;
  double y;
  const char pc[2][11] = {{0x40,0x40,0x40,0x40,0x40,0x41,0x42,0x44,0x48,0x50,0x60},
                          {0x00,0x10,0x20,0x40,0x80,0x00,0x00,0x00,0x00,0x00,0x00}};
  const char nc[2][10] = {{0x3f,0x3f,0x3f,0x3f,0x3e,0x3d,0x3b,0x37,0x2f,0x1f},
                          {0xe0,0xd0,0xb0,0x70,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0}};
  const int px[11] = { 1, 2, 3, 5,  9, 17, 33,  65, 129, 257, 513};
  const int nx[10] = { 1, 2, 4, 8, 16, 32, 64, 128, 256, 512};
  /* Infinity */
  c[0] = 0x00;
  c[1] = 0x00;
  c[2] = 0x00;
  c[3] = 0x00;
  c[4] = 0x00;
  c[5] = 0x00;
  c[6] = 0xf0;
  c[7] = 0x7f;
  if (1.0/exp(*x)!=0.0) return 1;
  /* Minus infinity */
  c[7] = 0xff;
  if (exp(*x)!=0.0) return 1;
  /* Any nonzero in c[1.5-7] is NaN */
  c[0] = 0x01;
  if (!isnan(*x)) return 1;
  c[0] = 0x02;
  if (!isnan(*x)) return 1;
  c[0] = 0x04;
  if (!isnan(*x)) return 1;
  c[0] = 0x08;
  if (!isnan(*x)) return 1;
  c[0] = 0x10;
  if (!isnan(*x)) return 1;
  c[0] = 0x20;
  if (!isnan(*x)) return 1;
  c[0] = 0x40;
  if (!isnan(*x)) return 1;
  c[0] = 0x80;
  if (!isnan(*x)) return 1;
  c[0] = 0x00;
  c[1] = 0x01;
  if (!isnan(*x)) return 1;
  c[1] = 0x02;
  if (!isnan(*x)) return 1;
  c[1] = 0x04;
  if (!isnan(*x)) return 1;
  c[1] = 0x08;
  if (!isnan(*x)) return 1;
  c[1] = 0x10;
  if (!isnan(*x)) return 1;
  c[1] = 0x20;
  if (!isnan(*x)) return 1;
  c[1] = 0x40;
  if (!isnan(*x)) return 1;
  c[1] = 0x80;
  if (!isnan(*x)) return 1;
  c[1] = 0x00;
  c[2] = 0x01;
  if (!isnan(*x)) return 1;
  c[2] = 0x02;
  if (!isnan(*x)) return 1;
  c[2] = 0x04;
  if (!isnan(*x)) return 1;
  c[2] = 0x08;
  if (!isnan(*x)) return 1;
  c[2] = 0x10;
  if (!isnan(*x)) return 1;
  c[2] = 0x20;
  if (!isnan(*x)) return 1;
  c[2] = 0x40;
  if (!isnan(*x)) return 1;
  c[2] = 0x80;
  if (!isnan(*x)) return 1;
  c[2] = 0x00;
  c[3] = 0x01;
  if (!isnan(*x)) return 1;
  c[3] = 0x02;
  if (!isnan(*x)) return 1;
  c[3] = 0x04;
  if (!isnan(*x)) return 1;
  c[3] = 0x08;
  if (!isnan(*x)) return 1;
  c[3] = 0x10;
  if (!isnan(*x)) return 1;
  c[3] = 0x20;
  if (!isnan(*x)) return 1;
  c[3] = 0x40;
  if (!isnan(*x)) return 1;
  c[3] = 0x80;
  if (!isnan(*x)) return 1;
  c[3] = 0x00;
  c[4] = 0x01;
  if (!isnan(*x)) return 1;
  c[4] = 0x02;
  if (!isnan(*x)) return 1;
  c[4] = 0x04;
  if (!isnan(*x)) return 1;
  c[4] = 0x08;
  if (!isnan(*x)) return 1;
  c[4] = 0x10;
  if (!isnan(*x)) return 1;
  c[4] = 0x20;
  if (!isnan(*x)) return 1;
  c[4] = 0x40;
  if (!isnan(*x)) return 1;
  c[4] = 0x80;
  if (!isnan(*x)) return 1;
  c[4] = 0x00;
  c[5] = 0x01;
  if (!isnan(*x)) return 1;
  c[5] = 0x02;
  if (!isnan(*x)) return 1;
  c[5] = 0x04;
  if (!isnan(*x)) return 1;
  c[5] = 0x08;
  if (!isnan(*x)) return 1;
  c[5] = 0x10;
  if (!isnan(*x)) return 1;
  c[5] = 0x20;
  if (!isnan(*x)) return 1;
  c[5] = 0x40;
  if (!isnan(*x)) return 1;
  c[5] = 0x80;
  if (!isnan(*x)) return 1;
  c[5] = 0x00;
  c[6] = 0xf1;
  if (!isnan(*x)) return 1;
  c[6] = 0xf2;
  if (!isnan(*x)) return 1;
  c[6] = 0xf4;
  if (!isnan(*x)) return 1;
  c[6] = 0xf8;
  if (!isnan(*x)) return 1;
  c[6] = 0x00;
  /* Zero */
  c[7] = 0x00;
  if ((*x)!=0.0) return 1;
  /* Minus zero */
  c[7] = 0x80;
  if ((*x)!=0.0) return 1;
  /* Unity */
  c[7] = 0x3f;
  c[6] = 0xf0;
  if ((*x)!=1.0) return 1;
  /* Minus unity */
  c[7] = 0xbf;
  if ((*x)!=-1.0) return 1;
  /* Test the bits in the exponent */
  y = 1.0;
  j = 0;
  for (i = 0; i < 11; i++)
  { c[7] = pc[0][i];
    c[6] = pc[1][i];
    for (; j < px[i]; j++) y *= 2.0;
    if (*x != y) return 1;
  }
  y = 1.0;
  j = 0;
  for (i = 0; i < 10; i ++)
  { c[7] = nc[0][i];
    c[6] = nc[1][i];
    for (; j < nx[i]; j++) y /= 2.0;
    if (*x != y) return 1;
  }
  /* Test the bits in the significand */
  c[7] = 0x3f;
  c[6] = 0xf8;
  y = 0.5;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0xf4;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0xf2;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0xf1;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0xf0;
  c[5] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x00;
  c[4] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x00;
  c[3] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x00;
  c[2] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x00;
  c[1] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0x00;
  c[0] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[0] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[0] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[0] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[0] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[0] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[0] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[0] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  /* Test denormals */
  c[7] = 0x00;
  c[6] = 0x08;
  c[0] = 0x00;
  y = 1.0;
  for (i = 0; i < 1023; i++) y/= 2;
  if (*x != y) return 1;
  c[6] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x00;
  c[5] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x00;
  c[4] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x00;
  c[3] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x00;
  c[2] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x00;
  c[1] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x00;
  c[0] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[0] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[0] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[0] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[0] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[0] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[0] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[0] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  /* No errors */
  return 0;
}
#endif

#ifdef MIEEE
int main(void)
{ int i, j;
  char c[8];
  double* x = (double*)c;
  double y;
  const char pc[2][11] = {{0x40,0x40,0x40,0x40,0x40,0x41,0x42,0x44,0x48,0x50,0x60},
                          {0x00,0x10,0x20,0x40,0x80,0x00,0x00,0x00,0x00,0x00,0x00}};
  const char nc[2][10] = {{0x3f,0x3f,0x3f,0x3f,0x3e,0x3d,0x3b,0x37,0x2f,0x1f},
                          {0xe0,0xd0,0xb0,0x70,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0}};
  const int px[11] = { 1, 2, 3, 5,  9, 17, 33,  65, 129, 257, 513};
  const int nx[10] = { 1, 2, 4, 8, 16, 32, 64, 128, 256, 512};
  /* Infinity */
  c[0] = 0x7f;
  c[1] = 0xf0;
  c[2] = 0x00;
  c[3] = 0x00;
  c[4] = 0x00;
  c[5] = 0x00;
  c[6] = 0x00;
  c[7] = 0x00;
  if (1.0/exp(*x)!=0.0) return 1;
  /* Minus infinity */
  c[0] = 0xff;
  if (exp(*x)!=0.0) return 1;
  /* Any nonzero in c[1.5-7] is NaN */
  c[7] = 0x01;
  if (!isnan(*x)) return 1;
  c[7] = 0x02;
  if (!isnan(*x)) return 1;
  c[7] = 0x04;
  if (!isnan(*x)) return 1;
  c[7] = 0x08;
  if (!isnan(*x)) return 1;
  c[7] = 0x10;
  if (!isnan(*x)) return 1;
  c[7] = 0x20;
  if (!isnan(*x)) return 1;
  c[7] = 0x40;
  if (!isnan(*x)) return 1;
  c[7] = 0x80;
  if (!isnan(*x)) return 1;
  c[7] = 0x00;
  c[6] = 0x01;
  if (!isnan(*x)) return 1;
  c[6] = 0x02;
  if (!isnan(*x)) return 1;
  c[6] = 0x04;
  if (!isnan(*x)) return 1;
  c[6] = 0x08;
  if (!isnan(*x)) return 1;
  c[6] = 0x10;
  if (!isnan(*x)) return 1;
  c[6] = 0x20;
  if (!isnan(*x)) return 1;
  c[6] = 0x40;
  if (!isnan(*x)) return 1;
  c[6] = 0x80;
  if (!isnan(*x)) return 1;
  c[6] = 0x00;
  c[5] = 0x01;
  if (!isnan(*x)) return 1;
  c[5] = 0x02;
  if (!isnan(*x)) return 1;
  c[5] = 0x04;
  if (!isnan(*x)) return 1;
  c[5] = 0x08;
  if (!isnan(*x)) return 1;
  c[5] = 0x10;
  if (!isnan(*x)) return 1;
  c[5] = 0x20;
  if (!isnan(*x)) return 1;
  c[5] = 0x40;
  if (!isnan(*x)) return 1;
  c[5] = 0x80;
  if (!isnan(*x)) return 1;
  c[5] = 0x00;
  c[4] = 0x01;
  if (!isnan(*x)) return 1;
  c[4] = 0x02;
  if (!isnan(*x)) return 1;
  c[4] = 0x04;
  if (!isnan(*x)) return 1;
  c[4] = 0x08;
  if (!isnan(*x)) return 1;
  c[4] = 0x10;
  if (!isnan(*x)) return 1;
  c[4] = 0x20;
  if (!isnan(*x)) return 1;
  c[4] = 0x40;
  if (!isnan(*x)) return 1;
  c[4] = 0x80;
  if (!isnan(*x)) return 1;
  c[4] = 0x00;
  c[3] = 0x01;
  if (!isnan(*x)) return 1;
  c[3] = 0x02;
  if (!isnan(*x)) return 1;
  c[3] = 0x04;
  if (!isnan(*x)) return 1;
  c[3] = 0x08;
  if (!isnan(*x)) return 1;
  c[3] = 0x10;
  if (!isnan(*x)) return 1;
  c[3] = 0x20;
  if (!isnan(*x)) return 1;
  c[3] = 0x40;
  if (!isnan(*x)) return 1;
  c[3] = 0x80;
  if (!isnan(*x)) return 1;
  c[3] = 0x00;
  c[2] = 0x01;
  if (!isnan(*x)) return 1;
  c[2] = 0x02;
  if (!isnan(*x)) return 1;
  c[2] = 0x04;
  if (!isnan(*x)) return 1;
  c[2] = 0x08;
  if (!isnan(*x)) return 1;
  c[2] = 0x10;
  if (!isnan(*x)) return 1;
  c[2] = 0x20;
  if (!isnan(*x)) return 1;
  c[2] = 0x40;
  if (!isnan(*x)) return 1;
  c[2] = 0x80;
  if (!isnan(*x)) return 1;
  c[2] = 0x00;
  c[1] = 0xf1;
  if (!isnan(*x)) return 1;
  c[1] = 0xf2;
  if (!isnan(*x)) return 1;
  c[1] = 0xf4;
  if (!isnan(*x)) return 1;
  c[1] = 0xf8;
  if (!isnan(*x)) return 1;
  c[1] = 0x00;
  /* Zero */
  c[0] = 0x00;
  if ((*x)!=0.0) return 1;
  /* Minus zero */
  c[0] = 0x80;
  if ((*x)!=0.0) return 1;
  /* Unity */
  c[0] = 0x3f;
  c[1] = 0xf0;
  if ((*x)!=1.0) return 1;
  /* Minus unity */
  c[0] = 0xbf;
  if ((*x)!=-1.0) return 1;
  /* Test the bits in the exponent */
  y = 1.0;
  j = 0;
  for (i = 0; i < 11; i++)
  { c[0] = pc[0][i];
    c[1] = pc[1][i];
    for (; j < px[i]; j++) y *= 2.0;
    if (*x != y) return 1;
  }
  y = 1.0;
  j = 0;
  for (i = 0; i < 10; i ++)
  { c[0] = nc[0][i];
    c[1] = nc[1][i];
    for (; j < nx[i]; j++) y /= 2.0;
    if (*x != y) return 1;
  }
  /* Test the bits in the significand */
  c[0] = 0x3f;
  c[1] = 0xf8;
  y = 0.5;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0xf4;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0xf2;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0xf1;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[1] = 0xf0;
  c[2] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[2] = 0x00;
  c[3] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[3] = 0x00;
  c[4] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[4] = 0x00;
  c[5] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[5] = 0x00;
  c[6] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[6] = 0x00;
  c[7] = 0x80;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[7] = 0x40;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[7] = 0x20;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[7] = 0x10;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[7] = 0x08;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[7] = 0x04;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[7] = 0x02;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  c[7] = 0x01;
  y /= 2;
  if (((*x)-1.0) != y) return 1;
  /* Test denormals */
  c[0] = 0x00;
  c[1] = 0x08;
  c[7] = 0x00;
  y = 1.0;
  for (i = 0; i < 1023; i++) y/= 2;
  if (*x != y) return 1;
  c[1] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[1] = 0x00;
  c[2] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[2] = 0x00;
  c[3] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[3] = 0x00;
  c[4] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[4] = 0x00;
  c[5] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[5] = 0x00;
  c[6] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  c[6] = 0x00;
  c[7] = 0x80;
  y /= 2;
  if (*x != y) return 1;
  c[7] = 0x40;
  y /= 2;
  if (*x != y) return 1;
  c[7] = 0x20;
  y /= 2;
  if (*x != y) return 1;
  c[7] = 0x10;
  y /= 2;
  if (*x != y) return 1;
  c[7] = 0x08;
  y /= 2;
  if (*x != y) return 1;
  c[7] = 0x04;
  y /= 2;
  if (*x != y) return 1;
  c[7] = 0x02;
  y /= 2;
  if (*x != y) return 1;
  c[7] = 0x01;
  y /= 2;
  if (*x != y) return 1;
  /* No errors */
  return 0;
}
#endif
