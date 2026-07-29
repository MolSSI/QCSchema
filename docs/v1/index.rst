.. _v1_index:

===========
QCSchema v1
===========

.. attention::

   **This documents QCSchema v1, which has been superseded by**
   :doc:`QCSchema v2 </index>`.

   It is kept for reference: a great deal of data and a number of programs still
   speak v1, and you may well need to read a v1 payload. New work should target
   v2, and these pages are deliberately less detailed than the v2 specification.

   Use the version dropdown in the header to switch between them.

QCSchema v1 is a JSON representation of a quantum chemistry computation. Its
purpose — unchanged in v2 — is to provide API-like access to existing workhorse
quantum chemistry packages, so that output variables, vectors, and matrices can be
read directly instead of being scraped out of ASCII output files.

.. toctree::
   :maxdepth: 2

   specification
   examples
   faq


The shape of a v1 payload
=========================

A v1 computation is described by two objects, and they are **flat**: the fields
describing how to run the computation sit directly on the input, and the result
carries those same fields alongside its own.

.. code-block:: text

   qcschema_input                  schema_version: 1
   ├── molecule                    qcschema_molecule, schema_version 2
   ├── driver                      energy | gradient | hessian | properties
   ├── model                       { method, basis }
   └── keywords                    program-specific settings

   qcschema_output                 schema_version: 1
   ├── molecule, driver, model, keywords     ← repeated from the input
   ├── success                     true or false
   ├── error                       present when success is false
   ├── return_result               the primary answer
   ├── properties                  named intermediate values
   └── provenance                  what produced this

The input fields are duplicated in the output so that a result is a complete trace
of the computation from specification to answer. Practically, that means the input
corresponding to any v1 output is everything above the ``provenance`` field.

.. note::

   The two most common surprises when reading v1 data:

   - **Coordinates are in Bohr** (:math:`a_0`), and stored flat as
     :math:`3 N_{\text{atom}}` numbers. Energies are Hartree.
   - ``schema_name`` was accepted in two spellings. Both ``qcschema_input`` and
     ``qc_schema_input`` appear in real data, as do ``qcschema_output`` and
     ``qc_schema_output``. Consumers should accept either.


What v1 covers
==============

.. list-table::
   :widths: 34 22 44
   :header-rows: 1

   * - Object
     - ``schema_name``
     - Version
   * - Single-point input
     - ``qcschema_input``
     - 1
   * - Single-point output
     - ``qcschema_output``
     - 1
   * - Molecule
     - ``qcschema_molecule``
     - 2
   * - Basis set
     - ``qcschema_basis``
     - 1

Geometry optimizations and torsion drives also have v1 representations
(``qcschema_optimization_input`` / ``_output`` and
``qcschema_torsion_drive_input`` / ``_output``), which follow the same flat
pattern: procedure-level fields on the input, repeated on the output. They are not
documented in detail here.

.. seealso::

   :doc:`/index`
      The QCSchema v2 specification — the current version, documented in full.
