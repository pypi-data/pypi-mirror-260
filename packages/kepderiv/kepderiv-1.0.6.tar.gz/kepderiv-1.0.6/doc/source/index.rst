
kepderiv documentation
======================

The kepderiv package allows to model Keplerian orbits in the context
of radial velocities and astrometry, using a flexible set of Keplerian parameters.
It additionnally provides gradient back-propagation methods.

Installation
------------

Using conda
~~~~~~~~~~~

The kepderiv package can be installed using conda with the following command:

``conda install -c conda-forge kepderiv``

Using pip
~~~~~~~~~

It can also be installed using pip with:

``pip install kepderiv``

Usage
-----

The kepderiv package defines the :doc:`_autosummary/kepderiv.Keplerian`
class, which can handle a flexible set of Keplerian parameters
and model the corresponding radial velocity and astrometric time series.

API Reference
-------------

.. autosummary::
   :toctree: _autosummary
   :template: autosummary/class.rst
   :nosignatures:

   kepderiv.Keplerian
