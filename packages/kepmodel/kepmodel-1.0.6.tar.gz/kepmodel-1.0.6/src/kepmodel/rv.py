# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np

from . import tools
from .timeseries import SingleTimeseriesModel


class RvModel(SingleTimeseriesModel):
  r"""
  Radial velocity model.

  Parameters
  ----------
  t : (n,) ndarray
    Times of radial velocity measurements.
  rv : (n,) ndarray
    Radial velocity values.
  cov : spleaf.cov.Cov (Optional)
    S+LEAF covariance matrix of the radial velocity time series.
    If `cov` is not provided, the S+LEAF terms should be provided as `**kwargs`.
  **kwargs :
    Optional arguments (S+LEAF terms) provided to spleaf.cov.Cov to generate
    the S+LEAF covariance matrix of the radial velocity time series.
    This is only used if `cov` is not directly provided.
  """

  def __init__(self, t, rv, series_index=[], **kwargs):
    super().__init__(t, rv, series_index, **kwargs)

  def _guess_keplerian_harmfit(self, P):
    res = self.residuals()
    u = self.cov.solveL(res) / self.cov.sqD()
    nu = 2 * np.pi / P
    nut_rad = nu * self.t
    Mt = np.concatenate((np.zeros((4, self.full_n)), self.get_fit_lin_M()[0]))
    Mt[0, self.series_index[0]] = np.cos(nut_rad)
    Mt[1, self.series_index[0]] = np.sin(nut_rad)
    Mt[2, self.series_index[0]] = np.cos(2 * nut_rad)
    Mt[3, self.series_index[0]] = np.sin(2 * nut_rad)
    Nt = np.array([self.cov.solveL(Mk) / self.cov.sqD() for Mk in Mt])
    covx = np.linalg.inv(Nt @ Nt.T)
    x = covx @ Nt @ u
    return (x[:4], covx[:4, :4])

  def _guess_keplerian_other(self, P, e, M0_rad):
    res = self.residuals()
    u = self.cov.solveL(res) / self.cov.sqD()
    Mt = np.concatenate((np.zeros((2, self.full_n)), self.get_fit_lin_M()[0]))
    Mt[:2, self.series_index[0]] = tools.design_matrix_Kom(self.t, P, e, M0_rad)
    Nt = np.array([self.cov.solveL(Mk) / self.cov.sqD() for Mk in Mt])
    covx = np.linalg.inv(Nt @ Nt.T)
    x = covx @ Nt @ u
    return (x[:2], covx[:2, :2])

  def guess_keplerian_param(self, P, emax=0.95):
    r"""
    Guess the Keplerian parameters from the period.

    Parameters
    ----------
    P : float
      Period of the Keplerian.
    emax : float
      Maximum allowed eccentricity.

    Returns
    -------
    value : (p,) ndarray
      Values of the Keplerian parameters.
    param : list
      List of the Keplerian parameters names.
    """

    x, covx = self._guess_keplerian_harmfit(P)
    e, M0_rad = tools.solve_eM0(x, covx, np.arange(4), datatype='rv', emax=emax)
    x, _ = self._guess_keplerian_other(P, e, M0_rad)
    K = np.sqrt(x[0] ** 2 + x[1] ** 2)
    omega_rad = np.arctan2(x[1], x[0])
    return (np.array([P, M0_rad, e, K, omega_rad]), ['P', 'M0', 'e', 'K', 'omega'])

  def keplerian_model(self, t=None):
    r"""
    Compute the Keplerian part of the model.

    Parameters
    ----------
    t : (m,) ndarray or None
      Times at which to compute the Keplerian model.
      If None, the measurements times are used.

    Returns
    -------
    rv : (m,) ndarray
      Keplerian model time series.
    """

    if t is None:
      t = self.t
    rv = np.zeros_like(t)
    for kep in self.keplerian.values():
      rv += kep.rv(t)
    return rv

  def _keplerian_grad(self, grad_res, grad_dict):
    grad_res = -grad_res
    for name in self.keplerian:
      grad_kep = self.keplerian[name].rv_back(grad_res)
      for par, grad_par in zip(self.keplerian[name].get_param(), grad_kep):
        key = f'kep.{name}.{par}'
        if key in self._default_fit_param:
          grad_dict[key] += grad_par

  def _perio_phi(self, cosnut, sinnut):
    return [cosnut, sinnut]

  def _fap_d(self):
    return 2

  def _fap_sqla(self, numax):
    W = self.cov.expandInv()[self.series_index[0], self.series_index[0]]
    nuDt = numax * (self.t[None, :] - self.t[:, None])
    sinc = np.sinc(nuDt / np.pi)
    Wsinc = W * sinc
    Wsinct = Wsinc @ self.t
    q = np.sum(Wsinc)
    s = np.sum(Wsinct)
    r = self.t @ Wsinct
    la = r / q - (s / q) ** 2
    sqla = np.sqrt(la)
    return np.array([sqla])
