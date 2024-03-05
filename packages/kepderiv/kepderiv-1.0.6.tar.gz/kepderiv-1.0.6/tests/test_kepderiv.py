import numpy as np

from kepderiv import Keplerian

nt = 253
delta = 1e-7
prec = 1e-10


def _max_err(x, y, relative=True, angle=[]):
  err = np.abs(x - y)
  if relative:
    err /= np.abs(x) + np.abs(y) + prec**2
  for k in angle:
    err[k] = abs((x[k] - y[k] + np.pi) % (2 * np.pi) - np.pi)
  print(err)
  return np.max(err)


def _generate_random_keplerian(seed=0):
  np.random.seed(seed)

  n = np.random.uniform(0.0, 100.0)
  M0 = np.random.uniform(0.0, 2.0 * np.pi)
  K = 10.0 ** np.random.uniform(-1.0, 4.0)
  e = np.random.uniform(0.0, 0.95)
  omega = np.random.uniform(0.0, 2.0 * np.pi)
  i = np.random.uniform(np.pi / 100, np.pi * 99 / 100)
  bigomega = np.random.uniform(0.0, np.pi)
  params = ['n', 'M0', 'K', 'e', 'omega', 'i', 'bigomega']
  values = np.array([n, M0, K, e, omega, i, bigomega])
  print(params)
  print(values)
  return Keplerian(values, param=params)


def _list_comb_5param():
  list_param = [
    ['n', 'P', 'log10P'],
    ['M0', 'MARG0', 'la0', 'TP', 'TC', 'TVMIN', 'TVMAX'],
    ['K', 'log10K', 'as', 'asini'],
    [('e', 'omega'), ('e', 'varpi'), ('ecosw', 'esinw'), ('sqecosw', 'sqesinw')],
  ]
  size_param = [len(par) for par in list_param]
  size_tot = np.prod(size_param)
  list_comb = []
  for k in range(size_tot):
    r = k
    param = []
    for d in range(4):
      kd = r % size_param[d]
      r = r // size_param[d]
      if isinstance(list_param[d][kd], tuple):
        param += list_param[d][kd]
      else:
        param.append(list_param[d][kd])
    np.random.shuffle(param)
    list_comb.append(param)
  return list_comb


def _list_comb_7param():
  l5 = _list_comb_5param()
  l7 = [l + ['i', 'BigOmega'] for l in l5] + [l + ['cosi', 'BigOmega'] for l in l5]
  l7 += [
    [freq, 'e', phase, 'TIA', 'TIB', 'TIF', 'TIG']
    for freq in ['n', 'P', 'log10P']
    for phase in ['M0', 'MARG0', 'la0', 'TP', 'TC', 'TVMIN', 'TVMAX']
  ]
  for param in l7:
    np.random.shuffle(param)
  return l7


def _list_comb_param():
  l5 = _list_comb_5param()
  l7 = _list_comb_7param()
  return l5 + l7


def test_set_param():
  kep = _generate_random_keplerian()
  par = kep.get_value()
  param0 = kep.get_param()
  for param in _list_comb_7param():
    kep.set_param(param)
    kepb = Keplerian(kep.get_value(), param)
    kepb.set_param(param0)
    err = _max_err(par, kepb.get_value(), False, [1, 4, 5, 6])
    print(par, kepb.get_value(), err)
    assert err < prec, 'change param not working ({}).'.format(param)


def _test_rv_back_param(param, seed=0):
  kep = _generate_random_keplerian(seed)
  kep.set_param(param)
  x = kep.get_value()
  t = np.cumsum(10 ** np.random.uniform(-2, 2, nt))
  rv = kep.rv(t)

  grad_rv = np.random.normal(0.0, delta, nt)
  grad_param = kep.rv_back(grad_rv)
  grad_param_num = []
  for dx in [-delta, -delta / 10, delta / 10, delta]:
    grad_param_num_dx = []
    for k in range(len(param)):
      x[k] += dx
      kep.set_value(x)
      drv = kep.rv(t) - rv
      grad_param_num_dx.append(drv @ grad_rv / dx)
      x[k] -= dx
    grad_param_num.append(grad_param_num_dx)
  grad_param_num = np.array(grad_param_num)
  print('grad_param', grad_param)
  print('grad_param_num', grad_param_num)

  err = _max_err(grad_param, np.median(grad_param_num, axis=0))
  num_err = np.max(
    [_max_err(grad_param_num[i], grad_param_num[j]) for i in range(4) for j in range(i)]
  )
  print(err, num_err)
  err = max(0.0, err - num_err)
  assert err < prec, (
    'rv_back ({}) not working' ' at required precision ({} > {})'
  ).format(param, err, prec)


def test_rv_back0():
  for k in range(100):
    _test_rv_back_param(['n', 'K', 'M0', 'e', 'omega'], k)


def test_rv_back():
  for param in _list_comb_param():
    _test_rv_back_param(param)


def _test_astro_back_param(param, seed=0):
  kep = _generate_random_keplerian(seed)
  kep.set_param(param)
  x = kep.get_value()
  t = np.cumsum(10 ** np.random.uniform(-2, 2, nt))
  astro_delta, astro_alpha = kep.astro(t)

  grad_delta = np.random.normal(0.0, delta, nt)
  grad_alpha = np.random.normal(0.0, delta, nt)
  grad_param = kep.astro_back(grad_delta, grad_alpha)

  grad_param_num = []
  for dx in [-delta, -delta / 10, delta / 10, delta]:
    grad_param_num_dx = []
    for k in range(len(param)):
      x[k] += dx
      kep.set_value(x)
      deltab, alphab = kep.astro(t)
      ddelta = deltab - astro_delta
      dalpha = alphab - astro_alpha
      grad_param_num_dx.append((ddelta @ grad_delta + dalpha @ grad_alpha) / dx)
      x[k] -= dx
    grad_param_num.append(grad_param_num_dx)
  grad_param_num = np.array(grad_param_num)
  print('grad_param', grad_param)
  print('grad_param_num', grad_param_num)

  err = _max_err(grad_param, np.median(grad_param_num, axis=0))
  num_err = np.max(
    [_max_err(grad_param_num[i], grad_param_num[j]) for i in range(4) for j in range(i)]
  )
  print(err, num_err)
  err = max(0.0, err - num_err)
  assert err < prec, (
    'astro_back ({}) not working' ' at required precision ({} > {})'
  ).format(param, err, prec)


def test_astro_back0():
  for k in range(100):
    _test_astro_back_param(['n', 'TIA', 'M0', 'e', 'TIB', 'TIF', 'TIG'], k)


def test_astro_back():
  for param in _list_comb_param():
    _test_astro_back_param(param)
