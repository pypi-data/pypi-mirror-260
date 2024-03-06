# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import warnings

import numpy as np

from . import tools
from .timeseries import MultiTimeseriesModel


class AstroRvModel(MultiTimeseriesModel):
  r"""
  Model combining Astrometry and radial velocities.

  Parameters
  ----------
  astro : AstroModel
    Astrometric model.
  rv : RvModel
    Radial velocity model.
  """

  def __init__(self, astro, rv):
    super().__init__(astro=astro, rv=rv)
    self.astro = astro
    self.rv = rv
    # Enforce use of physical parameters for the astrometry
    if self.astro._angular_keplerian_param:
      warnings.warn(
        'AstroRvModel cannot use angular keplerian parameters,\n'
        'switching AstroModel to use physical keplerian parameters',
        UserWarning,
      )
    self.astro._angular_keplerian_param = False

  def _guess_keplerian_harmfit(self, P):
    x_astro, covx_astro = self.astro._guess_keplerian_harmfit(P)
    x_rv, covx_rv = self.rv._guess_keplerian_harmfit(P)
    x = np.concatenate((x_astro, x_rv))
    covx = np.zeros((x.size, x.size))
    covx[: x_astro.size, : x_astro.size] = covx_astro
    covx[x_astro.size :, x_astro.size :] = covx_rv
    return (x, covx)

  def guess_keplerian_param(self, P, emax=0.95, velocity_coef=1731456.8368055555):
    r"""
    Guess the Keplerian parameters from the period.

    Parameters
    ----------
    P : float
      Period of the Keplerian.
    emax : float
      Maximum allowed eccentricity.
    velocity_coef : double
      Coefficient used for the definition of the velocity unit
      as a function of the distance and time units.
      The default value (1731456.8368055555) corresponds to
      AU for the distance, d for the time, and m/s for the velocity
      (following `IAU - Resolution B3 <http://arxiv.org/abs/1510.07674>`_).

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
      np.array([np.arange(k, 8, 2) for k in range(2)] + [np.arange(8, 12)]),
      datatype=['astro', 'astro', 'rv'],
      emax=emax,
    )
    x_astro, covx_astro = self.astro._guess_keplerian_other(P, e, M0_rad)
    x_rv, covx_rv = self.rv._guess_keplerian_other(P, e, M0_rad)

    # Compute U = (as_AU sini)**2 cos(2 omega)
    #         V = (as_AU sini)**2 sin(2 omega)
    # Astro:
    dx_astro = np.zeros((4, x_astro.size))
    for k in range(4):
      dx_astro[k, k] = 1
    xdx_astro = x_astro[:4, None] * dx_astro
    dplx = np.zeros_like(x_astro)
    plx = self.get_param('astro.lin.plx')
    if 'lin.plx' in self.astro._default_fit_param:
      kplx = 4 + [
        par for par in self.astro._default_fit_param if par.startswith('lin.')
      ].index('lin.plx')
      plx += x_astro[kplx]
      dplx[kplx] = 1

    U_astro = (
      x_astro[0] ** 2 + x_astro[1] ** 2 - x_astro[2] ** 2 - x_astro[3] ** 2
    ) / plx**2
    dU_astro = (
      2 * (xdx_astro[0] + xdx_astro[1] - xdx_astro[2] - xdx_astro[3]) / plx**2
      - 2 * U_astro / plx * dplx
    )
    varU_astro = dU_astro @ covx_astro @ dU_astro
    V_astro = -2 * (x_astro[0] * x_astro[2] + x_astro[1] * x_astro[3]) / plx**2
    dV_astro = (
      -2
      * (
        dx_astro[0] * x_astro[2]
        + dx_astro[1] * x_astro[3]
        + x_astro[0] * dx_astro[2]
        + x_astro[1] * dx_astro[3]
      )
      / plx**2
      - 2 * V_astro / plx * dplx
    )
    varV_astro = dV_astro @ covx_astro @ dV_astro

    # RV:
    dx_rv = np.zeros((2, x_rv.size))
    for k in range(2):
      dx_rv[k, k] = 1
    coef = (1 - e**2) * (P / (2 * np.pi * velocity_coef)) ** 2
    U_rv = coef * (x_rv[0] ** 2 - x_rv[1] ** 2)
    dU_rv = 2 * coef * (x_rv[0] * dx_rv[0] - x_rv[1] * dx_rv[1])
    varU_rv = dU_rv @ covx_rv @ dU_rv
    V_rv = 2 * coef * x_rv[0] * x_rv[1]
    dV_rv = 2 * coef * (x_rv[1] * dx_rv[0] + x_rv[0] * dx_rv[1])
    varV_rv = dV_rv @ covx_rv @ dV_rv

    # Combine U, V estimates
    U = (U_astro * varU_rv + U_rv * varU_astro) / (varU_rv + varU_astro)
    V = (V_astro * varV_rv + V_rv * varV_astro) / (varV_rv + varV_astro)

    # Deduce asini, omega
    asini = (U**2 + V**2) ** (1 / 4)
    om = np.arctan2(V, U) / 2
    om_rv = np.arctan2(x_rv[1], x_rv[0])
    om = (om - om_rv + np.pi / 2) % (np.pi) + om_rv - np.pi / 2

    # Compute i, Omega from astro (Popovic & Pavlovic 1995)
    com = np.cos(om)
    som = np.sin(om)
    Om = np.arctan2(
      x_astro[1] * com - x_astro[3] * som, x_astro[0] * com - x_astro[2] * som
    )
    m = x_astro[0] * x_astro[3] - x_astro[1] * x_astro[2]
    k = np.sum(x_astro[:4] ** 2) / 2
    j = np.sqrt(k**2 - m**2)
    i = np.arccos(m / (k + j))
    return (
      np.array([P, asini, M0_rad, e, om, i, Om]),
      ['P', 'assini', 'M0', 'e', 'omega', 'i', 'bigomega'],
    )
