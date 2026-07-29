========
QCSchema
========

*A JSON schema for quantum chemistry.*

QCSchema describes a quantum chemistry computation — what was asked for, what was
computed, and everything needed to reproduce it — as plain, validatable JSON.
These pages are its specification.


Pick a section
==============

.. grid:: 1 2 2 2
   :gutter: 3

   .. grid-item-card:: :octicon:`rocket;1.5em;sd-mr-1` Quickstart & Examples
      :link: quickstart/index
      :link-type: doc
      :class-card: qcs-nav-card

      Build your first input field by field, then read complete worked examples
      for energies, gradients, optimizations, and failures.

      +++
      New to QCSchema? Start here :octicon:`arrow-right;1em`

   .. grid-item-card:: :octicon:`book;1.5em;sd-mr-1` Schema User Guide
      :link: user_guide/index
      :link-type: doc
      :class-card: qcs-nav-card

      A field-by-field tour of every object in the specification: molecules,
      specifications, results, properties, wavefunctions, and basis sets.

      +++
      Look up what a field means :octicon:`arrow-right;1em`

   .. grid-item-card:: :octicon:`tools;1.5em;sd-mr-1` Schema Implementation Guide
      :link: implementation_guide/index
      :link-type: doc
      :class-card: qcs-nav-card

      Conventions, validation, protocols, and version negotiation — what your code
      is obliged to do to read and write conforming JSON.

      +++
      Wiring QCSchema into a program :octicon:`arrow-right;1em`

   .. grid-item-card:: :octicon:`git-pull-request;1.5em;sd-mr-1` Schema Development Guide
      :link: development_guide/index
      :link-type: doc
      :class-card: qcs-nav-card

      The goals of the project, the design decisions behind the current layout,
      the questions still open, and how to propose a change.

      +++
      Changing the specification itself :octicon:`arrow-right;1em`


What the JSON looks like
========================

The purpose of the format is to avoid **parsing ASCII output files**. Rather than
scraping numbers out of human-readable logs, a QCSchema-speaking program reads and
writes its variables, vectors, and matrices in a consistent, documented shape:

.. code-block:: json

   {
     "schema_name": "qcschema_atomic_input",
     "schema_version": 2,
     "molecule": {
       "schema_name": "qcschema_molecule",
       "schema_version": 3,
       "symbols": ["O", "H", "H"],
       "geometry": [0.0, 0.0, -0.1294, 0.0, -1.4941, 1.0274, 0.0, 1.4941, 1.0274]
     },
     "specification": {
       "schema_name": "qcschema_atomic_specification",
       "driver": "energy",
       "model": {"method": "MP2", "basis": "cc-pVDZ"},
       "keywords": {}
     }
   }

Those few lines name a molecule, a driver, and a model — and any program that
speaks QCSchema knows exactly what to do with them.

.. important::

   **The schema and the models are separate things.**

   This repository specifies QCSchema: the objects, their fields, the units, and
   the rules a valid document must satisfy. That specification is
   language-neutral, and the normative form of every object described on these
   pages is **JSON**.

   Python models for these objects are planned to live here eventually, in a
   simplified form. When they do, they will cover the schema and nothing else —
   no molecule-format parsing, no unit conversion, no program drivers, no
   database. Those are separate concerns belonging to separate packages; see
   :ref:`ecosystem`.

   Today there is no implementation in this repository at all. Where these docs
   show Python, it illustrates the shape of the data, not an API you can install
   from here.

The shape of the specification
==============================

Every QCSchema object carries a ``schema_name`` and, for the top-level
containers, a ``schema_version``. Objects compose in a consistent pattern:

.. code-block:: text

   Input   =  what to compute on  +  how to compute it
              (Molecule)             (Specification)

   Result  =  the Input that produced it  +  what came out
              (input_data)                  (properties, return_result, ...)

That pattern holds at every level of the specification. A single-point
calculation nests a molecule inside an :ref:`AtomicInput <model-atomicinput>`; a
geometry optimization nests an :ref:`AtomicSpecification
<model-atomicspecification>` inside an :ref:`OptimizationSpecification
<model-optimizationspecification>`; a torsion drive nests that in turn. See
:doc:`user_guide/concepts` for the full story.


.. _ecosystem:

Who uses QCSchema
=================

.. tab-set::

   .. tab-item:: Quantum chemistry engines

      - `CFOUR <https://cfour.uni-mainz.de>`_
      - `GAMESS <https://www.msg.chem.iastate.edu/gamess/>`_
      - `Molpro <https://www.molpro.net>`_
      - `MPQC <https://github.com/ValeevGroup/mpqc>`_
      - `NWChem <https://www.nwchem-sw.org>`_
      - `Psi4 <https://github.com/psi4/psi4>`_
      - `PySCF <https://pyscf.org>`_
      - `Q-Chem <https://www.q-chem.com>`_
      - `TeraChem <http://www.petachem.com>`_
      - `xtb <https://github.com/grimme-lab/xtb>`_ /
        `tblite <https://github.com/tblite/tblite>`_

   .. tab-item:: Drivers & workflows

      - `QCEngine <https://github.com/MolSSI/QCEngine>`_ — program adaptors
      - `QCFractal <https://github.com/MolSSI/QCFractal>`_ — distributed compute
        and database
      - `QCManyBody <https://github.com/MolSSI/QCManyBody>`_ — many-body expansions
      - `geomeTRIC <https://github.com/leeping/geomeTRIC>`_ and
        `optking <https://github.com/psi-rking/optking>`_ — geometry optimizers
      - `simple-dftd3 <https://github.com/dftd3/simple-dftd3>`_ /
        `dftd4 <https://github.com/dftd4/dftd4>`_ — dispersion corrections

   .. tab-item:: Libraries & translators

      - `QCElemental <https://github.com/MolSSI/QCElemental>`_ — Python models
        for QCSchema
      - `cclib <https://cclib.github.io>`_
      - `Open Babel <https://openbabel.org>`_
      - `Basis Set Exchange <https://www.basissetexchange.org>`_

   .. tab-item:: Visualizers

      - `Avogadro <https://avogadro.cc>`_
      - `Jmol / JSmol <https://jmol.sourceforge.net>`_
      - `VTK <https://www.vtk.org>`_

For detail on which packages support which version of the schema, see
:doc:`implementation_guide/software_status`.


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Quickstart & Examples

   quickstart/index

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Schema User Guide

   user_guide/index

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Schema Implementation Guide

   implementation_guide/index

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Schema Development Guide

   development_guide/index

.. Kept in the root toctree so that the v1 pages get a working sidebar, prev/next
   links and breadcrumbs. The resulting header-nav entry is redundant with the
   schema-version dropdown and is hidden in custom.css.
.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: QCSchema v1

   v1/index
