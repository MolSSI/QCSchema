.. _protocols:

=========
Protocols
=========

Protocols answer a question the rest of the schema does not: *how much of the
output should be kept?*

A wavefunction for a modest molecule in a decent basis is tens of megabytes. A
geometry optimization storing a complete result for every step multiplies that by
the iteration count. A torsion drive storing complete optimizations at every grid
point multiplies it again. Without a way to say "just the energies, please", a
database of computations becomes unstorable.

So the defaults keep very little, and you ask for more when you need it.

.. contents:: On this page
   :local:
   :depth: 1


Where protocols live
====================

Protocols are part of the *specification* — they are an input, not an output
setting — and each procedure has its own protocols object:

.. code-block:: text

   AtomicSpecification.protocols        qcschema_atomic_protocols
   OptimizationSpecification.protocols  qcschema_optimization_protocols
   TorsionDriveSpecification.protocols  qcschema_torsion_drive_protocols

They are enforced by the *result* constructor. A wavefunction handed to an
``AtomicResult`` whose input protocol says ``none`` is dropped, not stored. This
means the protocol is a guarantee to the consumer, not a hint to the producer.


Atomic protocols
================

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_atomic_protocols"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``wavefunction``
     - ``all``, ``orbitals_and_eigenvalues``, ``occupations_and_eigenvalues``, ``return_results``, ``none``
     - default ``"none"``
     - Wavefunction to keep from a computation.
   * - ``stdout``
     - boolean
     - default ``true``
     - Primary output file to keep from the computation
   * - ``error_correction``
     - :ref:`ErrorCorrectionProtocol <model-errorcorrectionprotocol>`
     - \-
     - Policies for error correction
   * - ``native_files``
     - ``all``, ``input``, ``none``
     - default ``"none"``
     - Policies for keeping processed files from the computation

``wavefunction``
----------------

.. list-table::
   :widths: 30 15 55
   :header-rows: 1

   * - Value
     - Size
     - Keeps
   * - ``all``
     - largest
     - Every wavefunction quantity the program produced.
   * - ``return_results``
     - moderate
     - Only the quantities named by the primary-return pointers, plus the
       pointers and the basis.
   * - ``orbitals_and_eigenvalues``
     - moderate
     - ``orbitals_*`` and ``eigenvalues_*``.
   * - ``occupations_and_eigenvalues``
     - small
     - ``occupations_*`` and ``eigenvalues_*``.
   * - ``none``
     - none
     - Nothing; ``wavefunction`` is ``null``. **Default.**

``return_results`` is usually the best trade: it is the smallest option that is
still self-describing, because the pointers tell the consumer what it received.
See :doc:`../user_guide/wavefunction`.

Note that filtering happens *after* the restricted/unrestricted reduction: if
``restricted`` is ``true``, all ``_b`` quantities are dropped regardless of
protocol.

``stdout``
----------

A plain boolean, defaulting to ``true``. This is the program's primary logging
output — natively standard output, or the output file for programs that write one.

Set it ``false`` for high-throughput work where you are storing millions of
records and will never read the logs. Keep it ``true`` when a human might need to
work out why an answer looks odd.

``native_files``
----------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Value
     - Keeps
   * - ``all``
     - Every program-native file the harness collected.
   * - ``input``
     - Only the generated input file.
   * - ``none``
     - Nothing. **Default.**

``input`` is the quietly useful one: storing the generated native input makes a
computation reproducible by hand, outside QCSchema entirely, at negligible cost.
When a result is disputed this is often the fastest way to settle it.

.. _model-errorcorrectionprotocol:

``error_correction``
--------------------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``default_policy``
     - boolean
     - default ``true``
     - Whether to allow error corrections that are not explicitly named in ``policies``.
   * - ``policies``
     - object
     - \-
     - Settings that define whether specific error corrections are allowed. Keys are the name of a known error and values are whether it is allowed to be used.

Controls whether a harness may automatically retry a failed computation with
adjusted settings — raising an iteration limit, switching an SCF algorithm.

.. code-block:: json

   {
     "error_correction": {
       "default_policy": true,
       "policies": {"scf_convergence": true, "memory_increase": false}
     }
   }

``default_policy`` applies to any correction not named in ``policies``. Keys in
``policies`` are the names of known errors as the implementing harness defines
them.

.. warning::

   Error-correction protocols are experimental and thinly implemented — in
   practice only some NWChem tasks act on them. Treat support as opt-in and
   program-specific.

Error correction has a consequence worth thinking about: a corrected computation
did not run with the settings in ``keywords``. If reproducibility matters more
than throughput, turn it off.


Optimization protocols
======================

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

.. list-table::
   :widths: 28 72
   :header-rows: 1

   * - ``trajectory_results``
     - Keeps
   * - ``all``
     - A full ``AtomicResult`` for every optimization step.
   * - ``initial_and_final``
     - The first and last steps only.
   * - ``final``
     - The last step only.
   * - ``none``
     - No full results. **Default.**

.. warning::

   The default is ``none``, so an optimization hands back no per-step results at
   all unless you ask for them. This is the single most surprising protocol
   default; if a trajectory you expected is empty, this is why.

``trajectory_properties`` is *not* protocol-controlled and is always populated
with abridged :ref:`AtomicProperties <model-atomicproperties>` for each step. That
is where per-step energies live, and for most analysis it is sufficient:

.. code-block:: python

   energies = [p.return_energy for p in result.trajectory_properties]

Ask for ``final`` when you want the converged single point's full detail —
including its wavefunction, if the nested atomic protocol asks for one — without
storing the whole path.


Torsion drive protocols
=======================

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

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - ``scan_results``
     - Keeps
   * - ``all``
     - Full optimization history at every grid point.
   * - ``lowest``
     - Only the lowest-energy optimization at each grid point.
   * - ``none``
     - No optimization results. **Default.**

The nesting compounds: ``scan_results: "all"`` combined with
``trajectory_results: "all"`` on the inner optimization spec and
``wavefunction: "all"`` on the innermost atomic spec will produce a record
thousands of times larger than the energies you probably wanted.

``scan_properties`` is always populated, and holds an
:ref:`OptimizationProperties <model-optimizationproperties>` per grid point —
enough for the energy profile:

.. code-block:: python

   profile = {g: p.return_energy for g, p in result.scan_properties.items()}


Choosing protocols
==================

.. list-table::
   :widths: 26 74
   :header-rows: 1

   * - Situation
     - Suggested protocols
   * - High-throughput database
     - All defaults, plus ``stdout: false``. Keep only properties.
   * - Reproducible archive
     - ``native_files: "input"``, ``stdout: true``, error correction off.
   * - Orbital analysis or visualization
     - ``wavefunction: "return_results"``, or ``"all"`` if you need Fock and
       density matrices.
   * - Debugging one calculation
     - ``stdout: true``, ``native_files: "all"``.
   * - Optimization you will re-analyze
     - ``trajectory_results: "final"`` — full detail where it matters, no path.
   * - Reaction-path or IRC analysis
     - ``trajectory_results: "all"``. Accept the size.

.. tip::

   Protocols are chosen at input time and cannot be recovered afterwards. A record
   written with the defaults has *discarded* the wavefunction and the trajectory —
   no later processing step can reconstruct them, and the only remedy is to run the
   computation again. Decide before you run, not after.

   If you also need to hand records to consumers that expect QCSchema v1, see
   :doc:`migrating_from_v1`.
