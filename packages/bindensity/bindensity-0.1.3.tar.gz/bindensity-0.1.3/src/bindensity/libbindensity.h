// Copyright 2020-2024 Jean-Baptiste Delisle
// Licensed under the EUPL-1.2 or later

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))
#define ABS(a) (((a)>0)?(a):-(a))

void resampling_check_def(
  long new_n_in,
  long *isdef,
  long *istart, long *iend);

void resampling_linear_weights(
  // Shapes
  long new_n_in,
  // Input
  double *dx, double *new_dx_in,
  double *delta,
  long *istart, long *isize,
  // Output
  double *w);

void resampling_cubic_weights(
  // Shapes
  long new_n_in,
  // Input
  long *dl, long *dr,
  double *dx, double *new_dx_in,
  double *Fkleft, double *Fkcenter, double *Fkright,
  long *istart, long *isize,
  // Output
  double *w);

void resampling_y(
  long new_n_in, long kstart,
  long *istart, long *iend, long *isize,
  double *y, double *w,
  double *new_y);

void resampling_covariance_nd(
  // Shapes
  long nd, long new_n_in,
  // Input
  long *istart, long *iend,
  // Output
  long *new_nd);

void resampling_covariance(
  // Shapes
  long n, long nd, long new_n,
  long kstart, long new_n_in,
  // Input
  double *cov,
  long *istart, long *iend, long *isize,
  double *w,
  // Output
  double *new_cov);
