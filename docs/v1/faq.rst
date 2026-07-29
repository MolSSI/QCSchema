==========================
Frequently asked questions
==========================

Answers as they applied to QCSchema v1. Most of these carry over to v2 unchanged;
where they do not, the v2 answer is in the :doc:`v2 FAQ </user_guide/faq>`.


Will the JSON be validated before it reaches my software?
=========================================================

That is a question for the producers and consumers of the schema. It is certainly
recommended to validate, and validation can be accomplished in a variety of
languages — see the
`JSON Schema implementations list <https://json-schema.org/implementations.html>`_.


Does the schema accept arbitrary extra fields if my software needs internal extensions?
=======================================================================================

Yes. ``keywords`` is the intended home for program-specific input settings and is
never validated by the schema, and ``extras`` is available as free-form scratch
space. v1 was generally permissive about additional fields; v2 tightened this, so
do not rely on unknown keys surviving a round-trip through newer tooling.


Are there libraries for writing the schema in *my* language?
============================================================

JSON is agnostic to the underlying programming language and is well supported in a
variety of languages — C, C++, Python, JavaScript, and others. For languages where
JSON support is less ergonomic, such as Fortran, the practical pattern is to keep
the JSON handling in a thin shim at the boundary and pass plain arrays inward.


Why not use XML?
================

The ability to hand-write and tweak a given input has been a sought-after property.
In addition, the overall structure of JSON is viewed as simpler and more intuitive
than XML. As the schema is fully specified, it is possible for a validator to take
in a JSON input and return an XML output.


What style is used for indexing and case?
=========================================

Zero-indexing for arrays and ``snake_case`` for keys. Multidimensional data is
stored flat and reshaped by the consumer, and matrix quantities in the wavefunction
block are column-major.


Is the schema versioned?
========================

Yes. ``schema_name`` and ``schema_version`` appear on the input and output objects
and on the molecule, so that the schema can evolve over time. QCSchema v2 is the
current version; see :doc:`/index`.

Note that in v1 the markers were leniently validated: ``qcschema_input`` and
``qc_schema_input`` were both accepted by regex, and an output object would accept
an *input* schema name and coerce it. Do not rely on this — v2 rejects both.


Why is ``geometry`` a flat list instead of a list of ``[x, y, z]``?
===================================================================

Serialization and deserialization are faster with fewer, larger objects, and the
flatter structure is generally easier to program against. Reshape to ``(nat, 3)``
on receipt.
