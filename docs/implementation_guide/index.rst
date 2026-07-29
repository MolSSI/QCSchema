.. _implementation_guide:

============================
Schema Implementation Guide
============================

This section is for people adding QCSchema support to software: a quantum
chemistry program, an optimizer, a database, a visualizer, or a workflow tool.
The :doc:`user guide <../user_guide/index>` says what the fields mean; this
section says what your code is obliged to do about them.

.. note::

   Everything on these pages is part of the specification and applies in any
   language. Where a snippet is shown in Python, it is pseudocode illustrating the
   rule — class names mirror the schema object names, and import paths are omitted
   because there is no implementation in this repository yet. See
   :doc:`../quickstart/the_schema_and_the_models`.

.. toctree::
   :maxdepth: 2

   conventions
   consuming
   producing
   protocols
   validation
   versioning
   migrating_from_v1
   software_status


The short version
=================

If you read nothing else on these pages:

.. card:: Coordinates are Bohr

   ``Molecule.geometry`` is in :math:`a_0`, stored flat as :math:`3N` numbers.
   Energies are :math:`E_h`. Nothing carries a unit tag; the unit is fixed per
   field. :doc:`conventions`

.. card:: Atom order is a contract

   If you reorder, translate, or rotate atoms internally, you must not attach the
   original molecule to the resulting per-atom, origin-sensitive, or
   frame-sensitive output. Return the frame your results actually belong to.
   :doc:`conventions`

.. card:: Emit less than you can

   Wavefunctions and scratch files are opt-in through protocols, and the defaults
   are ``none``. Honour them — they are what keeps records storable.
   :doc:`protocols`

.. card:: Stamp everything

   Every object gets a ``schema_name``; top-level containers get a
   ``schema_version``. Fill in ``provenance`` with your program name and version.
   :doc:`versioning`

.. card:: Fail with the right object

   A result object means success. Failures are ``FailedOperation``, with a short
   ``error_type`` classifier and the input that caused the problem.
   :doc:`../user_guide/errors`


Coming from QCSchema v1?
========================

These pages describe v2 only. If you have existing v1 payloads or v1 code, start
with :doc:`migrating_from_v1` — it collects the field-by-field mapping, the
renames, the protocol defaults that changed, and the places where conversion
loses information.


Do you need to write this yourself?
===================================

Probably not all of it. Before implementing a QCSchema interface from scratch,
consider:

**An adaptor may already cover your program.**
   Driver packages exist that wrap a QC program's existing text or Python
   interface and present it as QCSchema, without the program itself learning the
   format. Writing a harness for one of those is usually less work than a native
   interface, and version negotiation comes for free. See :ref:`ecosystem`.

**A library can do the validation.**
   Do not hand-roll validation logic if a library for your language already models
   the schema — construction then validates types, shapes, physics, and protocols
   in one step. See :doc:`../implementation_guide/software_status`.

**A native interface is worth it when** you want to skip the text round-trip
entirely, expose wavefunctions efficiently, or you are writing something that is
not a QC program — a database, a visualizer, a workflow engine.


The two halves of an interface
==============================

A program-side QCSchema interface has a natural shape, and nearly every
implementation converges on it:

.. code-block:: text

   JSON in ──▶ validate ──▶ convert to internal form ──▶ RUN
                                                          │
   JSON out ◀── stamp & protocol-filter ◀── collect ◀──────┘

The two edges are documented separately: :doc:`consuming` for the inbound half,
:doc:`producing` for the outbound half.

The pattern that has worked for QCEngine, Psi4, and others is to **convert to v2
at the boundary and use v2 internally**, accepting either version at the interface
and converting back on the way out. :doc:`versioning` describes this in detail.
