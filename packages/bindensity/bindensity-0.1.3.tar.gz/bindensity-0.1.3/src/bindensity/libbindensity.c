// Copyright 2020-2024 Jean-Baptiste Delisle
// Licensed under the EUPL-1.2 or later

#include "libbindensity.h"

void resampling_check_def(
  long new_n_in,
  long *isdef,
  long *istart, long *iend)
{
  // Avoid to compute undefined bins

  long i, k;

  for (k=0; k<new_n_in; k++) {
    for (i=istart[k]; i<iend[k]; i++) {
      if (!isdef[i]) {
        iend[k] = istart[k];
        break;
      }
    }
  }
}

void resampling_linear_weights(
  // Shapes
  long new_n_in,
  // Input
  double *dx, double *new_dx_in,
  double *delta,
  long *istart, long *isize,
  // Output
  double *w)
{
  // Compute weights according to linear interpolation rules

  long i, k;
  double *wk;

  wk = w;
  for (k=0; k<new_n_in; k++) {
    if (isize[k] == 0)
      continue;
    // Init
    for (i=0; i<isize[k]; i++) {
      wk[i] = dx[istart[k]+i];
    }
    // Right edge
    wk[isize[k]-1] = delta[k+1];
    // Left edge
    wk[0] -= delta[k];
    for (i=0; i<isize[k]; i++) {
      wk[i] /= new_dx_in[k];
    }
    wk += isize[k];
  }
}

void resampling_cubic_weights(
  // Shapes
  long new_n_in,
  // Input
  long *dl, long *dr,
  double *dx, double *new_dx_in,
  double *Fkleft, double *Fkcenter, double *Fkright,
  long *istart, long *isize,
  // Output
  double *w)
{
  // Compute weights according to cubic interpolation rules

  long i, k;
  double *wk;

  wk = w;
  for (k=0; k<new_n_in; k++) {
    if (isize[k] == 0)
      continue;
    // Init
    for (i=0; i<isize[k]; i++) {
      wk[i] = dx[istart[k]+i];
    }
    if (dl[k]) wk[0] = 0.0;
    if (dr[k+1]) wk[isize[k]-2] = 0.0;
    // Right edge
    wk[isize[k]-1] = Fkright[k+1];
    wk[isize[k]-1-dr[k+1]] += Fkcenter[k+1];
    wk[isize[k]-1-dl[k+1]-dr[k+1]] += Fkleft[k+1];
    // Left edge
    wk[dl[k]+dr[k]] -= Fkright[k];
    wk[dl[k]] -= Fkcenter[k];
    wk[0] -= Fkleft[k];
    for (i=0; i<isize[k]; i++) {
      wk[i] /= new_dx_in[k];
    }
    wk += isize[k];
  }
}

void resampling_y(
  long new_n_in, long kstart,
  long *istart, long *iend, long *isize,
  double *y, double *w,
  double *new_y)
{
  // Compute new bins density

  long i, k;
  double *wk;

  wk = w;
  for (k=0; k<new_n_in; k++) {
    if (isize[k] == 0)
      continue;
    new_y[kstart+k] = 0.0;
    for (i=istart[k]; i<iend[k]; i++) {
      new_y[kstart+k] += wk[i-istart[k]]*y[i];
    }
    wk += isize[k];
  }
}

void resampling_covariance_nd(
  // Shapes
  long nd, long new_n_in,
  // Input
  long *istart, long *iend,
  // Output
  long *new_nd)
{
  // Compute new covariance shape

  long k, l;

  new_nd[0] = 1;
  l = 0;
  k = 2;
  while (k < new_n_in) {
    while ((k < new_n_in) && (istart[k] < iend[l] + nd)) {
      k ++;
      new_nd[0] ++;
    }
    l ++;
    k ++;
  }
}

void resampling_covariance(
  // Shapes
  long n, long nd, long new_n,
  long kstart, long new_n_in,
  // Input
  double *cov,
  long *istart, long *iend, long *isize,
  double *w,
  // Output
  double *new_cov)
{
  // Compute new covariance

  long i, j, d, k, l, b;
  long l0;
  double *wk, *wl;

  wl = w;
  for (l=0; l<new_n_in; l++)
  {
    l0 = kstart + l;
    k = l;
    wk = wl;
    b = 0;
    while ((k < new_n_in) && (istart[k] < iend[l] + nd))
    {
      for (d=-nd; d<=nd; d++)
      {
        for (j=MAX(istart[l], istart[k]-d); j<MIN(iend[l], iend[k]-d); j++)
        {
          i = j + d;
          new_cov[new_n*b+l0] += (wk[i-istart[k]] * wl[j-istart[l]]
            * cov[n*ABS(d)+MIN(i,j)]);
        }
      }
      wk += isize[k];
      k ++;
      b ++;
    }
    wl += isize[l];
  }
}
