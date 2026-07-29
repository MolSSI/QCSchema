.. _model-basisset:

=========
Basis set
=========

:``schema_name``: ``qcschema_basis_set``
:``schema_version``: 2

Most of the time a basis set is just a name — ``"basis": "cc-pVDZ"`` — and the
program looks it up. The ``qcschema_basis_set`` object exists for when that is not
enough: custom bases, decontracted or modified standard bases, and reporting
exactly what a program actually used.

It is also mandatory inside a :ref:`wavefunction <model-wavefunctionproperties>`
block, because orbital and density matrices are indexed by basis function and are
meaningless without the full function list.

.. code-block:: json

   {
     "model": {
       "method": "HF",
       "basis": {
         "schema_name": "qcschema_basis_set",
         "schema_version": 2,
         "name": "custom-sto-3g",
         "center_data": {"H_basis": {"electron_shells": ["..."]}},
         "atom_map": ["H_basis", "H_basis"]
       }
     }
   }


Structure
=========

The object is deduplicated: shell data is defined once per *kind* of center in
``center_data``, and ``atom_map`` assigns a center definition to each atom of the
parent molecule.

.. code-block:: text

   BasisSet
   ├── center_data: {label -> BasisCenter}     the unique definitions
   │   └── BasisCenter
   │       ├── electron_shells: [ElectronShell, ...]
   │       └── ecp_potentials:  [ECPPotential, ...]
   └── atom_map: [label, label, ...]           one entry per atom, in atom order

A water molecule in a standard basis needs two definitions and three map entries:

.. code-block:: json

   {
     "center_data": {"O1": {"...": "..."}, "H1": {"...": "..."}},
     "atom_map": ["O1", "H1", "H1"]
   }

.. important::

   ``atom_map`` is indexed in the same order as ``Molecule.symbols``, and has one
   entry per atom — including ghost atoms. It is the link between the basis and
   the geometry, so the atom-ordering contract from :doc:`molecule` applies here
   too.


Fields
======

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_basis_set"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``schema_version``
     - ``2``
     - \-
     - The version of ``schema_name`` this conforms to. Fixed value.
   * - ``name``
     - string
     - **required**
     - The standard basis name if available (e.g., 'cc-pVDZ').
   * - ``description``
     - string
     - \-
     - Brief description of the basis set.
   * - ``center_data``
     - object
     - **required**
     - Shared basis data for all atoms/centers in the parent molecule
   * - ``atom_map``
     - array[string]
     - **required**
     - Mapping of all atoms/centers in the parent molecule to centers in ``center_data``.
   * - ``nbf``
     - integer
     - \-
     - The number of basis functions. Use for convenience or as checksum

``nbf`` is a convenience *and* a checksum. If you omit it the reference
implementation computes it; if you supply it and it disagrees with the shell data,
that is a validation error rather than a silently accepted inconsistency.

``atom_map`` entries must all be keys of ``center_data``; an unknown label is an
error.


.. _model-basiscenter:

BasisCenter
===========

Everything the basis places on one atom or center.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``electron_shells``
     - array[:ref:`ElectronShell <model-electronshell>`]
     - **required**
     - Electronic shells for this center.
   * - ``ecp_electrons``
     - integer
     - default ``0``
     - Number of electrons replaced by ECP, MCP, or other field potentials.
   * - ``ecp_potentials``
     - array[:ref:`ECPPotential <model-ecppotential>`]
     - \-
     - ECPs, MCPs, or other field potentials for this center.

``ecp_electrons`` is the number of electrons *replaced* by the potential, which a
consumer needs in order to get the electron count right. It defaults to ``0``,
meaning an all-electron center.


.. _model-electronshell:

ElectronShell
=============

One electronic shell: a set of primitive Gaussians and the contraction
coefficients combining them.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``angular_momentum``
     - array[integer]
     - **required**
     - Angular momentum for the shell as an array of integers.
   * - ``harmonic_type``
     - ``spherical``, ``cartesian``
     - **required**
     - The angular momentum representation of a shell.
   * - ``exponents``
     - array[number]
     - **required**
     - Exponents for the contracted shell.
   * - ``coefficients``
     - array[array[number]]
     - **required**
     - General contraction coefficients for the shell; individual list components will be the individual segment contraction coefficients.

The shapes are interlocking, and a validating consumer should check them:

- ``exponents`` has one entry per primitive.
- Each row of ``coefficients`` must be the same length as ``exponents``.
- ``coefficients`` has one row per contracted function produced by the shell.

Two shell kinds fall out of this:

**General contraction** — one angular momentum, several contractions sharing the
same primitives:

.. code-block:: json

   {
     "angular_momentum": [0],
     "harmonic_type": "spherical",
     "exponents": [130.70932, 23.808861, 6.4436083],
     "coefficients": [[0.15432897, 0.53532814, 0.44463454],
                      [0.09999999, 0.39951283, 0.70011547]]
   }

**Fused shell** — several angular momenta sharing primitives (an ``sp`` shell, as
in Pople bases). Here ``len(angular_momentum)`` must equal
``len(coefficients)``, one row per angular momentum:

.. code-block:: json

   {
     "angular_momentum": [0, 1],
     "harmonic_type": "cartesian",
     "exponents": [5.033151, 1.169596, 0.380389],
     "coefficients": [[-0.09996723, 0.39951283, 0.70011547],
                      [ 0.15591627, 0.60768372, 0.39195739]]
   }

``harmonic_type`` chooses between ``spherical`` (:math:`2L+1` functions per
angular momentum) and ``cartesian`` (:math:`(L+1)(L+2)/2`), which is what makes
``nbf`` computable from the shell data alone.

.. note::

   Exponents and coefficients may be given as **strings** as well as numbers,
   matching how the
   `Basis Set Exchange <https://www.basissetexchange.org>`_ stores them to avoid
   losing precision in float round-trips. Consumers should accept both spellings
   and parse them as numbers.


.. _model-ecppotential:

ECPPotential
============

An effective core potential on a center.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``ecp_type``
     - ``scalar``, ``spinorbit``
     - **required**
     - The type of the ECP potential.
   * - ``angular_momentum``
     - array[integer]
     - **required**
     - Angular momentum for the potential as an array of integers.
   * - ``r_exponents``
     - array[integer]
     - **required**
     - Exponents of the 'r' term.
   * - ``gaussian_exponents``
     - array[number]
     - **required**
     - Exponents of the 'gaussian' term.
   * - ``coefficients``
     - array[array[number]]
     - **required**
     - General contraction coefficients for the potential; individual list components will be the individual segment contraction coefficients.

``r_exponents``, ``gaussian_exponents``, and every row of ``coefficients`` must
all be the same length — one entry per term in the potential. ``ecp_type`` is
``scalar`` for the spin-averaged part and ``spinorbit`` for the spin–orbit part;
a center may carry both.

Remember to set ``BasisCenter.ecp_electrons`` alongside the potential.


Getting basis data
==================

You rarely construct these by hand. Two sources produce them for you:

- The `Basis Set Exchange <https://www.basissetexchange.org>`_ can emit basis data
  in QCSchema form directly, for any basis and element set it knows.
- A program that supports the ``wavefunction`` protocol reports the basis it
  actually used at ``wavefunction.basis`` in the result — which is the
  authoritative answer to "what did it really run", as opposed to what the input
  asked for.
