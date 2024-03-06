// Copyright 2019-2024 Jean-Baptiste Delisle
// Licensed under the EUPL-1.2 or later

#define NPY_NO_DEPRECATED_API NPY_1_18_API_VERSION

#include "libkeplerian.h"
#include <Python.h>
#include <numpy/arrayobject.h>

// Module docstring
static char module_docstring[] =
  "This module provides an interface for the C library libkeplerian.";

// Methods docstrings
static char M2E_docstring[] =
  "Compute eccentric anomaly from mean anomaly (and eccentricity),\n"
  "by solving Kepler's equation using Newton method.\n";
static char rv_vpar_docstring[] =
  "Compute the star radial velocity induced by a planet,\n"
  "using the default set of orbital parameters.\n";
static char astro_apar_docstring[] =
  "Compute the star astrometric motion induced by a planet,\n"
  "using the astro set of orbital parameters.\n";
static char time2M0_docstring[] =
  "Compute the mean anomaly at reference time\n"
  "from the time at which the true anomaly is thT.\n";
static char M02time_docstring[] =
  "Compute the time at which the true anomaly is thT\n"
  "from the mean anomaly at reference time.\n";
static char par2dpar_docstring[] =
  "Compute default parameters from specified parameters.\n"
  "Default parameters:\n"
  "FREQ_N, AMP_AS, PHASE_M0, ECC_E, OMEGA_OMEGA, INC_I, BIGOMEGA_BIGOMEGA\n";
static char dpar2par_docstring[] =
  "Compute specified parameters from default parameters.\n"
  "Default parameters:\n"
  "FREQ_N, AMP_AS, PHASE_M0, ECC_E, OMEGA_OMEGA, INC_I, BIGOMEGA_BIGOMEGA\n";
static char par2vpar_docstring[] =
  "Compute rv parameters from specified parameters.\n"
  "RV parameters:\n"
  "FREQ_N, AMP_K, PHASE_M0, ECC_E, OMEGA_OMEGA\n";
static char dpar2apar_docstring[] =
  "Compute astro parameters from default parameters.\n"
  "Astro parameters:\n"
  "FREQ_N, ECC_E, PHASE_M0, AMP_TIA, OMEGA_TIB, INC_TIF, BIGOMEGA_TIG\n"
  "Default parameters:\n"
  "FREQ_N, AMP_AS, PHASE_M0, ECC_E, OMEGA_OMEGA, INC_I, BIGOMEGA_BIGOMEGA\n";
static char par2apar_docstring[] =
  "Compute astro parameters from specified parameters.\n"
  "Astro parameters:\n"
  "FREQ_N, ECC_E, PHASE_M0, AMP_TIA, OMEGA_TIB, INC_TIF, BIGOMEGA_TIG\n";
static char rv_vpar_back_docstring[] =
  "Compute the derivatives of the star radial velocity,\n"
  "with respect to the default set of orbital parameters.\n";
static char astro_apar_back_docstring[] =
  "Compute the derivatives of the star astrometric motion,\n"
  "with respect to the default set of orbital parameters.\n";
static char time2M0_back_docstring[] =
  "Backward propagation of the gradient for time2M0.\n";
static char M02time_back_docstring[] =
  "Backward propagation of the gradient for M02time.\n";
static char atan2_back_docstring[] =
  "Backward propagation of the gradient for atan2.\n";
static char par2dpar_back_docstring[] =
  "Backward propagation of the gradient for par2dpar.\n";
static char par2vpar_back_docstring[] =
  "Backward propagation of the gradient for par2vpar.\n";
static char dpar2apar_back_docstring[] =
  "Backward propagation of the gradient for dpar2apar.\n";
static char par2apar_back_docstring[] =
  "Backward propagation of the gradient for par2apar.\n";

// Module methods
static PyObject *libkeplerian_M2E(PyObject *self, PyObject *args);
static PyObject *libkeplerian_rv_vpar(PyObject *self, PyObject *args);
static PyObject *libkeplerian_astro_apar(PyObject *self, PyObject *args);
static PyObject *libkeplerian_time2M0(PyObject *self, PyObject *args);
static PyObject *libkeplerian_M02time(PyObject *self, PyObject *args);
static PyObject *libkeplerian_par2dpar(PyObject *self, PyObject *args);
static PyObject *libkeplerian_dpar2par(PyObject *self, PyObject *args);
static PyObject *libkeplerian_par2vpar(PyObject *self, PyObject *args);
static PyObject *libkeplerian_dpar2apar(PyObject *self, PyObject *args);
static PyObject *libkeplerian_par2apar(PyObject *self, PyObject *args);
static PyObject *libkeplerian_rv_vpar_back(PyObject *self, PyObject *args);
static PyObject *libkeplerian_astro_apar_back(PyObject *self, PyObject *args);
static PyObject *libkeplerian_time2M0_back(PyObject *self, PyObject *args);
static PyObject *libkeplerian_M02time_back(PyObject *self, PyObject *args);
static PyObject *libkeplerian_atan2_back(PyObject *self, PyObject *args);
static PyObject *libkeplerian_par2dpar_back(PyObject *self, PyObject *args);
static PyObject *libkeplerian_par2vpar_back(PyObject *self, PyObject *args);
static PyObject *libkeplerian_dpar2apar_back(PyObject *self, PyObject *args);
static PyObject *libkeplerian_par2apar_back(PyObject *self, PyObject *args);
static PyMethodDef module_methods[] = {
  {"M2E", libkeplerian_M2E, METH_VARARGS, M2E_docstring},
  {"rv_vpar", libkeplerian_rv_vpar, METH_VARARGS, rv_vpar_docstring},
  {"astro_apar", libkeplerian_astro_apar, METH_VARARGS, astro_apar_docstring},
  {"time2M0", libkeplerian_time2M0, METH_VARARGS, time2M0_docstring},
  {"M02time", libkeplerian_M02time, METH_VARARGS, M02time_docstring},
  {"par2dpar", libkeplerian_par2dpar, METH_VARARGS, par2dpar_docstring},
  {"dpar2par", libkeplerian_dpar2par, METH_VARARGS, dpar2par_docstring},
  {"par2vpar", libkeplerian_par2vpar, METH_VARARGS, par2vpar_docstring},
  {"dpar2apar", libkeplerian_dpar2apar, METH_VARARGS, dpar2apar_docstring},
  {"par2apar", libkeplerian_par2apar, METH_VARARGS, par2apar_docstring},
  {"rv_vpar_back", libkeplerian_rv_vpar_back, METH_VARARGS, rv_vpar_back_docstring},
  {"astro_apar_back", libkeplerian_astro_apar_back, METH_VARARGS, astro_apar_back_docstring},
  {"time2M0_back", libkeplerian_time2M0_back, METH_VARARGS, time2M0_back_docstring},
  {"M02time_back", libkeplerian_M02time_back, METH_VARARGS, M02time_back_docstring},
  {"atan2_back", libkeplerian_atan2_back, METH_VARARGS, atan2_back_docstring},
  {"par2dpar_back", libkeplerian_par2dpar_back, METH_VARARGS, par2dpar_back_docstring},
  {"par2vpar_back", libkeplerian_par2vpar_back, METH_VARARGS, par2vpar_back_docstring},
  {"dpar2apar_back", libkeplerian_dpar2apar_back, METH_VARARGS, dpar2apar_back_docstring},
  {"par2apar_back", libkeplerian_par2apar_back, METH_VARARGS, par2apar_back_docstring},
  {NULL, NULL, 0, NULL}};

// Module definition
static struct PyModuleDef myModule = {
  PyModuleDef_HEAD_INIT, "libkeplerian", module_docstring, -1, module_methods};

// Module initialization
PyMODINIT_FUNC PyInit_libkeplerian(void)
{
  // import numpy arrays
  import_array();
  PyObject *module = PyModule_Create(&myModule);
  // Module constants
  PyModule_AddIntConstant(module, "INDEX_FREQ", INDEX_FREQ);
  PyModule_AddIntConstant(module, "INDEX_PHASE", INDEX_PHASE);
  PyModule_AddIntConstant(module, "INDEX_AMP", INDEX_AMP);
  PyModule_AddIntConstant(module, "INDEX_ECC", INDEX_ECC);
  PyModule_AddIntConstant(module, "INDEX_OMEGA", INDEX_OMEGA);
  PyModule_AddIntConstant(module, "INDEX_INC", INDEX_INC);
  PyModule_AddIntConstant(module, "INDEX_BIGOMEGA", INDEX_BIGOMEGA);
  PyModule_AddIntConstant(module, "NINDEX", NINDEX);
  PyModule_AddIntConstant(module, "NONE", NONE);
  PyModule_AddIntConstant(module, "FREQ_N", FREQ_N);
  PyModule_AddIntConstant(module, "FREQ_P", FREQ_P);
  PyModule_AddIntConstant(module, "FREQ_LOG10P", FREQ_LOG10P);
  PyModule_AddIntConstant(module, "PHASE_M0", PHASE_M0);
  PyModule_AddIntConstant(module, "PHASE_MARG0", PHASE_MARG0);
  PyModule_AddIntConstant(module, "PHASE_LA0", PHASE_LA0);
  PyModule_AddIntConstant(module, "PHASE_TP", PHASE_TP);
  PyModule_AddIntConstant(module, "PHASE_TC", PHASE_TC);
  PyModule_AddIntConstant(module, "PHASE_TVMIN", PHASE_TVMIN);
  PyModule_AddIntConstant(module, "PHASE_TVMAX", PHASE_TVMAX);
  PyModule_AddIntConstant(module, "ECC_E", ECC_E);
  PyModule_AddIntConstant(module, "ECC_K", ECC_K);
  PyModule_AddIntConstant(module, "ECC_SQK", ECC_SQK);
  PyModule_AddIntConstant(module, "AMP_K", AMP_K);
  PyModule_AddIntConstant(module, "AMP_LOG10K", AMP_LOG10K);
  PyModule_AddIntConstant(module, "AMP_AS", AMP_AS);
  PyModule_AddIntConstant(module, "AMP_AS_SINI", AMP_AS_SINI);
  PyModule_AddIntConstant(module, "AMP_TIA", AMP_TIA);
  PyModule_AddIntConstant(module, "OMEGA_OMEGA", OMEGA_OMEGA);
  PyModule_AddIntConstant(module, "OMEGA_VARPI", OMEGA_VARPI);
  PyModule_AddIntConstant(module, "OMEGA_H", OMEGA_H);
  PyModule_AddIntConstant(module, "OMEGA_SQH", OMEGA_SQH);
  PyModule_AddIntConstant(module, "OMEGA_TIB", OMEGA_TIB);
  PyModule_AddIntConstant(module, "INC_I", INC_I);
  PyModule_AddIntConstant(module, "INC_COSI", INC_COSI);
  PyModule_AddIntConstant(module, "INC_TIF", INC_TIF);
  PyModule_AddIntConstant(module, "BIGOMEGA_BIGOMEGA", BIGOMEGA_BIGOMEGA);
  PyModule_AddIntConstant(module, "BIGOMEGA_TIG", BIGOMEGA_TIG);
  return (module);
}

static PyObject *libkeplerian_M2E(PyObject *self, PyObject *args)
{
  double M;
  double e;
  double ftol;
  long maxiter;
  PyObject *obj_E;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "dddlO",
    &M,
    &e,
    &ftol,
    &maxiter,
    &obj_E))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_E = (PyArrayObject*) PyArray_FROM_OTF(obj_E, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_E == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_E);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *E = (double*)PyArray_DATA(arr_E);

  // Call the C function from libkeplerian
  M2E(
    M,
    e,
    ftol,
    maxiter,
    E);

  // Dereference arrays
  Py_XDECREF(arr_E);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_rv_vpar(PyObject *self, PyObject *args)
{
  long nt;
  PyObject *obj_t;
  PyObject *obj_vpar;
  PyObject *obj_rv;
  PyObject *obj_th;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "lOOOO",
    &nt,
    &obj_t,
    &obj_vpar,
    &obj_rv,
    &obj_th))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_t = (PyArrayObject*) PyArray_FROM_OTF(obj_t, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_vpar = (PyArrayObject*) PyArray_FROM_OTF(obj_vpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_rv = (PyArrayObject*) PyArray_FROM_OTF(obj_rv, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_th = (PyArrayObject*) PyArray_FROM_OTF(obj_th, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_t == NULL ||
    arr_vpar == NULL ||
    arr_rv == NULL ||
    arr_th == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_t);
    Py_XDECREF(arr_vpar);
    Py_XDECREF(arr_rv);
    Py_XDECREF(arr_th);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *t = (double*)PyArray_DATA(arr_t);
  double *vpar = (double*)PyArray_DATA(arr_vpar);
  double *rv = (double*)PyArray_DATA(arr_rv);
  double *th = (double*)PyArray_DATA(arr_th);

  // Call the C function from libkeplerian
  rv_vpar(
    nt,
    t,
    vpar,
    rv,
    th);

  // Dereference arrays
  Py_XDECREF(arr_t);
  Py_XDECREF(arr_vpar);
  Py_XDECREF(arr_rv);
  Py_XDECREF(arr_th);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_astro_apar(PyObject *self, PyObject *args)
{
  long nt;
  PyObject *obj_t;
  PyObject *obj_apar;
  PyObject *obj_delta;
  PyObject *obj_alpha;
  PyObject *obj_cosE;
  PyObject *obj_sinE;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "lOOOOOO",
    &nt,
    &obj_t,
    &obj_apar,
    &obj_delta,
    &obj_alpha,
    &obj_cosE,
    &obj_sinE))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_t = (PyArrayObject*) PyArray_FROM_OTF(obj_t, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_delta = (PyArrayObject*) PyArray_FROM_OTF(obj_delta, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_alpha = (PyArrayObject*) PyArray_FROM_OTF(obj_alpha, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_cosE = (PyArrayObject*) PyArray_FROM_OTF(obj_cosE, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_sinE = (PyArrayObject*) PyArray_FROM_OTF(obj_sinE, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_t == NULL ||
    arr_apar == NULL ||
    arr_delta == NULL ||
    arr_alpha == NULL ||
    arr_cosE == NULL ||
    arr_sinE == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_t);
    Py_XDECREF(arr_apar);
    Py_XDECREF(arr_delta);
    Py_XDECREF(arr_alpha);
    Py_XDECREF(arr_cosE);
    Py_XDECREF(arr_sinE);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *t = (double*)PyArray_DATA(arr_t);
  double *apar = (double*)PyArray_DATA(arr_apar);
  double *delta = (double*)PyArray_DATA(arr_delta);
  double *alpha = (double*)PyArray_DATA(arr_alpha);
  double *cosE = (double*)PyArray_DATA(arr_cosE);
  double *sinE = (double*)PyArray_DATA(arr_sinE);

  // Call the C function from libkeplerian
  astro_apar(
    nt,
    t,
    apar,
    delta,
    alpha,
    cosE,
    sinE);

  // Dereference arrays
  Py_XDECREF(arr_t);
  Py_XDECREF(arr_apar);
  Py_XDECREF(arr_delta);
  Py_XDECREF(arr_alpha);
  Py_XDECREF(arr_cosE);
  Py_XDECREF(arr_sinE);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_time2M0(PyObject *self, PyObject *args)
{
  PyObject *obj_par;
  PyObject *obj_dpar;
  double thT;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOd",
    &obj_par,
    &obj_dpar,
    &thT))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_par == NULL ||
    arr_dpar == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_dpar);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *par = (double*)PyArray_DATA(arr_par);
  double *dpar = (double*)PyArray_DATA(arr_dpar);

  // Call the C function from libkeplerian
  time2M0(
    par,
    dpar,
    thT);

  // Dereference arrays
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_dpar);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_M02time(PyObject *self, PyObject *args)
{
  PyObject *obj_dpar;
  PyObject *obj_par;
  double thT;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOd",
    &obj_dpar,
    &obj_par,
    &thT))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_dpar == NULL ||
    arr_par == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_dpar);
    Py_XDECREF(arr_par);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *dpar = (double*)PyArray_DATA(arr_dpar);
  double *par = (double*)PyArray_DATA(arr_par);

  // Call the C function from libkeplerian
  M02time(
    dpar,
    par,
    thT);

  // Dereference arrays
  Py_XDECREF(arr_dpar);
  Py_XDECREF(arr_par);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_par2dpar(PyObject *self, PyObject *args)
{
  PyObject *obj_ptype;
  PyObject *obj_par;
  PyObject *obj_dpar;
  double velocity_coef;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOOd",
    &obj_ptype,
    &obj_par,
    &obj_dpar,
    &velocity_coef))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_ptype = (PyArrayObject*) PyArray_FROM_OTF(obj_ptype, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_ptype == NULL ||
    arr_par == NULL ||
    arr_dpar == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_ptype);
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_dpar);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *ptype = (long*)PyArray_DATA(arr_ptype);
  double *par = (double*)PyArray_DATA(arr_par);
  double *dpar = (double*)PyArray_DATA(arr_dpar);

  // Call the C function from libkeplerian
  par2dpar(
    ptype,
    par,
    dpar,
    velocity_coef);

  // Dereference arrays
  Py_XDECREF(arr_ptype);
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_dpar);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_dpar2par(PyObject *self, PyObject *args)
{
  PyObject *obj_dpar;
  PyObject *obj_ptype;
  PyObject *obj_par;
  double velocity_coef;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOOd",
    &obj_dpar,
    &obj_ptype,
    &obj_par,
    &velocity_coef))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_ptype = (PyArrayObject*) PyArray_FROM_OTF(obj_ptype, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_dpar == NULL ||
    arr_ptype == NULL ||
    arr_par == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_dpar);
    Py_XDECREF(arr_ptype);
    Py_XDECREF(arr_par);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *dpar = (double*)PyArray_DATA(arr_dpar);
  long *ptype = (long*)PyArray_DATA(arr_ptype);
  double *par = (double*)PyArray_DATA(arr_par);

  // Call the C function from libkeplerian
  dpar2par(
    dpar,
    ptype,
    par,
    velocity_coef);

  // Dereference arrays
  Py_XDECREF(arr_dpar);
  Py_XDECREF(arr_ptype);
  Py_XDECREF(arr_par);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_par2vpar(PyObject *self, PyObject *args)
{
  PyObject *obj_ptype;
  PyObject *obj_par;
  PyObject *obj_vpar;
  double velocity_coef;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOOd",
    &obj_ptype,
    &obj_par,
    &obj_vpar,
    &velocity_coef))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_ptype = (PyArrayObject*) PyArray_FROM_OTF(obj_ptype, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_vpar = (PyArrayObject*) PyArray_FROM_OTF(obj_vpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_ptype == NULL ||
    arr_par == NULL ||
    arr_vpar == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_ptype);
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_vpar);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *ptype = (long*)PyArray_DATA(arr_ptype);
  double *par = (double*)PyArray_DATA(arr_par);
  double *vpar = (double*)PyArray_DATA(arr_vpar);

  // Call the C function from libkeplerian
  par2vpar(
    ptype,
    par,
    vpar,
    velocity_coef);

  // Dereference arrays
  Py_XDECREF(arr_ptype);
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_vpar);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_dpar2apar(PyObject *self, PyObject *args)
{
  PyObject *obj_dpar;
  PyObject *obj_apar;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OO",
    &obj_dpar,
    &obj_apar))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_dpar == NULL ||
    arr_apar == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_dpar);
    Py_XDECREF(arr_apar);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *dpar = (double*)PyArray_DATA(arr_dpar);
  double *apar = (double*)PyArray_DATA(arr_apar);

  // Call the C function from libkeplerian
  dpar2apar(
    dpar,
    apar);

  // Dereference arrays
  Py_XDECREF(arr_dpar);
  Py_XDECREF(arr_apar);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_par2apar(PyObject *self, PyObject *args)
{
  PyObject *obj_ptype;
  PyObject *obj_par;
  PyObject *obj_apar;
  PyObject *obj_dpar;
  double velocity_coef;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOOOd",
    &obj_ptype,
    &obj_par,
    &obj_apar,
    &obj_dpar,
    &velocity_coef))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_ptype = (PyArrayObject*) PyArray_FROM_OTF(obj_ptype, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_ptype == NULL ||
    arr_par == NULL ||
    arr_apar == NULL ||
    arr_dpar == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_ptype);
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_apar);
    Py_XDECREF(arr_dpar);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *ptype = (long*)PyArray_DATA(arr_ptype);
  double *par = (double*)PyArray_DATA(arr_par);
  double *apar = (double*)PyArray_DATA(arr_apar);
  double *dpar = (double*)PyArray_DATA(arr_dpar);

  // Call the C function from libkeplerian
  par2apar(
    ptype,
    par,
    apar,
    dpar,
    velocity_coef);

  // Dereference arrays
  Py_XDECREF(arr_ptype);
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_apar);
  Py_XDECREF(arr_dpar);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_rv_vpar_back(PyObject *self, PyObject *args)
{
  long nt;
  PyObject *obj_t;
  PyObject *obj_vpar;
  PyObject *obj_grad_rv;
  PyObject *obj_grad_vpar;
  PyObject *obj_th;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "lOOOOO",
    &nt,
    &obj_t,
    &obj_vpar,
    &obj_grad_rv,
    &obj_grad_vpar,
    &obj_th))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_t = (PyArrayObject*) PyArray_FROM_OTF(obj_t, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_vpar = (PyArrayObject*) PyArray_FROM_OTF(obj_vpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_rv = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_rv, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_vpar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_vpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_th = (PyArrayObject*) PyArray_FROM_OTF(obj_th, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_t == NULL ||
    arr_vpar == NULL ||
    arr_grad_rv == NULL ||
    arr_grad_vpar == NULL ||
    arr_th == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_t);
    Py_XDECREF(arr_vpar);
    Py_XDECREF(arr_grad_rv);
    Py_XDECREF(arr_grad_vpar);
    Py_XDECREF(arr_th);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *t = (double*)PyArray_DATA(arr_t);
  double *vpar = (double*)PyArray_DATA(arr_vpar);
  double *grad_rv = (double*)PyArray_DATA(arr_grad_rv);
  double *grad_vpar = (double*)PyArray_DATA(arr_grad_vpar);
  double *th = (double*)PyArray_DATA(arr_th);

  // Call the C function from libkeplerian
  rv_vpar_back(
    nt,
    t,
    vpar,
    grad_rv,
    grad_vpar,
    th);

  // Dereference arrays
  Py_XDECREF(arr_t);
  Py_XDECREF(arr_vpar);
  Py_XDECREF(arr_grad_rv);
  Py_XDECREF(arr_grad_vpar);
  Py_XDECREF(arr_th);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_astro_apar_back(PyObject *self, PyObject *args)
{
  long nt;
  PyObject *obj_t;
  PyObject *obj_apar;
  PyObject *obj_grad_delta;
  PyObject *obj_grad_alpha;
  PyObject *obj_grad_apar;
  PyObject *obj_cosE;
  PyObject *obj_sinE;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "lOOOOOOO",
    &nt,
    &obj_t,
    &obj_apar,
    &obj_grad_delta,
    &obj_grad_alpha,
    &obj_grad_apar,
    &obj_cosE,
    &obj_sinE))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_t = (PyArrayObject*) PyArray_FROM_OTF(obj_t, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_delta = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_delta, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_alpha = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_alpha, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_cosE = (PyArrayObject*) PyArray_FROM_OTF(obj_cosE, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_sinE = (PyArrayObject*) PyArray_FROM_OTF(obj_sinE, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_t == NULL ||
    arr_apar == NULL ||
    arr_grad_delta == NULL ||
    arr_grad_alpha == NULL ||
    arr_grad_apar == NULL ||
    arr_cosE == NULL ||
    arr_sinE == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_t);
    Py_XDECREF(arr_apar);
    Py_XDECREF(arr_grad_delta);
    Py_XDECREF(arr_grad_alpha);
    Py_XDECREF(arr_grad_apar);
    Py_XDECREF(arr_cosE);
    Py_XDECREF(arr_sinE);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *t = (double*)PyArray_DATA(arr_t);
  double *apar = (double*)PyArray_DATA(arr_apar);
  double *grad_delta = (double*)PyArray_DATA(arr_grad_delta);
  double *grad_alpha = (double*)PyArray_DATA(arr_grad_alpha);
  double *grad_apar = (double*)PyArray_DATA(arr_grad_apar);
  double *cosE = (double*)PyArray_DATA(arr_cosE);
  double *sinE = (double*)PyArray_DATA(arr_sinE);

  // Call the C function from libkeplerian
  astro_apar_back(
    nt,
    t,
    apar,
    grad_delta,
    grad_alpha,
    grad_apar,
    cosE,
    sinE);

  // Dereference arrays
  Py_XDECREF(arr_t);
  Py_XDECREF(arr_apar);
  Py_XDECREF(arr_grad_delta);
  Py_XDECREF(arr_grad_alpha);
  Py_XDECREF(arr_grad_apar);
  Py_XDECREF(arr_cosE);
  Py_XDECREF(arr_sinE);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_time2M0_back(PyObject *self, PyObject *args)
{
  PyObject *obj_par;
  PyObject *obj_dpar;
  double thT;
  PyObject *obj_grad_par;
  PyObject *obj_grad_thT;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOdOO",
    &obj_par,
    &obj_dpar,
    &thT,
    &obj_grad_par,
    &obj_grad_thT))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_par = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_thT = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_thT, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_par == NULL ||
    arr_dpar == NULL ||
    arr_grad_par == NULL ||
    arr_grad_thT == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_dpar);
    Py_XDECREF(arr_grad_par);
    Py_XDECREF(arr_grad_thT);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *par = (double*)PyArray_DATA(arr_par);
  double *dpar = (double*)PyArray_DATA(arr_dpar);
  double *grad_par = (double*)PyArray_DATA(arr_grad_par);
  double *grad_thT = (double*)PyArray_DATA(arr_grad_thT);

  // Call the C function from libkeplerian
  time2M0_back(
    par,
    dpar,
    thT,
    grad_par,
    grad_thT);

  // Dereference arrays
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_dpar);
  Py_XDECREF(arr_grad_par);
  Py_XDECREF(arr_grad_thT);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_M02time_back(PyObject *self, PyObject *args)
{
  PyObject *obj_dpar;
  PyObject *obj_par;
  double thT;
  PyObject *obj_grad_dpar;
  PyObject *obj_grad_thT;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOdOO",
    &obj_dpar,
    &obj_par,
    &thT,
    &obj_grad_dpar,
    &obj_grad_thT))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_thT = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_thT, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_dpar == NULL ||
    arr_par == NULL ||
    arr_grad_dpar == NULL ||
    arr_grad_thT == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_dpar);
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_grad_dpar);
    Py_XDECREF(arr_grad_thT);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *dpar = (double*)PyArray_DATA(arr_dpar);
  double *par = (double*)PyArray_DATA(arr_par);
  double *grad_dpar = (double*)PyArray_DATA(arr_grad_dpar);
  double *grad_thT = (double*)PyArray_DATA(arr_grad_thT);

  // Call the C function from libkeplerian
  M02time_back(
    dpar,
    par,
    thT,
    grad_dpar,
    grad_thT);

  // Dereference arrays
  Py_XDECREF(arr_dpar);
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_grad_dpar);
  Py_XDECREF(arr_grad_thT);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_atan2_back(PyObject *self, PyObject *args)
{
  double y;
  double x;
  double grad_theta;
  PyObject *obj_grad_y;
  PyObject *obj_grad_x;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "dddOO",
    &y,
    &x,
    &grad_theta,
    &obj_grad_y,
    &obj_grad_x))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_grad_y = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_y, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_x = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_x, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_grad_y == NULL ||
    arr_grad_x == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_grad_y);
    Py_XDECREF(arr_grad_x);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *grad_y = (double*)PyArray_DATA(arr_grad_y);
  double *grad_x = (double*)PyArray_DATA(arr_grad_x);

  // Call the C function from libkeplerian
  atan2_back(
    y,
    x,
    grad_theta,
    grad_y,
    grad_x);

  // Dereference arrays
  Py_XDECREF(arr_grad_y);
  Py_XDECREF(arr_grad_x);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_par2dpar_back(PyObject *self, PyObject *args)
{
  PyObject *obj_ptype;
  PyObject *obj_par;
  PyObject *obj_dpar;
  PyObject *obj_grad_dpar;
  PyObject *obj_grad_par;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOOOO",
    &obj_ptype,
    &obj_par,
    &obj_dpar,
    &obj_grad_dpar,
    &obj_grad_par))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_ptype = (PyArrayObject*) PyArray_FROM_OTF(obj_ptype, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_par = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_ptype == NULL ||
    arr_par == NULL ||
    arr_dpar == NULL ||
    arr_grad_dpar == NULL ||
    arr_grad_par == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_ptype);
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_dpar);
    Py_XDECREF(arr_grad_dpar);
    Py_XDECREF(arr_grad_par);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *ptype = (long*)PyArray_DATA(arr_ptype);
  double *par = (double*)PyArray_DATA(arr_par);
  double *dpar = (double*)PyArray_DATA(arr_dpar);
  double *grad_dpar = (double*)PyArray_DATA(arr_grad_dpar);
  double *grad_par = (double*)PyArray_DATA(arr_grad_par);

  // Call the C function from libkeplerian
  par2dpar_back(
    ptype,
    par,
    dpar,
    grad_dpar,
    grad_par);

  // Dereference arrays
  Py_XDECREF(arr_ptype);
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_dpar);
  Py_XDECREF(arr_grad_dpar);
  Py_XDECREF(arr_grad_par);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_par2vpar_back(PyObject *self, PyObject *args)
{
  PyObject *obj_ptype;
  PyObject *obj_par;
  PyObject *obj_vpar;
  PyObject *obj_grad_vpar;
  PyObject *obj_grad_par;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOOOO",
    &obj_ptype,
    &obj_par,
    &obj_vpar,
    &obj_grad_vpar,
    &obj_grad_par))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_ptype = (PyArrayObject*) PyArray_FROM_OTF(obj_ptype, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_vpar = (PyArrayObject*) PyArray_FROM_OTF(obj_vpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_vpar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_vpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_par = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_ptype == NULL ||
    arr_par == NULL ||
    arr_vpar == NULL ||
    arr_grad_vpar == NULL ||
    arr_grad_par == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_ptype);
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_vpar);
    Py_XDECREF(arr_grad_vpar);
    Py_XDECREF(arr_grad_par);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *ptype = (long*)PyArray_DATA(arr_ptype);
  double *par = (double*)PyArray_DATA(arr_par);
  double *vpar = (double*)PyArray_DATA(arr_vpar);
  double *grad_vpar = (double*)PyArray_DATA(arr_grad_vpar);
  double *grad_par = (double*)PyArray_DATA(arr_grad_par);

  // Call the C function from libkeplerian
  par2vpar_back(
    ptype,
    par,
    vpar,
    grad_vpar,
    grad_par);

  // Dereference arrays
  Py_XDECREF(arr_ptype);
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_vpar);
  Py_XDECREF(arr_grad_vpar);
  Py_XDECREF(arr_grad_par);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_dpar2apar_back(PyObject *self, PyObject *args)
{
  PyObject *obj_dpar;
  PyObject *obj_apar;
  PyObject *obj_grad_apar;
  PyObject *obj_grad_dpar;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOOO",
    &obj_dpar,
    &obj_apar,
    &obj_grad_apar,
    &obj_grad_dpar))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_dpar == NULL ||
    arr_apar == NULL ||
    arr_grad_apar == NULL ||
    arr_grad_dpar == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_dpar);
    Py_XDECREF(arr_apar);
    Py_XDECREF(arr_grad_apar);
    Py_XDECREF(arr_grad_dpar);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *dpar = (double*)PyArray_DATA(arr_dpar);
  double *apar = (double*)PyArray_DATA(arr_apar);
  double *grad_apar = (double*)PyArray_DATA(arr_grad_apar);
  double *grad_dpar = (double*)PyArray_DATA(arr_grad_dpar);

  // Call the C function from libkeplerian
  dpar2apar_back(
    dpar,
    apar,
    grad_apar,
    grad_dpar);

  // Dereference arrays
  Py_XDECREF(arr_dpar);
  Py_XDECREF(arr_apar);
  Py_XDECREF(arr_grad_apar);
  Py_XDECREF(arr_grad_dpar);

  Py_RETURN_NONE;
}

static PyObject *libkeplerian_par2apar_back(PyObject *self, PyObject *args)
{
  PyObject *obj_ptype;
  PyObject *obj_par;
  PyObject *obj_apar;
  PyObject *obj_grad_apar;
  PyObject *obj_grad_par;
  PyObject *obj_dpar;
  PyObject *obj_grad_dpar;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "OOOOOOO",
    &obj_ptype,
    &obj_par,
    &obj_apar,
    &obj_grad_apar,
    &obj_grad_par,
    &obj_dpar,
    &obj_grad_dpar))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_ptype = (PyArrayObject*) PyArray_FROM_OTF(obj_ptype, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_par = (PyArrayObject*) PyArray_FROM_OTF(obj_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_apar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_apar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_par = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_par, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_grad_dpar = (PyArrayObject*) PyArray_FROM_OTF(obj_grad_dpar, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_ptype == NULL ||
    arr_par == NULL ||
    arr_apar == NULL ||
    arr_grad_apar == NULL ||
    arr_grad_par == NULL ||
    arr_dpar == NULL ||
    arr_grad_dpar == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_ptype);
    Py_XDECREF(arr_par);
    Py_XDECREF(arr_apar);
    Py_XDECREF(arr_grad_apar);
    Py_XDECREF(arr_grad_par);
    Py_XDECREF(arr_dpar);
    Py_XDECREF(arr_grad_dpar);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *ptype = (long*)PyArray_DATA(arr_ptype);
  double *par = (double*)PyArray_DATA(arr_par);
  double *apar = (double*)PyArray_DATA(arr_apar);
  double *grad_apar = (double*)PyArray_DATA(arr_grad_apar);
  double *grad_par = (double*)PyArray_DATA(arr_grad_par);
  double *dpar = (double*)PyArray_DATA(arr_dpar);
  double *grad_dpar = (double*)PyArray_DATA(arr_grad_dpar);

  // Call the C function from libkeplerian
  par2apar_back(
    ptype,
    par,
    apar,
    grad_apar,
    grad_par,
    dpar,
    grad_dpar);

  // Dereference arrays
  Py_XDECREF(arr_ptype);
  Py_XDECREF(arr_par);
  Py_XDECREF(arr_apar);
  Py_XDECREF(arr_grad_apar);
  Py_XDECREF(arr_grad_par);
  Py_XDECREF(arr_dpar);
  Py_XDECREF(arr_grad_dpar);

  Py_RETURN_NONE;
}
