# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np
from kepderiv import Keplerian
from scipy.optimize import minimize
from scipy.special import gammaln
from spleaf.cov import Cov


class _KeplerianSystem(dict):
  r"""
  Keplerian system.

  This hidden class simply adds the `uid` attribute
  to the dict class in order to generate unique
  names for Keplerians.
  """

  def __init__(self):
    super().__init__()
    self.uid = 0


class ParamTranslator:
  r"""
  Parameter translator.

  This class is a template to define parameter translators
  for :func:`KeplerianModel`.
  One should create a child class and customize its methods,
  to define custom parameters and link them with the default
  :func:`KeplerianModel` parameters.
  Then a member of this child class can be passed
  to :func:`KeplerianModel.set_param_translator`.
  """

  def _link(self, model):
    self.model = model

  def get_default(self, custom_param):
    r"""
    Get the list of default parameters from which
    the provided custom parameters can be computed.

    Parameters
    ----------
    custom_param : list
      Names of the custom parameters.

    Returns
    -------
    default_param : list
      Names of the default parameters.
    """

    return custom_param

  def compute_custom(self, custom_param, default_value_dict):
    r"""
    Compute the values of the custom parameters
    from the values of the default ones.

    Parameters
    ----------
    custom_param : list
      Names of the custom parameters.
    default_values_dict : dict
      Values of the default parameters.

    Returns
    -------
    custom_value_dict : dict
      Values of the custom parameters.
    """

    return default_value_dict

  def compute_default(self, default_param, custom_value_dict):
    r"""
    Compute the values of the default parameters
    from the values of the custom ones.

    Parameters
    ----------
    default_param : list
      Names of the default parameters.
    custom_values_dict : dict
      Values of the custom parameters.

    Returns
    -------
    default_value_dict : dict
      Values of the default parameters.
    """

    return custom_value_dict

  def compute_default_back(self, custom_param, default_grad_dict):
    r"""
    Compute the gradient of a function with respect to the custom parameters
    from its gradient with respect to the default parameters.

    Parameters
    ----------
    custom_param : list
      Names of the custom parameters.
    default_grad_dict : dict
      Gradient with respect to the default parameters.

    Returns
    -------
    custom_grad_dict : dict
      Gradient with respect to the custom parameters.
    """

    return default_grad_dict


class KeplerianModel:
  r"""
  Generic class for a Keplerian model.
  """

  def __init__(self):
    self.keplerian = _KeplerianSystem()
    self._default_fit_param = []
    self._custom_fit_param = []
    self._param_translator = ParamTranslator()

  @property
  def nkep(self):
    return len(self.keplerian)

  def _get_fit_param(self):
    return self._custom_fit_param.copy()

  def _set_fit_param(self, new_fit_param):
    self._custom_fit_param = new_fit_param
    self._default_fit_param = self._param_translator.get_default(new_fit_param)

  fit_param = property(
    lambda self: self._get_fit_param(),
    lambda self, new_fit_param: self._set_fit_param(new_fit_param),
  )

  def set_param_translator(self, param_translator):
    r"""
    Set the parameter translator to be able to use custom parameters.

    Parameters
    ----------
    param_translator : ParamTranslator
      A :func:`kepmodel.timeseries.ParamTranslator` instance defining the custom parameters.
    """

    param_translator._link(self)
    self._param_translator = param_translator

  def fit_lin(self):
    r"""
    Fit the linear parameters set in fit_param.
    """
    raise NotImplementedError

  def add_keplerian(self, value, param, fit=True, name=None, **kwargs):
    r"""
    Add a Keplerian in the system.

    Parameters
    ----------
    value : (p,) ndarray
      The values of the Keplerian parameters listed in `param`.
    param : list
      List of defined parameters for the Keplerian (see `kepderiv` package).
    fit : bool
      Whether the Keplerian parameters should be added to the fit_param list
      for later fit (see :func:`fit`).
    name : str or None
      Name of the Keplerian (optional).
    **kwargs :
      Additional arguments for Keplerian (see `kepderiv` package).
    """

    if name is None:
      name = f'{self.keplerian.uid}'
      while name in self.keplerian:
        self.keplerian.uid += 1
        name = f'{self.keplerian.uid}'
    self.keplerian[name] = Keplerian(value, param, **kwargs)
    if fit:
      self.fit_param += [f'kep.{name}.{par}' for par in param]
    self.keplerian.uid += 1

  def guess_keplerian_param(self, P, **kwargs):
    raise NotImplementedError

  def add_keplerian_from_period(
    self, P, fit=True, name=None, guess_kwargs={}, **kwargs
  ):
    r"""
    Add a Keplerian in the system guessing
    all the Keplerian parameters from the period
    (see :func:`guess_keplerian_param`).

    Parameters
    ----------
    value : (p,) ndarray
      The values of the Keplerian parameters listed in `param`.
    P : double
      Orbital period.
    fit : bool
      Whether the Keplerian parameters should be added to the fit_param list
      for later fit (see :func:`fit`).
    name : str or None
      Name of the Keplerian (optional).
    guess_kwargs : dict
      Additional arguments for :func:`guess_keplerian_param`.
    **kwargs :
      Additional arguments for Keplerian (see `kepderiv` package).
    """

    value, param = self.guess_keplerian_param(P, **guess_kwargs)
    self.add_keplerian(value, param, fit, name, **kwargs)
    self.fit_lin()

  def set_keplerian_param(self, name, param):
    r"""
    Switch the set of defined parameters for a Keplerian.

    Parameters
    ----------
    name : str
      Name of the Keplerian.
    param : list
      List of new parameters for the Keplerian (see `kepderiv` package).
    """

    fit = False
    new_fit_param = self.fit_param
    for par in self.fit_param:
      if par.startswith(f'kep.{name}.'):
        new_fit_param.remove(par)
        fit = True
    self.keplerian[name].set_param(param)
    if fit:
      new_fit_param += [f'kep.{name}.{par}' for par in param]
    self.fit_param = new_fit_param

  def rm_keplerian(self, name):
    r"""
    Remove a Keplerian.

    Parameters
    ----------
    name : str
      Name of the Keplerian.
    """

    self.keplerian.pop(name)
    new_fit_param = self.fit_param
    for par in self.fit_param:
      if par.startswith(f'kep.{name}.'):
        new_fit_param.remove(par)
    self.fit_param = new_fit_param

  def _chi2(self):
    raise NotImplementedError

  def chi2(self, x=None, param=None, backup=True):
    r"""
    Compute the chi2 of the model.

    Parameters
    ----------
    x : (p,) ndarray or None
      Values of the parameters to set before computing the model.
      If None, keep current values.
    param : list or None
      List of parameter names to set.
      If None, use the fit_param list.
    backup : bool
      Whether to reset the parameters to their current values
      after the call to this method.

    Returns
    -------
    chi2 : float
      The model chi2.
    """

    if x is not None:
      if backup:
        x_old = self.get_param(param)
      self.set_param(x, param)
    chi2 = self._chi2()
    if x is not None and backup:
      self.set_param(x_old, param)
    return chi2

  def _loglike(self):
    raise NotImplementedError

  def loglike(self, x=None, param=None, backup=True):
    r"""
    Compute the log-likelihood of the model.

    Parameters
    ----------
    x : (p,) ndarray or None
      Values of the parameters to set before computing the model.
      If None, keep current values.
    param : list or None
      List of parameter names to set.
      If None, use the fit_param list.
    backup : bool
      Whether to reset the parameters to their current values
      after the call to this method.

    Returns
    -------
    loglike : float
      The model log-likelihood.
    """

    if x is not None:
      if backup:
        x_old = self.get_param(param)
      self.set_param(x, param)
    ll = self._loglike()
    if x is not None and backup:
      self.set_param(x_old, param)
    return ll

  def _func_default_grad(self, func_name):
    raise NotImplementedError

  def _func_grad(self, func_name, x=None, param=None, backup=True):
    r"""
    Gradient of the method `func_name`.
    """
    if x is not None:
      if backup:
        x_old = self.get_param(param)
      self.set_param(x, param)
    default_grad_dict = self._func_default_grad(func_name)
    grad_dict = self._param_translator.compute_default_back(
      self._custom_fit_param, default_grad_dict
    )
    grad = np.zeros(len(self._custom_fit_param))
    for k, par in enumerate(self._custom_fit_param):
      grad[k] = grad_dict[par]
    if x is not None and backup:
      self.set_param(x_old, param)
    return grad

  def chi2_grad(self, x=None, param=None, backup=True):
    r"""
    Gradient of :func:`chi2` with respect to
    the parameters listed in `fit_param`.

    Parameters
    ----------
    x : (p,) ndarray or None
      Value of the parameters listed in `param`.
      If None, the current value is kept.
    param : list or None
      List of defined parameters.
      If None, the list is assumed to be `fit_param`.
    backup : bool
      whether to reset the parameters to their current values
      after the gradient computation.

    Returns
    -------
    grad : (p,) ndarray
      Gradient.
    """

    return self._func_grad('chi2', x, param, backup)

  def loglike_grad(self, x=None, param=None, backup=True):
    r"""
    Gradient of :func:`loglike` with respect to
    the parameters listed in `fit_param`.

    Parameters
    ----------
    x : (p,) ndarray or None
      Value of the parameters listed in `param`.
      If None, the current value is kept.
    param : list or None
      List of defined parameters.
      If None, the list is assumed to be `fit_param`.
    backup : bool
      whether to reset the parameters to their current values
      after the gradient computation.

    Returns
    -------
    grad : (p,) ndarray
      Gradient.
    """

    return self._func_grad('loglike', x, param, backup)

  def loglike_hess(self, x=None, param=None, backup=True, step=1e-6):
    r"""
    Hessian matrix of :func:`loglike` with respect to
    the parameters listed in `fit_param`.

    Parameters
    ----------
    x : (p,) ndarray or None
      Value of the parameters listed in `param`.
      If None, the current value is kept.
    param : list or None
      List of defined parameters.
      If None, the list is assumed to be `fit_param`.
    backup : bool
      Whether to reset the parameters to their current values
      after the gradient computation.
    step : double
      Step size for the second order derivative estimates.

    Returns
    -------
    hess : (p, p) ndarray
      Hessian matrix.
    """

    if x is not None and backup:
      x_old = self.get_param(param)
    llj0 = self.loglike_grad(x, param, False)
    x0 = self.get_param(param)
    xb = list(x0)
    nparam = len(x0)
    hess = np.empty((nparam, nparam))
    for k in range(nparam):
      xb[k] += step
      hess[k] = (self.loglike_grad(xb, param, False) - llj0) / step
      xb[k] = x0[k]
    if x is not None and backup:
      self.set_param(x_old, param)
    else:
      self.set_param(x0, param)
    return (hess + hess.T) / 2

  def fit(self, method='L-BFGS-B', step_hess=1e-6, **kwargs):
    r"""
    Adjust the parameters listed in `fit_param` to fit the data.

    This method calls the `scipy.optimize.minimize` function.

    Parameters
    ----------
    method : str
      Minimization method (see `scipy.optimize.minimize`)
    step_hess : double
      Step size for the scale estimate (using :func:`loglike_hess`).
    **kwargs :
      Additional arguments for the `scipy.optimize.minimize` function.
    """

    scale = 1 / np.sqrt(np.abs(np.diag(self.loglike_hess(step=step_hess))))
    bounds = []
    if 'bounds' in kwargs:
      bdict = kwargs.pop('bounds')
    else:
      bdict = {}
    for par, sc in zip(self.fit_param, scale):
      if par in bdict:
        bounds.append((bdict[par][0] / sc, bdict[par][1] / sc))
      # eccentricity:
      elif par.startswith('kep.') and par.endswith('.e'):
        bounds.append((0, 0.95 / sc))
      elif par.startswith('kep.') and ('ecos' in par or 'esin' in par):
        bounds.append((-0.95 / sc, 0.95 / sc))
      # Amplitude
      elif par.startswith('kep.') and (
        par.endswith('.as')
        or par.endswith('.asini')
        or par.endswith('.assini')
        or par.endswith('.K')
      ):
        bounds.append((0, None))
      # Period
      elif par.startswith('kep.') and (par.endswith('.P') or par.endswith('.n')):
        bounds.append((1e-5 / sc, None))
      # Noise
      elif (
        par.endswith('.sig')
        or par.endswith('.P0')
        or par.endswith('.Q')
        or par.endswith('.rho')
      ):
        bounds.append((1e-5 / sc, None))
      else:
        bounds.append((None, None))
    x_old = self.get_param()
    result = minimize(
      lambda x: -self.loglike(x * scale, backup=False),
      np.array(x_old) / scale,
      jac=lambda x: -self.loglike_grad(x * scale, backup=False) * scale,
      method=method,
      bounds=bounds,
      **kwargs,
    )
    if result.success:
      self.set_param(result.x * scale)
      self.clean_param()
    else:
      print(result)
      print()
      self.set_param(x_old)
      raise Exception('Fit did not converge.')

  def _chi2ogram(self, nu0, dnu, nfreq):
    raise NotImplementedError

  def periodogram(self, nu0, dnu, nfreq):
    r"""
    Periodogram of the time series.

    Parameters
    ----------
    nu0 : double
      Minimum angular frequency.
    dnu : double
      Step size for the angular frequency.
    nfreq : int
      Number of sampled frequencies.

    Returns
    -------
    nu : (nfreq,) ndarray
      Angular frequencies.
    power : (nfreq,) ndarray
      Periodogram power.
    """

    chi20, chi2 = self._chi2ogram(nu0, dnu, nfreq)
    power = 1.0 - chi2 / chi20
    return (nu0 + np.arange(nfreq) * dnu, power)

  def _fap_Nh(self):
    raise NotImplementedError

  def _fap_d(self):
    raise NotImplementedError

  def _fap_sqla(self, numax):
    raise NotImplementedError

  def Teff(self, numax, d):
    r"""
    Effective time series length for the analytical FAP computation (see :func:`fap`).

    Parameters
    ----------
    numax : double
      Maximum angular frequency sampled in the periodogram.
    d : int
      Number of independant vectors for each frequency.

    Returns
    -------
    Teff : float
      Effective time series length.
    """

    sqla = self._fap_sqla(numax)
    if d == 2:
      return 2 * np.sqrt(np.pi) * sqla[0]
    elif d == 4:
      return (
        4
        / 3
        * np.sqrt(np.pi)
        * (sqla[0] + sqla[1] - sqla[0] * sqla[1] / (sqla[0] + sqla[1]))
      )
    elif d == 6:
      sumprod = np.sum([sqla[i] * sqla[j] for i in range(3) for j in range(i)])
      prodsum = np.prod([sqla[i] + sqla[j] for i in range(3) for j in range(i)])
      return 8 / 15 * np.sqrt(np.pi) * (np.sum(sqla) - sumprod**2 / prodsum)
    else:
      raise NotImplementedError

  def fap(self, zmax, numax, Teff=None):
    r"""
    Periodogram False Alarm Probability.

    Parameters
    ----------
    zmax : double
      Power of the highest peak in the periodogram.
    numax : double
      Maximum angular frequency sampled in the periodogram.
    Teff : double or None
      Effective time series length.
      If None, it is automatically computed using :func:`Teff`.

    Returns
    -------
    FAP : double
      Periodogram FAP.
    """

    Nh = self._fap_Nh()
    d = self._fap_d()
    Nk = Nh - d
    fmax = numax / (2.0 * np.pi)
    if Teff is None:
      Teff = self.Teff(numax, d)
    W = fmax * Teff
    chi2ratio = 1.0 - zmax
    FapSingle = chi2ratio ** (Nk / 2.0)
    if d == 4:
      FapSingle *= 1.0 + Nk / 2.0 * zmax
    elif d == 6:
      FapSingle *= 1.0 + Nk / 2.0 * zmax * (1.0 + (1.0 + Nk / 2.0) * zmax)
    elif d != 2:
      raise NotImplementedError

    # Without approximation on gamma:
    gamma = np.exp(gammaln(Nh / 2) - gammaln((Nk + 1) / 2))
    tau = gamma * W * zmax ** ((d - 1) / 2) * chi2ratio ** ((Nk - 1) / 2)
    # Assuming gamma ~ (Nh/2)**((d-1)/2):
    # tau = W * (zmax * Nh / 2.0) ** ((d - 1) / 2) * chi2ratio ** ((Nk - 1) / 2.0)

    # Fap = 1.0 - (1.0 - FapSingle) * np.exp(-tau)
    Fap = FapSingle - (1.0 - FapSingle) * np.expm1(-tau)
    return Fap

  def _get_default_param(self, param):
    raise NotImplementedError

  def get_param(self, param=None):
    r"""
    Get the current values of the model parameters.

    Parameters
    ----------
    param : list or None
      List of parameter names.
      If None, use the fit_param list.

    Returns
    -------
    value : (p,) ndarray
      The values of required parameters.
    """

    singlevar = False
    if param is None:
      param = self.fit_param
    elif isinstance(param, str):
      singlevar = True
      param = [param]
    default_param = self._param_translator.get_default(param)
    default_value_dict = self._get_default_param(default_param)
    value_dict = self._param_translator.compute_custom(param, default_value_dict)
    value = np.empty(len(param))
    for kpar, par in enumerate(param):
      value[kpar] = value_dict[par]
    if singlevar:
      return value[0]
    else:
      return value

  def _set_default_param(self, value_dict):
    raise NotImplementedError

  def set_param(self, value, param=None):
    r"""
    Set the values of the model parameters.

    Parameters
    ----------
    value : (p,) ndarray
      The values of specified parameters.
    param : list or None
      List of parameter names.
      If None, use the fit_param list.
    """

    if param is None:
      param = self.fit_param
    elif isinstance(param, str):
      param = [param]
      value = [value]
    value_dict = dict(zip(param, value))
    default_param = self._param_translator.get_default(param)
    default_value_dict = self._param_translator.compute_default(
      default_param, value_dict
    )
    self._set_default_param(default_value_dict)

  def get_param_error(self, param=None, step_hess=1e-6):
    r"""
    Get the current values and errorbars of the model parameters.

    Parameters
    ----------
    param : list or None
      List of parameters to show.
      If None, the list is assumed to be `fit_param`.
    step_hess : double
      Step size for the errobars estimates (using :func:`loglike_hess`).
    """

    if param is None:
      param = self.fit_param
    value = self.get_param(param)
    hess = self.loglike_hess(param=param, step=step_hess)
    error = np.sqrt(-np.diag(np.linalg.inv(hess)))
    return (value, error)

  def show_param(self, param=None, step_hess=1e-6, degree=True):
    r"""
    Print a summary of the values and errorbars of the model parameters.

    Parameters
    ----------
    param : list or None
      List of parameters to show.
      If None, the list is assumed to be `fit_param`.
    step_hess : double
      Step size for the errobars estimates (using :func:`loglike_hess`).
    degree : bool
      Whether to print the angles in degrees.
    """

    if param is None:
      param = self.fit_param
    value, error = self.get_param_error(param, step_hess)
    print('{:25s} {:>12s}     {:12s}'.format('Parameter', 'Value', 'Error'))
    for par, val, err in zip(param, value, error):
      parU = (
        par.split('.')[-1]
        .upper()
        .replace('_', '')
        .replace('SQRT', 'SQ')
        .replace('OMEGA', 'W')
      )
      if degree and parU in [
        'M0',
        'MARG0',
        'LA0',
        'W',
        'VARPI',
        'VPI',
        'BIGW',
        'INC',
        'I',
      ]:
        par += ' [deg]'
        val *= 180 / np.pi
        err *= 180 / np.pi
      if err == 0 or np.isnan(err):
        dec = 6
      else:
        dec = int(max(0, 3 - np.log10(err)))
      fmt = f'{{:25s}} {{:12.{dec}f}}  ±  {{:<12.{dec}f}}'
      print(fmt.format(par, val, err))
    print()

  def clean_param(self, param=None):
    r"""
    Clean the model parameters to have all angles in :math:`[0, 2\pi]`,
    and the inclination in :math:`[0, \pi]`.

    Parameters
    ----------
    param : list or None
      List of parameters to show.
      If None, the list is assumed to be `fit_param`.
    """

    if param is None:
      param = self.fit_param
    value = self.get_param(param)
    paramU = [
      par.upper()
      .replace('_', '')
      .replace('SQRT', 'SQ')
      .replace('OMEGA', 'W')
      .replace('INC', 'I')
      for par in param
    ]
    for kpar, parU in enumerate(paramU):
      parUend = parU.split('.')[-1]
      if parUend in ['M0', 'MARG0', 'LA0', 'W', 'VARPI', 'VPI', 'BIGW', 'I']:
        value[kpar] = value[kpar] % (2 * np.pi)
        if parUend == 'I' and value[kpar] > np.pi:
          try:
            kbigw = paramU.index(parU.replace('.I', '.BIGW'))
            value[kpar] = 2 * np.pi - value[kpar]
            value[kbigw] = (value[kbigw] + np.pi) % (2 * np.pi)
          except:
            pass
      if parUend in ['TP', 'TC', 'TVMIN', 'TVMAX']:
        try:
          kP = paramU.index(parU.replace(parUend, 'P'))
          value[kpar] = (value[kpar] + value[kP] / 2) % value[kP] - value[kP] / 2
        except:
          pass
    self.set_param(value, param)


class SingleTimeseriesModel(KeplerianModel):
  r"""
  Generic class for a Keplerian model considering a single time series.
  """

  def __init__(self, t, y, series_index=[], **kwargs):
    super().__init__()

    self._parent = None
    self._name = None

    self.full_t = t
    self.full_y = y
    self.full_n = t.size

    self.series_index = series_index + [slice(self.full_n)]
    self.t = t[self.series_index[0]]
    self.y = y[self.series_index[0]]
    self.n = self.t.size

    if 'cov' in kwargs:
      self.cov = kwargs['cov']
    else:
      self.cov = Cov(t, **kwargs)

    self.nlin = 0
    self._lin_uid = 0
    self._lin_name = []
    self._lin_par = np.empty(0)
    self._lin_M = np.empty((0, self.full_n))

  def _set_fit_param(self, new_fit_param):
    if self._parent is None:
      super()._set_fit_param(new_fit_param)
    else:
      self._parent._set_child_fit_param(self._name, new_fit_param)

  def add_lin(self, derivative, name=None, value=0.0, fit=True, series_id=0):
    r"""
    Add a linear predictor to the model.

    The linear predictor is of the form
    :math:`y = \alpha d`
    where `\alpha` is the amplitude (which can adjusted for)
    and `d` is the derivative of the predictor.

    Parameters
    ----------
    derivative : (n,) ndarray
      Time series of the predictor derivative (`d`).
    name : str or None
      Name of the predictor.
    value : float
      Initial value of the amplitude (`\alpha`).
    fit : bool
      Whether the amplitude should be added to the fit_param.
    """

    full_derivative = np.zeros(self.full_n)
    full_derivative[self.series_index[series_id]] = derivative
    self._lin_M = np.vstack((self._lin_M, full_derivative))
    if name is None:
      name = f'{self._lin_uid}'
      while name in self._lin_name:
        self._lin_uid += 1
        name = f'{self._lin_uid}'
    self._lin_name.append(name)
    self._lin_par = np.concatenate((self._lin_par, [value]))
    if fit:
      self.fit_param += [f'lin.{name}']
    self.nlin += 1
    self._lin_uid += 1

  def rm_lin(self, name):
    r"""
    Remove a linear predictor.

    Parameters
    ----------
    name : str
      Name of the predictor.
    """

    klin = self._lin_name.index(name)
    self._lin_M = np.delete(self._lin_M, klin, 0)
    self._lin_name.pop(klin)
    self._lin_par = np.delete(self._lin_par, klin, 0)
    par = f'lin.{name}'
    fit_param = self.fit_param
    if par in fit_param:
      fit_param.remove(par)
      self.fit_param = fit_param
    self.nlin -= 1

  def get_fit_lin_M(self):
    r"""
    Get the matrix of fitted linear predictors derivatives.
    """

    fit_lin_M = np.empty((0, self.full_n))
    fit_lin_param = []
    for klin in range(self.nlin):
      par = f'lin.{self._lin_name[klin]}'
      if par in self._default_fit_param:
        fit_lin_M = np.vstack((fit_lin_M, self._lin_M[klin]))
        fit_lin_param.append(par)
    return (fit_lin_M, fit_lin_param)

  def fit_lin(self):
    res = self.residuals()
    M, param = self.get_fit_lin_M()
    Nt = np.array([self.cov.solveL(Mk) / self.cov.sqD() for Mk in M]).reshape(
      -1, res.size
    )
    u = self.cov.solveL(res) / self.cov.sqD()
    covx = np.linalg.inv(Nt @ Nt.T)
    dx = covx @ Nt @ u
    x = self.get_param(param) + dx
    self.set_param(x, param)

  def _guess_keplerian_harmfit(self, P, **kwargs):
    raise NotImplementedError

  def _guess_keplerian_other(self, P, e, M0_rad, **kwargs):
    raise NotImplementedError

  def keplerian_model(self):
    raise NotImplementedError

  def model(self, x=None, param=None, backup=True, series_id=-1):
    r"""
    Compute the model time series.

    Parameters
    ----------
    x : (p,) ndarray or None
      Values of the parameters to set before computing the model.
      If None, keep current values.
    param : list or None
      List of parameter names to set.
      If None, use the fit_param list.
    backup : bool
      Whether to reset the parameters to their current values
      after the call to this method.

    Returns
    -------
    y : (n,) ndarray
      The model time series.
    """

    if x is not None:
      if backup:
        x_old = self.get_param(param)
      self.set_param(x, param)
    y = self._lin_par.dot(self._lin_M)
    y[self.series_index[0]] += self.keplerian_model()
    if x is not None and backup:
      self.set_param(x_old, param)
    return y[self.series_index[series_id]]

  def residuals(self, x=None, param=None, backup=True, series_id=-1):
    r"""
    Compute the residuals time series.

    Parameters
    ----------
    x : (p,) ndarray or None
      Values of the parameters to set before computing the model.
      If None, keep current values.
    param : list or None
      List of parameter names to set.
      If None, use the fit_param list.
    backup : bool
      Whether to reset the parameters to their current values
      after the call to this method.

    Returns
    -------
    y : (m,) ndarray
      The residuals time series.
    """
    return self.full_y[self.series_index[series_id]] - self.model(
      x=x, param=param, backup=backup, series_id=series_id
    )

  def _chi2(self):
    return self.cov.chi2(self.residuals())

  def _loglike(self):
    return self.cov.loglike(self.residuals())

  def _keplerian_grad(self, grad_res, grad):
    raise NotImplementedError

  def _func_default_grad(self, func_name):
    getattr(self, func_name)()
    grad_res, grad_noise = getattr(self.cov, func_name + '_grad')()
    grad_dict = {par: 0.0 for par in self._default_fit_param}
    self._keplerian_grad(grad_res[self.series_index[0]], grad_dict)
    for par in self._default_fit_param:
      par_split = par.split('.', 1)
      if par_split[0] == 'lin':
        grad_dict[par] -= self._lin_M[self._lin_name.index(par_split[1])].dot(grad_res)
      elif par_split[0] == 'cov':
        grad_dict[par] += grad_noise[self.cov.param.index(par_split[1])]
    return grad_dict

  def _perio_phi(self, cosnut, sinnut):
    raise NotImplementedError

  def _chi2ogram(self, nu0, dnu, nfreq):
    res = self.residuals()
    N0t = np.array(
      [self.cov.solveL(M0k) / self.cov.sqD() for M0k in self.get_fit_lin_M()[0]]
    ).reshape(-1, res.size)
    u = self.cov.solveL(res) / self.cov.sqD()
    u2 = np.sum(u * u)
    N0tu = N0t @ u
    chi20 = u2 - N0tu.T @ np.linalg.inv(N0t @ N0t.T) @ N0tu

    chi2 = np.empty(nfreq)
    dnut_rad = dnu * self.t
    cosdnut = np.cos(dnut_rad)
    sindnut = np.sin(dnut_rad)
    nu0t_rad = nu0 * self.t
    cosnut = np.cos(nu0t_rad)
    sinnut = np.sin(nu0t_rad)
    full_phik = np.zeros(self.full_n)
    d = self._fap_d()
    Nt = np.empty((d + N0t.shape[0], self.full_n))
    for k, phik in enumerate(self._perio_phi(cosnut, sinnut)):
      full_phik[self.series_index[0]] = phik
      Nt[k] = self.cov.solveL(full_phik) / self.cov.sqD()
    Nt[d:] = N0t
    Ntu = Nt @ u
    chi2[0] = u2 - Ntu.T @ np.linalg.inv(Nt @ Nt.T) @ Ntu
    for kfreq in range(1, nfreq):
      cosnut, sinnut = (
        cosnut * cosdnut - sinnut * sindnut,
        sinnut * cosdnut + cosnut * sindnut,
      )
      for k, phik in enumerate(self._perio_phi(cosnut, sinnut)):
        full_phik[self.series_index[0]] = phik
        Nt[k] = self.cov.solveL(full_phik) / self.cov.sqD()
        Ntu[k] = Nt[k] @ u
      chi2[kfreq] = u2 - Ntu.T @ np.linalg.inv(Nt @ Nt.T) @ Ntu
    return (chi20, chi2)

  def _fap_Nh(self):
    return self.full_n - np.sum(
      [
        f'lin.{self._lin_name[klin]}' in self._default_fit_param
        for klin in range(self.nlin)
      ]
    )

  def _get_default_param(self, param):
    value_dict = {}
    for par in param:
      par_split = par.split('.')
      if par_split[0] == 'kep':
        kpar = self.keplerian[par_split[1]].get_param().index(par_split[2])
        value_dict[par] = self.keplerian[par_split[1]].get_value()[kpar]
      elif par_split[0] == 'lin':
        value_dict[par] = self._lin_par[self._lin_name.index(par[4:])]
      elif par_split[0] == 'cov':
        value_dict[par] = self.cov.get_param([par[4:]])[0]
      else:
        value_dict[par] = np.nan
    return value_dict

  def _set_default_param(self, value_dict):
    noise_param = []
    noise_value = []
    kep_value = {name: self.keplerian[name].get_value() for name in self.keplerian}
    kep_change = []
    for par, val in value_dict.items():
      par_split = par.split('.')
      if par_split[0] == 'kep':
        kpar = self.keplerian[par_split[1]].get_param().index(par_split[2])
        kep_value[par_split[1]][kpar] = val
        kep_change.append(par_split[1])
      elif par_split[0] == 'lin':
        self._lin_par[self._lin_name.index(par[4:])] = val
      elif par_split[0] == 'cov':
        noise_param.append(par[4:])
        noise_value.append(val)
    if len(noise_param) > 0:
      self.cov.set_param(noise_value, noise_param)
    for name in kep_change:
      self.keplerian[name].set_value(kep_value[name])


class MultiTimeseriesModel(KeplerianModel):
  r"""
  Generic class for a Keplerian model considering several time series.
  """

  def __init__(self, **kwargs):
    super().__init__()

    self.timeseries = {}
    for key in kwargs:
      if kwargs[key].nkep != 0:
        raise Exception('MultiTimeseriesModel: Cannot merge models containing planets.')
      self.timeseries[key] = kwargs[key]
      self.timeseries[key]._parent = self
      self.timeseries[key]._name = key
      self.timeseries[key].keplerian = self.keplerian
      self._set_child_fit_param(key, self.timeseries[key]._custom_fit_param)

  def _set_fit_param(self, new_fit_param):
    super()._set_fit_param(new_fit_param)
    new_kep_param = []
    for ts in self.timeseries.values():
      ts._custom_fit_param = []
    for par in self._default_fit_param:
      par_split = par.split('.', 1)
      if par_split[0] == 'kep':
        new_kep_param.append(par)
      else:
        self.timeseries[par_split[0]]._custom_fit_param.append(par_split[1])
    for ts in self.timeseries.values():
      ts._custom_fit_param += new_kep_param
      ts._default_fit_param = ts._param_translator.get_default(ts._custom_fit_param)

  def _set_child_fit_param(self, key, new_child_fit_param):
    new_fit_param = [
      par
      for par in self._custom_fit_param
      if not (par.startswith(f'{key}.') or par.startswith('kep.'))
    ]
    for par in new_child_fit_param:
      if par.startswith('kep.'):
        new_fit_param.append(par)
      else:
        new_fit_param.append(f'{key}.{par}')
    self.fit_param = new_fit_param

  def fit_lin(self):
    for ts in self.timeseries.values():
      ts.fit_lin()

  def _guess_keplerian_harmfit(self, P, **kwargs):
    xcovx = [
      ts._guess_keplerian_harmfit(P, **kwargs) for ts in self.timeseries.values()
    ]
    x = np.array([xck[0] for xck in xcovx])
    covx = np.zeros((x.size, x.size))
    offset = 0
    for xk, covxk in xcovx:
      covx[offset : offset + xk.size, offset : offset + xk.size] = covxk
      offset += xk.size
    return (x, covx)

  def _guess_keplerian_other(self, P, e, M0_rad, **kwargs):
    xcovx = [ts._guess_keplerian_other(P, **kwargs) for ts in self.timeseries.values()]
    x = np.array([xck[0] for xck in xcovx])
    covx = np.zeros((x.size, x.size))
    offset = 0
    for xk, covxk in xcovx:
      covx[offset : offset + xk.size, offset : offset + xk.size] = covxk
      offset += xk.size
    return (x, covx)

  def _chi2(self):
    return np.sum([ts.chi2() for ts in self.timeseries.values()])

  def _loglike(self):
    return np.sum([ts.loglike() for ts in self.timeseries.values()])

  def _func_default_grad(self, func_name):
    grad_dict = {par: 0.0 for par in self._default_fit_param}
    for key in self.timeseries:
      default_grad_dict_ts = self.timeseries[key]._func_default_grad(func_name)
      grad_dict_ts = self.timeseries[key]._param_translator.compute_default_back(
        self.timeseries[key]._custom_fit_param, default_grad_dict_ts
      )
      for par in grad_dict_ts:
        if par.startswith('kep.'):
          grad_dict[par] += grad_dict_ts[par]
        else:
          grad_dict[f'{key}.{par}'] += grad_dict_ts[par]
    return grad_dict

  def _chi2ogram(self, nu0, dnu, nfreq):
    chi20 = 0
    chi2 = np.zeros(nfreq)
    for ts in self.timeseries.values():
      chi20k, chi2k = ts._chi2ogram(nu0, dnu, nfreq)
      chi20 += chi20k
      chi2 += chi2k
    return (chi20, chi2)

  def _fap_Nh(self):
    return np.sum([ts._fap_Nh() for ts in self.timeseries.values()])

  def _fap_d(self):
    return np.sum([ts._fap_d() for ts in self.timeseries.values()])

  def _fap_sqla(self, numax):
    return np.concatenate([ts._fap_sqla(numax) for ts in self.timeseries.values()])

  def _get_default_param(self, param):
    value_dict = {}
    ts_param = {key: [] for key in self.timeseries}
    for par in param:
      par_split = par.split('.')
      if par_split[0] == 'kep':
        kpar = self.keplerian[par_split[1]].get_param().index(par_split[2])
        value_dict[par] = self.keplerian[par_split[1]].get_value()[kpar]
      else:
        ts_param[par_split[0]].append('.'.join(par_split[1:]))
    for key in ts_param:
      if len(ts_param[key]) > 0:
        value = self.timeseries[key].get_param(ts_param[key])
        for par, val in zip(ts_param[key], value):
          value_dict[f'{key}.{par}'] = val
    return value_dict

  def _set_default_param(self, value_dict):
    ts_param = {key: [] for key in self.timeseries}
    ts_value = {key: [] for key in self.timeseries}
    kep_value = {name: self.keplerian[name].get_value() for name in self.keplerian}
    kep_change = []
    for par, val in value_dict.items():
      par_split = par.split('.')
      if par_split[0] == 'kep':
        kpar = self.keplerian[par_split[1]].get_param().index(par_split[2])
        kep_value[par_split[1]][kpar] = val
        kep_change.append(par_split[1])
      else:
        ts_param[par_split[0]].append('.'.join(par_split[1:]))
        ts_value[par_split[0]].append(val)
    for key in self.timeseries:
      if len(ts_param[key]) > 0:
        self.timeseries[key].set_param(ts_value[key], ts_param[key])
    for name in kep_change:
      self.keplerian[name].set_value(kep_value[name])
