.. _validation:

==========
Validation
==========

QCSchema is worth having only if payloads can be checked. This page covers what
"valid" actually means — which is more than field types — and how to check it.


Three kinds of validation
=========================

**Structural** — are the required fields present, are the types right, is
``schema_name`` the value it claims to be? Any JSON Schema validator does this.

**Shape** — does ``geometry`` have :math:`3N` entries for :math:`N` symbols? Is
the gradient castable to ``(nat, 3)``? Does each row of ``coefficients`` match the
length of ``exponents``? Some of this is expressible in JSON Schema and some is
not.

**Physical** — do any two atoms overlap? Is the multiplicity feasible for the
electron count? Do the fragment charges sum to the molecular charge? This is not
expressible in JSON Schema at all.

A generic JSON Schema validator gives you the first and part of the second. The
rest you either write yourself or get from a library that models the schema.

A conforming implementation should perform all three before running a
computation. Which of them a *consumer* of results needs depends on how much it
trusts the producer.


Validating with a schema library
================================

The least work is to hand the payload to a library that models QCSchema, since
validation then happens as a side effect of construction — there is no separate
validation step:

.. code-block:: python

   try:
       atomic_input = AtomicInput(**payload)
   except ValidationError as exc:
       print(exc)

.. note::

   There is no such library in this repository yet; see
   :doc:`../quickstart/the_schema_and_the_models`, and
   :doc:`software_status` for what exists elsewhere.

Errors name the offending path, which is what you want when the problem is six
levels down:

.. code-block:: text

   1 validation error for AtomicInput
   specification.driver
     Input should be 'energy', 'gradient', 'hessian' or 'properties'
     [type=enum, input_value='optimization']

Molecules are a special case, because physical validation is expensive enough to
be worth skipping on data you already trust. That is what the ``validated`` field
is for: when it is ``true``, a consumer may take the physics on faith and check
only the layout.

.. warning::

   Trust ``validated: true`` only from a source you control — your own
   constructor, your own database, or a payload you serialized yourself. Taking it
   on faith from outside means overlapping atoms and impossible multiplicities
   reach your program unchallenged. When in doubt, re-validate; it is cheap
   relative to the computation you are about to run.


Getting a JSON Schema document
==============================

This repository ships JSON Schema documents and a small helper to reach them:

.. code-block:: python

   import qcschema

   qcschema.validate(payload, "input")
   qcschema.get_schema("molecule", version=2)
   qcschema.list_versions("molecule")

.. warning::

   Those files predate the layout described in these docs — they still carry the
   older ``qcschema_input`` naming. Bringing them in line is outstanding work, so
   do not treat them as a validator for the current schema yet.

Until they are updated, there are two ways to get a machine-readable description
of v2:

**Write it from these pages.** The field tables in the
:doc:`user guide <../user_guide/index>` give the field names, JSON types,
requiredness, and shapes for each object, which is what a JSON Schema document
needs. This is the route to take if you want a schema you control.

**Export it from a library that models the schema.** Anything built on a modelling
framework can usually emit a JSON Schema document for each object; do that as a
build step and ship the output alongside your program.

Check the result against these pages before relying on it, though. An exported
schema reflects one library's modelling choices as much as the specification —
optional-versus-nullable, how unions are expressed, whether numeric strings are
accepted for basis exponents — and those choices are not all normative.


Outside Python
==============

Feed a generated schema to any validator from the
`JSON Schema implementations list <https://json-schema.org/implementations.html>`_.
For example, in JavaScript:

.. code-block:: javascript

   import Ajv from "ajv";

   const ajv = new Ajv({strict: false});
   const validate = ajv.compile(atomicInputSchema);

   if (!validate(payload)) {
       console.error(validate.errors);
   }

What a generic validator will *not* catch:

- ``geometry`` length not :math:`3 \times` the ``symbols`` length
- gradients not reshapable to ``(nat, 3)``
- ``atom_map`` referring to a label absent from ``center_data``
- ``nbf`` disagreeing with the shell data
- a wavefunction primary-return pointer naming a field that is not present
- overlapping atoms, or a multiplicity impossible for the electron count
- fragment charges not summing to the molecular charge

Unless your schema library covers them, write those checks by hand. They are the
ones that catch real bugs.


Validate what your program guarantees
=====================================

Structural validity is not the same as *supported*. A payload can be perfectly
valid and still ask for something you cannot do. Check for these explicitly and
report an ``input_error``:

.. code-block:: python

   spec = atomic_input.specification

   if spec.driver not in SUPPORTED_DRIVERS:
       raise InputError(f"{spec.driver} not supported")

   if spec.model.method.upper() not in SUPPORTED_METHODS:
       raise InputError(f"unknown method {spec.model.method}")

   if isinstance(spec.model.basis, BasisSet) and not SUPPORTS_CUSTOM_BASIS:
       raise InputError("custom basis sets not supported")

   if atomic_input.molecule.molecular_multiplicity != 1 and not SUPPORTS_OPEN_SHELL:
       raise InputError("open-shell references not supported")

Failing loudly here is the whole point. The alternative — running something
adjacent to what was asked for — produces a number that will be believed.


Four rules a validator must not relax
=====================================

**Schema markers are fixed values.** ``schema_name`` and ``schema_version`` have
exactly one legal value per object. Reject an unrecognized or mismatched marker
rather than coercing it; a validator that rewrites a wrong name has told you
nothing. See :doc:`versioning`.

**Unknown fields are errors.** Objects forbid keys the specification does not
define, so a misspelled key must be reported rather than dropped. The exceptions
are ``provenance`` and ``model``, which permit extra keys.

**Shapes must be checkable.** A gradient without ``calcinfo_natom`` cannot be
validated at all, and should be refused rather than stored in a shape nobody can
interpret.

**Protocols are a guarantee, not a request.** A wavefunction supplied against a
``none`` protocol must not appear in the result. That is what allows a consumer to
trust that a record contains what its protocols say it contains.
