===========================
The schema and the models
===========================

QCSchema is two things that are easy to conflate, and these docs keep them apart
deliberately.


The schema
==========

The schema is a set of **object definitions**: which fields exist, what types
they hold, which are required, what units they are in, what shape their arrays
have, and what obligations a producer and a consumer take on. It is described in
prose and JSON, and it is language-neutral.

That is what this repository is for, and what the rest of these docs describe.
The :doc:`user guide <../user_guide/index>` is the field-by-field reference; the
:doc:`implementation guide <../implementation_guide/index>` is the set of rules
your code has to follow.

A conforming QCSchema document is plain JSON. Nothing needs to be installed to
write one:

.. code-block:: json

   {
     "schema_name": "qcschema_molecule",
     "schema_version": 3,
     "symbols": ["He"],
     "geometry": [0.0, 0.0, 0.0]
   }

This repository additionally ships JSON Schema documents for validation, with a
small helper to reach them:

.. code-block:: python

   import qcschema

   qcschema.validate(payload, "input")
   qcschema.list_versions("molecule")

.. warning::

   Those files predate the layout described in these docs — they still carry the
   older ``qcschema_input`` naming. Aligning them is outstanding work, so do not
   treat them as a validator for the current schema yet. See
   :doc:`../implementation_guide/validation` for what to do in the meantime.


The models
==========

A *model* is one language's convenient representation of a schema object — a
Python class, say, that validates on construction and serializes to conforming
JSON. Models are enormously useful. They are not the specification.

Simplified Python models for the v2 objects are planned to live in this
repository. **They do not exist yet.** When they arrive:

- They will cover the schema objects and their validation, and gain an API
  reference section in these docs.
- They will **not** bring the surrounding conveniences with them. In particular,
  no molecule-format parsing, no unit conversion or physical constants, no
  database or identifier lookup, and no drivers for quantum chemistry programs.
  Those are real needs, but they are separate packages' business, not the
  schema's.

That boundary matters when reading examples here. If a snippet shows something
being *constructed*, it is illustrating schema structure. If you find yourself
wanting something to *parse an XYZ file*, convert Ångström to Bohr, or run a
computation, that is outside the scope of this project — see :ref:`ecosystem`.

.. note::

   Because there is no implementation here yet, the Python tabs in these docs omit
   their import lines. Class names mirror the schema object names —
   ``qcschema_atomic_input`` is ``AtomicInput`` — so the snippets read the same
   whichever library you use them with. See :ref:`tab_convention`.


Which do I need?
================

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - You want to
     - What you need
   * - Understand what a field means
     - The :doc:`user guide <../user_guide/index>`. Nothing installed.
   * - Write a document by hand
     - A text editor. Mind the units — see
       :doc:`../implementation_guide/conventions`.
   * - Emit or read QCSchema from a program
     - A JSON library, plus the
       :doc:`implementation guide <../implementation_guide/index>`.
   * - Validate documents
     - A `JSON Schema validator
       <https://json-schema.org/implementations.html>`_ and a schema document.
       See :doc:`../implementation_guide/validation`.
   * - Work with QCSchema objects in Python today
     - An external library — see :ref:`ecosystem` and
       :doc:`../implementation_guide/software_status`.
   * - Actually run computations
     - A quantum chemistry program, or a driver that wraps several. Out of scope
       here; see :ref:`ecosystem`.


Building these docs
===================

.. code-block:: console

   $ pip install -e ".[docs]"
   $ cd docs && make html

Output lands in ``docs/_build/html``. The build introspects no code — every field
table is hand-written — so Sphinx and the theme are the only requirements.
