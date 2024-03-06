# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np
from kepderiv import Keplerian
from spleaf import term

from kepmodel.astro import AstroModel
from kepmodel.astrorv import AstroRvModel
from kepmodel.rv import RvModel


def test_astrorvmodel(seed=0):
  np.random.seed(seed)
  n_astro = 251
  n_rv = 351

  th = np.random.uniform(0, 2 * np.pi, n_astro)
  cth = np.cos(th)
  sth = np.sin(th)
  delta = np.random.normal(0, 10)
  alpha = np.random.normal(0, 10)
  mud = np.random.normal(0, 10)
  mua = np.random.normal(0, 10)

  plx = 30.0
  plxfac = np.random.normal(0, 1.0, n_astro)

  offset = np.random.normal(0, 10)

  P = 10 ** np.random.uniform(2, 3)
  astar = 1e-2
  Marg0 = np.random.uniform(0, 2 * np.pi)
  e = np.random.uniform(0, 0.9)
  w = np.random.uniform(0, 2 * np.pi)
  i = np.arccos(np.random.uniform(0, 1))
  bigw = np.random.uniform(0, 2 * np.pi)
  true_param = np.array(
    [delta, alpha, mud, mua, plx, offset, P, astar, Marg0, e, w, i, bigw]
  )

  kep = Keplerian(true_param[6:], ['P', 'as', 'Marg0', 'e', 'w', 'i', 'bigw'])

  t_astro = np.sort(np.random.uniform(0, 2000, n_astro))
  sig_astro = np.random.uniform(0.1, 0.15, n_astro)
  kepd, kepa = kep.astro(t_astro)
  s = (
    cth * (delta + t_astro * mud + plx * kepd)
    + sth * (alpha + t_astro * mua + plx * kepa)
    + plx * plxfac
    + np.random.normal(0, sig_astro)
  )

  t_rv = np.sort(np.random.uniform(0, 2000, n_rv))
  sig_rv = np.random.uniform(3.0, 5.0, n_rv)
  rv = kep.rv(t_rv) + offset + np.random.normal(0, sig_rv)

  Pmin = 1.0
  Pmax = 10000
  nfreq = 10000
  nu0 = 2 * np.pi / Pmax
  dnu = (2 * np.pi / Pmin - nu0) / (nfreq - 1)

  astromodel = AstroModel(
    t_astro, s, cth, sth, err=term.Error(sig_astro), angular_keplerian_param=False
  )
  rvmodel = RvModel(t_rv, rv, err=term.Error(sig_rv))
  fullmodel = AstroRvModel(astromodel, rvmodel)
  astromodel.add_lin(cth, 'delta')
  astromodel.add_lin(sth, 'alpha')
  astromodel.add_lin(cth * t_astro, 'mud')
  astromodel.add_lin(sth * t_astro, 'mua')
  astromodel.add_lin(plxfac, 'plx')
  astromodel.fit()
  astromodel.show_param()

  rvmodel.add_lin(np.ones(n_rv), 'offset')
  rvmodel.fit()
  rvmodel.show_param()

  fullmodel.fit()
  fullmodel.show_param()

  nu, power = fullmodel.periodogram(nu0, dnu, nfreq)

  kmax = np.argmax(power)
  Pmax = 2 * np.pi / nu[kmax]
  fap = fullmodel.fap(power[kmax], nu.max())
  print(P, Pmax, power[kmax], fap)
  assert abs(1 / Pmax - 1 / P) < 1 / (t_rv.max() - t_rv.min())
  assert fap < 1e-3
  fullmodel.add_keplerian_from_period(Pmax)
  fullmodel.set_keplerian_param('0', ['P', 'as', 'Marg0', 'e', 'w', 'i', 'bigw'])
  fullmodel.fit()
  fullmodel.show_param()

  param, error = fullmodel.get_param_error()
  param[8:] = (
    (param[8:] - true_param[8:] + np.pi) % (2 * np.pi) + true_param[8:] - np.pi
  )
  print(true_param)
  print(param)
  print(error)
  print(((true_param - param) / error) ** 2)
  chi2r = np.mean(((true_param - param) / error) ** 2)
  assert chi2r < 2.0
