========================
Specification components
========================

A brief overview of the fields present in QCSchema v1. A significant amount of
customization can be added to each field; see :doc:`examples` for complete
payloads.


Input components
================

Molecule
--------

The closest representation to the real physical nature of the system. In practical
terms, for molecular sciences, this is the coordinates (in some form) and the
elements at those coordinates. For both QM and MM, this is your molecule. It may
include bonding information, unit cell and lattice parameters, and more.

This is the foundation upon which you build the model basis of your calculation.

.. code-block:: json

   {
     "molecule": {
       "schema_name": "qcschema_molecule",
       "schema_version": 2,
       "symbols": ["O", "H", "H"],
       "geometry": [
          0.0,  0.0000, -0.1294,
          0.0, -1.4941,  1.0274,
          0.0,  1.4941,  1.0274
       ]
     }
   }

Only ``symbols`` and ``geometry`` are required. ``geometry`` is in Bohr and stored
flat, :math:`3 N_{\text{atom}}` values in :math:`x, y, z` order per atom, in the
same order as ``symbols``.

Commonly used optional fields: ``molecular_charge`` (default ``0``),
``molecular_multiplicity`` (default ``1``), ``masses``, ``real`` for
ghost/virtual atoms, ``atomic_numbers``, ``mass_numbers``, ``atom_labels``,
``connectivity``, ``fragments`` with ``fragment_charges`` and
``fragment_multiplicities``, ``fix_com``, ``fix_orientation``, ``fix_symmetry``,
``name``, and ``comment``.

.. note::

   In v1 the molecule's ``schema_version`` is ``2``, not ``1``. The molecule schema
   was versioned before the family was, and its numbering has run one ahead ever
   since.

Driver
------

What you are looking to calculate: energy, gradient, Hessian, or properties.

.. code-block:: json

   {"driver": "energy"}

The driver determines the type of ``return_result`` in the output.

Model
-----

The overall mathematical model used for the calculation. Another way to think about
this is the largest superset that still obtains roughly the same result. In QM this
is the Hamiltonian (HF, DFT, …) combined with the overall basis of the calculation
— HF/STO-3G, or B3LYP/6-311G**. Custom basis sets can be handled with custom
keywords, or by supplying a ``qcschema_basis`` object in place of the name.

.. code-block:: json

   {
     "model": {
       "method": "B3LYP",
       "basis": "cc-pVDZ"
     }
   }

Keywords
--------

Various tunable parameters for the calculation. These vary widely depending on the
basis and model chemistry, and represent the keywords of individual programs. They
are not standardized or validated by the schema.

.. code-block:: json

   {
     "keywords": {
       "scf_type": "df",
       "e_convergence": 1e-7
     }
   }


Output components
=================

Input components
----------------

The input components are duplicated in the output, so that the result is a complete
trace of the requested computation from input specification to results.

Success
-------

A description of whether the computation succeeded. For unsuccessful computations,
standard errors are placed in the output — convergence failures, IO errors, and so
on.

.. code-block:: json

   {"success": true}

An unsuccessful computation:

.. code-block:: json

   {
     "success": false,
     "error": {
       "error_type": "convergence_error",
       "error_message": "SCF failed to converge after 50 iterations"
     }
   }

``error_type`` is a short classifier. Values seen in practice include
``input_error``, ``convergence_error``, ``memory_error``, ``file_error``,
``random_error``, and ``unknown_error``.

.. note::

   This is one of the larger differences from v2, where a result object always
   describes a success and failures are a separate ``qcschema_failed_operation``
   object. A v1 consumer must check ``success`` before trusting any other field,
   since a failed output may be only partially populated.

Returned result
---------------

The "primary" return of a given computation. For energy, gradient, and Hessian
quantities these are either single numbers or an array representing the derivative
quantity.

.. code-block:: json

   {"return_result": -76.4187620271478}

Arrays are stored flat: a gradient is :math:`3 N_{\text{atom}}` numbers reshapable
to ``(nat, 3)``, and a Hessian is :math:`(3 N_{\text{atom}})^2` numbers reshapable
to ``(3*nat, 3*nat)``.

Provenance
----------

A brief description of the program, version, and routine used to generate the
output. It can include more detailed information such as computation time,
processor information, and host location.

.. code-block:: json

   {
     "provenance": {
       "creator": "QM Program",
       "version": "1.1",
       "routine": "module.json.run_json"
     }
   }

Properties
----------

A set of intermediate values produced by the QM program, such as the one-electron
and two-electron energies in SCF. This also includes values such as the number of
atomic orbitals and the number of alpha and beta electrons.

.. code-block:: json

   {
     "properties": {
       "calcinfo_nbasis": 24,
       "calcinfo_nmo": 24,
       "calcinfo_nalpha": 5,
       "calcinfo_nbeta": 5,
       "nuclear_repulsion_energy": 8.80146205625184,
       "scf_one_electron_energy": -122.44534536383044,
       "scf_two_electron_energy": 37.622464940400654,
       "scf_total_energy": -76.02141836717794
     }
   }

Keys follow a ``<method>_<quantity>`` pattern with ``calcinfo_`` for computation
size and ``return_`` for the primary answer. Every field is optional, and absence
means "not computed" rather than zero.

Known variable lists that informed these names:

- `PsiVariables <https://psicode.org/psi4manual/master/glossary_psivariables.html>`_
- `cclib data notes <https://cclib.github.io/data_notes.html>`_
- `IUPAC Goldbook <https://goldbook.iupac.org>`_, and the
  `IUPAC recommendations for computational chemistry
  <https://doi.org/10.1515/pac-2012-1204>`_

Basis quantities
----------------

The schema supports the export of basis quantities such as the overlap matrix or
the orbitals, through a ``wavefunction`` block, with the basis itself described by
a ``qcschema_basis`` object. Matrices are stored in column-major order, and AO
basis functions are ordered according to the CCA standard as implemented in
`libint <https://github.com/evaleev/libint/wiki/using-modern-CPlusPlus-API#solid-harmonic-gaussians-ordering-and-normalization>`_.
