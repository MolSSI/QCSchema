.. _torsion_drive:

=============
Torsion drive
=============

A torsion drive scans one or more dihedral angles, running a constrained geometry
optimization at each grid point. It is the deepest nesting in the specification
and the clearest demonstration that the pattern scales:

.. code-block:: text

   TorsionDriveSpecification              qcschema_torsion_drive_specification
   ├── program                            the scanner, e.g. torsiondrive
   ├── keywords                           qcschema_torsion_drive_keywords
   ├── protocols                          qcschema_torsion_drive_protocols
   └── specification: OptimizationSpecification    how to optimize
       └── specification: AtomicSpecification      how to get a gradient

Three specifications, three programs, one object.


.. _model-torsiondrivekeywords:

TorsionDriveKeywords
====================

:``schema_name``: ``qcschema_torsion_drive_keywords``

Unlike ``keywords`` elsewhere in QCSchema — free-form dictionaries passed through
to a program — torsion drive keywords are a **typed, validated model**. The scan
definition is part of the specification, not an opaque payload.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_torsion_drive_keywords"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``dihedrals``
     - array[array[integer, integer, integer, integer]]
     - **required**
     - The list of dihedrals to select for the TorsionDrive operation. Each entry is a tuple of integers of for particle indices.
   * - ``grid_spacing``
     - array[integer]
     - **required**
     - List of grid spacing for dihedral scan in degrees. Multiple values will be mapped to each dihedral angle.
   * - ``dihedral_ranges``
     - array[array[integer, integer]]
     - \-
     - A list of dihedral range limits as a pair (lower, upper). Each range corresponds to the dihedrals in input.
   * - ``energy_decrease_thresh``
     - number
     - \-
     - The threshold of the smallest energy decrease amount to trigger activating optimizations from grid point.
   * - ``energy_upper_limit``
     - number
     - \-
     - The threshold if the energy of a grid point that is higher than the current global minimum, to start new optimizations, in unit of a.u. I.e. if energy_upper_limit = 0.05, current global minimum energy is -9.9 , then a new task starting with energy -9.8 will be skipped.

.. code-block:: json

   {
     "keywords": {
       "schema_name": "qcschema_torsion_drive_keywords",
       "dihedrals": [[0, 1, 2, 3]],
       "grid_spacing": [15],
       "dihedral_ranges": [[-180, 180]],
       "energy_upper_limit": 0.05
     }
   }

``dihedrals`` entries are 4-tuples of 0-indexed atom indices — the same indexing
as everything else attached to a :doc:`molecule`. Scanning two dihedrals at once
means two entries, and ``grid_spacing`` gets one value per dihedral.

``energy_decrease_thresh`` and ``energy_upper_limit`` control the scan's
pruning: the first is how much a grid point must improve to be worth re-visiting,
the second caps how far uphill the scan will follow a coordinate.


.. _model-torsiondrivespecification:

TorsionDriveSpecification
=========================

:``schema_name``: ``qcschema_torsion_drive_specification``

The outermost layer of the specification stack: how to scan, wrapping how to
optimize, wrapping how to compute a gradient.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_torsion_drive_specification"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``program``
     - string
     - default ``""``
     - The program with which to run the torsion scan.
   * - ``keywords``
     - :ref:`TorsionDriveKeywords <model-torsiondrivekeywords>`
     - **required**
     - The torsion drive specific keywords to be used.
   * - ``protocols``
     - :ref:`TorsionDriveProtocols <model-torsiondriveprotocols>`
     - \-
     - Directives for how much of the output to retain.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the computation. Use for schema development and scratch space.
   * - ``specification``
     - :ref:`OptimizationSpecification <model-optimizationspecification>`
     - **required**
     - The specification for how to run optimizations for the torsion scan (within this is spec for gradients for the optimization.

.. code-block:: json

   {
     "schema_name": "qcschema_torsion_drive_specification",
     "program": "torsiondrive",
     "keywords": {
       "schema_name": "qcschema_torsion_drive_keywords",
       "dihedrals": [[0, 1, 2, 3]],
       "grid_spacing": [15]
     },
     "specification": {
       "schema_name": "qcschema_optimization_specification",
       "program": "geometric",
       "keywords": {},
       "specification": {
         "schema_name": "qcschema_atomic_specification",
         "program": "psi4",
         "driver": "gradient",
         "model": {"method": "B3LYP", "basis": "def2-SVP"},
         "keywords": {}
       }
     }
   }

Read that from the outside in: ``torsiondrive`` scans the dihedral, calling
``geomeTRIC`` to optimize at each grid point, which in turn calls ``psi4`` for
each gradient.


.. _model-torsiondriveinput:

TorsionDriveInput
=================

:``schema_name``: ``qcschema_torsion_drive_input``
:``schema_version``: 2

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_torsion_drive_input"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``schema_version``
     - ``2``
     - \-
     - The version of ``schema_name`` this conforms to. Fixed value.
   * - ``id``
     - string
     - \-
     - An optional identifier for the computation.
   * - ``initial_molecule``
     - array[:ref:`Molecule <model-molecule>`]
     - **required**
     - The starting molecule(s) for the torsion drive.
   * - ``specification``
     - :ref:`TorsionDriveSpecification <model-torsiondrivespecification>`
     - **required**
     - How to run the torsion drive.
   * - ``provenance``
     - :ref:`Provenance <model-provenance>`
     - \-
     - Information about what created this input.

``initial_molecule`` is a **list**, with at least one entry — a torsion drive may
be seeded from several starting conformers to reduce the chance of the scan
getting trapped in a local basin.


.. _model-torsiondriveprotocols:

TorsionDriveProtocols
=====================

:``schema_name``: ``qcschema_torsion_drive_protocols``

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_torsion_drive_protocols"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``scan_results``
     - ``all``, ``lowest``, ``none``
     - default ``"none"``
     - Which optimization results to keep at each grid point.

``scan_results`` governs how much per-grid-point optimization history is kept:
``all``, ``lowest``, or ``none``. Since each grid point is a full optimization,
which may itself contain a trajectory, this compounds quickly — a 24-point scan
storing everything can be very large.


.. _model-torsiondriveproperties:

TorsionDriveProperties
======================

:``schema_name``: ``qcschema_torsion_drive_properties``

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_torsion_drive_properties"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``calcinfo_ngrid``
     - integer
     - \-
     - The number of dihedral constraints optimized.

Currently a placeholder holding a single value, and designed for expansion. Read
``calcinfo_ngrid`` from here rather than computing ``len()`` of a results dict.


.. _model-torsiondriveresult:

TorsionDriveResult
==================

:``schema_name``: ``qcschema_torsion_drive_result``
:``schema_version``: 2

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_torsion_drive_result"``
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
     - :ref:`TorsionDriveInput <model-torsiondriveinput>`
     - **required**
     - The complete input that produced this result.
   * - ``final_molecules``
     - object
     - **required**
     - The final molecule at each angle of the TorsionDrive scan.
   * - ``scan_properties``
     - object
     - **required**
     - The map of energies and other properties for each angle of the TorsionDrive scan.
   * - ``scan_results``
     - object
     - **required**
     - The map of each angle of the TorsionDrive scan to each optimization computations.
   * - ``stdout``
     - string
     - \-
     - The standard output of the program.
   * - ``stderr``
     - string
     - \-
     - The standard error of the program.
   * - ``native_files``
     - object
     - \-
     - Program-native files retained from the computation.
   * - ``properties``
     - :ref:`TorsionDriveProperties <model-torsiondriveproperties>`
     - **required**
     - Summary values for the torsion drive as a whole.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the computation. Use for schema development and scratch space.
   * - ``success``
     - ``true``
     - \-
     - The success of a given programs execution. If False, other fields may be blank.
   * - ``provenance``
     - :ref:`Provenance <model-provenance>`
     - **required**
     - Information about the program that produced this result.

The three grid-keyed dictionaries share a key convention: a string encoding the
dihedral angle(s) of that grid point, such as ``"[-165]"`` for a single dihedral
or ``"[-165, 30]"`` for two.

.. code-block:: text

   final_molecules["[-165]"]                  optimized geometry at that point
   scan_properties["[-165]"].return_energy    its energy
   scan_results["[-165]"]                     full optimization history, if kept

   scan_properties[*].return_energy           the whole energy profile


.. seealso::

   :doc:`../implementation_guide/migrating_from_v1` for the field-by-field
   mapping from QCSchema v1, if you have existing v1 payloads or code.
