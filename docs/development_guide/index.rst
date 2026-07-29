.. _development_guide:

=========================
Schema Development Guide
=========================

This section is about the specification itself: what it is trying to achieve,
which design questions have been settled and why, which remain open, and how to
propose a change.

If you are using QCSchema rather than developing it, you want the
:doc:`user guide <../user_guide/index>` or the
:doc:`implementation guide <../implementation_guide/index>`.

.. toctree::
   :maxdepth: 2

   goals
   design_decisions
   open_questions
   prior_art
   contributing


Scope
=====

QCSchema aims to describe **quantum chemistry computations** — a system, a method,
and the results of applying one to the other — completely enough that the record
can substitute for the program's own output.

It deliberately does not attempt to be:

- **A program-agnostic input language.** Method and keyword names are not a
  controlled vocabulary. ``keywords`` is explicitly a pass-through, and
  normalizing ``B3LYP`` across programs is the adaptor layer's job.
- **A general chemical file format.** There are good ones already; QCSchema's
  molecule exists to support computations, not to replace SDF or CIF.
- **A units system.** Each field has one fixed unit. See
  :doc:`open_questions` for the case against this choice.
- **A workflow description.** Composition of computations belongs to workflow
  tools; QCSchema describes the pieces they compose.

The line is worth keeping in mind when proposing additions. "Where does this
belong?" is usually answerable from the list above.


How the specification evolves
=============================

This repository holds the specification. Three kinds of artifact live alongside
each other, and they do not currently move at the same speed:

**These documents** — the specification
   The normative description of QCSchema v2: objects, fields, units,
   conventions, and obligations on producers and consumers. Hand-written, and the
   thing a change to the schema needs to land in.

**The JSON Schema files** in ``qcschema/data/``
   Machine-readable validation documents. Hand-maintained and currently well
   behind the prose — they still carry the older ``qcschema_input`` naming.
   Bringing them in line is outstanding work.

**Implementations** — in other repositories, for now
   Packages that read and write QCSchema; see
   :doc:`../implementation_guide/software_status`. A simplified implementation of
   v2 inside *this* repository is planned but does not exist yet. When it lands,
   these docs will gain an API reference section generated from it, and the field
   tables in the :doc:`user guide <../user_guide/index>` will be able to be
   generated rather than hand-maintained.

Until then, a schema change means editing these pages, and a change that also
affects validation means editing the JSON Schema files.

.. note::

   Historically the schema was documented largely by whichever implementation was
   furthest ahead, which made it hard to tell what was normative and what was one
   package's choice. These pages are an attempt to fix that: where they and any
   particular implementation disagree, that is a bug in one of them, and worth
   :doc:`reporting <contributing>`.

.. seealso:: :doc:`contributing`
