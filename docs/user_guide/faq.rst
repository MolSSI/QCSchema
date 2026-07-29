==========================
Frequently asked questions
==========================

.. contents:: Questions
   :local:
   :depth: 1


Will the JSON be validated before it reaches my software?
=========================================================

That is up to the producers and consumers in your particular pipeline — QCSchema
is a format, and nothing enforces it in transit. Validating on receipt is
strongly recommended, and validation is available in a wide range of languages
through the `JSON Schema implementations list
<https://json-schema.org/implementations.html>`_.

The practical answer in most languages is to hand the payload to a library that
models the schema, since validation then happens as a side effect of
construction:

.. code-block:: python

   atomic_input = AtomicInput(**payload)   # raises on invalid payloads

See :doc:`../implementation_guide/validation`.


Does the schema accept extra fields for my software's internal extensions?
==========================================================================

Yes, but in specific places rather than anywhere.

``extras``
   Free-form scratch space, present on specifications, inputs, results,
   molecules, and errors. This is the sanctioned home for data the specification
   does not describe.

``keywords``
   Program-specific input settings, never validated or standardized by QCSchema.

``provenance`` and ``model``
   These two objects permit arbitrary additional keys.

Everywhere else, an unrecognized key is an error rather than silently ignored
data. That is deliberate: a typo in a field name that vanishes quietly is a bad way
to lose a setting, and a silently-ignored convergence threshold produces a wrong
answer that looks right.


Are there libraries for writing QCSchema in *my* language?
==========================================================

JSON is language-agnostic and well supported in C, C++, Python, JavaScript, Rust,
Java, and so on, so in most languages you need nothing beyond your standard JSON
library plus this specification.

Libraries that model the schema — validating on construction and serializing to
conforming JSON — exist for Python today, and are listed under :ref:`ecosystem`.
None of them live in this repository yet; see
:doc:`../quickstart/the_schema_and_the_models`.

For Fortran and other languages without ergonomic JSON support, the practical
pattern used by several programs is to keep the JSON handling in a thin C or
Python shim at the boundary and pass plain arrays inward.


Why not use XML?
================

The ability to hand-write and tweak an input has been a sought-after property
throughout the project, and JSON's overall structure is viewed as simpler and
more intuitive than XML's. Since the schema is fully specified, a validator can
take JSON in and emit XML out if a consumer needs it.


What style is used for keys and indexing?
=========================================

- **Zero-indexed** arrays throughout. Atom index 0 is the first atom, and
  ``connectivity`` and ``fragments`` both use 0-indexed atom references.
- ``snake_case`` keys.
- Flat arrays for multidimensional data, reshaped by the consumer according to a
  documented shape.
- **Column-major** order for matrix quantities in the wavefunction block.


Is the schema versioned?
========================

Yes. Every object carries a ``schema_name``, and every top-level container also
carries a ``schema_version``. In v2 both are fixed values that are validated
strictly rather than coerced.

Version numbers are **per-object**, not global: while the family is called "v2",
``Molecule.schema_version`` is ``3``. Molecule's numbering has always run one
ahead of the family and this is intentional. See
:doc:`../implementation_guide/versioning`.


Why is ``geometry`` a flat list instead of a list of ``[x, y, z]``?
===================================================================

Serialization and deserialization are substantially faster with fewer, larger
objects, and the flatter structure is generally easier to program against. The
trade-off was considered explicitly and is recorded in
:doc:`../development_guide/design_decisions`.

Reshape it to ``(nat, 3)`` on receipt and the flatness stops mattering.


Why does ``AtomicResult`` contain a molecule when ``input_data`` already has one?
=================================================================================

Because they are not necessarily the same molecule. With the default
``fix_com=false`` and ``fix_orientation=false``, a program may translate the centre
of mass to the origin and rotate to the inertial frame. Per-atom results such as
gradients belong to the *post-processing* frame, which is the top-level
``molecule``; ``input_data.molecule`` preserves what you submitted.

Carrying only one of the two would force a consumer to guess which frame a gradient
belongs to.


Why does the result not have an ``error`` field any more?
=========================================================

Because a result that might be a failure has to be treated as suspect
everywhere it is read. In v2, if an ``AtomicResult`` validates, its numbers are
present. Failures are :ref:`FailedOperation <model-failedoperation>` objects
carrying the error and the input that caused it. See :doc:`errors`.


My wavefunction/trajectory came back empty. Why?
================================================

Almost certainly a protocol default. The defaults keep as little as possible,
because these are the fields that dominate a record's size:

- ``protocols.wavefunction`` defaults to ``none`` — no orbitals or densities.
- ``protocols.native_files`` defaults to ``none`` — no program scratch files.
- ``protocols.trajectory_results`` defaults to ``none`` — no per-step results from
  an optimization.

Ask for what you need explicitly, at input time. Protocols cannot be applied
retroactively: a record written with the defaults has discarded that data, and the
only remedy is to run the computation again. See
:doc:`../implementation_guide/protocols`.


Is there a reference implementation?
====================================

Not in this repository — yet. These pages are the specification; a simplified set
of Python models alongside them is planned but does not exist today. When it
arrives it will cover the schema objects only, not molecule parsing, unit
conversion, or program drivers. See
:doc:`../quickstart/the_schema_and_the_models`.

In the meantime several packages read and write QCSchema — see :ref:`ecosystem`
and :doc:`../implementation_guide/software_status`.

If an implementation and this specification disagree, that is a bug in one of
them, and worth :doc:`reporting <../development_guide/contributing>` rather than
assuming either side is right.


Where is the machine-readable schema?
=====================================

This repository ships JSON Schema documents under ``qcschema/data/``, reachable
through a small helper:

.. code-block:: python

   import qcschema

   qcschema.validate(payload, "input")

Be aware that those files predate the layout described here — they still carry the
older ``qcschema_input`` naming. Aligning them is outstanding work. See
:doc:`../implementation_guide/validation` for what to do in the meantime.


I have QCSchema v1 payloads. What do I do?
==========================================

See :doc:`../implementation_guide/migrating_from_v1`, which collects the
field-by-field mapping, the renames, the changed protocol defaults, and the places
where conversion loses information.

The short version: use a conversion routine rather than mapping fields by hand,
convert at the input or result level rather than a nested specification, and do not
mix the two versions within one object graph.
