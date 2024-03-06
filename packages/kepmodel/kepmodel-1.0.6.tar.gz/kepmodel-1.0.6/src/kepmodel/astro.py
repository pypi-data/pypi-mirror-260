# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np

from . import tools
from .timeseries import SingleTimeseriesModel


class AstroModel(SingleTimeseriesModel):
  r"""
  Astrometric model.

  Parameters
  ----------
  t : (n,) ndarray
    Times of astrometric measurements.
  s : (n,) ndarray
    Astrometric abscissa.
  cth : (n,) ndarray
    Cosine of the scan angle (GAIA convention).
  sth : (n,) ndarray
    Sine of the scan angle (GAIA convention).
  cov : spleaf.cov.Cov (Optional)
    S+LEAF covariance matrix of the astrometric time series.
    If `cov` is not provided, the S+LEAF terms should be provided as `**kwargs`.
  **kwargs :
    Optional arguments (S+LEAF terms) provided to spleaf.cov.Cov to generate
    the S+LEAF covariance matrix of the astrometric time series.
    This is only used if `cov` is not directly provided.
  """

  def __init__(
    self, t, s, cth, sth, angular_keplerian_param=True, series_index=[], **kwargs
  ):
    super().__init__(t, s, series_index, **kwargs)
    self.cth = cth
    self.sth = sth
    self._angular_keplerian_param = angular_keplerian_param

  def _guess_keplerian_harmfit(self, P):
    res = self.residuals()
    u = self.cov.solveL(res) / self.cov.sqD()
    nu = 2 * np.pi / P
    nut_rad = nu * self.t
    Mt = np.concatenate((np.zeros((8, self.full_n)), self.get_fit_lin_M()[0]))
    Mt[0, self.series_index[0]] = self.cth * np.cos(nut_rad)
    Mt[1, self.series_index[0]] = self.sth * np.cos(nut_rad)
    Mt[2, self.series_index[0]] = self.cth * np.sin(nut_rad)
    Mt[3, self.series_index[0]] = self.sth * np.sin(nut_rad)
    Mt[4, self.series_index[0]] = self.cth * np.cos(2 * nut_rad)
    Mt[5, self.series_index[0]] = self.sth * np.cos(2 * nut_rad)
    Mt[6, self.series_index[0]] = self.cth * np.sin(2 * nut_rad)
    Mt[7, self.series_index[0]] = self.sth * np.sin(2 * nut_rad)
    Nt = np.array([self.cov.solveL(Mk) / self.cov.sqD() for Mk in Mt])
    covx = np.linalg.inv(Nt @ Nt.T)
    x = covx @ Nt @ u
    return (x[:8], covx[:8, :8])

  def _guess_keplerian_other(self, P, e, M0_rad):
    res = self.residuals()
    u = self.cov.solveL(res) / self.cov.sqD()
    Mt = np.concatenate((np.zeros((4, self.full_n)), self.get_fit_lin_M()[0]))
    Mt[:4, self.series_index[0]] = tools.design_matrix_ABFG(
      self.t, P, e, M0_rad, self.cth, self.sth
    )
    Nt = np.array([self.cov.solveL(Mk) / self.cov.sqD() for Mk in Mt])
    covx = np.linalg.inv(Nt @ Nt.T)
    x = covx @ Nt @ u
    return (x, covx)

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
    e, M0_rad = tools.solve_eM0(
      x,
      covx,
      np.array([np.arange(k, 8, 2) for k in range(2)]),
      datatype='astro',
      emax=emax,
    )
    x, _ = self._guess_keplerian_other(P, e, M0_rad)
    if not self._angular_keplerian_param:
      plx = self.get_param('lin.plx')
      if 'lin.plx' in self._default_fit_param:
        kplx = 4 + [
          par for par in self._default_fit_param if par.startswith('lin.')
        ].index('lin.plx')
        plx += x[kplx]
      x[:4] /= plx
    return (
      np.concatenate(([P, M0_rad, e], x[:4])),
      ['P', 'M0', 'e', 'TIA', 'TIB', 'TIF', 'TIG'],
    )

  def keplerian_model(self):
    r"""
    Compute the Keplerian part of the model.

    Returns
    -------
    s : (n,) ndarray
      Astrometric abscissa.
    """

    self._kep_s = np.zeros_like(self.t)
    for kep in self.keplerian.values():
      ddelta, dalpha = kep.astro(self.t)
      self._kep_s += self.cth * ddelta + self.sth * dalpha
    self._kep_coef = 1
    if not self._angular_keplerian_param:
      self._kep_coef = self.get_param('lin.plx')
    return self._kep_coef * self._kep_s

  def _keplerian_grad(self, grad_res, grad_dict):
    if not self._angular_keplerian_param:
      if 'lin.plx' in self._default_fit_param:
        grad_dict['lin.plx'] -= self._kep_s.dot(grad_res)
    grad_res = grad_res * self._kep_coef
    grad_ddelta = -self.cth * grad_res
    grad_dalpha = -self.sth * grad_res
    for name in self.keplerian:
      grad_kep = self.keplerian[name].astro_back(grad_ddelta, grad_dalpha)
      for par, grad_par in zip(self.keplerian[name].get_param(), grad_kep):
        key = f'kep.{name}.{par}'
        if key in self._default_fit_param:
          grad_dict[key] += grad_par

  def _perio_phi(self, cosnut, sinnut):
    return [self.cth * cosnut, self.sth * cosnut, self.cth * sinnut, self.sth * sinnut]

  def _fap_d(self):
    return 4

  def _fap_sqla(self, numax):
    W = self.cov.expandInv()[self.series_index[0], self.series_index[0]]
    nuDt = numax * (self.t[None, :] - self.t[:, None])
    sincnuDt = np.sinc(nuDt / np.pi)
    coscnuDt = -np.sinc(nuDt / (2 * np.pi)) * np.sin(nuDt / 2)
    cosDth = (
      self.cth[None, :] * self.cth[:, None] + self.sth[None, :] * self.sth[:, None]
    )
    sinDth = (
      self.cth[None, :] * self.sth[:, None] - self.sth[None, :] * self.cth[:, None]
    )
    sincA = sincnuDt * cosDth
    sincB = coscnuDt * sinDth
    sincp = sincA + sincB
    sincm = sincA - sincB
    la = []
    for sinc in [sincp, sincm]:
      Wsinc = W * sinc
      Wsinct = Wsinc @ self.t
      q = np.sum(Wsinc)
      s = np.sum(Wsinct)
      r = self.t @ Wsinct
      la.append(r / q - (s / q) ** 2)
    sqla = np.sqrt(la)
    return sqla
