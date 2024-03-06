# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np
from kepderiv import Keplerian
from spleaf import term

from kepmodel.astro import AstroModel


def test_astromodel(seed=0):
  np.random.seed(seed)
  n = 351

  for use_angles in [True, False]:
    th = np.random.uniform(0, 2 * np.pi, n)
    cth = np.cos(th)
    sth = np.sin(th)
    delta = np.random.normal(0, 10)
    alpha = np.random.normal(0, 10)
    mud = np.random.normal(0, 0.1)
    mua = np.random.normal(0, 0.1)

    plx = 30.0
    fac = 1 if use_angles else plx
    plxfac = np.random.normal(0, 1.0, n)

    P = 10 ** np.random.uniform(0, 3)
    e = np.random.uniform(0, 0.9)
    la0 = np.random.uniform(0, 2 * np.pi)
    A = np.random.normal(0, 1.0) / fac
    B = np.random.normal(0, 1.0) / fac
    F = np.random.normal(0, 1.0) / fac
    G = np.random.normal(0, 1.0) / fac
    true_param = np.array([delta, alpha, mud, mua, plx, P, e, la0, A, B, F, G])

    kep = Keplerian(true_param[5:], ['P', 'e', 'la0', 'TIA', 'TIB', 'TIF', 'TIG'])

    t = np.sort(np.random.uniform(0, 2000, n))
    sig = np.random.uniform(0.5, 1.5, n)
    kepd, kepa = kep.astro(t)
    s = (
      cth * (delta + t * mud + fac * kepd)
      + sth * (alpha + t * mua + fac * kepa)
      + plx * plxfac
      + np.random.normal(0, sig)
    )

    Pmin = 1.0
    Pmax = 10000
    nfreq = 10000
    nu0 = 2 * np.pi / Pmax
    dnu = (2 * np.pi / Pmin - nu0) / (nfreq - 1)

    astromodel = AstroModel(
      t, s, cth, sth, err=term.Error(sig), angular_keplerian_param=use_angles
    )
    astromodel.add_lin(cth, 'delta')
    astromodel.add_lin(sth, 'alpha')
    astromodel.add_lin(cth * t, 'mud')
    astromodel.add_lin(sth * t, 'mua')
    astromodel.add_lin(plxfac, 'plx')
    astromodel.fit()
    astromodel.show_param()
    nu, power = astromodel.periodogram(nu0, dnu, nfreq)

    kmax = np.argmax(power)
    Pmax = 2 * np.pi / nu[kmax]
    fap = astromodel.fap(power[kmax], nu.max())
    print(P, Pmax, power[kmax], fap)
    assert abs(1 / Pmax - 1 / P) < 1 / (t.max() - t.min())
    assert fap < 1e-3

    astromodel.add_keplerian_from_period(Pmax)
    astromodel.set_keplerian_param('0', ['P', 'e', 'la0', 'TIA', 'TIB', 'TIF', 'TIG'])
    astromodel.fit()
    param, error = astromodel.get_param_error()
    param[7] = (param[7] - true_param[7] + np.pi) % (2 * np.pi) + true_param[7] - np.pi
    print(true_param)
    print(param)
    print(error)
    print(((true_param - param) / error) ** 2)
    chi2r = np.mean(((true_param - param) / error) ** 2)
    assert chi2r < 2.0
