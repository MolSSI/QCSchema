=================
Design decisions
=================

Questions that have been discussed and closed. Each one is recorded with the
alternatives, because the alternatives keep getting re-proposed.


Big arrays, not small objects
=============================

There are two ways to arrange data representing a collection of objects.

The **"big"** approach — one flat array per quantity:

.. code-block:: json

   {
     "symbols": ["C", "C"],
     "geometry": [0.000, 1.396, 0.000, 1.209, 0.698, 0.000],
     "masses": [12.017, 12.017]
   }

The **"small"** approach — a closer object mapping:

.. code-block:: json

   {
     "fields": ["symbols", "geometry", "masses"],
     "table": [
       ["C", [0.000, 1.396, 0.000], 12.017],
       ["C", [1.209, 0.698, 0.000], 12.017]
     ]
   }

**Decision: the "big" approach**, for three reasons:

- Serialization and deserialization are much faster, because far fewer objects are
  generated.
- The "small" approach tends toward a complex hierarchy of fields.
- The "big" approach is generally thought more straightforward to program against,
  because of its flatter structure.

The cost is that per-atom data is spread across several arrays that must be kept
in index correspondence — which is precisely why the atom-ordering contract in
:doc:`../implementation_guide/conventions` is stated as forcefully as it is.


JSON rather than XML
====================

The ability to hand-write and tweak a given input has been a sought-after property
of the format. Beyond that, JSON's overall structure is viewed as simpler and more
intuitive than XML's.

**Decision: JSON.** Because the schema is fully specified, it remains possible for
a validator to take a JSON input and return an XML representation for consumers
that need one, so nothing is foreclosed.


Zero-indexing and ``snake_case``
================================

**Decision:** zero-indexed arrays and ``snake_case`` keys throughout. Atom index 0
is the first atom, in ``connectivity``, in ``fragments``, and in torsion drive
``dihedrals`` alike.

The `Google JSON Style Guide
<https://google.github.io/styleguide/jsoncstyleguide.xml>`_ was considered, which
would have implied ``camelCase``. ``snake_case`` was chosen instead, matching the
conventions of the Python-dominated scientific ecosystem that consumes the format.


Object references by array index
================================

JSON does not support object references, which makes it non-trivial to maintain,
say, a list of bonds between atoms. Four options were on the table:

1. **By array index** — ``residue.atom_indices = [3, 4, 5, 6]``
2. **By JSON path reference** — see
   `draft-pbryan-zyp-json-ref <https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03>`_
3. **By JSON-LD**, which allows flexible referencing and would permit one document
   to be split into separately referenceable pieces
4. **By unique key** — ``residue.id = 'a83nd83'``,
   ``residue.atoms = ['a9n3d9', '31di3']``

**Decision: array index.** They are a little fragile, but no more fragile than
path references, and they require far less overhead than unique keys.

This is why ``connectivity`` is a list of index triples and ``fragments`` a list of
index lists.

.. note::

   This decision was made for atoms and bonds within one document. Referencing
   *across* documents — reusing data from a previous task in a workflow instead of
   repeating it — remains open. See :doc:`open_questions`.


Fixed units per field
=====================

**Decision:** every field has exactly one documented unit, and values carry no
unit tags. The units are atomic units throughout: Bohr, Hartree, and derived
quantities.

This keeps payloads small and comparison cheap, at the cost of making a whole class
of mistake silent — reading Ångström as Bohr produces a plausible number for the
wrong molecule. The alternatives, and the argument that this was the wrong call,
are in :doc:`open_questions`.


Specifications as first-class objects
=====================================

**Decision:** keep ``driver``, ``model``, ``keywords``, ``protocols``, and
``extras`` in a reusable ``*Specification`` object rather than on the input
directly, and let specifications nest.

The alternative — putting them on the input — made three things awkward:

- Describing "this level of theory" separately from any particular molecule
  becomes impossible, so a database storing a million computations at one level of
  theory repeats the description a million times.
- Each procedure ends up inventing its own field name for its sub-computation, so
  there is no general way to walk into a nested computation.
- There is nowhere to put a specification-level ``program`` field.

The cost is longer access paths — ``specification.model.method`` rather than
``model.method`` — and the mild awkwardness of a field named ``specification``
containing a field named ``specification``.


Results embed inputs rather than merging them
=============================================

**Decision:** a result *contains* its input, under ``input_data``, rather than
carrying the input's fields alongside its own.

Merging the two namespaces is more convenient to read — ``result.model.method``
rather than ``result.input_data.specification.model.method`` — but it allows only
one value per concept. The breaking case is ``molecule``: a program that reorients
has both an input frame and a result frame, and both matter to a consumer trying to
interpret a gradient. ``extras`` has the same problem in milder form, where a
driver's annotations and the program's would collide.

The cost is verbosity at every access site.


Failure as a distinct type
==========================

**Decision:** result objects have ``success`` fixed to ``true`` and no ``error``
field; failures are :ref:`FailedOperation <model-failedoperation>` objects.

Allowing ``success: false`` on a result means every field on every result is
conditionally present, and every consumer has to defend against that everywhere.
Making it a type distinction moves the check to one place: if a result validates,
its numbers are there.

The cost is that a producer must construct a different object on the failure path,
and that ``FailedOperation.input_data`` has to be untyped — a payload that failed
*because it was malformed* cannot be validated as any input object.

.. note::

   This decision was made with an explicit invitation for feedback: if you have a
   use case that the split breaks — somewhere a partially-populated result was
   genuinely the right thing — that is worth
   :doc:`reporting <contributing>`.
