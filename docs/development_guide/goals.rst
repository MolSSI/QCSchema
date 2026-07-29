=================
Goals and history
=================

The purpose of this schema is to provide API-like access to existing workhorse
quantum chemistry packages, so that more complex and unified workflows become
possible.

Primary to that is **avoiding parsing ASCII-based output files** — instead placing
output variables, vectors, and matrices in a consistent format that can be easily
read and loaded by humans or tools.


High-level aspirations
======================

These goals were set out to define the overall scope and direction of the
specification, and they still explain most of its design:

**Connecting QC to visualizers and GUIs**
   A visualizer should be able to render orbitals without implementing a binary
   checkpoint reader for every program. This is why the
   :doc:`wavefunction <../user_guide/wavefunction>` block exists, and why it
   carries a complete :ref:`BasisSet <model-basisset>` rather than a basis name.

**Connecting QC to existing workflow tools**
   Workflow engines already know how to move JSON around. Making a computation a
   JSON document makes it schedulable by tools that know nothing about chemistry.

**Transferring data between QC programs**
   Orbitals, densities, and Hamiltonians in a documented layout let one program
   start from another's wavefunction. This is what makes the
   :doc:`ordering conventions <../implementation_guide/conventions>` load-bearing
   rather than pedantic.

**Providing a rigorous record of computation for large-scale QC databases**
   A stored result should be complete enough to interpret, audit, and reproduce
   years later. This is the goal behind
   :ref:`Provenance <model-provenance>`, and behind v2's decision to embed
   ``input_data`` in every result.

**Providing a framework for QC API access**
   Treating a computation as a request/response pair — input in, result out — is
   what allows a quantum chemistry program to be exposed as a service.


How the goals shaped the layout
===============================

Four consequences of taking the fourth and fifth goals seriously, each of which
explains a piece of the current design.

*Records must be self-contained.* A result embeds the input that produced it, so
one stored object is a complete trace from request to answer — including the case
where the result frame differs from the frame that was submitted.

*Records must be storable.* If every result carried its wavefunction and every
optimization carried every step, a database of millions of computations would be
impossible. Hence :doc:`protocols <../implementation_guide/protocols>`, and hence
defaults that keep as little as possible.

*Records must not lie.* A result that might be a failure has to be treated as
suspect everywhere it is read. Hence ``success`` being a fixed value and failures
living in :ref:`FailedOperation <model-failedoperation>`.

*Specifications must be reusable.* A database storing a million computations at
one level of theory should describe that level of theory once. Hence the
``*Specification`` objects, and their nesting.


A note on the name
==================

The project has been called several things — "QC JSON Schema", "QC Schema",
"MolSSI QCSchema" — and traces of each survive in older field names and module
paths, including a ``qc_schema_input`` spelling that was once accepted. The current
schema standardizes on the ``qcschema_*`` prefix throughout.

Similarly, the numbering: ``Molecule.schema_version`` is one ahead of the family
version because the molecule schema was versioned before the family was. It is
kept that way rather than renumbered, since renumbering would break every stored
molecule in existence. See
:doc:`../implementation_guide/versioning`.
