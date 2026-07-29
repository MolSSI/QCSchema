================
Worked examples
================

Complete QCSchema v2 documents for the computations people actually run. These
are full objects, not excerpts — including the fields a producer fills in for you,
so what you see is what a v2-speaking program actually emits.

Arrays have been reflowed onto single lines and floating point values truncated
for legibility; no keys have been removed. ``provenance`` values are whatever
produced the object, and are stand-ins here.

Each example leads with JSON, with a **Python** tab showing the same object as
models — see :ref:`tab_convention`.

.. contents:: On this page
   :local:
   :depth: 1


Water MP2 energy
================

The canonical example: a single-point correlated energy.

.. tab-set::

   .. tab-item:: Input JSON

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
             "keywords": {},
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

   .. tab-item:: Result JSON

      .. code-block:: json

         {
           "schema_name": "qcschema_atomic_result",
           "schema_version": 2,
           "id": null,
           "input_data": {
             "id": null,
             "schema_name": "qcschema_atomic_input",
             "schema_version": 2,
             "molecule": "... the qcschema_molecule from the input ...",
             "specification": {
               "schema_name": "qcschema_atomic_specification",
               "keywords": {},
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
           },
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
             "provenance": {"creator": "MyDriver", "version": "1.0",
                            "routine": "mydriver.build_molecule"},
             "extras": {}
           },
           "properties": {
             "schema_name": "qcschema_atomic_properties",
             "calcinfo_nbasis": 24,
             "calcinfo_nmo": 24,
             "calcinfo_nalpha": 5,
             "calcinfo_nbeta": 5,
             "calcinfo_natom": 3,
             "nuclear_repulsion_energy": 8.80146205625184,
             "return_energy": -76.22836742810021,
             "scf_one_electron_energy": -122.44534536383037,
             "scf_two_electron_energy": 37.62246494040059,
             "scf_dipole_moment": [0.0, 0.0, 0.8244],
             "scf_total_energy": -76.02141836717794,
             "scf_iterations": 10,
             "mp2_same_spin_correlation_energy": -0.05198079291625,
             "mp2_opposite_spin_correlation_energy": -0.15496826800602,
             "mp2_singles_energy": 0.0,
             "mp2_doubles_energy": -0.20694906092227,
             "mp2_correlation_energy": -0.20694906092227,
             "mp2_total_energy": -76.22836742810021
           },
           "wavefunction": null,
           "return_result": -76.22836742810021,
           "stdout": null,
           "stderr": null,
           "native_files": {},
           "success": true,
           "provenance": {
             "creator": "Psi4",
             "version": "1.9",
             "routine": "psi4.schema_runner"
           },
           "extras": {}
         }

   .. tab-item:: Python

      .. code-block:: python

         water = Molecule(
             symbols=["O", "H", "H"],
             geometry=[0.0, 0.0, -0.1294, 0.0, -1.4941, 1.0274, 0.0, 1.4941, 1.0274],
         )
         atomic_input = AtomicInput(
             molecule=water,
             specification=AtomicSpecification(
                 program="psi4",
                 driver="energy",
                 model={"method": "MP2", "basis": "cc-pVDZ"},
             ),
         )

Points worth noticing:

- ``return_result`` is the *primary* answer, a bare number here because the
  driver was ``energy``. It is duplicated in ``properties.return_energy``.
- Intermediate quantities are named, not positional. Every SCF and MP2
  contribution has a documented key — see :doc:`../user_guide/properties`.
- ``properties`` omits every field that was not computed. The properties model
  has ~50 possible keys; only the ones with values are serialized.
- ``wavefunction`` is ``null`` because the default protocol discards it.
- ``molecule`` appears **twice**: once inside ``input_data`` (the frame you
  submitted) and once at the top level (the frame the results are in). For a
  single point these are usually the same; after reorientation they are not.


Water HF gradient
=================

Changing ``driver`` to ``gradient`` changes the type of ``return_result`` from a
scalar to a flat :math:`3 N_{\text{atom}}` array.

.. code-block:: json

   {
     "schema_name": "qcschema_atomic_result",
     "schema_version": 2,
     "input_data": {
       "schema_name": "qcschema_atomic_input",
       "schema_version": 2,
       "molecule": "... the qcschema_molecule ...",
       "specification": {
         "schema_name": "qcschema_atomic_specification",
         "keywords": {},
         "program": "psi4",
         "driver": "gradient",
         "model": {"method": "HF", "basis": "cc-pVDZ"},
         "protocols": {"schema_name": "qcschema_atomic_protocols",
                       "wavefunction": "none", "stdout": true,
                       "error_correction": {"default_policy": true, "policies": null},
                       "native_files": "none"},
         "extras": {}
       },
       "provenance": {"creator": "MyDriver", "version": "1.0",
                      "routine": "mydriver.build_input"}
     },
     "molecule": "... the qcschema_molecule ...",
     "properties": {
       "schema_name": "qcschema_atomic_properties",
       "calcinfo_nbasis": 24,
       "calcinfo_nmo": 24,
       "calcinfo_nalpha": 5,
       "calcinfo_nbeta": 5,
       "calcinfo_natom": 3,
       "nuclear_repulsion_energy": 8.80146205625184,
       "return_energy": -76.02141836717794,
       "return_gradient": [0.0, 0.0, -0.0595, 0.0, -0.0430, 0.0297, 0.0, 0.0430, 0.0297],
       "scf_total_energy": -76.02141836717794,
       "scf_total_gradient": [0.0, 0.0, -0.0595, 0.0, -0.0430, 0.0297, 0.0, 0.0430, 0.0297],
       "scf_iterations": 10
     },
     "wavefunction": null,
     "return_result": [0.0, 0.0, -0.0595, 0.0, -0.0430, 0.0297, 0.0, 0.0430, 0.0297],
     "stdout": null,
     "stderr": null,
     "native_files": {},
     "success": true,
     "provenance": {"creator": "Psi4", "version": "1.9", "routine": "psi4.schema_runner"},
     "extras": {}
   }

.. important::

   The gradient rows are in the same atom order as ``molecule.symbols``. A
   program that reorders atoms internally **must not** attach the original
   molecule to the reordered gradient. This obligation is stated on the field
   itself and is one of the load-bearing rules of the specification — see
   :doc:`../implementation_guide/conventions`.

Requesting a ``hessian`` works the same way; ``return_result`` becomes
:math:`3N \times 3N` numbers, again stored flat.


Geometry optimization
=====================

An optimization is where the nesting pattern earns its keep. The optimizer needs
its own program and keywords, *and* it needs to know how to compute the gradients
it will consume — so an :ref:`OptimizationSpecification
<model-optimizationspecification>` contains an :ref:`AtomicSpecification
<model-atomicspecification>`.

.. tab-set::

   .. tab-item:: Input JSON

      .. code-block:: json

         {
           "id": null,
           "schema_name": "qcschema_optimization_input",
           "schema_version": 2,
           "specification": {
             "schema_name": "qcschema_optimization_specification",
             "program": "geometric",
             "keywords": {"coordsys": "tric"},
             "protocols": {
               "schema_name": "qcschema_optimization_protocols",
               "trajectory_results": "none"
             },
             "extras": {},
             "specification": {
               "schema_name": "qcschema_atomic_specification",
               "keywords": {},
               "program": "psi4",
               "driver": "gradient",
               "model": {"method": "B3LYP", "basis": "def2-SVP"},
               "protocols": {
                 "schema_name": "qcschema_atomic_protocols",
                 "wavefunction": "none",
                 "stdout": true,
                 "error_correction": {"default_policy": true, "policies": null},
                 "native_files": "none"
               },
               "extras": {}
             }
           },
           "initial_molecule": "... the qcschema_molecule ...",
           "provenance": {
             "creator": "MyDriver",
             "version": "1.0",
             "routine": "mydriver.build_input"
           }
         }

   .. tab-item:: Result shape

      .. code-block:: json

         {
           "schema_name": "qcschema_optimization_result",
           "schema_version": 2,
           "input_data": "... the qcschema_optimization_input above ...",
           "final_molecule": "... the optimized qcschema_molecule ...",
           "trajectory_properties": [
             {"schema_name": "qcschema_atomic_properties",
              "return_energy": -76.3183, "calcinfo_natom": 3},
             {"schema_name": "qcschema_atomic_properties",
              "return_energy": -76.3244, "calcinfo_natom": 3},
             {"schema_name": "qcschema_atomic_properties",
              "return_energy": -76.3251, "calcinfo_natom": 3}
           ],
           "trajectory_results": [],
           "properties": {
             "schema_name": "qcschema_optimization_properties",
             "return_energy": -76.3251,
             "optimization_iterations": 3,
             "nuclear_repulsion_energy": 9.1214,
             "final_rms_force": 1.7e-05
           },
           "stdout": null,
           "stderr": null,
           "native_files": {},
           "success": true,
           "provenance": {"creator": "geomeTRIC", "version": "1.0",
                          "routine": "geometric.run_json"},
           "extras": {}
         }

   .. tab-item:: Python

      .. code-block:: python

         opt_input = OptimizationInput(
             initial_molecule=water,
             specification=OptimizationSpecification(
                 program="geometric",
                 keywords={"coordsys": "tric"},
                 specification=AtomicSpecification(
                     program="psi4",
                     driver="gradient",
                     model={"method": "B3LYP", "basis": "def2-SVP"},
                 ),
             ),
         )

Two things about the result are worth noting:

``trajectory_results`` is empty unless asked for
   A full result for every step would make optimization records enormous, so
   ``protocols.trajectory_results`` defaults to ``none``. Set it to ``all`` — or
   ``initial_and_final``, or ``final`` — when you want them.

``trajectory_properties`` is always there
   Per-step energies live in ``trajectory_properties``, a list of abridged
   :ref:`AtomicProperties <model-atomicproperties>`, which is kept regardless of
   protocol. Summary values for the whole optimization, including the final
   energy, are in ``properties``.

See :doc:`../user_guide/optimization`.


A computation that failed
=========================

In v2 a result object is always a *success*: ``AtomicResult.success`` is
``Literal[True]`` and there is no ``error`` field. Failures are a different type
of object entirely — a :ref:`FailedOperation <model-failedoperation>`.

.. code-block:: json

   {
     "schema_name": "qcschema_failed_operation",
     "schema_version": 2,
     "id": null,
     "input_data": "... the qcschema_atomic_input that failed ...",
     "success": false,
     "error": {
       "error_type": "convergence_error",
       "error_message": "SCF failed to converge after 100 iterations.",
       "extras": null
     },
     "extras": {}
   }

Because ``success`` is present on both kinds of object, and is a fixed value on
each, a consumer can branch on it before knowing which of the two it holds: check
``success``, then read ``return_result`` or ``error`` accordingly. A validator will
reject a result claiming to be a failure, and a ``FailedOperation`` claiming
success.

See :doc:`../user_guide/errors` for the error taxonomy and what belongs in
``error_type``.


Reusing one specification
=========================

Because the specification is a standalone object, "same method, many molecules"
means repeating one block rather than rebuilding the input each time. The
specification below is byte-identical across every input in the set; only
``molecule`` differs:

.. code-block:: json

   {
     "schema_name": "qcschema_atomic_specification",
     "program": "psi4",
     "driver": "energy",
     "model": {"method": "B3LYP-D3BJ", "basis": "def2-TZVP"},
     "keywords": {"scf_type": "df"}
   }

That matters for storage as much as for convenience: a database holding a million
computations at one level of theory can describe the theory once and reference it.

The same object drops into an ``OptimizationSpecification.specification`` slot
unchanged, which is exactly why v2 moved these fields off ``AtomicInput``.


Keeping the wavefunction
========================

Orbitals, densities, and Fock matrices are discarded by default. Ask for them
through the protocol:

.. code-block:: json

   {
     "schema_name": "qcschema_atomic_specification",
     "program": "psi4",
     "driver": "energy",
     "model": {"method": "HF", "basis": "cc-pVDZ"},
     "protocols": {"wavefunction": "orbitals_and_eigenvalues"}
   }

The result then carries a ``wavefunction`` block containing the full
:ref:`BasisSet <model-basisset>` the quantities are expressed in, plus the
requested matrices:

.. code-block:: json

   {
     "wavefunction": {
       "schema_name": "qcschema_wavefunction_properties",
       "restricted": true,
       "basis": {"schema_name": "qcschema_basis_set", "schema_version": 2,
                 "name": "cc-pVDZ", "center_data": {"...": "..."},
                 "atom_map": ["O1", "H1", "H1"], "nbf": 24},
       "scf_orbitals_a": ["... nao * nmo numbers, column-major ..."],
       "scf_eigenvalues_a": ["... nmo numbers ..."],
       "orbitals_a": "scf_orbitals_a",
       "eigenvalues_a": "scf_eigenvalues_a"
     }
   }

Note the indirection at the bottom: ``orbitals_a`` does not hold orbitals, it
holds the *name of the field* that does. This lets a consumer ask "what are the
orbitals of the method that was actually requested?" without knowing whether the
computation was HF, DFT, or something correlated. See
:doc:`../user_guide/wavefunction`.
