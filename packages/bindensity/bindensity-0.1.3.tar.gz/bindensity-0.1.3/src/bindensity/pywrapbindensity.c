// Copyright 2020-2024 Jean-Baptiste Delisle
// Licensed under the EUPL-1.2 or later

#define NPY_NO_DEPRECATED_API NPY_1_18_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>
#include "libbindensity.h"

// Module docstring
static char module_docstring[] =
  "This module provides an interface for the C library libbindensity.";

// Methods docstrings
static char resampling_check_def_docstring[] =
  "Avoid to compute undefined bins\n";
static char resampling_linear_weights_docstring[] =
  "Compute weights according to linear interpolation rules\n";
static char resampling_cubic_weights_docstring[] =
  "Compute weights according to cubic interpolation rules\n";
static char resampling_y_docstring[] =
  "Compute new bins density\n";
static char resampling_covariance_nd_docstring[] =
  "Compute new covariance shape\n";
static char resampling_covariance_docstring[] =
  "Compute new covariance\n";

// Module methods
static PyObject *libbindensity_resampling_check_def(PyObject *self, PyObject *args);
static PyObject *libbindensity_resampling_linear_weights(PyObject *self, PyObject *args);
static PyObject *libbindensity_resampling_cubic_weights(PyObject *self, PyObject *args);
static PyObject *libbindensity_resampling_y(PyObject *self, PyObject *args);
static PyObject *libbindensity_resampling_covariance_nd(PyObject *self, PyObject *args);
static PyObject *libbindensity_resampling_covariance(PyObject *self, PyObject *args);
static PyMethodDef module_methods[] = {
  {"resampling_check_def", libbindensity_resampling_check_def, METH_VARARGS, resampling_check_def_docstring},
  {"resampling_linear_weights", libbindensity_resampling_linear_weights, METH_VARARGS, resampling_linear_weights_docstring},
  {"resampling_cubic_weights", libbindensity_resampling_cubic_weights, METH_VARARGS, resampling_cubic_weights_docstring},
  {"resampling_y", libbindensity_resampling_y, METH_VARARGS, resampling_y_docstring},
  {"resampling_covariance_nd", libbindensity_resampling_covariance_nd, METH_VARARGS, resampling_covariance_nd_docstring},
  {"resampling_covariance", libbindensity_resampling_covariance, METH_VARARGS, resampling_covariance_docstring},
  
  {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef myModule = {
  PyModuleDef_HEAD_INIT,
  "libbindensity",
  module_docstring,
  -1,
  module_methods
};

// Module initialization
PyMODINIT_FUNC PyInit_libbindensity(void) {
  // import numpy arrays
  import_array();
  return PyModule_Create(&myModule);
}

static PyObject *libbindensity_resampling_check_def(PyObject *self, PyObject *args)
{
  long new_n_in;
  PyObject *obj_isdef;
  PyObject *obj_istart;
  PyObject *obj_iend;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "lOOO",
    &new_n_in,
    &obj_isdef,
    &obj_istart,
    &obj_iend))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_isdef = (PyArrayObject*) PyArray_FROM_OTF(obj_isdef, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_istart = (PyArrayObject*) PyArray_FROM_OTF(obj_istart, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_iend = (PyArrayObject*) PyArray_FROM_OTF(obj_iend, NPY_LONG, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_isdef == NULL ||
    arr_istart == NULL ||
    arr_iend == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_isdef);
    Py_XDECREF(arr_istart);
    Py_XDECREF(arr_iend);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *isdef = (long*)PyArray_DATA(arr_isdef);
  long *istart = (long*)PyArray_DATA(arr_istart);
  long *iend = (long*)PyArray_DATA(arr_iend);

  // Call the C function from libbindensity
  resampling_check_def(
    new_n_in,
    isdef,
    istart,
    iend);

  // Dereference arrays
  Py_XDECREF(arr_isdef);
  Py_XDECREF(arr_istart);
  Py_XDECREF(arr_iend);

  Py_RETURN_NONE;
}

static PyObject *libbindensity_resampling_linear_weights(PyObject *self, PyObject *args)
{
  long new_n_in;
  PyObject *obj_dx;
  PyObject *obj_new_dx_in;
  PyObject *obj_delta;
  PyObject *obj_istart;
  PyObject *obj_isize;
  PyObject *obj_w;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "lOOOOOO",
    &new_n_in,
    &obj_dx,
    &obj_new_dx_in,
    &obj_delta,
    &obj_istart,
    &obj_isize,
    &obj_w))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_dx = (PyArrayObject*) PyArray_FROM_OTF(obj_dx, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_new_dx_in = (PyArrayObject*) PyArray_FROM_OTF(obj_new_dx_in, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_delta = (PyArrayObject*) PyArray_FROM_OTF(obj_delta, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_istart = (PyArrayObject*) PyArray_FROM_OTF(obj_istart, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_isize = (PyArrayObject*) PyArray_FROM_OTF(obj_isize, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_w = (PyArrayObject*) PyArray_FROM_OTF(obj_w, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_dx == NULL ||
    arr_new_dx_in == NULL ||
    arr_delta == NULL ||
    arr_istart == NULL ||
    arr_isize == NULL ||
    arr_w == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_dx);
    Py_XDECREF(arr_new_dx_in);
    Py_XDECREF(arr_delta);
    Py_XDECREF(arr_istart);
    Py_XDECREF(arr_isize);
    Py_XDECREF(arr_w);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *dx = (double*)PyArray_DATA(arr_dx);
  double *new_dx_in = (double*)PyArray_DATA(arr_new_dx_in);
  double *delta = (double*)PyArray_DATA(arr_delta);
  long *istart = (long*)PyArray_DATA(arr_istart);
  long *isize = (long*)PyArray_DATA(arr_isize);
  double *w = (double*)PyArray_DATA(arr_w);

  // Call the C function from libbindensity
  resampling_linear_weights(
    new_n_in,
    dx,
    new_dx_in,
    delta,
    istart,
    isize,
    w);

  // Dereference arrays
  Py_XDECREF(arr_dx);
  Py_XDECREF(arr_new_dx_in);
  Py_XDECREF(arr_delta);
  Py_XDECREF(arr_istart);
  Py_XDECREF(arr_isize);
  Py_XDECREF(arr_w);

  Py_RETURN_NONE;
}

static PyObject *libbindensity_resampling_cubic_weights(PyObject *self, PyObject *args)
{
  long new_n_in;
  PyObject *obj_dl;
  PyObject *obj_dr;
  PyObject *obj_dx;
  PyObject *obj_new_dx_in;
  PyObject *obj_Fkleft;
  PyObject *obj_Fkcenter;
  PyObject *obj_Fkright;
  PyObject *obj_istart;
  PyObject *obj_isize;
  PyObject *obj_w;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "lOOOOOOOOOO",
    &new_n_in,
    &obj_dl,
    &obj_dr,
    &obj_dx,
    &obj_new_dx_in,
    &obj_Fkleft,
    &obj_Fkcenter,
    &obj_Fkright,
    &obj_istart,
    &obj_isize,
    &obj_w))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_dl = (PyArrayObject*) PyArray_FROM_OTF(obj_dl, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_dr = (PyArrayObject*) PyArray_FROM_OTF(obj_dr, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_dx = (PyArrayObject*) PyArray_FROM_OTF(obj_dx, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_new_dx_in = (PyArrayObject*) PyArray_FROM_OTF(obj_new_dx_in, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_Fkleft = (PyArrayObject*) PyArray_FROM_OTF(obj_Fkleft, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_Fkcenter = (PyArrayObject*) PyArray_FROM_OTF(obj_Fkcenter, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_Fkright = (PyArrayObject*) PyArray_FROM_OTF(obj_Fkright, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_istart = (PyArrayObject*) PyArray_FROM_OTF(obj_istart, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_isize = (PyArrayObject*) PyArray_FROM_OTF(obj_isize, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_w = (PyArrayObject*) PyArray_FROM_OTF(obj_w, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_dl == NULL ||
    arr_dr == NULL ||
    arr_dx == NULL ||
    arr_new_dx_in == NULL ||
    arr_Fkleft == NULL ||
    arr_Fkcenter == NULL ||
    arr_Fkright == NULL ||
    arr_istart == NULL ||
    arr_isize == NULL ||
    arr_w == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_dl);
    Py_XDECREF(arr_dr);
    Py_XDECREF(arr_dx);
    Py_XDECREF(arr_new_dx_in);
    Py_XDECREF(arr_Fkleft);
    Py_XDECREF(arr_Fkcenter);
    Py_XDECREF(arr_Fkright);
    Py_XDECREF(arr_istart);
    Py_XDECREF(arr_isize);
    Py_XDECREF(arr_w);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *dl = (long*)PyArray_DATA(arr_dl);
  long *dr = (long*)PyArray_DATA(arr_dr);
  double *dx = (double*)PyArray_DATA(arr_dx);
  double *new_dx_in = (double*)PyArray_DATA(arr_new_dx_in);
  double *Fkleft = (double*)PyArray_DATA(arr_Fkleft);
  double *Fkcenter = (double*)PyArray_DATA(arr_Fkcenter);
  double *Fkright = (double*)PyArray_DATA(arr_Fkright);
  long *istart = (long*)PyArray_DATA(arr_istart);
  long *isize = (long*)PyArray_DATA(arr_isize);
  double *w = (double*)PyArray_DATA(arr_w);

  // Call the C function from libbindensity
  resampling_cubic_weights(
    new_n_in,
    dl,
    dr,
    dx,
    new_dx_in,
    Fkleft,
    Fkcenter,
    Fkright,
    istart,
    isize,
    w);

  // Dereference arrays
  Py_XDECREF(arr_dl);
  Py_XDECREF(arr_dr);
  Py_XDECREF(arr_dx);
  Py_XDECREF(arr_new_dx_in);
  Py_XDECREF(arr_Fkleft);
  Py_XDECREF(arr_Fkcenter);
  Py_XDECREF(arr_Fkright);
  Py_XDECREF(arr_istart);
  Py_XDECREF(arr_isize);
  Py_XDECREF(arr_w);

  Py_RETURN_NONE;
}

static PyObject *libbindensity_resampling_y(PyObject *self, PyObject *args)
{
  long new_n_in;
  long kstart;
  PyObject *obj_istart;
  PyObject *obj_iend;
  PyObject *obj_isize;
  PyObject *obj_y;
  PyObject *obj_w;
  PyObject *obj_new_y;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "llOOOOOO",
    &new_n_in,
    &kstart,
    &obj_istart,
    &obj_iend,
    &obj_isize,
    &obj_y,
    &obj_w,
    &obj_new_y))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_istart = (PyArrayObject*) PyArray_FROM_OTF(obj_istart, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_iend = (PyArrayObject*) PyArray_FROM_OTF(obj_iend, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_isize = (PyArrayObject*) PyArray_FROM_OTF(obj_isize, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_y = (PyArrayObject*) PyArray_FROM_OTF(obj_y, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_w = (PyArrayObject*) PyArray_FROM_OTF(obj_w, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_new_y = (PyArrayObject*) PyArray_FROM_OTF(obj_new_y, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_istart == NULL ||
    arr_iend == NULL ||
    arr_isize == NULL ||
    arr_y == NULL ||
    arr_w == NULL ||
    arr_new_y == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_istart);
    Py_XDECREF(arr_iend);
    Py_XDECREF(arr_isize);
    Py_XDECREF(arr_y);
    Py_XDECREF(arr_w);
    Py_XDECREF(arr_new_y);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *istart = (long*)PyArray_DATA(arr_istart);
  long *iend = (long*)PyArray_DATA(arr_iend);
  long *isize = (long*)PyArray_DATA(arr_isize);
  double *y = (double*)PyArray_DATA(arr_y);
  double *w = (double*)PyArray_DATA(arr_w);
  double *new_y = (double*)PyArray_DATA(arr_new_y);

  // Call the C function from libbindensity
  resampling_y(
    new_n_in,
    kstart,
    istart,
    iend,
    isize,
    y,
    w,
    new_y);

  // Dereference arrays
  Py_XDECREF(arr_istart);
  Py_XDECREF(arr_iend);
  Py_XDECREF(arr_isize);
  Py_XDECREF(arr_y);
  Py_XDECREF(arr_w);
  Py_XDECREF(arr_new_y);

  Py_RETURN_NONE;
}

static PyObject *libbindensity_resampling_covariance_nd(PyObject *self, PyObject *args)
{
  long nd;
  long new_n_in;
  PyObject *obj_istart;
  PyObject *obj_iend;
  PyObject *obj_new_nd;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "llOOO",
    &nd,
    &new_n_in,
    &obj_istart,
    &obj_iend,
    &obj_new_nd))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_istart = (PyArrayObject*) PyArray_FROM_OTF(obj_istart, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_iend = (PyArrayObject*) PyArray_FROM_OTF(obj_iend, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_new_nd = (PyArrayObject*) PyArray_FROM_OTF(obj_new_nd, NPY_LONG, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_istart == NULL ||
    arr_iend == NULL ||
    arr_new_nd == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_istart);
    Py_XDECREF(arr_iend);
    Py_XDECREF(arr_new_nd);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  long *istart = (long*)PyArray_DATA(arr_istart);
  long *iend = (long*)PyArray_DATA(arr_iend);
  long *new_nd = (long*)PyArray_DATA(arr_new_nd);

  // Call the C function from libbindensity
  resampling_covariance_nd(
    nd,
    new_n_in,
    istart,
    iend,
    new_nd);

  // Dereference arrays
  Py_XDECREF(arr_istart);
  Py_XDECREF(arr_iend);
  Py_XDECREF(arr_new_nd);

  Py_RETURN_NONE;
}

static PyObject *libbindensity_resampling_covariance(PyObject *self, PyObject *args)
{
  long n;
  long nd;
  long new_n;
  long kstart;
  long new_n_in;
  PyObject *obj_cov;
  PyObject *obj_istart;
  PyObject *obj_iend;
  PyObject *obj_isize;
  PyObject *obj_w;
  PyObject *obj_new_cov;

  // Parse input tuple
  if (!PyArg_ParseTuple(args, "lllllOOOOOO",
    &n,
    &nd,
    &new_n,
    &kstart,
    &new_n_in,
    &obj_cov,
    &obj_istart,
    &obj_iend,
    &obj_isize,
    &obj_w,
    &obj_new_cov))
    return(NULL);

  // Interpret input objects as numpy arrays
  PyArrayObject *arr_cov = (PyArrayObject*) PyArray_FROM_OTF(obj_cov, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_istart = (PyArrayObject*) PyArray_FROM_OTF(obj_istart, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_iend = (PyArrayObject*) PyArray_FROM_OTF(obj_iend, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_isize = (PyArrayObject*) PyArray_FROM_OTF(obj_isize, NPY_LONG, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_w = (PyArrayObject*) PyArray_FROM_OTF(obj_w, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
  PyArrayObject *arr_new_cov = (PyArrayObject*) PyArray_FROM_OTF(obj_new_cov, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);

  // Generate exception in case of failure
  if (
    arr_cov == NULL ||
    arr_istart == NULL ||
    arr_iend == NULL ||
    arr_isize == NULL ||
    arr_w == NULL ||
    arr_new_cov == NULL) {
    // Dereference arrays
    Py_XDECREF(arr_cov);
    Py_XDECREF(arr_istart);
    Py_XDECREF(arr_iend);
    Py_XDECREF(arr_isize);
    Py_XDECREF(arr_w);
    Py_XDECREF(arr_new_cov);
    return NULL;
  }

  // Get C-types pointers to numpy arrays
  double *cov = (double*)PyArray_DATA(arr_cov);
  long *istart = (long*)PyArray_DATA(arr_istart);
  long *iend = (long*)PyArray_DATA(arr_iend);
  long *isize = (long*)PyArray_DATA(arr_isize);
  double *w = (double*)PyArray_DATA(arr_w);
  double *new_cov = (double*)PyArray_DATA(arr_new_cov);

  // Call the C function from libbindensity
  resampling_covariance(
    n,
    nd,
    new_n,
    kstart,
    new_n_in,
    cov,
    istart,
    iend,
    isize,
    w,
    new_cov);

  // Dereference arrays
  Py_XDECREF(arr_cov);
  Py_XDECREF(arr_istart);
  Py_XDECREF(arr_iend);
  Py_XDECREF(arr_isize);
  Py_XDECREF(arr_w);
  Py_XDECREF(arr_new_cov);

  Py_RETURN_NONE;
}
