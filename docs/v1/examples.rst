========
Examples
========

Complete QCSchema v1 payloads. Because the input is duplicated in the output, the
corresponding *input* for each of these is the input fields alone — effectively
everything above the ``provenance`` field.

For clarity, all array-based values have been truncated to four decimal places.


Water MP2 energy
================

.. code-block:: json

   {
     "schema_name": "qcschema_output",
     "schema_version": 1,
     "molecule": {
       "schema_name": "qcschema_molecule",
       "schema_version": 2,
       "geometry": [
         0.0,  0.0,    -0.1294,
         0.0, -1.4941,  1.0274,
         0.0,  1.4941,  1.0274
       ],
       "symbols": ["O", "H", "H"]
     },
     "driver": "energy",
     "model": {
       "method": "MP2",
       "basis": "cc-pVDZ"
     },
     "keywords": {},
     "provenance": {
       "creator": "QM Program",
       "version": "1.1",
       "routine": "module.json.run_json"
     },
     "return_result": -76.22836742810021,
     "success": true,
     "properties": {
       "calcinfo_nbasis": 24,
       "calcinfo_nmo": 24,
       "calcinfo_nalpha": 5,
       "calcinfo_nbeta": 5,
       "calcinfo_natom": 3,
       "return_energy": -76.22836742810021,
       "scf_one_electron_energy": -122.4453,
       "scf_two_electron_energy": 37.6224,
       "nuclear_repulsion_energy": 8.8014,
       "scf_dipole_moment": [0.0, 0.0, 0.8244],
       "scf_iterations": 10,
       "scf_total_energy": -76.0214,
       "mp2_same_spin_correlation_energy": -0.0519,
       "mp2_opposite_spin_correlation_energy": -0.1549,
       "mp2_singles_energy": 0.0,
       "mp2_doubles_energy": -0.2069,
       "mp2_total_correlation_energy": -0.2069,
       "mp2_total_energy": -76.2283
     }
   }

Points to note:

- ``return_result`` is a bare number because the driver was ``energy``. It is
  duplicated in ``properties.return_energy``.
- ``molecule``, ``driver``, ``model``, and ``keywords`` are the input, repeated
  verbatim.
- Only computed properties appear. ``mp2_singles_energy`` is genuinely ``0.0``
  here — it is zero except for ROHF references — which is different from a field
  being absent.
- The dipole moment is in :math:`e\,a_0`, not Debye.


Water HF gradient
=================

Changing ``driver`` to ``gradient`` changes ``return_result`` from a scalar to a
flat :math:`3 N_{\text{atom}}` array.

.. code-block:: json

   {
     "schema_name": "qcschema_output",
     "schema_version": 1,
     "molecule": {
       "schema_name": "qcschema_molecule",
       "schema_version": 2,
       "geometry": [
         0.0,  0.0,    -0.1294,
         0.0, -1.4941,  1.0274,
         0.0,  1.4941,  1.0274
       ],
       "symbols": ["O", "H", "H"]
     },
     "driver": "gradient",
     "model": {
       "method": "HF",
       "basis": "cc-pVDZ"
     },
     "keywords": {},
     "provenance": {
       "creator": "QM Program",
       "version": "1.1",
       "routine": "module.json.run_json"
     },
     "return_result": [
       0.0,  0.0,    -0.0595,
       0.0, -0.0430,  0.0297,
       0.0,  0.0430,  0.0297
     ],
     "success": true,
     "properties": {
       "calcinfo_nbasis": 24,
       "calcinfo_nmo": 24,
       "calcinfo_nalpha": 5,
       "calcinfo_nbeta": 5,
       "calcinfo_natom": 3,
       "return_energy": -76.0214,
       "scf_one_electron_energy": -122.4453,
       "scf_two_electron_energy": 37.6224,
       "nuclear_repulsion_energy": 8.8014,
       "scf_dipole_moment": [0.0, 0.0, 0.8244],
       "scf_iterations": 10,
       "scf_total_energy": -76.0214
     }
   }

.. important::

   The gradient rows are in the same atom order as ``molecule.symbols``. A program
   that reorders atoms internally must not attach the original molecule to the
   reordered gradient.


A failed computation
====================

In v1, failure is reported on the output object itself. Note that most result
fields are absent — a consumer must check ``success`` before reading anything else.

.. code-block:: json

   {
     "schema_name": "qcschema_output",
     "schema_version": 1,
     "molecule": {
       "schema_name": "qcschema_molecule",
       "schema_version": 2,
       "symbols": ["O", "H", "H"],
       "geometry": [0.0, 0.0, -0.1294, 0.0, -1.4941, 1.0274, 0.0, 1.4941, 1.0274]
     },
     "driver": "energy",
     "model": {"method": "MP2", "basis": "cc-pVDZ"},
     "keywords": {},
     "provenance": {
       "creator": "QM Program",
       "version": "1.1",
       "routine": "module.json.run_json"
     },
     "success": false,
     "error": {
       "error_type": "convergence_error",
       "error_message": "SCF failed to converge after 50 iterations"
     }
   }
