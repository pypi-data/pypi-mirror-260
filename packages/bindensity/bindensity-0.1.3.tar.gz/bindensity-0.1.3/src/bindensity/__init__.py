# -*- coding: utf-8 -*-

# Copyright 2020-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np

from . import libbindensity


def add(f, covf, g, covg):
  r"""
  Add two densities computed on the same bins and propagate the covariance.

  Parameters
  ----------
  f, g : (n,) ndarrays
    Densities.
  covf : (ndf+1, n) ndarrays
    Covariance matrix of f in lower banded form.
  covg : (ndg+1, n) ndarrays
    Covariance matrix of g in lower banded form.

  Returns
  -------
  h : (n,) ndarray
    The sum of the densities f and g.
  covh : (ndh+1, n) ndarray
    The covariance matrix of h in lower banded form
    (ndh is the max of ndf and ndg).
  """

  if covf.shape[0] < covg.shape[0]:
    return add(g, covg, f, covf)
  h = f + g
  covh = covf.copy()
  for d in range(covg.shape[0]):
    covh[d] += covg[d]
  return (h, covh)


def iadd(f, covf, g, covg):
  r"""
  In-place version of :func:`add`
  (f and covf are overwritten by the result).
  """

  f += g
  if covf.shape[0] < covg.shape[0]:
    covf.resize(covg.shape, refcheck=False)
  for d in range(covg.shape[0]):
    covf[d] += covg[d]


def sum(f_list, covf_list):
  r"""
  Sum a list of densities computed on the same bins
  and propagate the covariance.

  Parameters
  ----------
  f_list : list of (n,) ndarrays
    Densities.
  covf_list : list of (ndfk+1, n) ndarrays
    Covariance matrices in lower banded form.

  Returns
  -------
  h : (n,) ndarray
    The sum of densities.
  covh : (ndh+1, n) ndarray
    The covariance matrix of h in lower banded form
    (ndh is the max of all ndfk).
  """

  n = f_list[0].shape[0]
  ndh = np.max([covf.shape[0] for covf in covf_list])
  h = np.zeros(n)
  covh = np.zeros((ndh, n))
  for f, covf in zip(f_list, covf_list):
    iadd(h, covh, f, covf)
  return (h, covh)


def mul_array(f, covf, g):
  r"""
  Multiply a density by a vector of coefficients and propagate the covariance.

  Parameters
  ----------
  f : (n,) ndarrays
    Density.
  covf : (nd+1, n) ndarrays
    Covariance matrix of f in lower banded form.
  g : (n,) ndarrays
    Vector of coefficients.

  Returns
  -------
  h : (n,) ndarray
    The product of f and g.
  covh : (nd+1, n) ndarray
    The covariance matrix of h in lower banded form.
  """

  n = f.shape[0]
  h = f * g
  covh = np.empty_like(covf)
  for d in range(covf.shape[0]):
    covh[d, : n - d] = covf[d, : n - d] * g[d:] * g[: n - d]
  return (h, covh)


def imul_array(f, covf, g):
  r"""
  In-place version of :func:`mul_array`
  (f and covf are overwritten by the result).
  """

  n = f.shape[0]
  f *= g
  for d in range(covf.shape[0]):
    covf[d, : n - d] *= g[d:] * g[: n - d]


def mul(f, covf, g, covg):
  r"""
  Multiply two densities computed on the same bins
  and propagate the covariance.

  Parameters
  ----------
  f, g : (n,) ndarrays
    Densities.
  covf : (ndf+1, n) ndarrays
    Covariance matrix of f in lower banded form.
  covg : (ndg+1, n) ndarrays
    Covariance matrix of g in lower banded form.

  Returns
  -------
  h : (n,) ndarray
    The product of the densities f and g.
  covh : (ndh+1, n) ndarray
    The covariance matrix of h in lower banded form
    (ndh is the max of ndf and ndg).
  """

  if covf.shape[0] < covg.shape[0]:
    return mul(g, covg, f, covf)
  n = f.shape[0]
  h = f * g
  covh = np.empty_like(covf)
  for d in range(covf.shape[0]):
    covh[d, : n - d] = covf[d, : n - d] * g[d:] * g[: n - d]
  for d in range(covg.shape[0]):
    covh[d, : n - d] += (f[d:] * f[: n - d] + covf[d, : n - d]) * covg[d, : n - d]
  return (h, covh)


def imul(f, covf, g, covg):
  r"""
  In-place version of :func:`mul`
  (f and covf are overwritten by the result).
  """

  n = f.shape[0]
  ndf = covf.shape[0]
  ndg = covg.shape[0]
  f *= g
  if ndf < ndg:
    covf.resize(covg.shape, refcheck=False)
  for d in range(min(ndf, ndg)):
    covf[d, : n - d] *= g[d:] * g[: n - d] + covg[d, : n - d]
  for d in range(ndg, ndf):
    covf[d, : n - d] *= g[d:] * g[: n - d]
  for d in range(ndg):
    covf[d, : n - d] += f[d:] * f[: n - d] * covg[d, : n - d]


def prod(f_list, covf_list):
  r"""
  Compute the product of a list of densities computed on the same bins
  and propagate the covariance.

  Parameters
  ----------
  f_list : list of (n,) ndarrays
    Densities.
  covf_list : list of (ndfk+1, n) ndarrays
    Covariance matrices in lower banded form.

  Returns
  -------
  h : (n,) ndarray
    The product of densities.
  covh : (ndh+1, n) ndarray
    The covariance matrix of h in lower banded form
    (ndh is the max of all ndfk).
  """

  n = f_list[0].shape[0]
  ndh = np.max([covf.shape[0] for covf in covf_list])
  h = np.ones(n)
  covh = np.zeros((ndh, n))
  for f, covf in zip(f_list, covf_list):
    imul(h, covh, f, covf)
  return (h, covh)


def inv(f, covf):
  r"""
  Compute the inverse of a density and propagate the covariance.

  Parameters
  ----------
  f, g : (n,) ndarrays
    Density.
  covf : (nd+1, n) ndarrays
    Covariance matrix of f in lower banded form.

  Returns
  -------
  h : (n,) ndarray
    The inverse of f.
  covh : (nd+1, n) ndarray
    The covariance matrix of h in lower banded form.
  """

  # Assume covf << muf and perform first order series expansion
  # f ~ N(muf, covf)
  # 1/f = 1/(muf + eps) = 1/muf 1/(1+eps/muf) ~ 1/muf (1-eps/muf)
  # We thus approximate the random variable 1/f by
  # h = 1/muf - eps/muf^2
  # h ~ N(1/muf, covf/(muf muf^T)^2)

  n = f.shape[0]
  h = 1 / f
  h2 = h * h
  covh = np.empty_like(covf)
  for d in range(covf.shape[0]):
    covh[d, : n - d] = covf[d, : n - d] * h2[d:] * h2[: n - d]
  return (h, covh)


def iinv(f, covf):
  r"""
  In-place version of :func:`iinv`
  (f and covf are overwritten by the result).
  """

  n = f.shape[0]
  np.divide(1, f, out=f)
  f2 = f * f
  for d in range(covf.shape[0]):
    covf[d, : n - d] *= f2[d:] * f2[: n - d]


def div(f, covf, g, covg):
  r"""
  Divide two densities computed on the same bins
  and propagate the covariance.

  Parameters
  ----------
  f, g : (n,) ndarrays
    Densities.
  covf : (ndf+1, n) ndarrays
    Covariance matrix of f in lower banded form.
  covg : (ndg+1, n) ndarrays
    Covariance matrix of g in lower banded form.

  Returns
  -------
  h : (n,) ndarray
    The division of f by g.
  covh : (ndh+1, n) ndarray
    The covariance matrix of h in lower banded form
    (ndh is the max of ndf and ndg).
  """

  return mul(f, covf, *inv(g, covg))


def idiv(f, covf, g, covg):
  r"""
  In-place version of :func:`div`
  (f and covf are overwritten by the result).
  """

  imul(f, covf, *inv(g, covg))


def iidiv(f, covf, g, covg):
  r"""
  Double in-place version of :func:`div`
  (f and covf are overwritten by the result,
  g and covg are overwritten by the inverse of g).
  """

  iinv(g, covg)
  imul(f, covf, g, covg)


def resampling(new_x, x, y, cov=None, kind='cubic'):
  r"""
  Resample data on new bins using a linear or cubic
  interpolation of the cumulative.

  The linear interpolation of the cumulative corresponds to
  a uniform density on the bins.
  The only rule necessary to compute the interpolation is
  the conservation of the integral over each original bin
  (the value of the cumulative is fixed at each edge of a bin)
  This rule allows to determine the 2 coefficients of the interpolation.

  The cubic interpolation of the cumulative corresponds to
  a quadratic density on the bins.
  In order to minimize the correlation between new bins,
  the cubic interpolation is much simplified compared to
  a cubic spline interpolation.
  In particular, the interpolation is not C2 but only C1,
  which means that the density is continuous but not derivable.
  The rules to compute the interpolation are:
  - Conservation of the integral over each original bin
  (the value of the cumulative is fixed at each edge of a bin)
  - The derivative at an edge between two bins is fixed at
  the mean between the densities over each of the two bins.
  Those two rules allow to determine the 4 coefficients of the interpolation.

  Parameters
  ----------
  new_x : (new_n+1,) ndarray
    Edges of the new bins.
  x : (n+1,) ndarray
    Edges of the original bins.
  y : (n,) ndarray
    Density over each original bin.
  cov : (nd+1, n) ndarray, optional
    Covariance matrix of the density over original bins in lower banded form.
  kind : str, optional
    Kind of interpolation to use ('linear' or 'cubic').
    Default is 'cubic'.

  Returns
  -------
  new_y : (new_n,) ndarray
    The density resampled on the new bins.
  new_cov : (new_nd+1, new_n) ndarray
    The covariance of the new bins in lower banded form (if cov is provided).
  """

  # Check shapes
  new_n = new_x.size - 1
  n = y.size
  if x.size != n + 1:
    raise ValueError(
      'Incompatible sizes. ' + 'For n bins, x should be of size n+1 and y of size n.'
    )
  if cov is not None:
    if cov.shape[1] != n:
      raise ValueError('The shape of cov should be (nd+1, n).')
    nd = cov.shape[0] - 1
  dx = x[1:] - x[:-1]
  if np.any(dx <= 0):
    raise ValueError(
      'The bin edges should be provided ' + 'in strictly increasing order.'
    )
  # Check nans
  isdef = (y == y).astype(int)
  # Find the original bins in which the new bin edges are.
  ix = np.searchsorted(x, new_x, 'right').astype(int) - 1
  # Restrict to new bins that fall inside the original range.
  kstart = np.searchsorted(ix, 0, 'left').astype(int)
  kend = np.searchsorted(ix, n, 'left').astype(int)
  new_n_in = kend - kstart - 1
  new_x_in = new_x[kstart:kend]
  ix_in = ix[kstart:kend]
  new_dx_in = new_x_in[1:] - new_x_in[:-1]
  if np.any(new_dx_in <= 0):
    raise ValueError(
      'The bin edges should be provided ' + 'in strictly increasing order.'
    )
  # Position on each original bin
  delta = new_x_in - x[ix_in]
  # Range of original bins on which explicitly depends each new bin
  if kind == 'linear':
    istart = ix_in[:-1]
    iend = ix_in[1:] + 1
  elif kind == 'cubic':
    isdefleft = np.insert(isdef[:-1], 0, 0)
    isdefright = np.append(isdef[1:], 0)
    dl = isdefleft[ix_in]
    dr = isdefright[ix_in]
    istart = (ix_in - dl)[:-1]
    iend = (ix_in + dr + 1)[1:]
    # Precompute useful quantities for cubic weights
    t = delta / dx[ix_in]
    t2 = t * t
    t3 = t2 * t
    # t = 0 on the left border of the original bin and 1 on the right
    # Cubic Hermite basis
    # For a cubic polynomial f
    # f(t) = f(0)*h00(t) + f(1)*h01(t) + f'(0)*h10(t) + f'(1)*h11(t)
    h01 = 3 * t2 - 2 * t3
    h10 = t3 - 2 * t2 + t
    h11 = t3 - t2
    # Integral between the original bin left edge
    # and the position of the new edge,
    # as a function of the density over the 3 consecutive original bins.
    Fkcenter = (h01 + 0.5 * (h10 + h11)) * dx[ix_in]
    Fkleft = 0.5 * h10 * dx[ix_in]
    Fkright = 0.5 * h11 * dx[ix_in]
  else:
    raise Exception("The interpolation kind must be 'linear' or 'cubic'.")

  # Avoid to compute undefined bins
  libbindensity.resampling_check_def(new_n_in, isdef, istart, iend)
  isize = iend - istart

  # Weight of each original bin density to compute the new bins
  w = np.empty(np.sum(isize))
  if kind == 'linear':
    libbindensity.resampling_linear_weights(
      new_n_in, dx, new_dx_in, delta, istart, isize, w
    )
  else:
    libbindensity.resampling_cubic_weights(
      new_n_in, dl, dr, dx, new_dx_in, Fkleft, Fkcenter, Fkright, istart, isize, w
    )

  # Compute new bins density
  new_y = np.full(new_n, np.nan)
  libbindensity.resampling_y(new_n_in, kstart, istart, iend, isize, y, w, new_y)

  if cov is None:
    return new_y

  # Compute new covariance shape
  new_nd = np.empty(1, dtype=int)
  libbindensity.resampling_covariance_nd(nd, new_n_in, istart, iend, new_nd)
  new_nd = new_nd[0]

  # Compute new covariance
  new_cov = np.zeros((new_nd + 1, new_n))
  libbindensity.resampling_covariance(
    n, nd, new_n, kstart, new_n_in, cov, istart, iend, isize, w, new_cov
  )

  return (new_y, new_cov)
