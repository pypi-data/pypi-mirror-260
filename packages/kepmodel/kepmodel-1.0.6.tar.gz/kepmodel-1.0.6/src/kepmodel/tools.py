# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np


def _solve_eM0_single(x, indices, datatype, emax):
  r"""
  Solve for e, M0 from the amplitudes of the fundamental and first harmonics
  in a time series (rv or astro).
  """

  xi = x[indices]
  dx = np.zeros((4, x.size))
  for i, j in enumerate(indices):
    dx[i, j] = 1
  x2 = xi * xi

  # Fundamental
  ampf2 = x2[0] + x2[1]
  dampf2 = 2 * (xi[0] * dx[0] + xi[1] * dx[1])

  argf = np.arctan2(-xi[1], xi[0])
  dargf = (xi[1] * dx[0] - xi[0] * dx[1]) / ampf2

  # First harmonics
  amph2 = x2[2] + x2[3]
  damph2 = 2 * (xi[2] * dx[2] + xi[3] * dx[3])

  argh = np.arctan2(-xi[3], xi[2])
  dargh = (xi[3] * dx[2] - xi[2] * dx[3]) / amph2

  # Ratio
  amprho = np.sqrt(amph2 / ampf2)
  if datatype == 'astro':
    amprho *= 2
  damprho = amprho / 2 * (damph2 / amph2 - dampf2 / ampf2)

  argrho = argh - argf
  dargrho = dargh - dargf

  # Phase correction for e^3
  phi = 2 * argf - argh
  if datatype == 'astro':
    phi += np.pi / 2
  dphi = 2 * dargf - dargh

  r = (1 - np.cos(2 * phi) / 6) / 4
  dr = np.sin(2 * phi) / 12 * dphi

  # Solve eccentricity: amprho = e (1 - r e^2)
  if amprho > emax * (1 - r * emax**2):
    e = emax
  else:
    h = np.sqrt(3 * r) / 2
    e = np.cos((np.pi + np.arccos(3 * h * amprho)) / 3) / h
  de = (damprho + e**3 * dr) / (1 - 3 * r * e**2)

  # Solve M0
  a = 1 - r * e**2
  da = -(e**2) * dr - 2 * r * e * de
  b = -np.sin(2 * phi) / 24 * e**2
  db = -(np.cos(2 * phi) * e**2 * dphi + np.sin(2 * phi) * e * de) / 12

  M0 = argrho - np.arctan2(b, a)
  dM0 = dargrho - (a * db - b * da) / (a**2 + b**2)

  return (e, M0, de, dM0)


def solve_eM0(x, Cx, indices, datatype, emax):
  r"""
  Solve for the eccentricity and mean anomaly at `t = 0`,
  from the amplitudes of the fundamental and the first harmonics in
  one or more time series (radial velocity and/or astrometry).

  Parameters
  ----------
  x : (4 n,) ndarray
    Coefficients obtained after a linear fit of the time series,
    with the :math:`\cos` and :math:`\sin` of the fundamental
    and first harmonics.
  Cx : (4 n, 4n) ndarray
    Covariance matrix of the parameters `x`.
  indices : (n, 4) ndarray
    Indices corresponding to the :math:`\cos` and :math:`\sin` of the fundamental,
    and :math:`\cos` and :math:`\sin` of the first harmonics for each time series.
  datatype : bool or (n,) ndarray
    Type of each time series ('rv' or 'astro')
  emax : double
    Maximum allowed eccentricity.

  Returns
  -------
  e : double
    Eccentricity estimate.
  M0 : double
    Estimate of the mean anomaly at `t = 0`.
  """

  if len(indices.shape) != 2:
    indices = indices.reshape(1, -1)
  n = indices.shape[0]
  if isinstance(datatype, str):
    datatype = np.full(n, datatype)
  if n == 1:
    e, M0, _, _ = _solve_eM0_single(x, indices[0], datatype[0], emax)
    return (e, M0)
  ab = np.empty(2 * n)
  dabdx = np.empty((2 * n, x.size))
  for k in range(n):
    ek, M0k, dek, dM0k = _solve_eM0_single(x, indices[k], datatype[k], emax)
    ck = np.cos(M0k)
    sk = np.sin(M0k)
    ab[k] = ek * ck
    ab[k + n] = ek * sk
    dabdx[k] = ck * dek - ab[k + n] * dM0k
    dabdx[k + n] = sk * dek + ab[k] * dM0k
  Cab = dabdx @ Cx @ dabdx.T
  iCab = np.linalg.inv(Cab)
  A = np.array(n * [[1, 0]] + n * [[0, 1]])
  Cth = np.linalg.inv(A.T @ iCab @ A)
  th = Cth @ A.T @ iCab @ ab
  return (min(np.sqrt(th[0] ** 2 + th[1] ** 2), emax), np.arctan2(th[1], th[0]))


def _M2E(M, e, ftol=5e-16, maxiter=10):
  r"""
  Compute eccentric anomaly from mean anomaly (and eccentricity).
  """

  E = M + 0.85 * np.sign(np.sin(M)) * e
  dE = np.array([1.0 + ftol])
  for _ in range(maxiter):
    d3 = e * np.cos(E)
    d2 = e * np.sin(E)
    d1 = 1 - d3
    diff = M - E + d2
    dE = diff / d1
    dE = diff / (d1 + dE * d2 / 2)
    dE = diff / (d1 + dE * (d2 / 2 + dE * d3 / 6))
    E += dE
    if max(abs(dE)) < ftol:
      break
  return E


def _E2v(E, e):
  r"""
  Compute true anomaly from eccentric anomaly (and eccentricity).
  """

  v = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))
  return v


def _v2E(v, e):
  r"""
  Compute eccentric anomaly from true anomaly (and eccentricity).
  """

  E = 2 * np.arctan(np.sqrt((1 - e) / (1 + e)) * np.tan(v / 2))
  return E


def _E2M(E, e):
  r"""
  Compute mean anomaly from eccentric anomaly (and eccentricity).
  """

  M = E - e * np.sin(E)
  return M


def design_matrix_Kom(t, P, e, M0):
  r"""
  Design matrix for the linear fit of
  :math:`K\cos(\omega)` and :math:`K\sin(\omega)`.

  Parameters
  ----------
  t : (n,) ndarray
    Times of the measurements.
  P : double
    Orbital period.
  e : double
    Eccentricity
  M0 : double
    Mean anomaly at `t = 0`.

  Returns
  -------
  phi : (2, n) ndarray
    Design matrix.
  """

  M = M0 + 2 * np.pi * t / P
  E = _M2E(M, e)
  v = _E2v(E, e)
  return np.array([np.cos(v) + e, -np.sin(v)])


def design_matrix_ABFG(t, P, e, M0, cth, sth):
  r"""
  Design matrix for the linear fit of Thiele-Innes coefficients
  :math:`A`, :math:`B`, :math:`F`, and :math:`G`.

  Parameters
  ----------
  t : (n,) ndarray
    Times of the measurements.
  P : double
    Orbital period.
  e : double
    Eccentricity
  M0 : double
    Mean anomaly at `t = 0`.
  cth, sth : (n,) ndarrays
    :math:`\cos` and :math:`\sin` of the scan angle.

  Returns
  -------
  phi : (4, n) ndarray
    Design matrix.
  """

  M = M0 + 2 * np.pi * t / P
  E = _M2E(M, e)
  X = np.cos(E) - e
  Y = np.sqrt(1 - e * e) * np.sin(E)
  return np.array([X * cth, X * sth, Y * cth, Y * sth])


def smooth_timeseries(t, y, kernel, tau):
  r"""
  Apply the specified kernel to smooth the time series.

  Parameters
  ----------
  t : (n,) ndarray
    Times of the measurements.
  y : (n,) ndarray
    Time series values.
  kernel : function
    Kernel function for the smoothing.
  tau : double
    Smoothing time scale.

  Returns
  -------
  z : (n,) ndarray
    Smoothed time series.
  """

  kdef = ~np.isnan(y)
  x = t / tau
  dx = x[:, None] - x[None, kdef]
  w = kernel(dx)
  w /= np.sum(w, axis=1)[:, None]
  z = w @ y[kdef]
  return z


def gaussian_kernel(x):
  """
  Gaussian kernel for the :func:`smooth_timeseries` function.

  Parameters
  ----------
  x : ndarray
    Lag renormalized by time scale.

  Returns
  -------
  w : ndarray
    Corresponding weight.
  """
  return np.exp(-0.5 * x * x)


def box_kernel(x):
  """
  Box kernel for the :func:`smooth_timeseries` function.

  Parameters
  ----------
  x : ndarray
    Lag renormalized by time scale.

  Returns
  -------
  w : ndarray
    Corresponding weight.
  """
  return np.abs(x) <= 1.0


def epanechnikov_kernel(x):
  """
  Epanechnikov kernel for the :func:`smooth_timeseries` function.

  Parameters
  ----------
  x : ndarray
    Lag renormalized by time scale.

  Returns
  -------
  w : ndarray
    Corresponding weight.
  """
  return (np.abs(x) <= 1.0) * (1.0 - x * x)
