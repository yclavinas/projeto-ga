#include "Python.h"
#include "numpy/arrayobject.h"
#include "numpy/ufuncobject.h"
#include "numpy/halffloat.h"
#include "../config.h"

#ifdef HAVE_GAMMA
#define cephesgamma gamma
#endif

/* ========================================================================= */

/* Set up cbrt data */

extern double cbrt(double x);

static void * cbrt_data[] = {NULL, NULL, NULL, NULL};
static char cbrt_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};
static char cbrt_doc[] = "Cube root";

static void long_double_cbrt(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = cbrt((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_cbrt(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = cbrt(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_cbrt(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = cbrt((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_cbrt(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = cbrt(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction cbrt_functions[] = {&half_float_cbrt,
                                                  &float_cbrt,
                                                  &double_cbrt,
                                                  &long_double_cbrt};

/* ========================================================================= */

/* Set up erf data */

extern double erf(double x);

static char erf_doc[] = "Error function";

static void * erf_data[] = {NULL, NULL, NULL, NULL};
static char erf_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_erf(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = erf((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_erf(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = erf(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_erf(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = erf((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_erf(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = erf(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction erf_functions[] = {&half_float_erf,
                                                  &float_erf,
                                                  &double_erf,
                                                  &long_double_erf};

/* ========================================================================= */

/* Set up erfc data */

extern double erfc(double x);

static char erfc_doc[] = "Complementary error function";

static void * erfc_data[] = {NULL, NULL, NULL, NULL};
static char erfc_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_erfc(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = erfc((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_erfc(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = erfc(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_erfc(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = erfc((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_erfc(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = erfc(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction erfc_functions[] = {&half_float_erfc,
                                                  &float_erfc,
                                                  &double_erfc,
                                                  &long_double_erfc};


/* ========================================================================= */

/* Set up ndtr data */

extern double ndtr(double x);

static char ndtr_doc[] = "Cumulative standard normal distribution";

static void * ndtr_data[] = {NULL, NULL, NULL, NULL};
static char ndtr_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_ndtr(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = ndtr((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_ndtr(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = ndtr(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_ndtr(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = ndtr((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_ndtr(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = ndtr(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction ndtr_functions[] = {&half_float_ndtr,
                                                  &float_ndtr,
                                                  &double_ndtr,
                                                  &long_double_ndtr};

/* ========================================================================= */

/* Set up ndtri data */

extern double ndtri(double x);

static char ndtri_doc[] = "Inverse of the cumulative normal distribution";

static void * ndtri_data[] = {NULL, NULL, NULL, NULL};
static char ndtri_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_ndtri(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = ndtri((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_ndtri(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = ndtri(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_ndtri(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = ndtri((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_ndtri(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = ndtri(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction ndtri_functions[] = {&half_float_ndtri,
                                                  &float_ndtri,
                                                  &double_ndtri,
                                                  &long_double_ndtri};

/* ========================================================================= */

/* Set up dawsn data */

extern double dawsn(double x);

static char dawsn_doc[] = "Dawson's integral";

static void * dawsn_data[] = {NULL, NULL, NULL, NULL};
static char dawsn_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_dawsn(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = dawsn((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_dawsn(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = dawsn(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_dawsn(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = dawsn((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_dawsn(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = dawsn(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction dawsn_functions[] = {&half_float_dawsn,
                                                  &float_dawsn,
                                                  &double_dawsn,
                                                  &long_double_dawsn};

/* ========================================================================= */

/* Set up gamma data */

extern double cephesgamma(double x);

static char gamma_doc[] = "Gamma function";

static void * gamma_data[] = {NULL, NULL, NULL, NULL};
static char gamma_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_gamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = cephesgamma((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_gamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = cephesgamma(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_gamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = cephesgamma((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_gamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = cephesgamma(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction gamma_functions[] = {&half_float_gamma,
                                                  &float_gamma,
                                                  &double_gamma,
                                                  &long_double_gamma};

/* ========================================================================= */

/* Set up lgamma data */

extern double lgamma(double x);

static char lgamma_doc[] = "Natural logarithm of gamma function";

static void * lgamma_data[] = {NULL, NULL, NULL, NULL};
static char lgamma_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_lgamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = lgamma((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_lgamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = lgamma(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_lgamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = lgamma((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_lgamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = lgamma(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction lgamma_functions[] = {&half_float_lgamma,
                                                  &float_lgamma,
                                                  &double_lgamma,
                                                  &long_double_lgamma};

/* ========================================================================= */

/* Set up rgamma data  */

extern double rgamma(double x);

static char rgamma_doc[] = "Reciprocal gamma function";

static void * rgamma_data[] = {NULL, NULL, NULL, NULL};
static char rgamma_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_rgamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = rgamma((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_rgamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = rgamma(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_rgamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = rgamma((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_rgamma(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = rgamma(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction rgamma_functions[] = {&half_float_rgamma,
                                                  &float_rgamma,
                                                  &double_rgamma,
                                                  &long_double_rgamma};

/* ========================================================================= */

/* Set up psi data  */

extern double psi(double x);

static char psi_doc[] = "Psi (digamma) function";

static void * psi_data[] = {NULL, NULL, NULL, NULL};
static char psi_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_psi(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = psi((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_psi(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = psi(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_psi(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = psi((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_psi(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = psi(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction psi_functions[] = {&half_float_psi,
                                                  &float_psi,
                                                  &double_psi,
                                                  &long_double_psi};

/* ========================================================================= */

/* Set up j0 data */

extern double j0(double x);

static char j0_doc[] = "Bessel function of order zero";

static void * j0_data[] = {NULL, NULL, NULL, NULL};
static char j0_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_j0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = j0((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_j0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = j0(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_j0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = j0((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_j0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = j0(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction j0_functions[] = {&half_float_j0,
                                                  &float_j0,
                                                  &double_j0,
                                                  &long_double_j0};


/* ========================================================================= */

/* Set up y0 data */

extern double y0(double x);

static char y0_doc[] = "Bessel function of the second kind, order zero";

static void * y0_data[] = {NULL, NULL, NULL, NULL};
static char y0_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_y0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = y0((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_y0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = y0(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_y0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = y0((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_y0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = y0(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction y0_functions[] = {&half_float_y0,
                                                  &float_y0,
                                                  &double_y0,
                                                  &long_double_y0};


/* ========================================================================= */

/* Set up i0 data */

extern double i0(double x);

static char i0_doc[] = "Modified Bessel function of order zero";

static void * i0_data[] = {NULL, NULL, NULL, NULL};
static char i0_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_i0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = i0((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_i0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = i0(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_i0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = i0((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_i0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = i0(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction i0_functions[] = {&half_float_i0,
                                                  &float_i0,
                                                  &double_i0,
                                                  &long_double_i0};


/* ========================================================================= */

/* Set up i0e data */

extern double i0e(double x);

static char i0e_doc[] =
  "Modified Bessel function of order zero, exponentially scaled";

static void * i0e_data[] = {NULL, NULL, NULL, NULL};
static char i0e_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_i0e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = i0e((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_i0e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = i0e(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_i0e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = i0e((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_i0e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = i0e(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction i0e_functions[] = {&half_float_i0e,
                                                  &float_i0e,
                                                  &double_i0e,
                                                  &long_double_i0e};

/* ========================================================================= */

/* Set up k0 data */

extern double k0(double x);

static char k0_doc[] = "Modified Bessel function, third kind, order zero";

static void * k0_data[] = {NULL, NULL, NULL, NULL};
static char k0_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_k0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = k0((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_k0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = k0(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_k0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = k0((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_k0(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = k0(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction k0_functions[] = {&half_float_k0,
                                                  &float_k0,
                                                  &double_k0,
                                                  &long_double_k0};


/* ========================================================================= */

/* Set up k0e data */

extern double k0e(double x);

static char k0e_doc[] =
  "Modified Bessel function, third kind, order zero, exponentially scaled";

static void * k0e_data[] = {NULL, NULL, NULL, NULL};
static char k0e_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_k0e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = k0e((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_k0e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = k0e(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_k0e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = k0e((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_k0e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = k0e(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction k0e_functions[] = {&half_float_k0e,
                                                  &float_k0e,
                                                  &double_k0e,
                                                  &long_double_k0e};


/* ========================================================================= */

/* Set up j1 data */

extern double j1(double x);

static char j1_doc[] = "Bessel function of order one";

static void * j1_data[] = {NULL, NULL, NULL, NULL};
static char j1_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_j1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = j1((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_j1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = j1(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_j1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = j1((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_j1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = j1(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction j1_functions[] = {&half_float_j1,
                                                  &float_j1,
                                                  &double_j1,
                                                  &long_double_j1};


/* ========================================================================= */

/* Set up y1 data */

extern double y1(double x);

static char y1_doc[] = "Bessel function of the second kind, order one";

static void * y1_data[] = {NULL, NULL, NULL, NULL};
static char y1_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_y1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = y1((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_y1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = y1(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_y1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = y1((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_y1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = y1(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction y1_functions[] = {&half_float_y1,
                                                  &float_y1,
                                                  &double_y1,
                                                  &long_double_y1};


/* ========================================================================= */

/* Set up i1 data */

extern double i1(double x);

static char i1_doc[] = "Modified Bessel function of order one";

static void * i1_data[] = {NULL, NULL, NULL, NULL};
static char i1_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_i1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = i1((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_i1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = i1(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_i1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = i1((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_i1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = i1(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction i1_functions[] = {&half_float_i1,
                                                  &float_i1,
                                                  &double_i1,
                                                  &long_double_i1};


/* ========================================================================= */

/* Set up i1e data */

extern double i1e(double x);

static char i1e_doc[] =
  "Modified Bessel function of order one, exponentially scaled";

static void * i1e_data[] = {NULL, NULL, NULL, NULL};
static char i1e_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_i1e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = i1e((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_i1e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = i1e(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_i1e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = i1e((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_i1e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = i1e(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction i1e_functions[] = {&half_float_i1e,
                                                  &float_i1e,
                                                  &double_i1e,
                                                  &long_double_i1e};


/* ========================================================================= */

/* Set up k1 data */

extern double k1(double x);

static char k1_doc[] = "Modified Bessel function, third kind, order one";

static void * k1_data[] = {NULL, NULL, NULL, NULL};
static char k1_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_k1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = k1((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_k1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = k1(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_k1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = k1((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_k1(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = k1(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction k1_functions[] = {&half_float_k1,
                                                  &float_k1,
                                                  &double_k1,
                                                  &long_double_k1};


/* ========================================================================= */

/* Set up k1e data */

extern double k1e(double x);

static char k1e_doc[] =
  "Modified Bessel function, third kind, order one, exponentially scaled";

static void * k1e_data[] = {NULL, NULL, NULL, NULL};
static char k1e_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_k1e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = k1e((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_k1e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = k1e(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_k1e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = k1e((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_k1e(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = k1e(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction k1e_functions[] = {&half_float_k1e,
                                                  &float_k1e,
                                                  &double_k1e,
                                                  &long_double_k1e};

/* ========================================================================= */

/* Set up ellpe data */

extern double ellpe(double x);

static char ellpe_doc[] =
  "Complete elliptic integral of the second kind";

static void * ellpe_data[] = {NULL, NULL, NULL, NULL};
static char ellpe_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_ellpe(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = ellpe((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_ellpe(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = ellpe(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_ellpe(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = ellpe((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_ellpe(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = ellpe(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction ellpe_functions[] = {&half_float_ellpe,
                                                  &float_ellpe,
                                                  &double_ellpe,
                                                  &long_double_ellpe};

/* ========================================================================= */

/* Set up ellpk data */

extern double ellpk(double m1);

static char ellpk_doc[] =
  "Complete elliptic integral of the first kind";

static void * ellpk_data[] = {NULL, NULL, NULL, NULL};
static char ellpk_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_ellpk(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = ellpk((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_ellpk(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = ellpk(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_ellpk(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = ellpk((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_ellpk(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = ellpk(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction ellpk_functions[] = {&half_float_ellpk,
                                                  &float_ellpk,
                                                  &double_ellpk,
                                                  &long_double_ellpk};

/* ========================================================================= */

/* Set up spence data */

extern double spence(double x);

static char spence_doc[] = "Dilogarithm";

static void * spence_data[] = {NULL, NULL, NULL, NULL};
static char spence_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_spence(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = spence((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_spence(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = spence(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_spence(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = spence((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_spence(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = spence(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction spence_functions[] = {&half_float_spence,
                                                  &float_spence,
                                                  &double_spence,
                                                  &long_double_spence};

/* ========================================================================= */

/* Set up zetac data */

extern double zetac(double x);

static char zetac_doc[] = "Riemann zeta function";

static void * zetac_data[] = {NULL, NULL, NULL, NULL};
static char zetac_types[8] = {NPY_HALF, NPY_HALF,
                             NPY_FLOAT, NPY_FLOAT,
                             NPY_DOUBLE,NPY_DOUBLE,
                             NPY_LONGDOUBLE, NPY_LONGDOUBLE};

static void long_double_zetac(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    long double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(long double*)in;
        *((long double*)out) = zetac((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void double_zetac(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = *(double*)in;
        *((double*)out) = zetac(tmp);
        in += in_step;
        out += out_step;
    }
}

static void float_zetac(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    float tmp;

    for (i = 0; i < n; i++) {
        tmp = *(float*)in;
        *((float*)out) = zetac((double)tmp);
        in += in_step;
        out += out_step;
    }
}

static void half_float_zetac(char** args, npy_intp* dimensions, npy_intp* steps, void* data)
{
    npy_intp i;
    npy_intp n = dimensions[0];
    char* in = args[0];
    char* out = args[1];
    npy_intp in_step = steps[0];
    npy_intp out_step = steps[1];
    double tmp;

    for (i = 0; i < n; i++) {
        tmp = npy_half_to_double(*(npy_half*)in);
        tmp = zetac(tmp);
        *((npy_half*)out) = npy_double_to_half(tmp);
        in += in_step;
        out += out_step;
    }
}

static PyUFuncGenericFunction zetac_functions[] = {&half_float_zetac,
                                                  &float_zetac,
                                                  &double_zetac,
                                                  &long_double_zetac};

/* ========================================================================= */

/* fac */

extern double fac(int i);

static char fac__doc__[] = "Factorial function";

static PyObject* transcendental_fac (PyObject* unused, PyObject* args)
{ double result;
  int i;
  if(!PyArg_ParseTuple(args, "i", &i)) return NULL;
  result = fac(i);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* bdtr */

extern double bdtr(int k, int n, double p);

static char bdtr__doc__[] = "Cumulative binomial probability density";

static PyObject* transcendental_bdtr (PyObject* unused, PyObject* args)
{ double result;
  int k;
  int n;
  double p;
  if(!PyArg_ParseTuple(args, "iid", &k, &n, &p)) return NULL;
  result = bdtr(k, n, p);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* bdtrc */

extern double bdtrc(int k, int n, double p);

static char bdtrc__doc__[] = "Complemented binomial distribution";

static PyObject* transcendental_bdtrc (PyObject* unused, PyObject* args)
{ double result;
  int k;
  int n;
  double p;
  if(!PyArg_ParseTuple(args, "iid", &k, &n, &p)) return NULL;
  result = bdtrc(k, n, p);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* bdtri */

extern double bdtri(int k, int n, double y);

static char bdtri__doc__[] = "Inverse binomial distribution";

static PyObject* transcendental_bdtri (PyObject* unused, PyObject* args)
{ double result;
  int k;
  int n;
  double y;
  if(!PyArg_ParseTuple(args, "iid", &k, &n, &y)) return NULL;
  result = bdtri(k, n, y);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* nbdtr */

extern double nbdtr(int k, int n, double p);

static char nbdtr__doc__[] = "Cumulative negative binomial probability density";

static PyObject* transcendental_nbdtr (PyObject* unused, PyObject* args)
{ double result;
  int k;
  int n;
  double p;
  if(!PyArg_ParseTuple(args, "iid", &k, &n, &p)) return NULL;
  result = nbdtr(k, n, p);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* nbdtrc */

extern double nbdtrc(int k, int n, double p);

static char nbdtrc__doc__[] =
"Complemented cumulative negative binomial distribution";

static PyObject* transcendental_nbdtrc (PyObject* unused, PyObject* args)
{ double result;
  int k;
  int n;
  double p;
  if(!PyArg_ParseTuple(args, "iid", &k, &n, &p)) return NULL;
  result = nbdtrc(k, n, p);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* nbdtri */

extern double nbdtri(int k, int n, double p);

static char nbdtri__doc__[] =
"Inverse of the cumulative negative binomial distribution";

static PyObject* transcendental_nbdtri (PyObject* unused, PyObject* args)
{ double result;
  int k;
  int n;
  double y;
  if(!PyArg_ParseTuple(args, "iid", &k, &n, &y)) return NULL;
  result = nbdtri(k, n, y);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* gdtr */

extern double gdtr(double a, double b, double x);

static char gdtr__doc__[] = "Cumulative gamma probability density";

static PyObject* transcendental_gdtr (PyObject* unused, PyObject* args)
{ double result;
  double a;
  double b;
  double x;
  if(!PyArg_ParseTuple(args, "ddd", &a, &b, &x)) return NULL;
  result = gdtr(a, b, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* gdtrc */

static char gdtrc__doc__[] =
"Complemented cumulative gamma distribution function";

extern double gdtrc(double a, double b, double x);

static PyObject* transcendental_gdtrc (PyObject* unused, PyObject* args)
{ double result;
  double a;
  double b;
  double x;
  if(!PyArg_ParseTuple(args, "ddd", &a, &b, &x)) return NULL;
  result = gdtrc(a, b, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* pdtr */

static char pdtr__doc__[] = "Cumulative Poisson distribution";

extern double pdtr(int k, double m);

static PyObject* transcendental_pdtr (PyObject* unused, PyObject* args)
{ double result;
  int k;
  double m;
  if(!PyArg_ParseTuple(args, "id", &k, &m)) return NULL;
  result = pdtr(k, m);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* pdtrc */

static char pdtrc__doc__[] = "Complemented cumulative Poisson distribution";

extern double pdtrc(int k, double m);

static PyObject* transcendental_pdtrc (PyObject* unused, PyObject* args)
{ double result;
  int k;
  double m;
  if(!PyArg_ParseTuple(args, "id", &k, &m)) return NULL;
  result = pdtrc(k, m);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* pdtri */

static char pdtri__doc__[] = "Inverse of the cumulative Poisson distribution";

extern double pdtri(int k, double y);

static PyObject* transcendental_pdtri (PyObject* unused, PyObject* args)
{ double result;
  int k;
  double y;
  if(!PyArg_ParseTuple(args, "id", &k, &y)) return NULL;
  result = pdtri(k, y);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* beta */

static char beta__doc__[] = "Beta function";

extern double beta(double a, double b);

static PyObject* transcendental_beta (PyObject* unused, PyObject* args)
{ double result;
  double a;
  double b;
  if(!PyArg_ParseTuple(args, "dd", &a, &b)) return NULL;
  result = beta(a, b);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* igam */

static char igam__doc__[] = "Incomplete gamma integral";

extern double igam(double a, double x);

static PyObject* transcendental_igam (PyObject* unused, PyObject* args)
{ double result;
  double x;
  double a;
  if(!PyArg_ParseTuple(args, "dd", &a, &x)) return NULL;
  result = igam(a, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* igamc */

static char igamc__doc__[] = "Complemented incomplete gamma integral";

extern double igamc(double a, double x);

static PyObject* transcendental_igamc (PyObject* unused, PyObject* args)
{ double result;
  double x;
  double a;
  if(!PyArg_ParseTuple(args, "dd", &a, &x)) return NULL;
  result = igamc(a, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* igami */

static char igami__doc__[] =
"Inverse of the complemented incomplete gamma integral";

extern double igami(double a, double p);

static PyObject* transcendental_igami (PyObject* unused, PyObject* args)
{ double result;
  double p;
  double a;
  if(!PyArg_ParseTuple(args, "dd", &a, &p)) return NULL;
  result = igami(a, p);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* incbet */

static char incbet__doc__[] = "Incomplete beta integral";

extern double incbet(double a, double b, double x);

static PyObject* transcendental_incbet (PyObject* unused, PyObject* args)
{ double result;
  double a;
  double b;
  double x;
  if(!PyArg_ParseTuple(args, "ddd", &a, &b, &x)) return NULL;
  result = incbet(a, b, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* incbi */

static char incbi__doc__[] = "Inverse of the incomplete beta integral";

extern double incbi(double a, double b, double y);

static PyObject* transcendental_incbi (PyObject* unused, PyObject* args)
{ double result;
  double a;
  double b;
  double y;
  if(!PyArg_ParseTuple(args, "ddd", &a, &b, &y)) return NULL;
  result = incbi(a, b, y);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* fresnl */

static char fresnl__doc__[] = "Fresnel cosine and sine integrals";

extern double fresnl(double x, double* c, double* s);

static PyObject* transcendental_fresnl (PyObject* unused, PyObject* args)
{ double s;
  double c;
  double x;
  if(!PyArg_ParseTuple(args, "d", &x)) return NULL;
  fresnl(x, &s, &c);
  return Py_BuildValue("dd", s, c);
}

/* ========================================================================= */

/* stdtr */

static char stdtr__doc__[] = "Cumulative Student's t distribution";

extern double stdtr(int k, double t);

static PyObject* transcendental_stdtr (PyObject* unused, PyObject* args)
{ double result;
  double t;
  int k;
  if(!PyArg_ParseTuple(args, "id", &k, &t)) return NULL;
  result = stdtr(k, t);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* stdtri */

static char stdtri__doc__[] =
"Inverse of the cumulative Student's t distribution";

extern double stdtri(int k, double t);

static PyObject* transcendental_stdtri (PyObject* unused, PyObject* args)
{ double result;
  double t;
  int k;
  if(!PyArg_ParseTuple(args, "id", &k, &t)) return NULL;
  result = stdtri(k, t);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* chdtr */

static char chdtr__doc__[] = "Cumulative chi square distribution";

extern double chdtr(double nu, double x);

static PyObject* transcendental_chdtr (PyObject* unused, PyObject* args)
{ double result;
  double x;
  double nu;
  if(!PyArg_ParseTuple(args, "dd", &nu, &x)) return NULL;
  result = chdtr(nu, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* chdtrc */

static char chdtrc__doc__[] = "Complemented cumulative chi square distribution";

extern double chdtrc(double nu, double x);

static PyObject* transcendental_chdtrc (PyObject* unused, PyObject* args)
{ double result;
  double x;
  double nu;
  if(!PyArg_ParseTuple(args, "dd", &nu, &x)) return NULL;
  result = chdtrc(nu, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* chdtri */

static char chdtri__doc__[] =
"Inverse of the complemented cumulative chi square distribution.";

extern double chdtri(double nu, double y);

static PyObject* transcendental_chdtri (PyObject* unused, PyObject* args)
{ double result;
  double y;
  double nu;
  if(!PyArg_ParseTuple(args, "dd", &nu, &y)) return NULL;
  result = chdtri(nu, y);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* fdtr */

static char fdtr__doc__[] = "Cumulative F distribution";

extern double fdtr(int nu1, int nu2, double x);

static PyObject* transcendental_fdtr (PyObject* unused, PyObject* args)
{ double result;
  double x;
  int nu1, nu2;
  if(!PyArg_ParseTuple(args, "iid", &nu1, &nu2, &x)) return NULL;
  result = fdtr(nu1, nu2, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* fdtrc */

static char fdtrc__doc__[] = "Complemented cumulative F distribution";

extern double fdtrc(int nu1, int nu2, double x);

static PyObject* transcendental_fdtrc (PyObject* unused, PyObject* args)
{ double result;
  double x;
  int nu1, nu2;
  if(!PyArg_ParseTuple(args, "iid", &nu1, &nu2, &x)) return NULL;
  result = fdtrc(nu1, nu2, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* fdtri */

static char fdtri__doc__[] =
"Inverse of the complemented cumulative F distribution";

extern double fdtri(int nu1, int nu2, double x);

static PyObject* transcendental_fdtri (PyObject* unused, PyObject* args)
{ double result;
  double x;
  int nu1, nu2;
  if(!PyArg_ParseTuple(args, "iid", &nu1, &nu2, &x)) return NULL;
  result = fdtri(nu1, nu2, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* jn */

static char jn__doc__[] = "Bessel function of integer order";

extern double jn(int n,  double x);

static PyObject* transcendental_jn (PyObject* unused, PyObject* args)
{ double result;
  int n;
  double x;
  if(!PyArg_ParseTuple(args, "id", &n, &x)) return NULL;
  result = jn(n, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* jv */

static char jv__doc__[] = "Bessel function of noninteger order";

extern double jv(double v,  double x);

static PyObject* transcendental_jv (PyObject* unused, PyObject* args)
{ double result;
  double v;
  double x;
  if(!PyArg_ParseTuple(args, "dd", &v, &x)) return NULL;
  result = jv(v, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* yn */

static char yn__doc__[] = "Bessel function of second kind of integer order";

extern double yn(int n,  double x);

static PyObject* transcendental_yn (PyObject* unused, PyObject* args)
{ double result;
  int n;
  double x;
  if(!PyArg_ParseTuple(args, "id", &n, &x)) return NULL;
  result = yn(n, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* yv */

static char yv__doc__[] = "Bessel function of second kind of noninteger order";

extern double yv(double v,  double x);

static PyObject* transcendental_yv (PyObject* unused, PyObject* args)
{ double result;
  double v;
  double x;
  if(!PyArg_ParseTuple(args, "dd", &v, &x)) return NULL;
  result = yv(v, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* iv */

static char iv__doc__[] = "Modified Bessel function of noninteger order";

extern double iv(double v,  double x);

static PyObject* transcendental_iv (PyObject* unused, PyObject* args)
{ double result;
  double v;
  double x;
  if(!PyArg_ParseTuple(args, "dd", &v, &x)) return NULL;
  result = iv(v, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* kn */

static char kn__doc__[] =
  "Modified Bessel function, third kind, integer order";

extern double kn(int n,  double x);

static PyObject* transcendental_kn (PyObject* unused, PyObject* args)
{ double result;
  int n;
  double x;
  if(!PyArg_ParseTuple(args, "id", &n, &x)) return NULL;
  result = kn(n, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* airy */

static char airy__doc__[] = "Airy function";

extern int airy(double x, double* ai, double* aip, double* bi, double* bip);

static PyObject* transcendental_airy (PyObject* unused, PyObject* args)
{ int errorcode;
  double x;
  double ai, aip, bi, bip;
  if(!PyArg_ParseTuple(args, "d", &x)) return NULL;
  errorcode = airy(x,&ai,&aip,&bi,&bip);
  if (errorcode<0)
  { PyObject* error =
      PyString_FromString("WARNING: Argument larger than MAXAIRY in airy\n");
    if (error!=NULL)
    { PyObject_Print(error, stdout, Py_PRINT_RAW);
      Py_DECREF(error);
    }
  }
  return Py_BuildValue("dddd", ai, aip, bi, bip);
}

/* ======================================================================== */

/* expn */

static char expn__doc__[] = "Exponential integral En";

extern double expn(int n,  double x);

static PyObject* transcendental_expn (PyObject* unused, PyObject* args)
{ double result;
  int n;
  double x;
  if(!PyArg_ParseTuple(args, "id", &n, &x)) return NULL;
  result = expn(n, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* shichi */

static char shichi__doc__[] = "Hyperbolic sine and cosine integrals";

extern int shichi(double x, double* Chi, double* Shi);

static PyObject* transcendental_shichi (PyObject* unused, PyObject* args)
{ double x;
  double Chi, Shi;
  if(!PyArg_ParseTuple(args, "d", &x)) return NULL;
  shichi(x,&Chi,&Shi);
  return Py_BuildValue("dd", Chi, Shi);
}

/* ======================================================================== */

/* sici */

static char sici__doc__[] = "Sine and cosine integrals";

extern int sici(double x, double* Si, double* Ci);

static PyObject* transcendental_sici (PyObject* unused, PyObject* args)
{ double x;
  double Ci, Si;
  if(!PyArg_ParseTuple(args, "d", &x)) return NULL;
  sici(x,&Ci,&Si);
  return Py_BuildValue("dd", Ci, Si);
}

/* ========================================================================= */

/* hyperg */

extern double hyperg(double a, double b, double x);

static char hyperg__doc__[] = "Confluent hypergeometric function";

static PyObject* transcendental_hyperg (PyObject* unused, PyObject* args)
{ double result;
  double a, b, x;
  if(!PyArg_ParseTuple(args, "ddd", &a, &b, &x)) return NULL;
  result = hyperg(a, b, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* hyp2f1 */

extern double hyp2f1(double a, double b, double c, double x);

static char hyp2f1__doc__[] = "Gauss hypergeometric function";

static PyObject* transcendental_hyp2f1 (PyObject* unused, PyObject* args)
{ double result;
  double a, b, c, x;
  if(!PyArg_ParseTuple(args, "dddd", &a, &b, &c, &x)) return NULL;
  result = hyp2f1(a, b, c, x);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* ellik */

extern double ellik(double phi, double m);

static char ellik__doc__[] = "Incomplete elliptic integral of the first kind";

static PyObject* transcendental_ellik (PyObject* unused, PyObject* args)
{ double result;
  double phi, m;
  if(!PyArg_ParseTuple(args, "dd", &phi, &m)) return NULL;
  result = ellik(phi, m);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* ellie */

extern double ellie(double phi, double m);

static char ellie__doc__[] = "Incomplete elliptic integral of the second kind";

static PyObject* transcendental_ellie (PyObject* unused, PyObject* args)
{ double result;
  double phi, m;
  if(!PyArg_ParseTuple(args, "dd", &phi, &m)) return NULL;
  result = ellie(phi, m);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */

/* ellpj */

static char ellpj__doc__[] = "Jacobian Elliptic Functions";

extern int ellpj(double x, double m,
                 double* sn, double* cn, double* dn, double* phi);

static PyObject* transcendental_ellpj (PyObject* unused, PyObject* args)
{ int errorcode;
  double u, m;
  double sn, cn, dn, phi;
  if(!PyArg_ParseTuple(args, "dd", &u, &m)) return NULL;
  errorcode = ellpj(u,m,&sn,&cn,&dn,&phi);
  if (errorcode<0)
  { PyObject* error =
      PyString_FromString("WARNING: Error occurred in ellpj\n");
    if (error!=NULL)
    { PyObject_Print(error, stdout, Py_PRINT_RAW);
      Py_DECREF(error);
    }
  }
  return Py_BuildValue("dddd", sn, cn, dn, phi);
}

/* ========================================================================= */

/* zeta */

extern double zeta(double x, double q);

static char zeta__doc__[] = "Riemann zeta function of two arguments";

static PyObject* transcendental_zeta (PyObject* unused, PyObject* args)
{ double result;
  double x, q;
  if(!PyArg_ParseTuple(args, "dd", &x, &q)) return NULL;
  result = zeta(x, q);
  return Py_BuildValue("d",result);
}

/* ========================================================================= */

/* struve */

extern double struve(double v, double x);

static char struve__doc__[] = "Struve function";

static PyObject* transcendental_struve (PyObject* unused, PyObject* args)
{ double result;
  double v, x;
  if(!PyArg_ParseTuple(args, "dd", &v, &x)) return NULL;
  result = struve(v, x);
  return Py_BuildValue("d",result);
}

/* ======================================================================== */
/* ======================================================================== */
/* Methods table                                                            */
/* ======================================================================== */
/* ======================================================================== */

static struct PyMethodDef methods[] =
{ {"fdtr", (PyCFunction) transcendental_fdtr, METH_VARARGS, fdtr__doc__},
  {"fdtrc", (PyCFunction) transcendental_fdtrc, METH_VARARGS, fdtrc__doc__},
  {"fdtri", (PyCFunction) transcendental_fdtri, METH_VARARGS, fdtri__doc__},
  {"chdtr", (PyCFunction) transcendental_chdtr, METH_VARARGS, chdtr__doc__},
  {"chdtrc", (PyCFunction) transcendental_chdtrc, METH_VARARGS, chdtrc__doc__},
  {"chdtri", (PyCFunction) transcendental_chdtri, METH_VARARGS, chdtri__doc__},
  {"pdtr", (PyCFunction) transcendental_pdtr, METH_VARARGS, pdtr__doc__},
  {"pdtrc", (PyCFunction) transcendental_pdtrc, METH_VARARGS, pdtrc__doc__},
  {"pdtri", (PyCFunction) transcendental_pdtri, METH_VARARGS, pdtri__doc__},
  {"bdtr", (PyCFunction) transcendental_bdtr, METH_VARARGS, bdtr__doc__},
  {"bdtrc", (PyCFunction) transcendental_bdtrc, METH_VARARGS, bdtrc__doc__},
  {"bdtri", (PyCFunction) transcendental_bdtri, METH_VARARGS, bdtri__doc__},
  {"nbdtr", (PyCFunction) transcendental_nbdtr, METH_VARARGS, nbdtr__doc__},
  {"nbdtrc", (PyCFunction) transcendental_nbdtrc, METH_VARARGS, nbdtrc__doc__},
  {"nbdtri", (PyCFunction) transcendental_nbdtri, METH_VARARGS, nbdtri__doc__},
  {"gdtr", (PyCFunction) transcendental_gdtr, METH_VARARGS, gdtr__doc__},
  {"gdtrc", (PyCFunction) transcendental_gdtrc, METH_VARARGS, gdtrc__doc__},
  {"stdtr", (PyCFunction) transcendental_stdtr, METH_VARARGS, stdtr__doc__},
  {"stdtri", (PyCFunction) transcendental_stdtri, METH_VARARGS, stdtri__doc__},
  {"fac", (PyCFunction) transcendental_fac, METH_VARARGS, fac__doc__},
  {"beta", (PyCFunction) transcendental_beta, METH_VARARGS, beta__doc__},
  {"igam", (PyCFunction) transcendental_igam, METH_VARARGS, igam__doc__},
  {"igamc", (PyCFunction) transcendental_igamc, METH_VARARGS, igamc__doc__},
  {"igami", (PyCFunction) transcendental_igami, METH_VARARGS, igami__doc__},
  {"incbet", (PyCFunction) transcendental_incbet, METH_VARARGS, incbet__doc__},
  {"incbi", (PyCFunction) transcendental_incbi, METH_VARARGS, incbi__doc__},
  {"fresnl", (PyCFunction) transcendental_fresnl, METH_VARARGS, fresnl__doc__},
  {"jn", (PyCFunction) transcendental_jn, METH_VARARGS, jn__doc__},
  {"jv", (PyCFunction) transcendental_jv, METH_VARARGS, jv__doc__},
  {"yn", (PyCFunction) transcendental_yn, METH_VARARGS, yn__doc__},
  {"yv", (PyCFunction) transcendental_yv, METH_VARARGS, yv__doc__},
  {"iv", (PyCFunction) transcendental_iv, METH_VARARGS, iv__doc__},
  {"kn", (PyCFunction) transcendental_kn, METH_VARARGS, kn__doc__},
  {"airy", (PyCFunction) transcendental_airy, METH_VARARGS, airy__doc__},
  {"expn", (PyCFunction) transcendental_expn, METH_VARARGS, expn__doc__},
  {"shichi", (PyCFunction) transcendental_shichi, METH_VARARGS, shichi__doc__},
  {"sici", (PyCFunction) transcendental_sici, METH_VARARGS, sici__doc__},
  {"hyperg", (PyCFunction) transcendental_hyperg, METH_VARARGS, hyperg__doc__},
  {"hyp2f1", (PyCFunction) transcendental_hyp2f1, METH_VARARGS, hyp2f1__doc__},
  {"ellik", (PyCFunction) transcendental_ellik, METH_VARARGS, ellik__doc__},
  {"ellie", (PyCFunction) transcendental_ellie, METH_VARARGS, ellie__doc__},
  {"ellpj", (PyCFunction) transcendental_ellpj, METH_VARARGS, ellpj__doc__},
  {"zeta", (PyCFunction) transcendental_zeta, METH_VARARGS, zeta__doc__},
  {"struve", (PyCFunction) transcendental_struve, METH_VARARGS, struve__doc__},
  {NULL, NULL, 0, NULL}
};

/* ========================================================================= */

#if defined(INFINITY) || defined(HUGE_VAL)
extern double CEPHESINFINITY;
#endif

static char transcendental_module_documentation[] =
"Transcendental functions for Python";

void init_transcendental(void) {
  PyObject *m, *d, *f;

  /* Import the array and ufunc objects */
  import_array();
  import_ufunc();

  /* CEPHESINFINITY has to be set inside a function if HUGE_VAL is used */ 
#ifdef INFINITY
  CEPHESINFINITY = INFINITY;
#else
#ifdef HUGE_VAL
  CEPHESINFINITY = HUGE_VAL;
#endif
#endif
 
  /* Create the module and add the functions */
  m = Py_InitModule4("_transcendental",
                     methods,
		     transcendental_module_documentation,
		     (PyObject*)NULL,
		     PYTHON_API_VERSION); 
  d = PyModule_GetDict(m);

  f = PyUFunc_FromFuncAndData(cbrt_functions,
                              cbrt_data,
                              cbrt_types, 
                              4, 1, 1, PyUFunc_None,
		              "cbrt", cbrt_doc, 0);
  PyDict_SetItemString(d, "cbrt", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(erf_functions,
                              erf_data,
                              erf_types, 
                              4, 1, 1, PyUFunc_None,
		              "erf", erf_doc, 1);
  PyDict_SetItemString(d, "erf", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(erfc_functions,
                              erfc_data,
                              erfc_types, 
                              4, 1, 1, PyUFunc_None,
		              "erfc", erfc_doc, 1);
  PyDict_SetItemString(d, "erfc", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(ndtr_functions,
                              ndtr_data,
                              ndtr_types, 
                              4, 1, 1, PyUFunc_None,
		              "ndtr", ndtr_doc, 1);
  PyDict_SetItemString(d, "ndtr", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(ndtri_functions,
                              ndtri_data,
                              ndtri_types, 
                              4, 1, 1, PyUFunc_None,
		              "ndtri", ndtri_doc, 1);
  PyDict_SetItemString(d, "ndtri", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(dawsn_functions,
                              dawsn_data,
                              dawsn_types, 
                              4, 1, 1, PyUFunc_None,
		              "dawsn", dawsn_doc, 1);
  PyDict_SetItemString(d, "dawsn", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(gamma_functions,
                              gamma_data,
                              gamma_types, 
                              4, 1, 1, PyUFunc_None,
		              "gamma", gamma_doc, 1);
  PyDict_SetItemString(d, "gamma", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(lgamma_functions,
                              lgamma_data,
                              lgamma_types, 
                              4, 1, 1, PyUFunc_None,
		              "lgamma", lgamma_doc, 1);
  PyDict_SetItemString(d, "lgamma", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(rgamma_functions,
                              rgamma_data,
                              rgamma_types, 
                              4, 1, 1, PyUFunc_None,
		              "rgamma", rgamma_doc, 1);
  PyDict_SetItemString(d, "rgamma", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(psi_functions,
                              psi_data,
                              psi_types, 
                              4, 1, 1, PyUFunc_None,
		              "psi", psi_doc, 1);
  PyDict_SetItemString(d, "psi", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(j0_functions,
                              j0_data,
                              j0_types, 
                              4, 1, 1, PyUFunc_None,
		              "j0", j0_doc, 1);
  PyDict_SetItemString(d, "j0", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(y0_functions,
                              y0_data,
                              y0_types, 
                              4, 1, 1, PyUFunc_None,
		              "y0", y0_doc, 1);
  PyDict_SetItemString(d, "y0", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(i0_functions,
                              i0_data,
                              i0_types, 
                              4, 1, 1, PyUFunc_None,
		              "i0", i0_doc, 1);
  PyDict_SetItemString(d, "i0", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(i0e_functions,
                              i0e_data,
                              i0e_types, 
                              4, 1, 1, PyUFunc_None,
		              "i0e", i0e_doc, 1);
  PyDict_SetItemString(d, "i0e", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(k0_functions,
                              k0_data,
                              k0_types, 
                              4, 1, 1, PyUFunc_None,
		              "k0", k0_doc, 1);
  PyDict_SetItemString(d, "k0", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(k0e_functions,
                              k0e_data,
                              k0e_types, 
                              4, 1, 1, PyUFunc_None,
		              "k0e", k0e_doc, 1);
  PyDict_SetItemString(d, "k0e", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(j1_functions,
                              j1_data,
                              j1_types, 
                              4, 1, 1, PyUFunc_None,
		              "j1", j1_doc, 1);
  PyDict_SetItemString(d, "j1", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(y1_functions,
                              y1_data,
                              y1_types, 
                              4, 1, 1, PyUFunc_None,
		              "y1", y1_doc, 1);
  PyDict_SetItemString(d, "y1", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(i1_functions,
                              i1_data,
                              i1_types, 
                              4, 1, 1, PyUFunc_None,
		              "i1", i1_doc, 1);
  PyDict_SetItemString(d, "i1", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(i1e_functions,
                              i1e_data,
                              i1e_types, 
                              4, 1, 1, PyUFunc_None,
		              "i1e", i1e_doc, 1);
  PyDict_SetItemString(d, "i1e", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(k1_functions,
                              k1_data,
                              k1_types, 
                              4, 1, 1, PyUFunc_None,
		              "k1", k1_doc, 1);
  PyDict_SetItemString(d, "k1", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(k1e_functions,
                              k1e_data,
                              k1e_types, 
                              4, 1, 1, PyUFunc_None,
		              "k1e", k1e_doc, 1);
  PyDict_SetItemString(d, "k1e", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(ellpe_functions,
                              ellpe_data,
                              ellpe_types, 
                              4, 1, 1, PyUFunc_None,
		              "ellpe", ellpe_doc, 1);
  PyDict_SetItemString(d, "ellpe", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(ellpk_functions,
                              ellpk_data,
                              ellpk_types, 
                              4, 1, 1, PyUFunc_None,
		              "ellpk", ellpk_doc, 1);
  PyDict_SetItemString(d, "ellpk", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(spence_functions,
                              spence_data,
                              spence_types, 
                              4, 1, 1, PyUFunc_None,
		              "spence", spence_doc, 1);
  PyDict_SetItemString(d, "spence", f);
  Py_DECREF(f);

  f = PyUFunc_FromFuncAndData(zetac_functions,
                              zetac_data,
                              zetac_types, 
                              4, 1, 1, PyUFunc_None,
		              "zetac", zetac_doc, 1);
  PyDict_SetItemString(d, "zetac", f);
  Py_DECREF(f);

  /* Check for errors */
  if (PyErr_Occurred())
    Py_FatalError("can't initialize module _transcendental");
}
