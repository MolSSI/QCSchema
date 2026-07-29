.. _versioning:

==========
Versioning
==========

QCSchema is versioned so that it can change without breaking everything that
reads it. This page covers what the version markers mean and what your code
should do with them.

.. note::

   Migrating existing v1 payloads or v1 code is covered separately, on
   :doc:`migrating_from_v1`.


The markers
===========

Every object carries a ``schema_name``. Every top-level container — the kind of
object you would send or store on its own — also carries a ``schema_version``.

.. code-block:: json

   {
     "schema_name": "qcschema_atomic_input",
     "schema_version": 2,
     "molecule": {
       "schema_name": "qcschema_molecule",
       "schema_version": 3,
       "...": "..."
     },
     "specification": {
       "schema_name": "qcschema_atomic_specification",
       "...": "..."
     }
   }

Note that the nested molecule carries its own markers, and that its version
number differs from the enclosing input's.

``schema_name`` is what makes heterogeneous storage tractable: given an anonymous
blob of JSON, it tells you what the object is and which rules apply. Read it
before you parse anything else, and do not infer the type from which fields happen
to be present. See :doc:`consuming`.


Version numbers are per-object
==============================

.. important::

   **The numbers are per-object, not global.** The family as a whole is called
   "v2", but the objects within it are numbered independently:

   .. list-table::
      :widths: 50 15 35
      :header-rows: 1

      * - Object
        - Version
        - Note
      * - ``qcschema_molecule``
        - **3**
        - Runs one ahead of the family, and always has
      * - ``qcschema_basis_set``
        - **2**
        -
      * - ``qcschema_atomic_input``
        - **2**
        -
      * - ``qcschema_atomic_result``
        - **2**
        -
      * - ``qcschema_optimization_input``
        - **2**
        -
      * - ``qcschema_optimization_result``
        - **2**
        -
      * - ``qcschema_torsion_drive_input``
        - **2**
        -
      * - ``qcschema_torsion_drive_result``
        - **2**
        -
      * - ``qcschema_failed_operation``
        - **2**
        -

   The molecule's offset is historical: the molecule schema was versioned before
   the family was. It is kept rather than renumbered, because renumbering would
   invalidate every stored molecule in existence. It is not a mistake, and not
   something to correct.

Objects that are always embedded in a parent carry a ``schema_name`` but **no**
``schema_version`` — they are versioned along with whatever contains them. That
covers the specifications, the properties and protocols objects, and small objects
such as ``provenance`` and ``model``. The full list is in the
:doc:`object index <../user_guide/index>`.


Both markers are fixed values
=============================

``schema_name`` and ``schema_version`` are not free-form. Each object has exactly
one legal value for each, and a conforming consumer validates them strictly rather
than coercing what it is given.

That means:

- A payload whose ``schema_name`` is unrecognized, or is the name of a *different*
  object, must be rejected. Do not, for example, accept an input's name on a result
  and quietly rewrite it.
- A payload whose ``schema_version`` does not match the ``schema_name`` it claims
  must be rejected.
- Neither marker should ever be omitted. This is why you should not strip unset or
  default-valued fields when serializing across a process boundary — see
  :doc:`conventions`.

Being strict here is what makes the markers worth trusting at all. A validator that
coerces a wrong name has told you nothing about the payload.


Negotiating versions with callers
=================================

If your software supports more than one version of the schema, the convention
across the ecosystem is **version-in-is-version-out**: the version you were handed
is the version you return, unless the caller explicitly asks for something else.

Internally, pick one version and normalize to it at the boundary:

.. code-block:: text

   ┌─ schema wrapper ────────────────────────────────────────────┐
   │  1. inspect schema_name / schema_version                    │
   │  2. normalize to the version you work in                    │
   │  3. ---- all internal code speaks one version ----          │
   │  4. convert the result back to the requested version        │
   │  5. return                                                  │
   └─────────────────────────────────────────────────────────────┘

Do not attempt to mix versions within a single object graph. Beyond being
meaningless, some implementations cannot represent such a hybrid at all.

.. seealso::

   :doc:`migrating_from_v1`
      Field-by-field mapping, conversion pitfalls, and a migration checklist.

   :doc:`software_status`
      Which packages speak which version.


How the schema will change
==========================

What a version bump does and does not imply:

**Adding an optional field is not a version bump.** New optional fields — a new
property name, say — can appear within a version. Track the specification rather
than pinning to a fixed field list, and do not treat an unfamiliar optional field
as fatal in a payload that is otherwise valid.

**Renames, retypes, and default changes are.** Anything that would make a
previously valid payload invalid, or that changes the meaning of an existing
field, belongs in a new version.

**Version numbers are integers and only move forward.** There is no minor version,
and no ordering beyond "later is newer".

To propose a change, see :doc:`../development_guide/contributing`.
