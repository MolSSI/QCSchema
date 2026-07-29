.. _model-atomicproperties:

==========
Properties
==========

:``schema_name``: ``qcschema_atomic_properties``

``properties`` is where QCSchema does the thing it was invented for. Instead of
grepping a total energy out of an output file and hoping the format never
changes, a program publishes every intermediate it computed under a documented,
stable key.

.. code-block:: json

   {
     "properties": {
       "schema_name": "qcschema_atomic_properties",
       "calcinfo_nbasis": 24,
       "calcinfo_nmo": 24,
       "calcinfo_nalpha": 5,
       "calcinfo_nbeta": 5,
       "calcinfo_natom": 3,
       "nuclear_repulsion_energy": 8.80146205625184,
       "scf_one_electron_energy": -122.44534536383037,
       "scf_two_electron_energy": 37.62246494040059,
       "scf_total_energy": -76.02141836717794,
       "mp2_correlation_energy": -0.20694906092227,
       "mp2_total_energy": -76.22836742810021,
       "return_energy": -76.22836742810021
     }
   }

Every field is optional. A program reports what it has and omits the rest —
``properties`` is one of the few v2 models that strips ``null`` values on
serialization, so the ~50 possible keys never clutter a real payload.

.. contents:: Property groups
   :local:
   :depth: 1


Naming conventions
==================

Keys are ``snake_case`` and read ``<method>_<quantity>``:

``<method>``
   The theory level that produced the value: ``scf``, ``mp2``, ``ccsd``,
   ``ccsdt``, ``ccsdtq``, or ``ccsd_prt_pr``. The last one spells CCSD(T) —
   parentheses are awkward in keys, so ``(T)`` is written "paren-T-paren".

``<quantity>``
   ``total_energy``, ``correlation_energy``, ``dipole_moment``, ``iterations``,
   and so on.

Two prefixes are not method names:

``calcinfo_``
   Basic facts about the computation's size, needed to interpret every array in
   the record.

``return_``
   The primary answer, duplicated here from ``AtomicResult.return_result`` so
   that a consumer reading only ``properties`` still finds it.

.. note::

   ``nuclear_repulsion_energy`` carries no method prefix because it is a property
   of the geometry alone.


Calculation information
=======================

These are not results so much as the dimensions everything else is expressed in.
``calcinfo_natom`` in particular is required before any derivative can be
validated, since it fixes the shape.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``calcinfo_nbasis``
     - integer
     - \-
     - The number of basis functions for the computation.
   * - ``calcinfo_nmo``
     - integer
     - \-
     - The number of molecular orbitals for the computation.
   * - ``calcinfo_nalpha``
     - integer
     - \-
     - The number of alpha electrons in the computation.
   * - ``calcinfo_nbeta``
     - integer
     - \-
     - The number of beta electrons in the computation.
   * - ``calcinfo_natom``
     - integer
     - \-
     - The number of atoms in the computation.

``calcinfo_nmo`` is often smaller than ``calcinfo_nbasis`` — linear dependencies
get projected out, and frozen-core or frozen-virtual schemes reduce the active
space.


Canonical values
================

The requested answer, plus the geometry-only nuclear repulsion.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``nuclear_repulsion_energy``
     - number
     - \-
     - The nuclear repulsion energy.
   * - ``return_energy``
     - number
     - \-
     - The energy of the requested method, identical to ``return_result`` for ``driver`` = ``energy`` computations.
   * - ``return_gradient``
     - array[number]
     - units ``E_h/a0``
     - The gradient of the requested method, identical to ``return_result`` for ``driver`` = ``gradient`` computations.
   * - ``return_hessian``
     - array[number]
     - units ``E_h/a0^2``
     - The Hessian of the requested method, identical to ``return_result`` for ``driver`` = ``hessian`` computations.

``return_energy`` is always populated when an energy was computed, whatever the
driver — a gradient computation reports both ``return_gradient`` and
``return_energy``. ``return_energy`` is the energy of the *requested method*: for
an MP2 job it equals ``mp2_total_energy``, not ``scf_total_energy``.


Self-consistent field
=====================

Fields added at the SCF level. This covers both Hartree–Fock and Density
Functional Theory; the DFT-specific pieces (``scf_xc_energy``,
``scf_vv10_energy``, ``scf_dispersion_correction_energy``) are simply absent for
HF.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``scf_one_electron_energy``
     - number
     - units ``E_h``
     - The one-electron (core Hamiltonian) energy contribution to the total SCF energy.
   * - ``scf_two_electron_energy``
     - number
     - units ``E_h``
     - The two-electron energy contribution to the total SCF energy.
   * - ``scf_vv10_energy``
     - number
     - units ``E_h``
     - The VV10 functional energy contribution to the total SCF energy.
   * - ``scf_xc_energy``
     - number
     - units ``E_h``
     - The functional (XC) energy contribution to the total SCF energy.
   * - ``scf_dispersion_correction_energy``
     - number
     - units ``E_h``
     - The dispersion correction appended to an underlying functional when a DFT-D method is requested.
   * - ``scf_dipole_moment``
     - array[number]
     - units ``e a0``
     - The SCF X, Y, and Z dipole components
   * - ``scf_quadrupole_moment``
     - array[number]
     - units ``e a0^2``; shape ``(3, 3)``
     - The quadrupole components (redundant; 6 unique).
   * - ``scf_total_energy``
     - number
     - units ``E_h``
     - The total electronic energy of the SCF stage of the calculation.
   * - ``scf_total_gradient``
     - array[number]
     - units ``E_h/a0``
     - The total electronic gradient of the SCF stage of the calculation.
   * - ``scf_total_hessian``
     - array[number]
     - units ``E_h/a0^2``
     - The total electronic Hessian of the SCF stage of the calculation.
   * - ``scf_iterations``
     - integer
     - \-
     - The number of SCF iterations taken before convergence.

Note that ``scf_total_energy`` is not generally the sum of the one- and
two-electron energies: the nuclear repulsion, exchange–correlation, and any
dispersion correction all contribute. And for a DFT-D calculation,
``scf_dispersion_correction_energy`` is the piece appended to the underlying
functional, which is useful when you want the bare functional energy back.

``scf_quadrupole_moment`` is stored as a redundant :math:`3 \times 3` (nine
numbers, six unique).


Møller–Plesset
==============

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``mp2_same_spin_correlation_energy``
     - number
     - units ``E_h``
     - The portion of MP2 doubles correlation energy from same-spin (i.e. triplet) correlations, without any user scaling.
   * - ``mp2_opposite_spin_correlation_energy``
     - number
     - units ``E_h``
     - The portion of MP2 doubles correlation energy from opposite-spin (i.e. singlet) correlations, without any user scaling.
   * - ``mp2_singles_energy``
     - number
     - units ``E_h``
     - The singles portion of the MP2 correlation energy. Zero except in ROHF.
   * - ``mp2_doubles_energy``
     - number
     - units ``E_h``
     - The doubles portion of the MP2 correlation energy including same-spin and opposite-spin correlations.
   * - ``mp2_correlation_energy``
     - number
     - units ``E_h``
     - The MP2 correlation energy.
   * - ``mp2_total_energy``
     - number
     - units ``E_h``
     - The total MP2 energy (MP2 correlation energy + HF energy).
   * - ``mp2_dipole_moment``
     - array[number]
     - units ``e a0``; shape ``(3)``
     - The MP2 X, Y, and Z dipole components.

The spin decomposition is reported **without any user scaling** — these are the
raw same-spin and opposite-spin contributions, so a consumer can construct
SCS-MP2 or any other scaled variant itself. ``mp2_singles_energy`` is zero except
in ROHF-based references.

The relationships that hold:

.. math::

   E_{\text{corr}}^{\text{MP2}} &= E_{\text{singles}} + E_{\text{doubles}} \\
   E_{\text{doubles}} &= E_{\text{same-spin}} + E_{\text{opposite-spin}} \\
   E_{\text{total}}^{\text{MP2}} &= E_{\text{total}}^{\text{SCF}} + E_{\text{corr}}^{\text{MP2}}


Coupled cluster
===============

CCSD
----

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``ccsd_same_spin_correlation_energy``
     - number
     - units ``E_h``
     - The portion of CCSD doubles correlation energy from same-spin (i.e. triplet) correlations, without any user scaling.
   * - ``ccsd_opposite_spin_correlation_energy``
     - number
     - units ``E_h``
     - The portion of CCSD doubles correlation energy from opposite-spin (i.e. singlet) correlations, without any user scaling.
   * - ``ccsd_singles_energy``
     - number
     - units ``E_h``
     - The singles portion of the CCSD correlation energy. Zero except in ROHF.
   * - ``ccsd_doubles_energy``
     - number
     - units ``E_h``
     - The doubles portion of the CCSD correlation energy including same-spin and opposite-spin correlations.
   * - ``ccsd_correlation_energy``
     - number
     - units ``E_h``
     - The CCSD correlation energy.
   * - ``ccsd_total_energy``
     - number
     - units ``E_h``
     - The total CCSD energy (CCSD correlation energy + HF energy).
   * - ``ccsd_dipole_moment``
     - array[number]
     - units ``e a0``; shape ``(3)``
     - The CCSD X, Y, and Z dipole components.
   * - ``ccsd_iterations``
     - integer
     - \-
     - The number of CCSD iterations taken before convergence.

CCSD(T)
-------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``ccsd_prt_pr_correlation_energy``
     - number
     - units ``E_h``
     - The CCSD(T) correlation energy.
   * - ``ccsd_prt_pr_total_energy``
     - number
     - units ``E_h``
     - The total CCSD(T) energy (CCSD(T) correlation energy + HF energy).
   * - ``ccsd_prt_pr_dipole_moment``
     - array[number]
     - units ``e a0``; shape ``(3)``
     - The CCSD(T) X, Y, and Z dipole components.

CCSDT and CCSDTQ
----------------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``ccsdt_correlation_energy``
     - number
     - units ``E_h``
     - The CCSDT correlation energy.
   * - ``ccsdt_total_energy``
     - number
     - units ``E_h``
     - The total CCSDT energy (CCSDT correlation energy + HF energy).
   * - ``ccsdt_dipole_moment``
     - array[number]
     - units ``e a0``; shape ``(3)``
     - The CCSDT X, Y, and Z dipole components.
   * - ``ccsdt_iterations``
     - integer
     - \-
     - The number of CCSDT iterations taken before convergence.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``ccsdtq_correlation_energy``
     - number
     - units ``E_h``
     - The CCSDTQ correlation energy.
   * - ``ccsdtq_total_energy``
     - number
     - units ``E_h``
     - The total CCSDTQ energy (CCSDTQ correlation energy + HF energy).
   * - ``ccsdtq_dipole_moment``
     - array[number]
     - units ``e a0``; shape ``(3)``
     - The CCSDTQ X, Y, and Z dipole components.
   * - ``ccsdtq_iterations``
     - integer
     - \-
     - The number of CCSDTQ iterations taken before convergence.

.. important::

   ``ccsdt_`` (full triples) and ``ccsd_prt_pr_`` (perturbative triples) are
   different methods with confusingly similar keys. CCSD(T) is the far more
   commonly computed of the two.


Prior art for property names
============================

The names above did not appear from nowhere, and QCSchema is not the only project
to have catalogued quantum chemistry output variables. When proposing a new
property name, these are worth consulting first:

- `PsiVariables <https://psicode.org/psi4manual/master/glossary_psivariables.html>`_
  — Psi4's variable glossary, which QCSchema's naming most closely tracks
- `cclib data notes <https://cclib.github.io/data_notes.html>`_ — parsed
  quantities across many programs
- `IUPAC recommendations for computational chemistry
  <https://doi.org/10.1515/pac-2012-1204>`_ and the
  `IUPAC Goldbook <https://goldbook.iupac.org>`_ — for terminology and units

See :doc:`../development_guide/index` if you want to add one.


Properties for other procedures
===============================

Optimizations and torsion drives have their own, much smaller properties models
holding summary values for the whole procedure:

- :ref:`OptimizationProperties <model-optimizationproperties>` —
  ``qcschema_optimization_properties``
- :ref:`TorsionDriveProperties <model-torsiondriveproperties>` —
  ``qcschema_torsion_drive_properties``

Both are new in v2. Previously you had to derive these numbers by digging into
the last element of a trajectory.
