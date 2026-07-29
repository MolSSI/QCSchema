.. _quickstart:

======================
Quickstart & Examples
======================

QCSchema is a data format. You can produce and consume it with nothing more than
a JSON library, and the fastest way to get a feel for it is to read a few
complete examples and then write your own.

.. toctree::
   :maxdepth: 2

   the_schema_and_the_models
   first_input
   examples

.. grid:: 1 1 3 3
   :gutter: 2

   .. grid-item-card:: :octicon:`git-compare;1.2em;sd-mr-1` Schema vs. models
      :link: the_schema_and_the_models
      :link-type: doc

      What this repository defines, and what it deliberately leaves out.

   .. grid-item-card:: :octicon:`code;1.2em;sd-mr-1` Your first input
      :link: first_input
      :link-type: doc

      Build an atomic input from nothing and read it back field by field.

   .. grid-item-card:: :octicon:`list-unordered;1.2em;sd-mr-1` Worked examples
      :link: examples
      :link-type: doc

      Full JSON for an energy, a gradient, an optimization, and a failure.


.. _tab_convention:

How to read the examples
========================

Every example on these pages leads with **JSON**, because JSON is the normative
form of the specification. Where a **Python** tab appears alongside it, it shows
the same object built as a model — useful for seeing the nesting at a glance, but
not itself part of the specification.

In those Python snippets, class names mirror the schema: ``qcschema_atomic_input``
is ``AtomicInput``, ``qcschema_atomic_specification`` is ``AtomicSpecification``,
and so on. Import paths are deliberately omitted, because there is no
implementation in this repository yet and the path depends on whichever library
you use. See :doc:`the_schema_and_the_models`.


The 60-second version
=====================

A single-point energy computation is one JSON object with two interesting keys —
``molecule`` (*what* to compute on) and ``specification`` (*how* to compute it):

.. tab-set::

   .. tab-item:: JSON

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
             "program": "psi4",
             "driver": "energy",
             "model": {"method": "MP2", "basis": "cc-pVDZ"},
             "keywords": {"scf_type": "df"}
           }
         }

   .. tab-item:: Python

      .. code-block:: python

         AtomicInput(
             molecule=Molecule(
                 symbols=["O", "H", "H"],
                 geometry=[0.0,  0.0000, -0.1294,
                           0.0, -1.4941,  1.0274,
                           0.0,  1.4941,  1.0274],
             ),
             specification=AtomicSpecification(
                 program="psi4",
                 driver="energy",
                 model={"method": "MP2", "basis": "cc-pVDZ"},
                 keywords={"scf_type": "df"},
             ),
         )

Send that to any program that speaks QCSchema and you get back an
:ref:`AtomicResult <model-atomicresult>` containing the energy, a bundle of named
:doc:`properties <../user_guide/properties>`, and a copy of the input that
produced it.

.. seealso::

   :doc:`../user_guide/concepts`
      Why the input splits into ``molecule`` and ``specification``.

   :doc:`../implementation_guide/index`
      What your program must do to accept input like the one above.
