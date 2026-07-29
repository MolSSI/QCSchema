=====================
Your first input
=====================

This page builds one single-point energy input from nothing, then reads the
resulting JSON field by field. If you understand this object you understand
most of QCSchema.

JSON is the specification; the Python tabs show the same structure as models, per
:ref:`tab_convention`.


Step 1: describe the molecule
=============================

A :doc:`Molecule <../user_guide/molecule>` is the physical system: which atoms,
and where they are. Only two fields are required — ``symbols`` and ``geometry``.

.. tab-set::

   .. tab-item:: JSON

      .. code-block:: json

         {
           "schema_name": "qcschema_molecule",
           "schema_version": 3,
           "symbols": ["O", "H", "H"],
           "geometry": [
              0.0,  0.0000, -0.1294,
              0.0, -1.4941,  1.0274,
              0.0,  1.4941,  1.0274
           ]
         }

   .. tab-item:: Python

      .. code-block:: python

         Molecule(
             symbols=["O", "H", "H"],
             geometry=[
                  0.0,  0.0000, -0.1294,
                  0.0, -1.4941,  1.0274,
                  0.0,  1.4941,  1.0274,
             ],
         )

.. important::

   ``geometry`` is in **Bohr** (:math:`a_0`), not Ångström, and is stored flat:
   :math:`3 N_{\text{atom}}` numbers in :math:`x_1, y_1, z_1, x_2, \ldots` order.
   This trips up nearly everyone once. See
   :doc:`../implementation_guide/conventions`.

   Converting from whatever units your structures are stored in is your job, not
   the schema's — take the factor from a CODATA-derived source rather than a
   literal in your source file.


Step 2: describe the computation
================================

An :ref:`AtomicSpecification <model-atomicspecification>` is *how* to compute —
and deliberately says nothing about *what* it is computed on. Splitting it out
this way means one specification can be reused across many molecules.

.. tab-set::

   .. tab-item:: JSON

      .. code-block:: json

         {
           "schema_name": "qcschema_atomic_specification",
           "program": "psi4",
           "driver": "energy",
           "model": {"method": "MP2", "basis": "cc-pVDZ"},
           "keywords": {"scf_type": "df"}
         }

   .. tab-item:: Python

      .. code-block:: python

         AtomicSpecification(
             program="psi4",
             driver="energy",
             model={"method": "MP2", "basis": "cc-pVDZ"},
             keywords={"scf_type": "df"},
         )

The four pieces:

``driver``
   What you want back: ``energy``, ``gradient``, ``hessian``, or ``properties``.

``model``
   The physics: a ``method`` (functional, correlation treatment, or force field
   name) and a ``basis``. Together these define the mathematical model — the
   largest superset that still gives roughly the same answer.

``keywords``
   Everything program-specific. QCSchema deliberately does **not** standardize
   these; ``scf_type`` means whatever Psi4 says it means.

``program``
   Which code the specification is aimed at. Informational — useful when a
   specification is stored or passed around separately from a runner.


Step 3: put them together
=========================

.. tab-set::

   .. tab-item:: JSON

      .. code-block:: json

         {
           "schema_name": "qcschema_atomic_input",
           "schema_version": 2,
           "molecule": {"schema_name": "qcschema_molecule", "...": "..."},
           "specification": {"schema_name": "qcschema_atomic_specification",
                             "...": "..."}
         }

   .. tab-item:: Python

      .. code-block:: python

         AtomicInput(molecule=water, specification=spec)


Step 4: read the complete input
===============================

Written out in full, including the defaults a producer fills in, that input is:

.. code-block:: json

   {
     "id": null,
     "schema_name": "qcschema_atomic_input",
     "schema_version": 2,
     "molecule": {
       "schema_name": "qcschema_molecule",
       "schema_version": 3,
       "validated": true,
       "symbols": ["O", "H", "H"],
       "geometry": [0.0, 0.0, -0.1294, 0.0, -1.4941, 1.0274, 0.0, 1.4941, 1.0274],
       "name": "H2O",
       "molecular_charge": 0.0,
       "molecular_multiplicity": 1.0,
       "fix_com": false,
       "fix_orientation": false,
       "provenance": {
         "creator": "MyDriver",
         "version": "1.0",
         "routine": "mydriver.build_molecule"
       },
       "extras": {}
     },
     "specification": {
       "schema_name": "qcschema_atomic_specification",
       "keywords": {"scf_type": "df"},
       "program": "psi4",
       "driver": "energy",
       "model": {"method": "MP2", "basis": "cc-pVDZ"},
       "protocols": {
         "schema_name": "qcschema_atomic_protocols",
         "wavefunction": "none",
         "stdout": true,
         "error_correction": {"default_policy": true, "policies": null},
         "native_files": "none"
       },
       "extras": {}
     },
     "provenance": {
       "creator": "MyDriver",
       "version": "1.0",
       "routine": "mydriver.build_input"
     }
   }

Several things are there that you did not write:

``schema_name`` / ``schema_version``
   Stamped on every object. This is how a consumer knows what it is holding and
   which rules apply. See :doc:`../implementation_guide/versioning`.

``name: "H2O"``, ``molecular_charge``, ``molecular_multiplicity``
   Defaults. A neutral singlet is assumed unless you say otherwise, and the
   molecular formula is derivable from ``symbols``.

``validated: true``
   A speed flag saying this molecule has already been checked for schema and
   physics compliance — no overlapping atoms, feasible multiplicity. Only a
   trusted producer should ever set it.

``protocols``
   Knobs controlling *how much output to keep*. Wavefunctions and scratch files
   can be enormous, so the defaults discard them. See
   :doc:`../implementation_guide/protocols`.

``provenance``
   Who built this object — a stand-in here for whatever produced it. Results add
   their own provenance on top, so an object that has passed through several
   programs carries a trail.

.. note::

   ``Molecule.schema_version`` is ``3``, not ``2``. The molecule's version
   numbering is intentionally one ahead of the overall "QCSchema vN" numbering for
   historical reasons — it is not a mistake, and not something to correct.


Step 5: what comes back
=======================

Send the input to a program that speaks QCSchema and you get an
:ref:`AtomicResult <model-atomicresult>`:

.. code-block:: json

   {
     "schema_name": "qcschema_atomic_result",
     "schema_version": 2,
     "input_data": "... the qcschema_atomic_input above ...",
     "molecule": "... the frame the results are in ...",
     "properties": {
       "schema_name": "qcschema_atomic_properties",
       "calcinfo_natom": 3,
       "return_energy": -76.22836742810021,
       "scf_total_energy": -76.02141836717794,
       "mp2_correlation_energy": -0.20694906092227
     },
     "return_result": -76.22836742810021,
     "success": true,
     "provenance": {"creator": "Psi4", "version": "1.9",
                    "routine": "psi4.schema_runner"}
   }

Note that the result *contains* the input, as ``input_data``, rather than merging
its fields in. That means a result is always a complete, self-contained record of a
computation: reading the method back out is
``input_data.specification.model.method``. See :doc:`../user_guide/atomic`.

Continue to :doc:`examples` for complete results.
