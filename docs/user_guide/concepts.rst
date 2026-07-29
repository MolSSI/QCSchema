.. _concepts:

==================
Concepts & layout
==================

QCSchema is built from a small number of ideas applied consistently. Learn these
five and the rest of the specification is largely mechanical.

.. contents:: On this page
   :local:
   :depth: 1


1. Molecule, Specification, Input, Result
=========================================

Four roles account for nearly every object in the schema.

**Molecule** — what to compute on
   The closest representation to the real physical nature of the system: for
   molecular sciences, coordinates plus elements. It may also carry bonding,
   fragmentation, charges, and masses. For both QM and MM, this is your molecule.
   It is the foundation on which the model of the calculation is built.

**Specification** — how to compute it
   The method, basis, driver, program-specific keywords, and output-retention
   protocols. Deliberately says nothing about the system, so one specification
   is reusable across many molecules.

**Input** — a molecule plus a specification
   A complete, runnable request.

**Result** — the input plus what came out
   Properties, the primary return value, provenance, and optionally the
   wavefunction and program logs.

.. code-block:: text

   AtomicInput
   ├── molecule           ── qcschema_molecule
   └── specification      ── qcschema_atomic_specification
       ├── driver
       ├── model          ── method + basis
       ├── keywords
       └── protocols

   AtomicResult
   ├── input_data         ── the whole AtomicInput above
   ├── molecule           ── result frame (may differ from input frame)
   ├── properties         ── qcschema_atomic_properties
   ├── return_result      ── the primary answer
   ├── wavefunction       ── optional, protocol-controlled
   └── provenance


2. Specifications nest
======================

A geometry optimization needs gradients; a torsion drive needs optimizations.
Rather than inventing new fields for each layer, v2 nests specifications inside
one another, always under the field name ``specification``:

.. code-block:: text

   TorsionDriveSpecification        how to scan dihedrals
   └── specification: OptimizationSpecification    how to optimize
       └── specification: AtomicSpecification      how to get a gradient

Reading a deeply nested payload becomes a matter of walking down that chain:

.. code-block:: text

   specification.keywords                                torsion drive keywords
   specification.specification.program                   the optimizer
   specification.specification.specification.model       the gradient method

The field is always called ``specification``, at every level, so walking into a
nested computation does not require knowing which procedure you are looking at.


3. Results contain their inputs
===============================

A result **embeds** the input that produced it, under ``input_data``. Reading back
what was asked for therefore means walking through it:

.. code-block:: text

   input_data.specification.model.method     what was requested
   properties.return_energy                  what came out

The access path is longer than it would be if the fields were merged, and that
buys two things:

- A result is a complete, self-contained record. Store one object and you have the
  full trace from request to answer — which is exactly what a large-scale database
  of computations needs.
- Input and result can hold *different* values for the same concept. The clearest
  case is ``molecule``: ``input_data.molecule`` is the frame that was submitted,
  while the top-level ``molecule`` is the frame the results are expressed in. After
  a program recentres or reorients, these genuinely differ, and both matter.
  ``extras`` splits the same way, so a driver's annotations are not overwritten by
  the program's.


4. Success is a type, not a flag
================================

A v2 result object always describes a successful computation:
``AtomicResult.success`` is fixed to ``true`` and there is no ``error`` field at
all. A failure is a :ref:`FailedOperation <model-failedoperation>`, whose
``success`` is fixed to ``false`` and which carries the error and the input that
provoked it.

Both objects have a ``success`` field, so a consumer can branch on it before
knowing which type it holds — but a validator will reject a result claiming to be
a failure, and vice versa.

.. seealso:: :doc:`errors`


5. Every object announces itself
================================

``schema_name`` is present on essentially every object, and ``schema_version`` on
every top-level container. Both are fixed values, validated strictly: a payload
whose marker does not match the object it claims to be must be rejected, not
coerced into shape.

This is what makes heterogeneous storage tractable. Given an anonymous blob of
JSON, ``schema_name`` tells you what it is and which rules to apply.

.. seealso:: :doc:`../implementation_guide/versioning`


Flat arrays and "big" layout
============================

QCSchema stores collections as parallel flat arrays keyed by quantity, not as
lists of per-atom objects:

.. code-block:: json

   {
     "symbols": ["C", "C", "H"],
     "geometry": [0.0, 1.396, 0.0, 1.209, 0.698, 0.0, 2.418, 1.396, 0.0],
     "masses": [12.011, 12.011, 1.008]
   }

rather than

.. code-block:: json

   {
     "atoms": [
       {"symbol": "C", "xyz": [0.0, 1.396, 0.0], "mass": 12.011}
     ]
   }

Index :math:`i` of every per-atom array refers to the same atom. Multidimensional
arrays are stored flat and reshaped by the consumer according to a documented
shape — ``geometry`` is ``(nat, 3)``, a Hessian is ``(3*nat, 3*nat)``, and matrix
quantities in the wavefunction block are **column-major**.

The reasoning behind this choice, and the alternative that was rejected, is
recorded in :doc:`../development_guide/design_decisions`.


Units are fixed, not tagged
===========================

QCSchema does not carry units alongside values. Instead each field has one
documented unit, and it is atomic units throughout:

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Quantity
     - Unit
     - Notes
   * - Coordinates
     - :math:`a_0`
     - Bohr, **not** Ångström
   * - Energy
     - :math:`E_h`
     - Hartree
   * - Gradient
     - :math:`E_h/a_0`
     -
   * - Hessian
     - :math:`E_h/a_0^2`
     -
   * - Dipole moment
     - :math:`e\,a_0`
     - not Debye
   * - Quadrupole moment
     - :math:`e\,a_0^2`
     -
   * - Mass
     - u
     - unified atomic mass units

Whether units *should* be tagged rather than fixed is a question the project has
considered and not closed; see
:doc:`../development_guide/open_questions`.


Extension points
================

Two mechanisms let you carry information the specification does not describe:

``keywords``
   Program-specific input settings. QCSchema does not standardize these and does
   not validate them — ``{"scf_type": "df"}`` means whatever the target program
   says it means. This is the intended home for everything that varies by code.

``extras``
   Free-form scratch space for schema development and for annotations a driver
   wants to carry alongside a computation. Present on specifications, inputs,
   results, molecules, and errors.

Most objects otherwise **forbid** unknown fields: a key the specification does
not define is an error, not silently ignored data. The exceptions are
:ref:`Provenance <model-provenance>` and :ref:`Model <model-model>`, which permit
extra keys.
