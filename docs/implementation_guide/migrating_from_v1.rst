.. _migrating_from_v1:

===================
Migrating from v1
===================

The rest of these docs describe QCSchema v2 on its own terms. This page is the
exception: it is for people with existing v1 payloads or v1 code, and it collects
everything that changed, why, and what to do about it.

If you have no v1 history, you can skip this page entirely.

.. contents:: On this page
   :local:
   :depth: 2


What changed, in summary
========================

Four structural changes account for most of the migration effort:

**Specifications were extracted.**
   ``driver``, ``model``, ``keywords``, ``protocols``, and ``extras`` moved off
   the input into a reusable ``*Specification`` object — and specifications nest,
   so an optimization spec contains the atomic spec it uses for gradients.

**Results stopped inheriting from inputs.**
   v1's ``AtomicResult`` *subclassed* ``AtomicInput``, flattening input and output
   fields into one namespace. A v2 result **embeds** its input as ``input_data``.

**Failure became a separate type.**
   v1 allowed ``success: false`` with an ``error`` on any result. In v2 a result's
   ``success`` is fixed ``true`` and there is no ``error`` field; failures are
   ``qcschema_failed_operation`` objects.

**Properties objects were added** for optimizations and torsion drives, holding
summary values that previously had to be dug out of trajectory list indices.

Plus a set of behavioural changes covered under
:ref:`behavioural-changes` below.

Why do it at all? To make subschemas reusable and composable, and to standardize
naming and field availability so they are predictable. The v1 layout had grown a
different shape for each procedure, and no way to describe a level of theory
separately from a molecule.


Schema names and versions
=========================

Every ``schema_name`` was systematically reviewed; ``output`` became ``result``,
and nearly every embedded object gained a name of its own.

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - v1 ``schema_name``
     - v2 ``schema_name``
   * - ``qcschema_input`` / ``qc_schema_input``
     - ``qcschema_atomic_input``
   * - ``qcschema_output`` / ``qc_schema_output``
     - ``qcschema_atomic_result``
   * - ``qcschema_optimization_input``
     - ``qcschema_optimization_input`` *(unchanged)*
   * - ``qcschema_optimization_output``
     - ``qcschema_optimization_result``
   * - ``qcschema_torsion_drive_input``
     - ``qcschema_torsion_drive_input`` *(unchanged)*
   * - ``qcschema_torsion_drive_output``
     - ``qcschema_torsion_drive_result``
   * - ``qcschema_basis``
     - ``qcschema_basis_set``
   * - *(no name)*
     - ``qcschema_atomic_specification``,
       ``qcschema_atomic_properties``, ``qcschema_atomic_protocols``,
       ``qcschema_wavefunction_properties``, ``qcschema_failed_operation``,
       ``qcschema_optimization_specification``,
       ``qcschema_optimization_properties``,
       ``qcschema_optimization_protocols``,
       ``qcschema_torsion_drive_specification``,
       ``qcschema_torsion_drive_keywords``,
       ``qcschema_torsion_drive_properties``,
       ``qcschema_torsion_drive_protocols``

.. important::

   **v2 validates its markers strictly.** v1 was lenient: ``AtomicInput``
   accepted both ``qc_schema_input`` and ``qcschema_input`` by regex, and
   ``AtomicResult`` would accept an *input* schema name and silently rewrite it to
   the output one. v2 does neither — a payload carrying a v1 name is rejected, not
   coerced.

   So the first symptom of an unconverted payload is usually a rejected
   ``schema_name``. Convert it properly rather than patching the marker by hand;
   the marker is not the only thing that changed.

Version numbers also moved, and they are **per-object**:
``Molecule.schema_version`` went from ``2`` to ``3``, ``BasisSet.schema_version``
is ``2``, and every other v2 top-level container is ``2``. Molecule's numbering has
always run one ahead of the family. See :doc:`versioning`.


Atomic (single point)
=====================

Field moves
-----------

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - QCSchema v1
     - QCSchema v2
   * - ``AtomicInput.driver``
     - ``AtomicInput.specification.driver``
   * - ``AtomicInput.model``
     - ``AtomicInput.specification.model``
   * - ``AtomicInput.keywords``
     - ``AtomicInput.specification.keywords``
   * - ``AtomicInput.protocols``
     - ``AtomicInput.specification.protocols``
   * - ``AtomicInput.extras``
     - ``AtomicInput.specification.extras``
   * - —
     - ``AtomicInput.specification.program`` *(new)*
   * - ``AtomicResult.model`` *(inherited)*
     - ``AtomicResult.input_data.specification.model``
   * - ``AtomicResult.driver`` *(inherited)*
     - ``AtomicResult.input_data.specification.driver``
   * - ``AtomicResult.keywords`` *(inherited)*
     - ``AtomicResult.input_data.specification.keywords``
   * - ``AtomicResult.extras`` *(inherited from input)*
     - ``AtomicResult.input_data.specification.extras`` for input extras;
       ``AtomicResult.extras`` is now separate
   * - ``AtomicResult.success: bool``
     - ``AtomicResult.success``, fixed ``true``
   * - ``AtomicResult.error``
     - removed — use ``qcschema_failed_operation``

Renames
-------

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - v1 object
     - v2 object
   * - ``AtomicResultProperties``
     - ``AtomicProperties``
   * - ``AtomicResultProtocols``
     - ``AtomicProtocols``
   * - ``QCInputSpecification``
     - ``AtomicSpecification``

The two molecules
-----------------

v1 had a single ``molecule`` field on the result, which meant a program that
reoriented or recentred had nowhere to record both frames. v2 keeps both:

.. code-block:: text

   input_data.molecule    the frame that was submitted
   molecule               the frame the results are expressed in

Per-atom results — gradients, Hessians — belong to the top-level ``molecule``.
This is the reason the change was made; see
:doc:`../implementation_guide/conventions` for the obligations that follow from
it.

The two extras
--------------

v1 results inherited ``extras`` from the input, so there was one dictionary. v2
has two: ``input_data.specification.extras`` for whatever the caller attached, and
``extras`` on the result for whatever the program attached. A driver's annotations
no longer get overwritten by the program's.


Optimization
============

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - QCSchema v1
     - QCSchema v2
   * - ``OptimizationInput.keywords``
     - ``.specification.keywords``
   * - ``OptimizationInput.protocols``
     - ``.specification.protocols``
   * - ``OptimizationInput.extras``
     - ``.specification.extras``
   * - ``OptimizationInput.input_specification``
     - ``.specification.specification`` *(the gradient spec)*
   * - ``keywords["program"]`` *(by convention)*
     - ``.specification.program`` *(a real field)*
   * - ``OptimizationInput.hash_index``
     - removed
   * - ``protocols.trajectory`` *(default* ``all`` *)*
     - ``protocols.trajectory_results`` *(default* ``none`` *)*
   * - ``result.trajectory``
     - ``result.trajectory_results``
   * - ``result.energies``
     - ``result.trajectory_properties[*].return_energy``
   * - ``result.energies[-1]``
     - ``result.properties.return_energy``
   * - ``success: bool`` / ``error``
     - ``success`` fixed ``true``; failures via ``qcschema_failed_operation``

.. warning::

   **The trajectory default flipped.** v1's ``trajectory`` protocol defaulted to
   ``all``, so every optimization record carried a complete result for every step —
   frequently megabytes for a routine optimization. v2's ``trajectory_results``
   defaults to ``none``.

   If you relied on the v1 behaviour, ask for it explicitly:

   .. code-block:: json

      {"protocols": {"trajectory_results": "all"}}

   Note also that ``trajectory_properties`` is populated regardless and holds the
   per-step energies, which is what most v1 code was actually reading ``energies``
   for.

Two other v1 habits to unlearn: the optimizer program was conventionally smuggled
through ``keywords["program"]`` and is now a dedicated field, and summary values
like the final energy were read out of list indices and now live in
``result.properties``.


Torsion drive
=============

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - QCSchema v1
     - QCSchema v2
   * - ``TDKeywords``
     - ``TorsionDriveKeywords``
   * - ``TorsionDriveInput.keywords``
     - ``.specification.keywords``
   * - ``TorsionDriveInput.extras``
     - ``.specification.extras``
   * - ``TorsionDriveInput.optimization_spec``
     - ``.specification.specification``
   * - ``TorsionDriveInput.input_specification``
     - ``.specification.specification.specification``
   * - ``result.final_energies``
     - ``result.scan_properties[grid].return_energy``
   * - ``result.optimization_history``
     - ``result.scan_results`` *(protocol-controlled)*
   * - ``success: bool`` / ``error``
     - ``success`` fixed ``true``; failures via ``qcschema_failed_operation``

v1 had no torsion-drive specification layer; it hung a ``QCInputSpecification``
and an ``OptimizationSpecification`` off the input side by side. v2 replaces both
with a single nested chain — see :doc:`../user_guide/torsion_drive`.


.. _behavioural-changes:

Behavioural changes
===================

**Serialization emits all fields.** v1 skipped *unset* fields; v2 emits
everything, with five objects excepted that omit *null* values: ``Molecule``,
``AtomicProperties``, ``WavefunctionProperties``, ``OptimizationProperties``, and
``ManyBodyProperties``.

The two rules select different keys, so pipelines that serialize, edit the result,
and reconstruct — a common way to build an ionized molecule from a neutral one —
can behave differently than they did under v1.

**Unknown fields are errors.** v2 objects forbid keys the specification does not
define, so a misspelled key is reported rather than silently dropped. The
exceptions are ``provenance`` and ``model``, which permit extra keys. This is
stricter than v1 and deliberately so — a typo'd convergence threshold that is
quietly ignored produces a wrong answer that looks right.

**Protocol defaults keep less data.** Beyond the optimization trajectory change
above, be aware that ``wavefunction`` and ``native_files`` both default to
``none``. See :doc:`protocols`.

**Shapes are validated.** A gradient or Hessian without ``calcinfo_natom`` cannot
be checked and should be refused rather than stored in an uninterpretable shape.


Converting payloads
===================

Do not map fields by hand. The moves above are mostly mechanical, but the lossy
ones are not the ones you would guess — use whatever conversion routine your
library provides.

.. important::

   Convert at the **Input** or **Result** level, never a bare specification.
   Because fields move *between* the input and the specification across versions,
   converting an ``AtomicSpecification`` alone has nowhere to put ``protocols`` or
   ``program`` and loses them; converting the whole ``AtomicInput`` preserves them.

Where conversion loses information
----------------------------------

**v1 → v2 results.** v1 has one molecule and one ``extras`` where v2 has two of
each. On up-conversion the molecule has to be duplicated into both slots and the
extras assigned to one of them, unless the converter is separately told what the
original input was.

**v2 → v1 results.** The two ``extras`` dictionaries must be merged into v1's
single one; by convention the result wins on key collisions.

**v2 → v1 optimizations and torsion drives.** The v2 defaults keep no trajectory
or scan history, so there is nothing to fill v1's ``trajectory`` (whose default was
``all``). If you plan to down-convert, run with ``trajectory_results="all"`` and
``scan_results="all"``.


Supporting both versions at once
================================

.. danger::

   **Do not mix versions within one object graph.** A v2 molecule does not belong
   inside a v1 input. Beyond being meaningless, some implementations cannot
   represent such a hybrid at all. Plan to overhaul your QCSchema handling in one
   go rather than migrating file by file.

The pattern that works — normalize inward at the boundary, work in one version
internally, convert back on the way out:

.. code-block:: text

   ┌─ schema wrapper (accepts v1 or v2) ─────────────────────────┐
   │  1. inspect schema_name / schema_version                    │
   │  2. build the corresponding v1 or v2 object                 │
   │  3. convert it to v2            ← normalize at the boundary │
   │  4. ---- all internal code is v2 only ----                  │
   │  5. convert the result back to the requested version        │
   │  6. return                                                  │
   └─────────────────────────────────────────────────────────────┘

The default convention across the ecosystem is **version-in-is-version-out** — the
version you were handed is the version you return — with an explicit override for
callers that want something specific.

Whichever library you use, parametrize your tests over both versions rather than
testing one and hoping.


Checklist
=========

.. list-table::
   :widths: 6 94
   :header-rows: 0

   * - ☐
     - Update ``schema_name`` and ``schema_version`` on every object; v2 rejects v1
       markers rather than coercing them.
   * - ☐
     - Move ``driver`` / ``model`` / ``keywords`` / ``protocols`` / ``extras``
       accesses under ``.specification``.
   * - ☐
     - Move result-side input accesses under ``.input_data``.
   * - ☐
     - Split the two molecules: submitted frame in ``input_data.molecule``, result
       frame at the top level.
   * - ☐
     - Stop emitting or expecting ``success: false`` results; emit and handle
       ``qcschema_failed_operation`` instead.
   * - ☐
     - Set ``trajectory_results`` and ``scan_results`` explicitly if you relied on
       v1 protocol defaults.
   * - ☐
     - Read optimization summary values from ``properties`` rather than trajectory
       list indices.
   * - ☐
     - Rename ``AtomicResultProperties`` → ``AtomicProperties``,
       ``AtomicResultProtocols`` → ``AtomicProtocols``, ``QCInputSpecification`` →
       ``AtomicSpecification``, ``TDKeywords`` → ``TorsionDriveKeywords``.
   * - ☐
     - Stop stripping unset fields when serializing across a process boundary — it
       removes ``schema_name`` and ``schema_version``.
   * - ☐
     - Check for keys your code passes that v2 now forbids; they used to be
       ignored, and are now errors.

.. seealso::

   :doc:`software_status`
      Which packages speak which version, and library-specific notes.

   :doc:`../development_guide/design_decisions`
      Why the v2 layout is shaped the way it is.
