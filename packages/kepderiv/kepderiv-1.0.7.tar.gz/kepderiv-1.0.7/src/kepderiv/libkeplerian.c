// Copyright 2019-2024 Jean-Baptiste Delisle
// Licensed under the EUPL-1.2 or later

#include "libkeplerian.h"

void M2E(double M, double e, double ftol, long maxiter, double *E)
{
  // Compute eccentric anomaly from mean anomaly (and eccentricity),
  // by solving Kepler's equation using Newton method.

  long iter;
  double diff, d1, d2, d3, dE;
  *E = M + ((sin(M) > 0) ? 0.85 : -0.85) * e;

  for (iter = 0; iter < maxiter; iter++) {
    d2 = e * sin(*E);
    d3 = e * cos(*E);
    d1 = 1.0 - d3;
    diff = M - *E + d2;
    dE = diff / d1;
    dE = diff / (d1 + dE * d2 / 2.0);
    dE = diff / (d1 + dE * (d2 / 2.0 + dE * d3 / 6.0));
    *E += dE;
    if (fabs(dE) < ftol) {
      break;
    }
  }
}

void rv_vpar(long nt, double *t, double *vpar, double *rv, double *th)
{
  // Compute the star radial velocity induced by a planet,
  // using the default set of orbital parameters.

  long i;
  double n, M0, K, e, omega;
  double k, coef_e, M, E;

  n = vpar[INDEX_FREQ];
  M0 = vpar[INDEX_PHASE];
  K = vpar[INDEX_AMP];
  e = vpar[INDEX_ECC];
  omega = vpar[INDEX_OMEGA];

  k = e * cos(omega);
  coef_e = sqrt((1.0 + e) / (1.0 - e));
  for (i = 0; i < nt; i++) {
    // Mean anomaly
    M = M0 + n * t[i];
    // Eccentric anomaly
    M2E(M, e, 5e-16, 10, &E);
    // True anomaly
    th[i] = 2.0 * atan(coef_e * tan(E / 2.0));
    // rv
    rv[i] = K * (cos(th[i] + omega) + k);
  }
}

void astro_apar(
  long nt, double *t, double *apar, double *delta, double *alpha, double *cosE,
  double *sinE)
{
  // Compute the star astrometric motion induced by a planet,
  // using the astro set of orbital parameters.

  long i;
  double n, M0, e, A, B, F, G;
  double sqe2, M, E, x, y;

  n = apar[INDEX_FREQ];
  M0 = apar[INDEX_PHASE];
  e = apar[INDEX_ECC];
  A = apar[INDEX_AMP];
  B = apar[INDEX_OMEGA];
  F = apar[INDEX_INC];
  G = apar[INDEX_BIGOMEGA];
  sqe2 = sqrt(1.0 - e * e);

  for (i = 0; i < nt; i++) {
    // Mean anomaly
    M = M0 + n * t[i];
    // Eccentric anomaly
    M2E(M, e, 5e-16, 10, &E);
    cosE[i] = cos(E);
    sinE[i] = sin(E);
    // x, y
    x = cosE[i] - e;
    y = sqe2 * sinE[i];
    delta[i] = A * x + F * y;
    alpha[i] = B * x + G * y;
  }
}

void time2M0(double *par, double *dpar, double thT)
{
  // Compute the mean anomaly at reference time
  // from the time at which the true anomaly is thT.

  double ET, MT;
  ET = 2.0 *
    atan(sqrt((1.0 - dpar[INDEX_ECC]) / (1.0 + dpar[INDEX_ECC])) *
         tan(thT / 2.0));
  MT = ET - dpar[INDEX_ECC] * sin(ET);
  dpar[INDEX_PHASE] = MT - dpar[INDEX_FREQ] * par[INDEX_PHASE];
}

void M02time(double *dpar, double *par, double thT)
{
  // Compute the time at which the true anomaly is thT
  // from the mean anomaly at reference time.

  double ET, MT;
  ET = 2.0 *
    atan(sqrt((1.0 - dpar[INDEX_ECC]) / (1.0 + dpar[INDEX_ECC])) *
         tan(thT / 2.0));
  MT = ET - dpar[INDEX_ECC] * sin(ET);
  par[INDEX_PHASE] = (MT - dpar[INDEX_PHASE]) / dpar[INDEX_FREQ];
}

void par2dpar(long *ptype, double *par, double *dpar, double velocity_coef)
{
  // Compute default parameters from specified parameters.
  // Default parameters:
  // FREQ_N, AMP_AS, PHASE_M0, ECC_E, OMEGA_OMEGA, INC_I, BIGOMEGA_BIGOMEGA

  double sini, A, B, F, G, popovic_k, popovic_m, popovic_j, vpi, Omo;

  // Compute mean-motion
  switch (ptype[INDEX_FREQ]) {
  case FREQ_P:
    dpar[INDEX_FREQ] = M_2PI / par[INDEX_FREQ];
    break;
  case FREQ_LOG10P:
    dpar[INDEX_FREQ] = M_2PI * pow(10.0, -par[INDEX_FREQ]);
    break;
  default:
    dpar[INDEX_FREQ] = par[INDEX_FREQ];
  }

  // Compute i, sini or solve parameters from ABFG using Popovic 1995
  switch (ptype[INDEX_INC]) {
  case INC_I:
    dpar[INDEX_INC] = par[INDEX_INC];
    sini = sin(par[INDEX_INC]);
    break;
  case INC_COSI:
    dpar[INDEX_INC] = acos(par[INDEX_INC]);
    sini = sqrt(1.0 - par[INDEX_INC] * par[INDEX_INC]);
    break;
  case INC_TIF: // Assume the parameters to be A, B, F, G.
    A = par[INDEX_AMP];
    B = par[INDEX_OMEGA];
    F = par[INDEX_INC];
    G = par[INDEX_BIGOMEGA];
    popovic_k = (A * A + B * B + F * F + G * G) / 2.0;
    popovic_m = A * G - B * F;
    popovic_j = sqrt(popovic_k * popovic_k - popovic_m * popovic_m);
    dpar[INDEX_AMP] = sqrt(popovic_j + popovic_k); // as
    dpar[INDEX_INC] = atan2(dpar[INDEX_AMP] * sqrt(2.0 * popovic_j), popovic_m);
    vpi = atan2(B - F, A + G);
    Omo = atan2(B + F, A - G);
    dpar[INDEX_BIGOMEGA] = fmod((vpi + Omo) / 2.0 + M_2PI, M_PI);
    dpar[INDEX_OMEGA] = fmod(vpi - dpar[INDEX_BIGOMEGA] + M_2PI, M_2PI);
    break;
  default:
    dpar[INDEX_INC] = M_PI_2;
    sini = 1.0;
  }

  // Compute BIGOMEGA
  switch (ptype[INDEX_BIGOMEGA]) {
  case BIGOMEGA_BIGOMEGA:
    dpar[INDEX_BIGOMEGA] = par[INDEX_BIGOMEGA];
    break;
  case BIGOMEGA_TIG:
    break;
  default:
    dpar[INDEX_BIGOMEGA] = 0.0;
  }

  // Compute e, omega, vpi
  switch (ptype[INDEX_ECC]) {
  case ECC_K:
    dpar[INDEX_ECC] = sqrt(
      par[INDEX_ECC] * par[INDEX_ECC] + par[INDEX_OMEGA] * par[INDEX_OMEGA]);
    dpar[INDEX_OMEGA] = atan2(par[INDEX_OMEGA], par[INDEX_ECC]);
    break;
  case ECC_SQK:
    dpar[INDEX_ECC] =
      par[INDEX_ECC] * par[INDEX_ECC] + par[INDEX_OMEGA] * par[INDEX_OMEGA];
    dpar[INDEX_OMEGA] = atan2(par[INDEX_OMEGA], par[INDEX_ECC]);
    break;
  default:
    dpar[INDEX_ECC] = par[INDEX_ECC];
  }

  switch (ptype[INDEX_OMEGA]) {
  case OMEGA_TIB:
    break;
  case OMEGA_VARPI:
    vpi = par[INDEX_OMEGA];
    dpar[INDEX_OMEGA] = vpi - dpar[INDEX_BIGOMEGA];
    break;
  case OMEGA_OMEGA:
    dpar[INDEX_OMEGA] = par[INDEX_OMEGA];
  default:
    vpi = dpar[INDEX_OMEGA] + dpar[INDEX_BIGOMEGA];
  }

  // Compute M0
  switch (ptype[INDEX_PHASE]) {
  case PHASE_MARG0:
    dpar[INDEX_PHASE] = par[INDEX_PHASE] - dpar[INDEX_OMEGA];
    break;
  case PHASE_LA0:
    dpar[INDEX_PHASE] = par[INDEX_PHASE] - vpi;
    break;
  case PHASE_TP:
    dpar[INDEX_PHASE] = -dpar[INDEX_FREQ] * par[INDEX_PHASE];
    break;
  case PHASE_TC:
    time2M0(par, dpar, M_PI_2 - dpar[INDEX_OMEGA]);
    break;
  case PHASE_TVMIN:
    time2M0(par, dpar, -dpar[INDEX_OMEGA]);
    break;
  case PHASE_TVMAX:
    time2M0(par, dpar, M_PI - dpar[INDEX_OMEGA]);
    break;
  default:
    dpar[INDEX_PHASE] = par[INDEX_PHASE];
  }

  // Compute a_s
  switch (ptype[INDEX_AMP]) {
  case AMP_K:
    dpar[INDEX_AMP] = par[INDEX_AMP] / velocity_coef *
      sqrt(1.0 - dpar[INDEX_ECC] * dpar[INDEX_ECC]) / (dpar[INDEX_FREQ] * sini);
    break;
  case AMP_LOG10K:
    dpar[INDEX_AMP] = pow(10.0, par[INDEX_AMP]) / velocity_coef *
      sqrt(1.0 - dpar[INDEX_ECC] * dpar[INDEX_ECC]) / (dpar[INDEX_FREQ] * sini);
    break;
  case AMP_AS_SINI:
    dpar[INDEX_AMP] = par[INDEX_AMP] / sini;
    break;
  case AMP_AS:
    dpar[INDEX_AMP] = par[INDEX_AMP];
    break;
  case AMP_TIA:
    break;
  default:
    dpar[INDEX_AMP] = 0.0;
  }
}

void dpar2par(double *dpar, long *ptype, double *par, double velocity_coef)
{
  // Compute specified parameters from default parameters.
  // Default parameters:
  // FREQ_N, AMP_AS, PHASE_M0, ECC_E, OMEGA_OMEGA, INC_I, BIGOMEGA_BIGOMEGA

  double sqe, cosi, sini, vpi, coso, sino, cosO, sinO;

  // mean-motion
  switch (ptype[INDEX_FREQ]) {
  case FREQ_P:
    par[INDEX_FREQ] = M_2PI / dpar[INDEX_FREQ];
    break;
  case FREQ_LOG10P:
    par[INDEX_FREQ] = log10(M_2PI / dpar[INDEX_FREQ]);
    break;
  default:
    par[INDEX_FREQ] = dpar[INDEX_FREQ];
  }

  // Inclination
  sini = sin(dpar[INDEX_INC]);
  switch (ptype[INDEX_INC]) {
  case INC_I:
    par[INDEX_INC] = dpar[INDEX_INC];
    break;
  case INC_COSI:
    par[INDEX_INC] = cos(dpar[INDEX_INC]);
    break;
  case INC_TIF: // Assume the parameters to be A, B, F, G.
    // Compute ABFG
    cosi = cos(dpar[INDEX_INC]);
    coso = cos(dpar[INDEX_OMEGA]);
    sino = sin(dpar[INDEX_OMEGA]);
    cosO = cos(dpar[INDEX_BIGOMEGA]);
    sinO = sin(dpar[INDEX_BIGOMEGA]);
    par[INDEX_AMP] = dpar[INDEX_AMP] * (coso * cosO - sino * sinO * cosi);
    par[INDEX_OMEGA] = dpar[INDEX_AMP] * (coso * sinO + sino * cosO * cosi);
    par[INDEX_INC] = dpar[INDEX_AMP] * (-sino * cosO - coso * sinO * cosi);
    par[INDEX_BIGOMEGA] = dpar[INDEX_AMP] * (-sino * sinO + coso * cosO * cosi);
    break;
  }

  // BIGOMEGA
  if (ptype[INDEX_BIGOMEGA] == BIGOMEGA_BIGOMEGA) {
    par[INDEX_BIGOMEGA] = dpar[INDEX_BIGOMEGA];
  }

  // e, omega, vpi
  switch (ptype[INDEX_ECC]) {
  case ECC_K:
    par[INDEX_ECC] = dpar[INDEX_ECC] * cos(dpar[INDEX_OMEGA]);
    par[INDEX_OMEGA] = dpar[INDEX_ECC] * sin(dpar[INDEX_OMEGA]);
    break;
  case ECC_SQK:
    sqe = sqrt(dpar[INDEX_ECC]);
    par[INDEX_ECC] = sqe * cos(dpar[INDEX_OMEGA]);
    par[INDEX_OMEGA] = sqe * sin(dpar[INDEX_OMEGA]);
    break;
  default:
    par[INDEX_ECC] = dpar[INDEX_ECC];
  }
  vpi = dpar[INDEX_OMEGA] + dpar[INDEX_BIGOMEGA];
  switch (ptype[INDEX_OMEGA]) {
  case OMEGA_VARPI:
    par[INDEX_OMEGA] = vpi;
    break;
  case OMEGA_OMEGA:
    par[INDEX_OMEGA] = dpar[INDEX_OMEGA];
    break;
  }

  // Phase
  switch (ptype[INDEX_PHASE]) {
  case PHASE_MARG0:
    par[INDEX_PHASE] = dpar[INDEX_PHASE] + dpar[INDEX_OMEGA];
    break;
  case PHASE_LA0:
    par[INDEX_PHASE] = dpar[INDEX_PHASE] + vpi;
    break;
  case PHASE_TP:
    par[INDEX_PHASE] = -dpar[INDEX_PHASE] / dpar[INDEX_FREQ];
    break;
  case PHASE_TC:
    M02time(dpar, par, M_PI_2 - dpar[INDEX_OMEGA]);
    break;
  case PHASE_TVMIN:
    M02time(dpar, par, -dpar[INDEX_OMEGA]);
    break;
  case PHASE_TVMAX:
    M02time(dpar, par, M_PI - dpar[INDEX_OMEGA]);
    break;
  default:
    par[INDEX_PHASE] = dpar[INDEX_PHASE];
  }

  // Amplitude
  switch (ptype[INDEX_AMP]) {
  case AMP_K:
    par[INDEX_AMP] = velocity_coef * dpar[INDEX_AMP] * dpar[INDEX_FREQ] * sini /
      sqrt(1.0 - dpar[INDEX_ECC] * dpar[INDEX_ECC]);
    break;
  case AMP_LOG10K:
    par[INDEX_AMP] = log10(
      velocity_coef * dpar[INDEX_AMP] * dpar[INDEX_FREQ] * sini /
      sqrt(1.0 - dpar[INDEX_ECC] * dpar[INDEX_ECC]));
    break;
  case AMP_AS_SINI:
    par[INDEX_AMP] = dpar[INDEX_AMP] * sini;
    break;
  case AMP_TIA:
    break;
  default:
    par[INDEX_AMP] = dpar[INDEX_AMP];
  }
}

void par2vpar(long *ptype, double *par, double *vpar, double velocity_coef)
{
  // Compute rv parameters from specified parameters.
  // RV parameters:
  // FREQ_N, AMP_K, PHASE_M0, ECC_E, OMEGA_OMEGA

  double sini, A, B, F, G, popovic_k, popovic_m, popovic_j, vpi, Omo, Omega;

  // Compute mean-motion
  switch (ptype[INDEX_FREQ]) {
  case FREQ_P:
    vpar[INDEX_FREQ] = M_2PI / par[INDEX_FREQ];
    break;
  case FREQ_LOG10P:
    vpar[INDEX_FREQ] = M_2PI * pow(10.0, -par[INDEX_FREQ]);
    break;
  default:
    vpar[INDEX_FREQ] = par[INDEX_FREQ];
  }

  // Compute sin(i) or solve parameters from ABFG using Popovic 1995
  switch (ptype[INDEX_INC]) {
  case INC_I:
    sini = sin(par[INDEX_INC]);
    break;
  case INC_COSI:
    sini = sqrt(1.0 - par[INDEX_INC] * par[INDEX_INC]);
    break;
  case INC_TIF: // Assume the parameters to be A, B, F, G.
    A = par[INDEX_AMP];
    B = par[INDEX_OMEGA];
    F = par[INDEX_INC];
    G = par[INDEX_BIGOMEGA];
    popovic_k = (A * A + B * B + F * F + G * G) / 2.0;
    popovic_m = A * G - B * F;
    popovic_j = sqrt(popovic_k * popovic_k - popovic_m * popovic_m);
    vpar[INDEX_AMP] = velocity_coef * vpar[INDEX_FREQ] *
      sqrt(2.0 * popovic_j / (1.0 - vpar[INDEX_ECC] * vpar[INDEX_ECC]));
    vpi = atan2(B - F, A + G);
    Omo = atan2(B + F, A - G);
    Omega = fmod((vpi + Omo) / 2.0, M_PI);
    vpar[INDEX_OMEGA] = fmod(vpi - Omega, M_2PI);
    break;
  default:
    sini = 1.0;
  }

  // Compute BIGOMEGA
  switch (ptype[INDEX_BIGOMEGA]) {
  case BIGOMEGA_BIGOMEGA:
    Omega = par[INDEX_BIGOMEGA];
    break;
  case BIGOMEGA_TIG:
    break;
  default:
    Omega = 0.0;
  }

  // Compute e, omega, vpi
  switch (ptype[INDEX_ECC]) {
  case ECC_K:
    vpar[INDEX_ECC] = sqrt(
      par[INDEX_ECC] * par[INDEX_ECC] + par[INDEX_OMEGA] * par[INDEX_OMEGA]);
    vpar[INDEX_OMEGA] = atan2(par[INDEX_OMEGA], par[INDEX_ECC]);
    break;
  case ECC_SQK:
    vpar[INDEX_ECC] =
      par[INDEX_ECC] * par[INDEX_ECC] + par[INDEX_OMEGA] * par[INDEX_OMEGA];
    vpar[INDEX_OMEGA] = atan2(par[INDEX_OMEGA], par[INDEX_ECC]);
    break;
  default:
    vpar[INDEX_ECC] = par[INDEX_ECC];
  }
  switch (ptype[INDEX_OMEGA]) {
  case OMEGA_VARPI:
    vpi = par[INDEX_OMEGA];
    vpar[INDEX_OMEGA] = vpi - Omega;
    break;
  case OMEGA_OMEGA:
    vpar[INDEX_OMEGA] = par[INDEX_OMEGA];
  default:
    vpi = vpar[INDEX_OMEGA] + Omega;
  }

  // Compute M0
  switch (ptype[INDEX_PHASE]) {
  case PHASE_MARG0:
    vpar[INDEX_PHASE] = par[INDEX_PHASE] - vpar[INDEX_OMEGA];
    break;
  case PHASE_LA0:
    vpar[INDEX_PHASE] = par[INDEX_PHASE] - vpi;
    break;
  case PHASE_TP:
    vpar[INDEX_PHASE] = -vpar[INDEX_FREQ] * par[INDEX_PHASE];
    break;
  case PHASE_TC:
    time2M0(par, vpar, M_PI_2 - vpar[INDEX_OMEGA]);
    break;
  case PHASE_TVMIN:
    time2M0(par, vpar, -vpar[INDEX_OMEGA]);
    break;
  case PHASE_TVMAX:
    time2M0(par, vpar, M_PI - vpar[INDEX_OMEGA]);
    break;
  default:
    vpar[INDEX_PHASE] = par[INDEX_PHASE];
  }

  // Compute K
  switch (ptype[INDEX_AMP]) {
  case AMP_LOG10K:
    vpar[INDEX_AMP] = pow(10.0, par[INDEX_AMP]);
    break;
  case AMP_AS:
    vpar[INDEX_AMP] = velocity_coef * par[INDEX_AMP] * sini * vpar[INDEX_FREQ] /
      sqrt(1.0 - vpar[INDEX_ECC] * vpar[INDEX_ECC]);
    break;
  case AMP_AS_SINI:
    vpar[INDEX_AMP] = velocity_coef * par[INDEX_AMP] * vpar[INDEX_FREQ] /
      sqrt(1.0 - vpar[INDEX_ECC] * vpar[INDEX_ECC]);
    break;
  case AMP_TIA:
    break;
  default:
    vpar[INDEX_AMP] = par[INDEX_AMP];
  }
}

void dpar2apar(double *dpar, double *apar)
{
  // Compute astro parameters from default parameters.
  // Astro parameters:
  // FREQ_N, ECC_E, PHASE_M0, AMP_TIA, OMEGA_TIB, INC_TIF, BIGOMEGA_TIG
  // Default parameters:
  // FREQ_N, AMP_AS, PHASE_M0, ECC_E, OMEGA_OMEGA, INC_I, BIGOMEGA_BIGOMEGA

  double cosi, coso, sino, cosO, sinO;
  apar[INDEX_FREQ] = dpar[INDEX_FREQ];
  apar[INDEX_PHASE] = dpar[INDEX_PHASE];
  apar[INDEX_ECC] = dpar[INDEX_ECC];
  cosi = cos(dpar[INDEX_INC]);
  coso = cos(dpar[INDEX_OMEGA]);
  sino = sin(dpar[INDEX_OMEGA]);
  cosO = cos(dpar[INDEX_BIGOMEGA]);
  sinO = sin(dpar[INDEX_BIGOMEGA]);
  apar[INDEX_AMP] = dpar[INDEX_AMP] * (coso * cosO - sino * sinO * cosi);
  apar[INDEX_OMEGA] = dpar[INDEX_AMP] * (coso * sinO + sino * cosO * cosi);
  apar[INDEX_INC] = dpar[INDEX_AMP] * (-sino * cosO - coso * sinO * cosi);
  apar[INDEX_BIGOMEGA] = dpar[INDEX_AMP] * (-sino * sinO + coso * cosO * cosi);
}

void par2apar(
  long *ptype, double *par, double *apar, double *dpar, double velocity_coef)
{
  // Compute astro parameters from specified parameters.
  // Astro parameters:
  // FREQ_N, ECC_E, PHASE_M0, AMP_TIA, OMEGA_TIB, INC_TIF, BIGOMEGA_TIG

  // if (ptype[INDEX_AMP] == AMP_TIA) {
  //   // Assume the parameters A, B, F, G.
  //   apar[INDEX_ECC] = par[INDEX_ECC];
  //   apar[INDEX_PHASE] = par[INDEX_PHASE];
  //   apar[INDEX_AMP] = par[INDEX_AMP];
  //   apar[INDEX_OMEGA] = par[INDEX_OMEGA];
  //   apar[INDEX_INC] = par[INDEX_INC];
  //   apar[INDEX_BIGOMEGA] = par[INDEX_BIGOMEGA];

  //   // Compute mean-motion
  //   switch (ptype[INDEX_FREQ]) {
  //   case FREQ_P:
  //     apar[INDEX_FREQ] = M_2PI / par[INDEX_FREQ];
  //     break;
  //   case FREQ_LOG10P:
  //     apar[INDEX_FREQ] = M_2PI * pow(10.0, -par[INDEX_FREQ]);
  //     break;
  //   default:
  //     apar[INDEX_FREQ] = par[INDEX_FREQ];
  //   }
  // } else {
  par2dpar(ptype, par, dpar, velocity_coef);
  dpar2apar(dpar, apar);
  // }
}

void rv_vpar_back(
  long nt, double *t, double *vpar, double *grad_rv, double *grad_vpar,
  double *th)
{
  // Compute the derivatives of the star radial velocity,
  // with respect to the default set of orbital parameters.

  long i;
  double K, e, omega;
  double cosom, k, h, ome2, sqe2;
  double l, sinl, aOr, grad_M;

  K = vpar[INDEX_AMP];
  e = vpar[INDEX_ECC];
  omega = vpar[INDEX_OMEGA];

  grad_vpar[INDEX_FREQ] = 0.0;
  grad_vpar[INDEX_PHASE] = 0.0;
  grad_vpar[INDEX_AMP] = 0.0;
  grad_vpar[INDEX_ECC] = 0.0;
  grad_vpar[INDEX_OMEGA] = 0.0;

  cosom = cos(omega);
  k = e * cosom;
  h = e * sin(omega);
  ome2 = 1.0 - e * e;
  sqe2 = sqrt(ome2);

  for (i = 0; i < nt; i++) {
    // True longitude
    l = th[i] + omega;
    sinl = sin(l);
    aOr = (1.0 + e * cos(th[i])) / ome2;

    // grad propagation
    grad_M = -K * sqe2 * sinl * aOr * aOr * grad_rv[i];
    grad_vpar[INDEX_FREQ] += t[i] * grad_M; // n
    grad_vpar[INDEX_PHASE] += grad_M; // M0
    grad_vpar[INDEX_AMP] += (cos(l) + k) * grad_rv[i]; // K
    grad_vpar[INDEX_ECC] +=
      K * (cosom - (1.0 / ome2 + aOr) * sin(th[i]) * sinl) * grad_rv[i]; // e
    grad_vpar[INDEX_OMEGA] -= K * (sinl + h) * grad_rv[i]; // omega
  }
}

void astro_apar_back(
  long nt, double *t, double *apar, double *grad_delta, double *grad_alpha,
  double *grad_apar, double *cosE, double *sinE)
{
  // Compute the derivatives of the star astrometric motion,
  // with respect to the default set of orbital parameters.

  long i;
  double e, A, B, F, G;
  double sqe2, aOr, x, y, grad_x, grad_y, grad_M;

  e = apar[INDEX_ECC];
  A = apar[INDEX_AMP];
  B = apar[INDEX_OMEGA];
  F = apar[INDEX_INC];
  G = apar[INDEX_BIGOMEGA];
  sqe2 = sqrt(1.0 - e * e);

  grad_apar[INDEX_FREQ] = 0.0;
  grad_apar[INDEX_PHASE] = 0.0;
  grad_apar[INDEX_ECC] = 0.0;
  grad_apar[INDEX_AMP] = 0.0;
  grad_apar[INDEX_OMEGA] = 0.0;
  grad_apar[INDEX_INC] = 0.0;
  grad_apar[INDEX_BIGOMEGA] = 0.0;

  for (i = 0; i < nt; i++) {
    aOr = 1.0 / (1.0 - e * cosE[i]);
    x = cosE[i] - e;
    y = sqe2 * sinE[i];
    grad_x = A * grad_delta[i] + B * grad_alpha[i];
    grad_y = F * grad_delta[i] + G * grad_alpha[i];
    grad_M = aOr * (sqe2 * cosE[i] * grad_y - sinE[i] * grad_x);
    grad_apar[INDEX_FREQ] += t[i] * grad_M;
    grad_apar[INDEX_PHASE] += grad_M;
    grad_apar[INDEX_ECC] += aOr * sinE[i] / sqe2 * x * grad_y -
      (1.0 + aOr * sinE[i] * sinE[i]) * grad_x;
    grad_apar[INDEX_AMP] += x * grad_delta[i];
    grad_apar[INDEX_OMEGA] += x * grad_alpha[i];
    grad_apar[INDEX_INC] += y * grad_delta[i];
    grad_apar[INDEX_BIGOMEGA] += y * grad_alpha[i];
  }
}

void time2M0_back(
  double *par, double *dpar, double thT, double *grad_par, double *grad_thT)
{
  // Backward propagation of the gradient for time2M0.

  double ET;
  double ome2, rOa, sinET;
  double grad_MT, grad_ET;

  // Compute ET and useful quantities
  ET = 2.0 *
    atan(sqrt((1.0 - dpar[INDEX_ECC]) / (1.0 + dpar[INDEX_ECC])) *
         tan(thT / 2.0));
  ome2 = 1.0 - dpar[INDEX_ECC] * dpar[INDEX_ECC];
  rOa = 1.0 - dpar[INDEX_ECC] * cos(ET);
  sinET = sin(ET);

  // Backpropagation
  // dpar[INDEX_PHASE] = MT - dpar[INDEX_FREQ]*par[INDEX_PHASE];
  grad_MT = grad_par[INDEX_PHASE];
  grad_par[INDEX_FREQ] -= par[INDEX_PHASE] * grad_par[INDEX_PHASE];
  grad_par[INDEX_PHASE] *= -dpar[INDEX_FREQ];
  // MT = ET - dpar[INDEX_ECC]*sin(ET);
  grad_par[INDEX_ECC] -= sinET * grad_MT;
  grad_ET = rOa * grad_MT;
  // ET = 2.0*atan(sqrt((1-dpar[INDEX_ECC])/(1+dpar[INDEX_ECC]))*tan(thT/2.0));
  *grad_thT = rOa / sqrt(ome2) * grad_ET;
  grad_par[INDEX_ECC] -= sinET / ome2 * grad_ET;
}

void M02time_back(
  double *dpar, double *par, double thT, double *grad_dpar, double *grad_thT)
{
  // Backward propagation of the gradient for M02time.

  double ET;
  double ome2, rOa, sinET;
  double grad_MT, grad_ET;

  // Compute ET and useful quantities
  ET = 2.0 *
    atan(sqrt((1.0 - dpar[INDEX_ECC]) / (1.0 + dpar[INDEX_ECC])) *
         tan(thT / 2.0));
  ome2 = 1.0 - dpar[INDEX_ECC] * dpar[INDEX_ECC];
  rOa = 1.0 - dpar[INDEX_ECC] * cos(ET);
  sinET = sin(ET);

  // Backpropagation
  // par[INDEX_PHASE] = (MT - dpar[INDEX_PHASE]) / dpar[INDEX_FREQ];
  grad_MT = grad_dpar[INDEX_PHASE] / dpar[INDEX_FREQ];
  grad_dpar[INDEX_FREQ] -=
    par[INDEX_PHASE] / dpar[INDEX_FREQ] * grad_dpar[INDEX_PHASE];
  grad_dpar[INDEX_PHASE] /= -dpar[INDEX_FREQ];
  // MT = ET - dpar[INDEX_ECC] * sin(ET);
  grad_dpar[INDEX_ECC] -= sinET * grad_MT;
  grad_ET = rOa * grad_MT;
  // ET = 2.0 * atan(sqrt((1.0 - dpar[INDEX_ECC]) / (1.0 + dpar[INDEX_ECC])) *
  // tan(thT / 2.0));
  *grad_thT = rOa / sqrt(ome2) * grad_ET;
  grad_dpar[INDEX_ECC] -= sinET / ome2 * grad_ET;
}

void atan2_back(
  double y, double x, double grad_theta, double *grad_y, double *grad_x)
{
  // Backward propagation of the gradient for atan2.

  double tmp;
  tmp = grad_theta / (x * x + y * y);
  *grad_y = x * tmp;
  *grad_x = -y * tmp;
}

void par2dpar_back(
  long *ptype, double *par, double *dpar, double *grad_dpar, double *grad_par)
{
  // Backward propagation of the gradient for par2dpar.

  double A, B, F, G, grad_A, grad_B, grad_F, grad_G, popovic_k, popovic_m,
    popovic_j;
  double grad_k, grad_m, grad_j, num, grad_num, grad_deno;
  double sini, grad_sini, grad_vpi, grad_thT, grad_Omega, cosom, sinom, tmp;
  double grad_Omo;

  memcpy(grad_par, grad_dpar, NINDEX * sizeof(double));
  grad_sini = 0.0;
  grad_vpi = 0.0;
  grad_Omega = 0.0;

  // Recompute sin(i) before propagating gradient
  switch (ptype[INDEX_INC]) {
  case INC_I:
    sini = sin(par[INDEX_INC]);
    break;
  case INC_COSI:
    sini = sqrt(1.0 - par[INDEX_INC] * par[INDEX_INC]);
    break;
  default:
    sini = 1.0;
  }

  // Gradient propagation
  // a_s
  switch (ptype[INDEX_AMP]) {
  case AMP_K:
    // dpar[INDEX_AMP] = par[INDEX_AMP]/velocity_coef *
    // sqrt(1.0-dpar[INDEX_ECC]*dpar[INDEX_ECC])/(dpar[INDEX_FREQ]*sini);
    grad_par[INDEX_FREQ] -=
      dpar[INDEX_AMP] / dpar[INDEX_FREQ] * grad_par[INDEX_AMP];
    grad_sini -= dpar[INDEX_AMP] / sini * grad_par[INDEX_AMP];
    grad_par[INDEX_ECC] -= dpar[INDEX_AMP] * dpar[INDEX_ECC] /
      (1.0 - dpar[INDEX_ECC] * dpar[INDEX_ECC]) * grad_par[INDEX_AMP];
    grad_par[INDEX_AMP] *= dpar[INDEX_AMP] / par[INDEX_AMP];
    break;
  case AMP_LOG10K:
    // dpar[INDEX_AMP] = pow(10.0, par[INDEX_AMP])/velocity_coef *
    // sqrt(1.0-dpar[INDEX_ECC]*dpar[INDEX_ECC])/(dpar[INDEX_FREQ]*sini);
    grad_par[INDEX_FREQ] -=
      dpar[INDEX_AMP] / dpar[INDEX_FREQ] * grad_par[INDEX_AMP];
    grad_sini -= dpar[INDEX_AMP] / sini * grad_par[INDEX_AMP];
    grad_par[INDEX_ECC] -= dpar[INDEX_AMP] * dpar[INDEX_ECC] /
      (1.0 - dpar[INDEX_ECC] * dpar[INDEX_ECC]) * grad_par[INDEX_AMP];
    grad_par[INDEX_AMP] *= log(10.0) * dpar[INDEX_AMP];
    break;
  case AMP_AS_SINI:
    // dpar[INDEX_AMP] = par[INDEX_AMP]/sini;
    // grad_sini -= dpar[INDEX_AMP]/sini * grad_par[INDEX_AMP];
    grad_par[INDEX_AMP] /= sini;
    grad_sini -= dpar[INDEX_AMP] * grad_par[INDEX_AMP];
    break;
  default:;
  }

  // M0
  switch (ptype[INDEX_PHASE]) {
  case PHASE_MARG0:
    // dpar[INDEX_PHASE] = par[INDEX_PHASE]-dpar[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] -= grad_par[INDEX_PHASE];
    break;
  case PHASE_LA0:
    // dpar[INDEX_PHASE] = par[INDEX_PHASE]-vpi;
    grad_vpi -= grad_par[INDEX_PHASE];
    break;
  case PHASE_TP:
    // dpar[INDEX_PHASE] = -dpar[INDEX_FREQ]*par[INDEX_PHASE];
    grad_par[INDEX_FREQ] -= par[INDEX_PHASE] * grad_par[INDEX_PHASE];
    grad_par[INDEX_PHASE] *= -dpar[INDEX_FREQ];
    break;
  case PHASE_TC:
    // time2M0(par, dpar, M_PI_2-dpar[INDEX_OMEGA]);
    time2M0_back(par, dpar, M_PI_2 - dpar[INDEX_OMEGA], grad_par, &grad_thT);
    grad_par[INDEX_OMEGA] -= grad_thT;
    break;
  case PHASE_TVMIN:
    // time2M0(par, dpar, -dpar[INDEX_OMEGA]);
    time2M0_back(par, dpar, -dpar[INDEX_OMEGA], grad_par, &grad_thT);
    grad_par[INDEX_OMEGA] -= grad_thT;
    break;
  case PHASE_TVMAX:
    // time2M0(par, dpar, M_PI-dpar[INDEX_OMEGA]);
    time2M0_back(par, dpar, M_PI - dpar[INDEX_OMEGA], grad_par, &grad_thT);
    grad_par[INDEX_OMEGA] -= grad_thT;
    break;
  default:;
  }

  // e, omega, vpi
  switch (ptype[INDEX_OMEGA]) {
  case OMEGA_TIB:
    break;
  case OMEGA_VARPI:
    // vpi = dpar[INDEX_OMEGA];
    // dpar[INDEX_OMEGA] = vpi - Omega;
    grad_Omega -= grad_par[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] += grad_vpi;
    break;
  default:
    // vpi = dpar[INDEX_OMEGA] + Omega;
    grad_par[INDEX_OMEGA] += grad_vpi;
    grad_Omega += grad_vpi;
  }

  switch (ptype[INDEX_ECC]) {
  case ECC_K:
    // dpar[INDEX_ECC] =
    // sqrt(par[INDEX_ECC]*par[INDEX_ECC]+par[INDEX_OMEGA]*par[INDEX_OMEGA]);
    // dpar[INDEX_OMEGA] = atan2(par[INDEX_OMEGA], par[INDEX_ECC]);
    cosom = par[INDEX_ECC] / dpar[INDEX_ECC];
    sinom = par[INDEX_OMEGA] / dpar[INDEX_ECC];
    grad_par[INDEX_OMEGA] /= dpar[INDEX_ECC];
    tmp = cosom * grad_par[INDEX_ECC] - sinom * grad_par[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] =
      sinom * grad_par[INDEX_ECC] + cosom * grad_par[INDEX_OMEGA];
    grad_par[INDEX_ECC] = tmp;
    break;
  case ECC_SQK:
    // dpar[INDEX_ECC] =
    // par[INDEX_ECC]*par[INDEX_ECC]+par[INDEX_OMEGA]*par[INDEX_OMEGA];
    // dpar[INDEX_OMEGA] = atan2(par[INDEX_OMEGA], par[INDEX_ECC]);
    grad_par[INDEX_ECC] *= 2.0;
    grad_par[INDEX_OMEGA] /= dpar[INDEX_ECC];
    tmp = par[INDEX_ECC] * grad_par[INDEX_ECC] -
      par[INDEX_OMEGA] * grad_par[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] = par[INDEX_ECC] * grad_par[INDEX_OMEGA] +
      par[INDEX_OMEGA] * grad_par[INDEX_ECC];
    grad_par[INDEX_ECC] = tmp;
    break;
  default:;
  }

  // BIGOMEGA
  switch (ptype[INDEX_BIGOMEGA]) {
  case BIGOMEGA_BIGOMEGA:
    // Omega = par[INDEX_BIGOMEGA];
    grad_par[INDEX_BIGOMEGA] = grad_dpar[INDEX_BIGOMEGA] + grad_Omega;
    break;
  default:;
  }

  // sin(i) or ABFG (Popovic 1995)
  switch (ptype[INDEX_INC]) {
  case INC_I:
    // sini = sin(par[INDEX_INC]);
    grad_par[INDEX_INC] = cos(par[INDEX_INC]) * grad_sini;
    // dpar[INDEX_INC] = par[INDEX_INC];
    grad_par[INDEX_INC] += grad_dpar[INDEX_INC];
    break;
  case INC_COSI:
    // sini = sqrt(1.0-par[INDEX_INC]*par[INDEX_INC]);
    grad_par[INDEX_INC] = -par[INDEX_INC] / sini * grad_sini;
    // dpar[INDEX_INC] = acos(par[INDEX_INC]);
    grad_par[INDEX_INC] -= grad_dpar[INDEX_INC] / sini;
    break;
  case INC_TIF: // Assume the parameters to be A, B, F, G.
    // Recompute useful quantities before propagating gradient
    A = par[INDEX_AMP];
    B = par[INDEX_OMEGA];
    F = par[INDEX_INC];
    G = par[INDEX_BIGOMEGA];
    popovic_k = (A * A + B * B + F * F + G * G) / 2.0;
    popovic_m = A * G - B * F;
    popovic_j = sqrt(popovic_k * popovic_k - popovic_m * popovic_m);
    // Gradient propagation
    // dpar[INDEX_OMEGA] = fmod(vpi - dpar[INDEX_BIGOMEGA] + M_2PI, M_2PI);
    grad_vpi += grad_par[INDEX_OMEGA];
    grad_par[INDEX_BIGOMEGA] -= grad_par[INDEX_OMEGA];
    // dpar[INDEX_BIGOMEGA] = fmod((vpi + Omo) / 2.0 + M_2PI, M_PI);
    grad_vpi += grad_par[INDEX_BIGOMEGA] / 2.0;
    grad_Omo = grad_par[INDEX_BIGOMEGA] / 2.0;
    // Omo = atan2(B+F, A-G);
    atan2_back(B + F, A - G, grad_Omo, &grad_num, &grad_deno);
    grad_B = grad_num;
    grad_F = grad_num;
    grad_A = grad_deno;
    grad_G = -grad_deno;
    // vpi = atan2(B-F, A+G);
    atan2_back(B - F, A + G, grad_vpi, &grad_num, &grad_deno);
    grad_B += grad_num;
    grad_F -= grad_num;
    grad_A += grad_deno;
    grad_G += grad_deno;
    // dpar[INDEX_INC] = atan2(dpar[INDEX_AMP] * sqrt(2.0 * popovic_j), popovic_m);
    num = dpar[INDEX_AMP] * sqrt(2.0 * popovic_j);
    atan2_back(num, popovic_m, grad_par[INDEX_INC], &grad_num, &grad_m);
    grad_par[INDEX_AMP] += num / dpar[INDEX_AMP] * grad_num;
    grad_j = num / (2.0 * popovic_j) * grad_num;
    // dpar[INDEX_AMP] = sqrt(popovic_j + popovic_k); // as
    grad_k =
      dpar[INDEX_AMP] / (2.0 * (popovic_j + popovic_k)) * grad_par[INDEX_AMP];
    grad_j += grad_k;
    // popovic_j = sqrt(popovic_k*popovic_k - popovic_m*popovic_m);
    grad_k += popovic_k / popovic_j * grad_j;
    grad_m -= popovic_m / popovic_j * grad_j;
    // popovic_m = A*G - B*F;
    grad_A += G * grad_m;
    grad_G += A * grad_m;
    grad_B -= F * grad_m;
    grad_F -= B * grad_m;
    // popovic_k = (A*A + B*B + F*F + G*G)/2.0;
    grad_A += A * grad_k;
    grad_B += B * grad_k;
    grad_F += F * grad_k;
    grad_G += G * grad_k;
    // G = par[INDEX_BIGOMEGA];
    grad_par[INDEX_BIGOMEGA] = grad_G;
    // F = par[INDEX_INC];
    grad_par[INDEX_INC] = grad_F;
    // B = par[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] = grad_B;
    // A = par[INDEX_AMP];
    grad_par[INDEX_AMP] = grad_A;
    break;
  default:;
  }

  // mean-motion
  switch (ptype[INDEX_FREQ]) {
  case FREQ_P:
    // dpar[INDEX_FREQ] = M_2PI/par[INDEX_FREQ];
    grad_par[INDEX_FREQ] *= -dpar[INDEX_FREQ] / par[INDEX_FREQ];
    break;
  case FREQ_LOG10P:
    // dpar[INDEX_FREQ] = M_2PI*pow(10.0, -par[INDEX_FREQ]);
    grad_par[INDEX_FREQ] *= -log(10.0) * dpar[INDEX_FREQ];
    break;
  default:;
  }
}

void par2vpar_back(
  long *ptype, double *par, double *vpar, double *grad_vpar, double *grad_par)
{
  // Backward propagation of the gradient for par2vpar.

  double A, B, F, G, grad_A, grad_B, grad_F, grad_G, popovic_k, popovic_m,
    popovic_j;
  double grad_k, grad_m, grad_j, grad_num, grad_deno;
  double sini, grad_sini, grad_vpi, grad_thT, grad_Omega, cosom, sinom, tmp;
  double grad_Omo;

  memcpy(grad_par, grad_vpar, 5 * sizeof(double));
  grad_sini = 0.0;
  grad_vpi = 0.0;
  grad_Omega = 0.0;

  // Recompute sin(i) and Omega before propagating gradient
  // Compute sin(i)
  switch (ptype[INDEX_INC]) {
  case INC_I:
    sini = sin(par[INDEX_INC]);
    break;
  case INC_COSI:
    sini = sqrt(1.0 - par[INDEX_INC] * par[INDEX_INC]);
    break;
  default:
    sini = 1.0;
  }

  // Gradient propagation
  // K
  switch (ptype[INDEX_AMP]) {
  case AMP_LOG10K:
    // vpar[INDEX_AMP] = pow(10.0, par[INDEX_AMP]);
    grad_par[INDEX_AMP] *= log(10.0) * vpar[INDEX_AMP];
    break;
  case AMP_AS:
    // vpar[INDEX_AMP] = velocity_coef * par[INDEX_AMP] * sini *
    // vpar[INDEX_FREQ]/sqrt(1.0-vpar[INDEX_ECC]*vpar[INDEX_ECC]);
    grad_par[INDEX_FREQ] +=
      vpar[INDEX_AMP] / vpar[INDEX_FREQ] * grad_par[INDEX_AMP];
    grad_par[INDEX_ECC] += vpar[INDEX_AMP] * vpar[INDEX_ECC] /
      (1.0 - vpar[INDEX_ECC] * vpar[INDEX_ECC]) * grad_par[INDEX_AMP];
    grad_sini += vpar[INDEX_AMP] / sini * grad_par[INDEX_AMP];
    grad_par[INDEX_AMP] *= vpar[INDEX_AMP] / par[INDEX_AMP];
    break;
  case AMP_AS_SINI:
    // vpar[INDEX_AMP] = velocity_coef * par[INDEX_AMP] *
    // vpar[INDEX_FREQ]/sqrt(1.0-vpar[INDEX_ECC]*vpar[INDEX_ECC]);
    grad_par[INDEX_FREQ] +=
      vpar[INDEX_AMP] / vpar[INDEX_FREQ] * grad_par[INDEX_AMP];
    grad_par[INDEX_ECC] += vpar[INDEX_AMP] * vpar[INDEX_ECC] /
      (1.0 - vpar[INDEX_ECC] * vpar[INDEX_ECC]) * grad_par[INDEX_AMP];
    grad_par[INDEX_AMP] *= vpar[INDEX_AMP] / par[INDEX_AMP];
    break;
  default:;
  }

  // M0
  switch (ptype[INDEX_PHASE]) {
  case PHASE_MARG0:
    // vpar[INDEX_PHASE] = par[INDEX_PHASE]-vpar[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] -= grad_par[INDEX_PHASE];
    break;
  case PHASE_LA0:
    // vpar[INDEX_PHASE] = par[INDEX_PHASE]-vpi;
    grad_vpi -= grad_par[INDEX_PHASE];
    break;
  case PHASE_TP:
    // vpar[INDEX_PHASE] = -vpar[INDEX_FREQ]*par[INDEX_PHASE];
    grad_par[INDEX_FREQ] -= par[INDEX_PHASE] * grad_par[INDEX_PHASE];
    grad_par[INDEX_PHASE] *= -vpar[INDEX_FREQ];
    break;
  case PHASE_TC:
    // time2M0(par, vpar, M_PI_2-vpar[INDEX_OMEGA]);
    time2M0_back(par, vpar, M_PI_2 - vpar[INDEX_OMEGA], grad_par, &grad_thT);
    grad_par[INDEX_OMEGA] -= grad_thT;
    break;
  case PHASE_TVMIN:
    // time2M0(par, vpar, -vpar[INDEX_OMEGA]);
    time2M0_back(par, vpar, -vpar[INDEX_OMEGA], grad_par, &grad_thT);
    grad_par[INDEX_OMEGA] -= grad_thT;
    break;
  case PHASE_TVMAX:
    // time2M0(par, vpar, M_PI-vpar[INDEX_OMEGA]);
    time2M0_back(par, vpar, M_PI - vpar[INDEX_OMEGA], grad_par, &grad_thT);
    grad_par[INDEX_OMEGA] -= grad_thT;
    break;
  default:;
  }

  // e, omega, vpi
  if (ptype[INDEX_OMEGA] == OMEGA_VARPI) {
    // vpi = vpar[INDEX_OMEGA];
    // vpar[INDEX_OMEGA] = vpi - Omega;
    grad_Omega -= grad_par[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] += grad_vpi;
  } else {
    // vpi = vpar[INDEX_OMEGA] + Omega;
    grad_par[INDEX_OMEGA] += grad_vpi;
    grad_Omega += grad_vpi;
  }
  switch (ptype[INDEX_ECC]) {
  case ECC_K:
    // vpar[INDEX_ECC] =
    // sqrt(par[INDEX_ECC]*par[INDEX_ECC]+par[INDEX_OMEGA]*par[INDEX_OMEGA]);
    // vpar[INDEX_OMEGA] = atan2(par[INDEX_OMEGA], par[INDEX_ECC]);
    cosom = par[INDEX_ECC] / vpar[INDEX_ECC];
    sinom = par[INDEX_OMEGA] / vpar[INDEX_ECC];
    grad_par[INDEX_OMEGA] /= vpar[INDEX_ECC];
    tmp = cosom * grad_par[INDEX_ECC] - sinom * grad_par[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] =
      sinom * grad_par[INDEX_ECC] + cosom * grad_par[INDEX_OMEGA];
    grad_par[INDEX_ECC] = tmp;
    break;
  case ECC_SQK:
    // vpar[INDEX_ECC] =
    // par[INDEX_ECC]*par[INDEX_ECC]+par[INDEX_OMEGA]*par[INDEX_OMEGA];
    // vpar[INDEX_OMEGA] = atan2(par[INDEX_OMEGA], par[INDEX_ECC]);
    grad_par[INDEX_ECC] *= 2.0;
    grad_par[INDEX_OMEGA] /= vpar[INDEX_ECC];
    tmp = par[INDEX_ECC] * grad_par[INDEX_ECC] -
      par[INDEX_OMEGA] * grad_par[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] = par[INDEX_ECC] * grad_par[INDEX_OMEGA] +
      par[INDEX_OMEGA] * grad_par[INDEX_ECC];
    grad_par[INDEX_ECC] = tmp;
    break;
  default:;
  }

  // BIGOMEGA
  switch (ptype[INDEX_BIGOMEGA]) {
  case BIGOMEGA_BIGOMEGA:
    // Omega = par[INDEX_BIGOMEGA];
    grad_par[INDEX_BIGOMEGA] = grad_Omega;
    break;
  default:;
  }

  // sin(i) or ABFG (Popovic 1995)
  switch (ptype[INDEX_INC]) {
  case INC_I:
    // sini = sin(par[INDEX_INC]);
    grad_par[INDEX_INC] = cos(par[INDEX_INC]) * grad_sini;
    break;
  case INC_COSI:
    // sini = sqrt(1.0-par[INDEX_INC]*par[INDEX_INC]);
    grad_par[INDEX_INC] = -par[INDEX_INC] / sini * grad_sini;
    break;
  case INC_TIF: // Assume the parameters to be A, B, F, G.
    // Recompute useful quantities before propagating gradient
    A = par[INDEX_AMP];
    B = par[INDEX_OMEGA];
    F = par[INDEX_INC];
    G = par[INDEX_BIGOMEGA];
    popovic_k = (A * A + B * B + F * F + G * G) / 2.0;
    popovic_m = A * G - B * F;
    popovic_j = sqrt(popovic_k * popovic_k - popovic_m * popovic_m);
    // Gradient propagation
    // vpar[INDEX_OMEGA] = fmod(vpi - Omega, M_2PI);
    grad_vpi += grad_par[INDEX_OMEGA];
    grad_Omega -= grad_par[INDEX_OMEGA];
    // Omega = fmod((vpi + Omo)/2.0, M_PI);
    grad_vpi += grad_Omega / 2.0;
    grad_Omo = grad_Omega / 2.0;
    // Omo = atan2(B+F, A-G);
    atan2_back(B + F, A - G, grad_Omo, &grad_num, &grad_deno);
    grad_B = grad_num;
    grad_F = grad_num;
    grad_A = grad_deno;
    grad_G = -grad_deno;
    // vpi = atan2(B-F, A+G);
    atan2_back(B - F, A + G, grad_vpi, &grad_num, &grad_deno);
    grad_B += grad_num;
    grad_F -= grad_num;
    grad_A += grad_deno;
    grad_G += grad_deno;
    // vpar[INDEX_AMP] = velocity_coef * vpar[INDEX_FREQ] *
    // sqrt(2.0*popovic_j/(1.0-vpar[INDEX_ECC]*vpar[INDEX_ECC]));
    grad_par[INDEX_FREQ] +=
      vpar[INDEX_AMP] / vpar[INDEX_FREQ] * grad_par[INDEX_AMP];
    grad_j = vpar[INDEX_AMP] / (2.0 * popovic_j) * grad_par[INDEX_AMP];
    grad_par[INDEX_ECC] += vpar[INDEX_AMP] * vpar[INDEX_ECC] /
      (1.0 - vpar[INDEX_ECC] * vpar[INDEX_ECC]) * grad_par[INDEX_AMP];
    // popovic_j = sqrt(popovic_k*popovic_k - popovic_m*popovic_m);
    grad_k = popovic_k / popovic_j * grad_j;
    grad_m = -popovic_m / popovic_j * grad_j;
    // popovic_m = A*G - B*F;
    grad_A += G * grad_m;
    grad_G += A * grad_m;
    grad_B -= F * grad_m;
    grad_F -= B * grad_m;
    // popovic_k = (A*A + B*B + F*F + G*G)/2.0;
    grad_A += A * grad_k;
    grad_B += B * grad_k;
    grad_F += F * grad_k;
    grad_G += G * grad_k;
    // G = par[INDEX_BIGOMEGA];
    grad_par[INDEX_BIGOMEGA] = grad_G;
    // F = par[INDEX_INC];
    grad_par[INDEX_INC] = grad_F;
    // B = par[INDEX_OMEGA];
    grad_par[INDEX_OMEGA] = grad_B;
    // A = par[INDEX_AMP];
    grad_par[INDEX_AMP] = grad_A;
    break;
  default:;
  }

  // mean-motion
  switch (ptype[INDEX_FREQ]) {
  case FREQ_P:
    // vpar[INDEX_FREQ] = M_2PI/par[INDEX_FREQ];
    grad_par[INDEX_FREQ] *= -vpar[INDEX_FREQ] / par[INDEX_FREQ];
    break;
  case FREQ_LOG10P:
    // vpar[INDEX_FREQ] = M_2PI*pow(10.0, -par[INDEX_FREQ]);
    grad_par[INDEX_FREQ] *= -log(10.0) * vpar[INDEX_FREQ];
    break;
  default:;
  }
}

void dpar2apar_back(
  double *dpar, double *apar, double *grad_apar, double *grad_dpar)
{
  // Backward propagation of the gradient for dpar2apar.

  double cosi, coso, sino, cosO, sinO;
  double grad_cosi, grad_coso, grad_sino, grad_cosO, grad_sinO;

  // Recompute useful quantities
  cosi = cos(dpar[INDEX_INC]);
  coso = cos(dpar[INDEX_OMEGA]);
  sino = sin(dpar[INDEX_OMEGA]);
  cosO = cos(dpar[INDEX_BIGOMEGA]);
  sinO = sin(dpar[INDEX_BIGOMEGA]);

  // apar[INDEX_BIGOMEGA] = dpar[INDEX_AMP] * (-sino * sinO + coso * cosO *
  // cosi);
  grad_dpar[INDEX_AMP] =
    apar[INDEX_BIGOMEGA] / dpar[INDEX_AMP] * grad_apar[INDEX_BIGOMEGA];
  grad_sino = -dpar[INDEX_AMP] * sinO * grad_apar[INDEX_BIGOMEGA];
  grad_sinO = -dpar[INDEX_AMP] * sino * grad_apar[INDEX_BIGOMEGA];
  grad_coso = dpar[INDEX_AMP] * cosO * cosi * grad_apar[INDEX_BIGOMEGA];
  grad_cosO = dpar[INDEX_AMP] * coso * cosi * grad_apar[INDEX_BIGOMEGA];
  grad_cosi = dpar[INDEX_AMP] * coso * cosO * grad_apar[INDEX_BIGOMEGA];

  // apar[INDEX_INC] = dpar[INDEX_AMP] * (-sino * cosO - coso * sinO * cosi);
  grad_dpar[INDEX_AMP] +=
    apar[INDEX_INC] / dpar[INDEX_AMP] * grad_apar[INDEX_INC];
  grad_sino -= dpar[INDEX_AMP] * cosO * grad_apar[INDEX_INC];
  grad_cosO -= dpar[INDEX_AMP] * sino * grad_apar[INDEX_INC];
  grad_coso -= dpar[INDEX_AMP] * sinO * cosi * grad_apar[INDEX_INC];
  grad_sinO -= dpar[INDEX_AMP] * coso * cosi * grad_apar[INDEX_INC];
  grad_cosi -= dpar[INDEX_AMP] * coso * sinO * grad_apar[INDEX_INC];

  // apar[INDEX_OMEGA] = dpar[INDEX_AMP] * (coso * sinO + sino * cosO * cosi);
  grad_dpar[INDEX_AMP] +=
    apar[INDEX_OMEGA] / dpar[INDEX_AMP] * grad_apar[INDEX_OMEGA];
  grad_coso += dpar[INDEX_AMP] * sinO * grad_apar[INDEX_OMEGA];
  grad_sinO += dpar[INDEX_AMP] * coso * grad_apar[INDEX_OMEGA];
  grad_sino += dpar[INDEX_AMP] * cosO * cosi * grad_apar[INDEX_OMEGA];
  grad_cosO += dpar[INDEX_AMP] * sino * cosi * grad_apar[INDEX_OMEGA];
  grad_cosi += dpar[INDEX_AMP] * sino * cosO * grad_apar[INDEX_OMEGA];

  // apar[INDEX_AMP] = dpar[INDEX_AMP] * (coso * cosO - sino * sinO * cosi);
  grad_dpar[INDEX_AMP] +=
    apar[INDEX_AMP] / dpar[INDEX_AMP] * grad_apar[INDEX_AMP];
  grad_coso += dpar[INDEX_AMP] * cosO * grad_apar[INDEX_AMP];
  grad_cosO += dpar[INDEX_AMP] * coso * grad_apar[INDEX_AMP];
  grad_sino -= dpar[INDEX_AMP] * sinO * cosi * grad_apar[INDEX_AMP];
  grad_sinO -= dpar[INDEX_AMP] * sino * cosi * grad_apar[INDEX_AMP];
  grad_cosi -= dpar[INDEX_AMP] * sino * sinO * grad_apar[INDEX_AMP];

  // cosi = cos(dpar[INDEX_INC]);
  grad_dpar[INDEX_INC] = -sin(dpar[INDEX_INC]) * grad_cosi;
  // coso = cos(dpar[INDEX_OMEGA]);
  grad_dpar[INDEX_OMEGA] = -sino * grad_coso;
  // sino = sin(dpar[INDEX_OMEGA]);
  grad_dpar[INDEX_OMEGA] += coso * grad_sino;
  // cosO = cos(dpar[INDEX_BIGOMEGA]);
  grad_dpar[INDEX_BIGOMEGA] = -sinO * grad_cosO;
  // sinO = sin(dpar[INDEX_BIGOMEGA]);
  grad_dpar[INDEX_BIGOMEGA] += cosO * grad_sinO;

  // apar[INDEX_FREQ] = dpar[INDEX_FREQ];
  grad_dpar[INDEX_FREQ] = grad_apar[INDEX_FREQ];
  // apar[INDEX_PHASE] = dpar[INDEX_PHASE];
  grad_dpar[INDEX_PHASE] = grad_apar[INDEX_PHASE];
  // apar[INDEX_ECC] = dpar[INDEX_ECC];
  grad_dpar[INDEX_ECC] = grad_apar[INDEX_ECC];
}

void par2apar_back(
  long *ptype, double *par, double *apar, double *grad_apar, double *grad_par,
  double *dpar, double *grad_dpar)
{
  // Backward propagation of the gradient for par2apar.

  // if (ptype[INDEX_AMP] == AMP_TIA) {
  //   // Assume the parameters (except freq) to be e, M0, A, B, F, G.
  //   memcpy(grad_par, grad_apar, 7 * sizeof(double));
  //   // Compute mean-motion
  //   switch (ptype[INDEX_FREQ]) {
  //   case FREQ_P:
  //     // apar[INDEX_FREQ] = M_2PI/par[INDEX_FREQ];
  //     grad_par[INDEX_FREQ] *= -apar[INDEX_FREQ] / par[INDEX_FREQ];
  //     break;
  //   case FREQ_LOG10P:
  //     // apar[INDEX_FREQ] = M_2PI*pow(10.0, -par[INDEX_FREQ]);
  //     grad_par[INDEX_FREQ] *= -log(10.0) * apar[INDEX_FREQ];
  //     break;
  //   default:;
  //   }
  // } else {
  // dpar2apar(dpar, apar);
  dpar2apar_back(dpar, apar, grad_apar, grad_dpar);
  // par2dpar(ptype, par, dpar);
  par2dpar_back(ptype, par, dpar, grad_dpar, grad_par);
  // }
}
