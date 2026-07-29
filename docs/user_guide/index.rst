.. _user_guide:

==================
Schema User Guide
==================

This section documents what is *in* QCSchema v2: every object, every field, and
what each one means. It is written for people producing or consuming QCSchema
data — if you are adding QCSchema support to a program, read
:doc:`../implementation_guide/index` alongside it.

.. toctree::
   :maxdepth: 2

   concepts
   molecule
   atomic
   properties
   wavefunction
   basis_set
   optimization
   torsion_drive
   errors
   faq


Object index
============

Every QCSchema object identifies itself with a ``schema_name``. Top-level
containers — the ones you would send or store on their own — also carry a
``schema_version``. The table below is the complete v2 set.

.. list-table::
   :widths: 30 40 10 20
   :header-rows: 1

   * - Object
     - ``schema_name``
     - Version
     - Documented in
   * - :ref:`Molecule <model-molecule>`
     - ``qcschema_molecule``
     - 3
     - :doc:`molecule`
   * - :ref:`BasisSet <model-basisset>`
     - ``qcschema_basis_set``
     - 2
     - :doc:`basis_set`
   * - :ref:`AtomicSpecification <model-atomicspecification>`
     - ``qcschema_atomic_specification``
     - —
     - :doc:`atomic`
   * - :ref:`AtomicProtocols <model-atomicprotocols>`
     - ``qcschema_atomic_protocols``
     - —
     - :doc:`../implementation_guide/protocols`
   * - :ref:`AtomicInput <model-atomicinput>`
     - ``qcschema_atomic_input``
     - 2
     - :doc:`atomic`
   * - :ref:`AtomicProperties <model-atomicproperties>`
     - ``qcschema_atomic_properties``
     - —
     - :doc:`properties`
   * - :ref:`WavefunctionProperties <model-wavefunctionproperties>`
     - ``qcschema_wavefunction_properties``
     - —
     - :doc:`wavefunction`
   * - :ref:`AtomicResult <model-atomicresult>`
     - ``qcschema_atomic_result``
     - 2
     - :doc:`atomic`
   * - :ref:`OptimizationProtocols <model-optimizationprotocols>`
     - ``qcschema_optimization_protocols``
     - —
     - :doc:`../implementation_guide/protocols`
   * - :ref:`OptimizationSpecification <model-optimizationspecification>`
     - ``qcschema_optimization_specification``
     - —
     - :doc:`optimization`
   * - :ref:`OptimizationInput <model-optimizationinput>`
     - ``qcschema_optimization_input``
     - 2
     - :doc:`optimization`
   * - :ref:`OptimizationProperties <model-optimizationproperties>`
     - ``qcschema_optimization_properties``
     - —
     - :doc:`optimization`
   * - :ref:`OptimizationResult <model-optimizationresult>`
     - ``qcschema_optimization_result``
     - 2
     - :doc:`optimization`
   * - :ref:`TorsionDriveKeywords <model-torsiondrivekeywords>`
     - ``qcschema_torsion_drive_keywords``
     - —
     - :doc:`torsion_drive`
   * - :ref:`TorsionDriveProtocols <model-torsiondriveprotocols>`
     - ``qcschema_torsion_drive_protocols``
     - —
     - :doc:`../implementation_guide/protocols`
   * - :ref:`TorsionDriveSpecification <model-torsiondrivespecification>`
     - ``qcschema_torsion_drive_specification``
     - —
     - :doc:`torsion_drive`
   * - :ref:`TorsionDriveInput <model-torsiondriveinput>`
     - ``qcschema_torsion_drive_input``
     - 2
     - :doc:`torsion_drive`
   * - :ref:`TorsionDriveProperties <model-torsiondriveproperties>`
     - ``qcschema_torsion_drive_properties``
     - —
     - :doc:`torsion_drive`
   * - :ref:`TorsionDriveResult <model-torsiondriveresult>`
     - ``qcschema_torsion_drive_result``
     - 2
     - :doc:`torsion_drive`
   * - :ref:`FailedOperation <model-failedoperation>`
     - ``qcschema_failed_operation``
     - 2
     - :doc:`errors`

A handful of small objects are always embedded in a parent and carry no
``schema_name`` of their own: :ref:`Provenance <model-provenance>`,
:ref:`Model <model-model>`, :ref:`ComputeError <model-computeerror>`,
:ref:`Identifiers <model-identifiers>`, and the basis set components
:ref:`BasisCenter <model-basiscenter>`, :ref:`ElectronShell
<model-electronshell>`, and :ref:`ECPPotential <model-ecppotential>`.

.. note::

   ``Molecule.schema_version`` is ``3`` and ``BasisSet.schema_version`` is ``2``
   while the family as a whole is "v2". Molecule's numbering has always run one
   ahead; treat the numbers as per-object, not global. See
   :doc:`../implementation_guide/versioning`.
