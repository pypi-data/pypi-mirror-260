# -*- coding: utf-8 -*-

# Copyright 2019-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

__all__ = ['Keplerian']

import numpy as np

from . import libkeplerian


class Keplerian:
  r"""
  Keplerian class.

  Parameters
  ----------
  value : (p,) ndarray
    Values of the parameters listed in `param`.
  param : list
    List of the defined Keplerian parameters, among:

    - 'n' : mean-motion,
    - 'P', 'log10P' : period,
    - 'M0' : mean anomaly at t=0,
    - 'Marg0' : mean argument at t=0 (M0 + omega),
    - 'la0' : mean longitude at t=0 (M0 + varpi),
    - 'Tp' : time of periastron passage,
    - 'Tc' : time of conjunction,
    - 'TVmin' : time of minimum of radial velocity,
    - 'TVmax' : time of maximum of radial velocity,
    - 'K', 'log10K' : radial velocity semi-amplitude
    - 'as' : semi-major axis of the star
    - 'assini',
    - 'e' : eccentricity,
    - 'omega', 'w' : argument of periastron,
    - 'ecosw', 'esinw',
    - 'sqecosw', 'sqecosw',
    - 'varpi' : longitude of periastron (w + bigw),
    - 'i' : inclination,
    - 'bigomega', 'bigw' : longitude of ascending node,
    - 'TIA', 'TIB', 'TIF', 'TIG' : Thiele-Innes coefficients,

  velocity_coef : double
    Coefficient used for the definition of the velocity unit
    as a function of the distance and time units.
    The default value (1731456.8368055555) corresponds to
    AU for the distance, d for the time, and m/s for the velocity
    (following `IAU - Resolution B3 <http://arxiv.org/abs/1510.07674>`_).
  """

  def __init__(
    self, value, param=['n', 'M0', 'K', 'e', 'omega'], velocity_coef=1731456.8368055555
  ):
    self.velocity_coef = velocity_coef
    self._nparam = len(param)
    self._param = param
    self._index = np.empty(libkeplerian.NINDEX, dtype=int)
    self._ptype = np.full(libkeplerian.NINDEX, libkeplerian.NONE, dtype=int)
    self._par = np.empty(libkeplerian.NINDEX)
    self._dpar = np.empty(libkeplerian.NINDEX)
    self._vpar = np.empty(libkeplerian.NINDEX)
    self._apar = np.empty(libkeplerian.NINDEX)
    for k, (par, val) in enumerate(zip(param, value)):
      parU = (
        par.upper()
        .replace('_', '')
        .replace('SQRT', 'SQ')
        .replace('OMEGA', 'W')
        .replace('ASIN', 'ASSIN')
        .replace('AS', 'A')
        .replace('INC', 'I')
      )
      if parU == 'N':
        self._par[libkeplerian.INDEX_FREQ] = val
        self._ptype[libkeplerian.INDEX_FREQ] = libkeplerian.FREQ_N
        self._index[k] = libkeplerian.INDEX_FREQ
      elif parU == 'P':
        self._par[libkeplerian.INDEX_FREQ] = val
        self._ptype[libkeplerian.INDEX_FREQ] = libkeplerian.FREQ_P
        self._index[k] = libkeplerian.INDEX_FREQ
      elif parU == 'LOG10P':
        self._par[libkeplerian.INDEX_FREQ] = val
        self._ptype[libkeplerian.INDEX_FREQ] = libkeplerian.FREQ_LOG10P
        self._index[k] = libkeplerian.INDEX_FREQ
      elif parU == 'M0':
        self._par[libkeplerian.INDEX_PHASE] = val
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_M0
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'MARG0':
        self._par[libkeplerian.INDEX_PHASE] = val
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_MARG0
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'LA0':
        self._par[libkeplerian.INDEX_PHASE] = val
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_LA0
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'TP':
        self._par[libkeplerian.INDEX_PHASE] = val
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_TP
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'TC':
        self._par[libkeplerian.INDEX_PHASE] = val
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_TC
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'TVMIN':
        self._par[libkeplerian.INDEX_PHASE] = val
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_TVMIN
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'TVMAX':
        self._par[libkeplerian.INDEX_PHASE] = val
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_TVMAX
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'K':
        self._par[libkeplerian.INDEX_AMP] = val
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_K
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'LOG10K':
        self._par[libkeplerian.INDEX_AMP] = val
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_LOG10K
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'A':
        self._par[libkeplerian.INDEX_AMP] = val
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_AS
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'ASINI':
        self._par[libkeplerian.INDEX_AMP] = val
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_AS_SINI
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'E':
        self._par[libkeplerian.INDEX_ECC] = val
        self._ptype[libkeplerian.INDEX_ECC] = libkeplerian.ECC_E
        self._index[k] = libkeplerian.INDEX_ECC
      elif parU == 'W':
        self._par[libkeplerian.INDEX_OMEGA] = val
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_OMEGA
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU in ['VARPI', 'VPI']:
        self._par[libkeplerian.INDEX_OMEGA] = val
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_VARPI
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU == 'ECOSW':
        self._par[libkeplerian.INDEX_ECC] = val
        self._ptype[libkeplerian.INDEX_ECC] = libkeplerian.ECC_K
        self._index[k] = libkeplerian.INDEX_ECC
      elif parU == 'ESINW':
        self._par[libkeplerian.INDEX_OMEGA] = val
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_H
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU == 'SQECOSW':
        self._par[libkeplerian.INDEX_ECC] = val
        self._ptype[libkeplerian.INDEX_ECC] = libkeplerian.ECC_SQK
        self._index[k] = libkeplerian.INDEX_ECC
      elif parU == 'SQESINW':
        self._par[libkeplerian.INDEX_OMEGA] = val
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_SQH
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU == 'I':
        self._par[libkeplerian.INDEX_INC] = val
        self._ptype[libkeplerian.INDEX_INC] = libkeplerian.INC_I
        self._index[k] = libkeplerian.INDEX_INC
      elif parU == 'COSI':
        self._par[libkeplerian.INDEX_INC] = val
        self._ptype[libkeplerian.INDEX_INC] = libkeplerian.INC_COSI
        self._index[k] = libkeplerian.INDEX_INC
      elif parU == 'BIGW':
        self._par[libkeplerian.INDEX_BIGOMEGA] = val
        self._ptype[libkeplerian.INDEX_BIGOMEGA] = libkeplerian.BIGOMEGA_BIGOMEGA
        self._index[k] = libkeplerian.INDEX_BIGOMEGA
      elif parU == 'TIA':
        self._par[libkeplerian.INDEX_AMP] = val
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_TIA
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'TIB':
        self._par[libkeplerian.INDEX_OMEGA] = val
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_TIB
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU == 'TIF':
        self._par[libkeplerian.INDEX_INC] = val
        self._ptype[libkeplerian.INDEX_INC] = libkeplerian.INC_TIF
        self._index[k] = libkeplerian.INDEX_INC
      elif parU == 'TIG':
        self._par[libkeplerian.INDEX_BIGOMEGA] = val
        self._ptype[libkeplerian.INDEX_BIGOMEGA] = libkeplerian.BIGOMEGA_TIG
        self._index[k] = libkeplerian.INDEX_BIGOMEGA
      else:
        raise Exception('Unknown parameter ({}).'.format(par))

  def get_param(self):
    r"""
    Get the list of currently defined parameters.

    Returns
    -------
    param : list
      List of currently defined parameters.
    """

    return self._param.copy()

  def set_param(self, param=['n', 'M0', 'K', 'e', 'omega']):
    r"""
    Switch the set of defined parameters.

    Parameters
    ----------
    param : list
      List of new parameters.
    """

    libkeplerian.par2dpar(self._ptype, self._par, self._dpar, self.velocity_coef)
    self._nparam = len(param)
    self._param = param
    for k, par in enumerate(param):
      parU = (
        par.upper()
        .replace('_', '')
        .replace('SQRT', 'SQ')
        .replace('OMEGA', 'W')
        .replace('ASIN', 'ASSIN')
        .replace('AS', 'A')
        .replace('INC', 'I')
      )
      if parU == 'N':
        self._ptype[libkeplerian.INDEX_FREQ] = libkeplerian.FREQ_N
        self._index[k] = libkeplerian.INDEX_FREQ
      elif parU == 'P':
        self._ptype[libkeplerian.INDEX_FREQ] = libkeplerian.FREQ_P
        self._index[k] = libkeplerian.INDEX_FREQ
      elif parU == 'LOG10P':
        self._ptype[libkeplerian.INDEX_FREQ] = libkeplerian.FREQ_LOG10P
        self._index[k] = libkeplerian.INDEX_FREQ
      elif parU == 'M0':
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_M0
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'MARG0':
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_MARG0
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'LA0':
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_LA0
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'TP':
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_TP
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'TC':
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_TC
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'TVMIN':
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_TVMIN
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'TVMAX':
        self._ptype[libkeplerian.INDEX_PHASE] = libkeplerian.PHASE_TVMAX
        self._index[k] = libkeplerian.INDEX_PHASE
      elif parU == 'K':
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_K
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'LOG10K':
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_LOG10K
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'A':
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_AS
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'ASINI':
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_AS_SINI
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'E':
        self._ptype[libkeplerian.INDEX_ECC] = libkeplerian.ECC_E
        self._index[k] = libkeplerian.INDEX_ECC
      elif parU == 'W':
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_OMEGA
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU in ['VARPI', 'VPI']:
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_VARPI
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU == 'ECOSW':
        self._ptype[libkeplerian.INDEX_ECC] = libkeplerian.ECC_K
        self._index[k] = libkeplerian.INDEX_ECC
      elif parU == 'ESINW':
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_H
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU == 'SQECOSW':
        self._ptype[libkeplerian.INDEX_ECC] = libkeplerian.ECC_SQK
        self._index[k] = libkeplerian.INDEX_ECC
      elif parU == 'SQESINW':
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_SQH
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU == 'I':
        self._ptype[libkeplerian.INDEX_INC] = libkeplerian.INC_I
        self._index[k] = libkeplerian.INDEX_INC
      elif parU == 'COSI':
        self._ptype[libkeplerian.INDEX_INC] = libkeplerian.INC_COSI
        self._index[k] = libkeplerian.INDEX_INC
      elif parU == 'BIGW':
        self._ptype[libkeplerian.INDEX_BIGOMEGA] = libkeplerian.BIGOMEGA_BIGOMEGA
        self._index[k] = libkeplerian.INDEX_BIGOMEGA
      elif parU == 'TIA':
        self._ptype[libkeplerian.INDEX_AMP] = libkeplerian.AMP_TIA
        self._index[k] = libkeplerian.INDEX_AMP
      elif parU == 'TIB':
        self._ptype[libkeplerian.INDEX_OMEGA] = libkeplerian.OMEGA_TIB
        self._index[k] = libkeplerian.INDEX_OMEGA
      elif parU == 'TIF':
        self._ptype[libkeplerian.INDEX_INC] = libkeplerian.INC_TIF
        self._index[k] = libkeplerian.INDEX_INC
      elif parU == 'TIG':
        self._ptype[libkeplerian.INDEX_BIGOMEGA] = libkeplerian.BIGOMEGA_TIG
        self._index[k] = libkeplerian.INDEX_BIGOMEGA
      else:
        raise Exception('Unknown parameter ({}).'.format(par))
    libkeplerian.dpar2par(self._dpar, self._ptype, self._par, self.velocity_coef)

  def get_value(self):
    r"""
    Get the values of currently defined parameters.

    Returns
    -------
    value : (p,) ndarray
      Values of currently defined parameters.
    """

    return self._par[self._index[: self._nparam]]

  def set_value(self, value):
    r"""
    Set the values of currently defined parameters.

    Parameters
    ----------
    value : (p,) ndarray
      New values.
    """

    for ind, val in zip(self._index[: self._nparam], value):
      self._par[ind] = val

  def rv(self, t):
    r"""
    Compute the star radial velocity time series due to the Keplerian.

    Parameters
    ----------
    t : (n,) ndarray
      Calendar of the time series.

    Returns
    -------
    v : (n,) ndarray
      The radial velocity time series.
    """

    self._t = t
    self._nt = t.size
    v = np.empty(self._nt)
    self._th = np.empty(self._nt)
    libkeplerian.par2vpar(self._ptype, self._par, self._vpar, self.velocity_coef)
    libkeplerian.rv_vpar(self._nt, t, self._vpar, v, self._th)
    return v

  def rv_back(self, grad_rv):
    r"""
    Backward propagation of the gradient for :func:`rv`.

    Propagate the gradient of a function with respect
    to the radial velocity time series,
    to its gradient with respect to the currently defined Keplerian parameters.

    Parameters
    ----------
    grad_rv : (n,) ndarray
      Gradient of the function with respect to the radial velocity time series.

    Returns
    -------
    grad_param : (p,) ndarray
      Gradient of the function with respect to currently defined parameters.
    """

    grad_par = np.empty(libkeplerian.NINDEX)
    grad_vpar = np.empty(libkeplerian.NINDEX)
    libkeplerian.rv_vpar_back(
      self._nt, self._t, self._vpar, grad_rv, grad_vpar, self._th
    )
    libkeplerian.par2vpar_back(self._ptype, self._par, self._vpar, grad_vpar, grad_par)
    return grad_par[self._index[: self._nparam]]

  def astro(self, t):
    r"""
    Compute the star astrometric time series due to the Keplerian.

    Parameters
    ----------
    t : (n,) ndarray
      Calendar of the time series.

    Returns
    -------
    delta, alpha : (n,) ndarrays
      The astrometric time series.
    """

    self._t = t
    self._nt = t.size
    delta = np.empty(self._nt)
    alpha = np.empty(self._nt)
    self._cosE = np.empty(self._nt)
    self._sinE = np.empty(self._nt)
    libkeplerian.par2apar(
      self._ptype, self._par, self._apar, self._dpar, self.velocity_coef
    )
    libkeplerian.astro_apar(
      self._nt, t, self._apar, delta, alpha, self._cosE, self._sinE
    )
    return (delta, alpha)

  def astro_back(self, grad_delta, grad_alpha):
    r"""
    Backward propagation of the gradient for :func:`astro`.

    Propagate the gradient of a function with respect
    to the astrometric time series,
    to its gradient with respect to the currently defined Keplerian parameters.

    Parameters
    ----------
    grad_delta, grad_alpha : (n,) ndarray
      Gradient of the function with respect to the astrometric time series.

    Returns
    -------
    grad_param : (p,) ndarray
      Gradient of the function with respect to currently defined parameters.
    """

    grad_par = np.empty(libkeplerian.NINDEX)
    grad_dpar = np.empty(libkeplerian.NINDEX)
    grad_apar = np.empty(libkeplerian.NINDEX)
    libkeplerian.astro_apar_back(
      self._nt,
      self._t,
      self._apar,
      grad_delta,
      grad_alpha,
      grad_apar,
      self._cosE,
      self._sinE,
    )
    libkeplerian.par2apar_back(
      self._ptype, self._par, self._apar, grad_apar, grad_par, self._dpar, grad_dpar
    )
    return grad_par[self._index[: self._nparam]]
