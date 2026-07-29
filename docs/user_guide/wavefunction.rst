.. _model-wavefunctionproperties:

============
Wavefunction
============

:``schema_name``: ``qcschema_wavefunction_properties``

The wavefunction block carries the matrices themselves — orbitals, densities,
Fock and core-Hamiltonian matrices, eigenvalues, occupations. This is what makes
it possible to transfer a wavefunction between programs, or to hand orbitals to a
visualizer, without either side parsing a binary checkpoint format.

It is also, by a wide margin, the largest thing in a QCSchema record, which is why
it is **absent by default**. You get it only by asking:

.. code-block:: json

   {
     "schema_name": "qcschema_atomic_specification",
     "driver": "energy",
     "model": {"method": "HF", "basis": "cc-pVDZ"},
     "protocols": {"wavefunction": "all"}
   }

.. contents:: On this page
   :local:
   :depth: 1


Conventions
===========

.. important::

   Three rules govern every matrix in this block:

   1. **Matrices are stored in column-major order.**
   2. **Arrays are stored flat** and reshaped by the consumer using the
      documented shape, in terms of ``nao`` (:math:`=`
      ``calcinfo_nbasis``) and ``nmo`` (:math:`=` ``calcinfo_nmo``).
   3. **AO basis functions are ordered** according to the CCA standard as
      implemented in
      `libint <https://github.com/evaleev/libint/wiki/using-modern-CPlusPlus-API#solid-harmonic-gaussians-ordering-and-normalization>`_.

Rule 3 is the one that silently corrupts results if ignored. Two programs can
agree on every number in an orbital matrix and still disagree about which basis
function each row refers to.


Restricted and unrestricted
===========================

Every quantity comes in an ``_a`` (alpha-spin) and ``_b`` (beta-spin) pair, and
``restricted`` says whether the two are the same.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_wavefunction_properties"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``basis``
     - :ref:`BasisSet <model-basisset>`
     - **required**
     - The complete basis set the matrix quantities in this object are expressed in.
   * - ``restricted``
     - boolean
     - **required**
     - Whether the computation was restricted (alpha == beta). If ``true``, all beta quantities are omitted rather than duplicated.

When ``restricted`` is ``true``, **all beta quantities are omitted** rather than
duplicated. A consumer of a restricted wavefunction must read ``_a`` and
understand it to apply to both spins. A producer must not emit ``_b`` quantities
alongside ``restricted: true``.

``basis`` is a full :ref:`BasisSet <model-basisset>` object, not a name — the
matrices are meaningless without knowing exactly which functions index them, so
the complete basis travels with them.


Core Hamiltonian
================

One-electron and effective one-electron Hamiltonians in the AO basis.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``h_core_a``
     - array[number]
     - shape ``(nao, nao)``
     - Alpha-spin core (one-electron) Hamiltonian in the AO basis.
   * - ``h_core_b``
     - array[number]
     - shape ``(nao, nao)``
     - Beta-spin core (one-electron) Hamiltonian in the AO basis.
   * - ``h_effective_a``
     - array[number]
     - shape ``(nao, nao)``
     - Alpha-spin effective core (one-electron) Hamiltonian in the AO basis.
   * - ``h_effective_b``
     - array[number]
     - shape ``(nao, nao)``
     - Beta-spin effective core (one-electron) Hamiltonian in the AO basis

``h_effective_*`` covers cases where the effective one-electron operator differs
from the bare core Hamiltonian — ECPs, embedding potentials, and similar.


SCF quantities
==============

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``scf_orbitals_a``
     - array[number]
     - shape ``(nao, nmo)``
     - SCF alpha-spin orbitals in the AO basis.
   * - ``scf_orbitals_b``
     - array[number]
     - shape ``(nao, nmo)``
     - SCF beta-spin orbitals in the AO basis.
   * - ``scf_density_a``
     - array[number]
     - shape ``(nao, nao)``
     - SCF alpha-spin density matrix in the AO basis.
   * - ``scf_density_b``
     - array[number]
     - shape ``(nao, nao)``
     - SCF beta-spin density matrix in the AO basis.
   * - ``scf_fock_a``
     - array[number]
     - shape ``(nao, nao)``
     - SCF alpha-spin Fock matrix in the AO basis.
   * - ``scf_fock_b``
     - array[number]
     - shape ``(nao, nao)``
     - SCF beta-spin Fock matrix in the AO basis.
   * - ``scf_eigenvalues_a``
     - array[number]
     - shape ``(nmo)``
     - SCF alpha-spin orbital eigenvalues.
   * - ``scf_eigenvalues_b``
     - array[number]
     - shape ``(nmo)``
     - SCF beta-spin orbital eigenvalues.
   * - ``scf_occupations_a``
     - array[number]
     - shape ``(nmo)``
     - SCF alpha-spin orbital occupations.
   * - ``scf_occupations_b``
     - array[number]
     - shape ``(nmo)``
     - SCF beta-spin orbital occupations.
   * - ``scf_coulomb_a``
     - array[number]
     - shape ``(nao, nao)``
     - SCF alpha-spin Coulomb matrix in the AO basis.
   * - ``scf_coulomb_b``
     - array[number]
     - shape ``(nao, nao)``
     - SCF beta-spin Coulomb matrix in the AO basis.
   * - ``scf_exchange_a``
     - array[number]
     - shape ``(nao, nao)``
     - SCF alpha-spin exchange matrix in the AO basis.
   * - ``scf_exchange_b``
     - array[number]
     - shape ``(nao, nao)``
     - SCF beta-spin exchange matrix in the AO basis.

The orbital matrices are ``(nao, nmo)``: rows are AO basis functions, columns are
molecular orbitals. Density, Fock, Coulomb, and exchange matrices are
``(nao, nao)``; eigenvalues and occupations are length ``nmo``.


Localized orbitals
==================

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``localized_orbitals_a``
     - array[number]
     - shape ``(nao, nmo)``
     - Localized alpha-spin orbitals in the AO basis. All nmo orbitals are included, even if only a subset were localized.
   * - ``localized_orbitals_b``
     - array[number]
     - shape ``(nao, nmo)``
     - Localized beta-spin orbitals in the AO basis. All nmo orbitals are included, even if only a subset were localized.
   * - ``localized_fock_a``
     - array[number]
     - shape ``(nmo, nmo)``
     - Alpha-spin Fock matrix in the localized molecular orbital basis. All nmo orbitals are included, even if only a subset were localized.
   * - ``localized_fock_b``
     - array[number]
     - shape ``(nmo, nmo)``
     - Beta-spin Fock matrix in the localized molecular orbital basis. All nmo orbitals are included, even if only a subset were localized.

Note the sizing rule: **full MO matrices are stored even if only a subset of
orbitals were localized.** A localization of the occupied space still reports all
``nmo`` columns, with the untouched orbitals carried through unchanged. This keeps
indices comparable with ``scf_orbitals_*``.


The primary-return indirection
==============================

The last ten fields are the subtle part of this object. They do not contain
matrices — they contain the **names of the fields that do**.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``orbitals_a``
     - string
     - \-
     - Index to the alpha-spin orbitals of the primary return.
   * - ``orbitals_b``
     - string
     - \-
     - Index to the beta-spin orbitals of the primary return.
   * - ``density_a``
     - string
     - \-
     - Index to the alpha-spin density of the primary return.
   * - ``density_b``
     - string
     - \-
     - Index to the beta-spin density of the primary return.
   * - ``fock_a``
     - string
     - \-
     - Index to the alpha-spin Fock matrix of the primary return.
   * - ``fock_b``
     - string
     - \-
     - Index to the beta-spin Fock matrix of the primary return.
   * - ``eigenvalues_a``
     - string
     - \-
     - Index to the alpha-spin orbital eigenvalues of the primary return.
   * - ``eigenvalues_b``
     - string
     - \-
     - Index to the beta-spin orbital eigenvalues of the primary return.
   * - ``occupations_a``
     - string
     - \-
     - Index to the alpha-spin orbital occupations of the primary return.
   * - ``occupations_b``
     - string
     - \-
     - Index to the beta-spin orbital occupations of the primary return.

So a Hartree–Fock computation reports:

.. code-block:: json

   {
     "restricted": true,
     "scf_orbitals_a": ["... nao * nmo numbers ..."],
     "scf_eigenvalues_a": ["... nmo numbers ..."],
     "orbitals_a": "scf_orbitals_a",
     "eigenvalues_a": "scf_eigenvalues_a"
   }

Why the extra hop? Because "the orbitals of this calculation" is
method-dependent. For DFT they are the SCF orbitals; for a correlated method they
might be Brueckner or natural orbitals stored under a different key. The
indirection lets a consumer ask for *the result* without knowing the method:

.. code-block:: text

   wavefunction.orbitals_a          ->  "scf_orbitals_a"      (a field name)
   wavefunction.scf_orbitals_a      ->  [ ... the numbers ... ]

   so: wavefunction[ wavefunction.orbitals_a ]  is the orbital matrix

A pointer must resolve. Setting ``orbitals_a`` to ``"scf_orbitals_a"`` when
``scf_orbitals_a`` is absent is invalid — the specification does not permit
dangling references here, and a validating consumer should reject them.


Choosing how much to keep
=========================

The ``wavefunction`` protocol takes five values, in decreasing order of size:

.. list-table::
   :widths: 32 68
   :header-rows: 1

   * - Value
     - Keeps
   * - ``all``
     - Everything the program produced.
   * - ``return_results``
     - Only the quantities the primary-return pointers name, plus the pointers
       and the basis.
   * - ``orbitals_and_eigenvalues``
     - Orbitals and eigenvalues (both spins if unrestricted).
   * - ``occupations_and_eigenvalues``
     - Occupations and eigenvalues.
   * - ``none`` *(default)*
     - Nothing; the ``wavefunction`` field is ``null``.

``return_results`` is usually what you want: it is the smallest option that is
still self-describing, since the pointers tell a consumer what it received.

.. seealso:: :doc:`../implementation_guide/protocols`
