.. _optimization:

=====================
Geometry optimization
=====================

A geometry optimization is a *procedure*: it runs many single points and reports
where it ended up. The schema mirrors that structure — an optimization
specification contains the atomic specification it will use to get gradients.

.. code-block:: text

   OptimizationInput               qcschema_optimization_input
   ├── initial_molecule
   └── specification               qcschema_optimization_specification
       ├── program                 the optimizer, e.g. geomeTRIC, optking
       ├── keywords                optimizer keywords
       ├── protocols               qcschema_optimization_protocols
       └── specification           qcschema_atomic_specification  ← the gradients

   OptimizationResult              qcschema_optimization_result
   ├── input_data
   ├── final_molecule
   ├── trajectory_properties       per-step abridged properties
   ├── trajectory_results          per-step full AtomicResults (opt-in)
   └── properties                  qcschema_optimization_properties


.. _model-optimizationspecification:

OptimizationSpecification
=========================

:``schema_name``: ``qcschema_optimization_specification``

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_optimization_specification"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``program``
     - string
     - default ``""``
     - The program with which to run the geometry optimization.
   * - ``keywords``
     - object
     - \-
     - The optimization specific keywords to be used.
   * - ``protocols``
     - :ref:`OptimizationProtocols <model-optimizationprotocols>`
     - \-
     - Directives for how much of the output to retain.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the computation. Use for schema development and scratch space.
   * - ``specification``
     - :ref:`AtomicSpecification <model-atomicspecification>` or ``ManyBodySpecification``
     - **required**
     - A directive for how to compute a gradient for the optimization. Either an ordinary atomic/single-point or a many-body spec.

The nested ``specification`` field is the important one: it describes how to
produce the gradients the optimizer consumes. It is normally an
:ref:`AtomicSpecification <model-atomicspecification>` with
``driver: "gradient"``, but anything that can produce a gradient works —
a many-body expansion, for instance.

.. note::

   When `QCManyBody <https://github.com/MolSSI/QCManyBody>`_ is installed, this
   field, ``trajectory_properties``, and ``trajectory_results`` widen into
   discriminated unions accepting the corresponding ``ManyBody*`` models
   alongside the ``Atomic*`` ones. Those models are documented by QCManyBody
   rather than here. Without QCManyBody installed the fields accept only the
   atomic forms, so the exact type shown in the tables on this page depends on
   your environment.

.. code-block:: json

   {
     "schema_name": "qcschema_optimization_specification",
     "program": "geometric",
     "keywords": {"coordsys": "tric", "convergence_set": "gau_tight"},
     "specification": {
       "schema_name": "qcschema_atomic_specification",
       "program": "psi4",
       "driver": "gradient",
       "model": {"method": "B3LYP", "basis": "def2-SVP"},
       "keywords": {}
     }
   }

.. important::

   There are two ``program`` fields here and they mean different things:
   ``OptimizationSpecification.program`` is the optimizer, while
   ``OptimizationSpecification.specification.program`` is the code computing
   gradients. Do not conflate them.


.. _model-optimizationinput:

OptimizationInput
=================

:``schema_name``: ``qcschema_optimization_input``
:``schema_version``: 2

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``id``
     - string
     - \-
     - An optional identifier for the computation.
   * - ``schema_name``
     - ``"qcschema_optimization_input"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``schema_version``
     - ``2``
     - \-
     - The version of ``schema_name`` this conforms to. Fixed value.
   * - ``specification``
     - :ref:`OptimizationSpecification <model-optimizationspecification>`
     - **required**
     - How to run the geometry optimization.
   * - ``initial_molecule``
     - :ref:`Molecule <model-molecule>`
     - **required**
     - The starting molecule for the geometry optimization.
   * - ``provenance``
     - :ref:`Provenance <model-provenance>`
     - \-
     - Information about what created this input.

Note ``initial_molecule`` rather than ``molecule`` — the geometry is going to
change, and the field name says which end you are holding. The optimized geometry
comes back as ``final_molecule`` on the result.


.. _model-optimizationprotocols:

OptimizationProtocols
=====================

:``schema_name``: ``qcschema_optimization_protocols``

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_optimization_protocols"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``trajectory_results``
     - ``all``, ``initial_and_final``, ``final``, ``none``
     - default ``"none"``
     - Which gradient evaluations to keep in an optimization trajectory.

.. warning::

   **``trajectory_results`` defaults to ``none``.** A full result for every step of
   a routine optimization is frequently megabytes, so nothing is kept unless you
   ask:

   .. code-block:: json

      {"protocols": {"trajectory_results": "all"}}

   The options are ``all``, ``initial_and_final``, ``final``, and ``none``.

You usually do not need the full trajectory: ``trajectory_properties`` is kept
regardless and holds the per-step energies and other abridged properties, which
is what most analysis actually wants.


.. _model-optimizationproperties:

OptimizationProperties
======================

:``schema_name``: ``qcschema_optimization_properties``

New in v2. Summary values for the optimization as a whole, evaluated at the final
geometry.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_optimization_properties"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``nuclear_repulsion_energy``
     - number
     - \-
     - The nuclear repulsion energy.
   * - ``return_energy``
     - number
     - units ``E_h``
     - The energy of the final optimized molecule. Always available. Identical to the final ``return_energy``.
   * - ``return_gradient``
     - array[number]
     - units ``E_h/a0``; shape ``(nat, 3)``
     - The gradient of the final optimized molecule. Always available. Identical to ``return_gradient``.
   * - ``optimization_iterations``
     - integer
     - \-
     - The number of geometry iterations taken before convergence.
   * - ``final_max_force``
     - number
     - \-
     - The largest force component at the final geometry.
   * - ``final_rms_force``
     - number
     - units ``E_h/a0``
     - The final RMS gradient of the molecule in Hartrees/Bohr.
   * - ``final_max_displacement``
     - number
     - \-
     - The largest coordinate displacement of the final step.
   * - ``final_rms_displacement``
     - number
     - \-
     - The RMS coordinate displacement of the final step.

These are the values you would otherwise have to dig out of the last element of a
trajectory, and they are present whether or not the trajectory itself was kept.
The final energy is ``properties.return_energy``.


.. _model-optimizationresult:

OptimizationResult
==================

:``schema_name``: ``qcschema_optimization_result``
:``schema_version``: 2

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_optimization_result"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``schema_version``
     - ``2``
     - \-
     - The version of ``schema_name`` this conforms to. Fixed value.
   * - ``id``
     - string
     - \-
     - The optional ID for the computation.
   * - ``input_data``
     - :ref:`OptimizationInput <model-optimizationinput>`
     - **required**
     - The complete input that produced this result.
   * - ``final_molecule``
     - :ref:`Molecule <model-molecule>`
     - **required**
     - The final molecule of the geometry optimization.
   * - ``trajectory_results``
     - array[:ref:`AtomicResult <model-atomicresult>`] or array[``ManyBodyResult``]
     - **required**
     - An ordered list of single-geometry result objects for each step in the optimization. Either an ordinary atomic/single-point or a many-body result.
   * - ``trajectory_properties``
     - array[:ref:`AtomicProperties <model-atomicproperties>`] or array[``ManyBodyProperties``]
     - **required**
     - An ordered list of abridged single-geometry property sets (energy and other properties) for each step in the optimization. Either an ordinary atomic/single-point or a many-body properties.
   * - ``stdout``
     - string
     - \-
     - The standard output of the program.
   * - ``stderr``
     - string
     - \-
     - The standard error of the program.
   * - ``success``
     - ``true``
     - \-
     - The success of a given programs execution. If False, other fields may be blank.
   * - ``provenance``
     - :ref:`Provenance <model-provenance>`
     - **required**
     - Information about the program that produced this result.
   * - ``native_files``
     - object
     - \-
     - Program-native files retained from the computation.
   * - ``properties``
     - :ref:`OptimizationProperties <model-optimizationproperties>`
     - **required**
     - Summary values for the optimization as a whole.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the computation. Use for schema development and scratch space.

Reading a result
----------------

Field paths from the top of the result object:

.. code-block:: text

   final_molecule                                    the optimized geometry
   properties.return_energy                          final energy
   properties.optimization_iterations                how many steps
   properties.final_rms_force                        convergence achieved

   trajectory_properties[*].return_energy            per-step energies
   trajectory_results                                full per-step results,
                                                     only if the protocol asked

   input_data.specification.program                  the optimizer
   input_data.specification.specification.model      the gradient method

As with :ref:`AtomicResult <model-atomicresult>`, ``success`` is fixed to ``true``
and there is no ``error`` field; a failed optimization is a
:ref:`FailedOperation <model-failedoperation>`.


.. seealso::

   :doc:`../implementation_guide/migrating_from_v1` for the field-by-field
   mapping from QCSchema v1, if you have existing v1 payloads or code.
