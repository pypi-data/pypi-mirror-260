# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np
from kepderiv import Keplerian
from spleaf import term

from kepmodel.rv import RvModel


def test_rvmodel(seed=0):
  np.random.seed(seed)
  n = 351

  offset = np.random.normal(0, 10)
  P = 10 ** np.random.uniform(0, 3)
  K = 1.0
  la0 = np.random.uniform(0, 2 * np.pi)
  ecosw = np.random.normal(0, 0.1)
  esinw = np.random.normal(0, 0.1)
  true_param = np.array([offset, P, K, la0, ecosw, esinw])

  kep = Keplerian(true_param[1:], ['P', 'K', 'la0', 'ecosw', 'esinw'])

  t = np.sort(np.random.uniform(0, 2000, n))
  sig = np.random.uniform(0.25, 0.5, n)
  rv = kep.rv(t) + offset + np.random.normal(0, sig)

  Pmin = 1.0
  Pmax = 10000
  nfreq = 10000
  nu0 = 2 * np.pi / Pmax
  dnu = (2 * np.pi / Pmin - nu0) / (nfreq - 1)

  rvmodel = RvModel(t, rv, err=term.Error(sig))
  rvmodel.add_lin(np.ones(n), 'offset')
  rvmodel.fit()
  rvmodel.show_param()
  nu, power = rvmodel.periodogram(nu0, dnu, nfreq)

  kmax = np.argmax(power)
  Pmax = 2 * np.pi / nu[kmax]
  fap = rvmodel.fap(power[kmax], nu.max())
  print(P, Pmax, power[kmax], fap)
  assert abs(1 / Pmax - 1 / P) < 1 / (t.max() - t.min())
  assert fap < 1e-3

  rvmodel.add_keplerian_from_period(Pmax)
  rvmodel.set_keplerian_param('0', ['P', 'K', 'la0', 'ecosw', 'esinw'])
  rvmodel.fit()
  param, error = rvmodel.get_param_error()
  param[3] = (param[3] - true_param[3] + np.pi) % (2 * np.pi) + true_param[3] - np.pi
  print(true_param)
  print(param)
  print(error)
  print(((true_param - param) / error) ** 2)
  chi2r = np.mean(((true_param - param) / error) ** 2)
  assert chi2r < 2.0
