// Copyright 2019-2024 Jean-Baptiste Delisle
// Licensed under the EUPL-1.2 or later

#define _USE_MATH_DEFINES
#include <math.h>
#include <string.h>
#define M_2PI (2.0 * M_PI)

typedef enum {
  INDEX_FREQ,
  INDEX_PHASE,
  INDEX_AMP,
  INDEX_ECC,
  INDEX_OMEGA,
  INDEX_INC,
  INDEX_BIGOMEGA,
  NINDEX
} Index;

typedef enum {
  NONE,
  // Freq
  FREQ_N, // Mean motion
  FREQ_P, // Period
  FREQ_LOG10P, // log10 of period
  // Phase
  PHASE_M0, // Mean anomaly at t=0
  PHASE_MARG0, // Mean argument at t=0
  PHASE_LA0, // Mean longitude at t=0
  PHASE_TP, // Time of periastron passage
  PHASE_TC, // Time of conjunction
  PHASE_TVMIN, // Time of rv min
  PHASE_TVMAX, // Time of rv max
  // Ecc
  ECC_E, // eccentricity
  ECC_K, // e cos(omega)
  ECC_SQK, // sqrt(e) cos(omega)
  // Amp
  AMP_K, // rv semiamplitude
  AMP_LOG10K, // log10 of semiamplitude
  AMP_AS, // Semi-major axis of star/CM
  AMP_AS_SINI,
  AMP_TIA, // Thiele-Innes A
  // Omega
  OMEGA_OMEGA, // argument of periastron
  OMEGA_VARPI, // longitude of periastron
  OMEGA_H, // e sin(omega)
  OMEGA_SQH, // sqrt(e) sin(omega)
  OMEGA_TIB, // Thiele-Innes B
  // INC
  INC_I, // inclination
  INC_COSI,
  INC_TIF, // Thiele-Innes F
  // BIGOMEGA
  BIGOMEGA_BIGOMEGA, // Longitude of ascending node
  BIGOMEGA_TIG // Thiele-Innes G
} ParType;

void M2E(double M, double e, double ftol, long maxiter, double *E);

void rv_vpar(long nt, double *t, double *vpar, double *rv, double *th);

void astro_apar(
  long nt, double *t, double *apar, double *delta, double *alpha, double *cosE,
  double *sinE);

void time2M0(double *par, double *dpar, double thT);

void M02time(double *dpar, double *par, double thT);

void par2dpar(long *ptype, double *par, double *dpar, double velocity_coef);

void dpar2par(double *dpar, long *ptype, double *par, double velocity_coef);

void par2vpar(long *ptype, double *par, double *vpar, double velocity_coef);

void dpar2apar(double *dpar, double *apar);

void par2apar(
  long *ptype, double *par, double *apar, double *dpar, double velocity_coef);

void rv_vpar_back(
  long nt, double *t, double *vpar, double *grad_rv, double *grad_vpar,
  double *th);

void astro_apar_back(
  long nt, double *t, double *apar, double *grad_delta, double *grad_alpha,
  double *grad_apar, double *cosE, double *sinE);

void time2M0_back(
  double *par, double *dpar, double thT, double *grad_par, double *grad_thT);

void M02time_back(
  double *dpar, double *par, double thT, double *grad_dpar, double *grad_thT);

void atan2_back(
  double y, double x, double grad_theta, double *grad_y, double *grad_x);

void par2dpar_back(
  long *ptype, double *par, double *dpar, double *grad_dpar, double *grad_par);

void par2vpar_back(
  long *ptype, double *par, double *vpar, double *grad_vpar, double *grad_par);

void dpar2apar_back(
  double *dpar, double *apar, double *grad_apar, double *grad_dpar);

void par2apar_back(
  long *ptype, double *par, double *apar, double *grad_apar, double *grad_par,
  double *dpar, double *grad_dpar);
