============
Contributing
============

The QCSchema specification — these documents and the JSON Schema files — is
developed in the open at
`MolSSI/QCSchema <https://github.com/MolSSI/QCSchema>`_.


Where to raise what
===================

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - You want to
     - Go to
   * - Propose a new field, object, or property name
     - A `QCSchema issue <https://github.com/MolSSI/QCSchema/issues>`_, for
       discussion before implementation
   * - Report that these docs are wrong or unclear
     - A `QCSchema issue <https://github.com/MolSSI/QCSchema/issues>`_
   * - Report a bug in an implementation
     - That implementation's own tracker, not this one — see :ref:`ecosystem`
   * - Ask how to use QCSchema with a particular program
     - That program's tracker, or the driver package you reach it through
   * - Discuss the database and compute stack
     - `QCFractal <https://github.com/MolSSI/QCFractal>`_

A schema change lands here first, in these documents. It then has to reach the
implementations before anyone can use it, and reach the JSON Schema files before
anyone can validate against it — see :doc:`index`.


Proposing a schema change
=========================

Before opening an issue, it is worth answering these, because they are what the
discussion will turn on:

**Is it in scope?**
   QCSchema describes computations, not workflows, not general chemical files, and
   not a program-agnostic input language. See :doc:`index`.

**Has it been decided already?**
   Check :doc:`design_decisions` — several recurring proposals are closed — and
   :doc:`open_questions` for those that are not.

**Does it already exist elsewhere?**
   Check :doc:`prior_art`. Matching an existing name from PsiVariables or cclib is
   nearly always better than coining a new one.

**Where does it belong?**
   Genuinely new physics probably wants a field. Something one program needs
   probably wants ``keywords`` or ``extras``. Something that varies per computation
   but not per program probably wants a specification field.

**What breaks?**
   Adding an optional field breaks little. Renaming, retyping, or changing a
   default breaks every consumer, and belongs in a version bump.

**Who will produce it, and who will read it?**
   A field no program emits is dead weight. Naming at least one producer and one
   consumer makes the case much stronger.


Adding a property name
======================

New entries in :ref:`AtomicProperties <model-atomicproperties>` are the most
common kind of change. Conventions to follow:

- ``snake_case``, and ``<method>_<quantity>``.
- Reuse the method prefixes that exist: ``scf``, ``mp2``, ``ccsd``,
  ``ccsd_prt_pr``, ``ccsdt``, ``ccsdtq``.
- Reuse quantity suffixes: ``total_energy``, ``correlation_energy``,
  ``dipole_moment``, ``iterations``.
- Avoid characters awkward in keys. This is why CCSD(T) is ``ccsd_prt_pr``.
- State the unit in the field metadata, and the shape for anything array-valued.
- Report unscaled values. Spin components are stored raw so consumers can build
  scaled variants themselves.
- Make it optional. Absence must mean "not computed", which in turn means no
  property may be required.


Building and checking the docs
==============================

.. code-block:: console

   $ pip install -e ".[docs]"
   $ cd docs && make html

Output lands in ``docs/_build/html``.

Some structure worth knowing before you edit:

**Everything is hand-written.** Nothing in these docs introspects code, so the
build has no dependency beyond Sphinx and the theme. Field tables are
``list-table`` blocks with four columns — Field, Type, Notes, Description — and
adding a field means adding a row. Keep the Type column in JSON terms
(``string``, ``number``, ``array[number]``, ``object``) rather than the types of
any particular language.

**Model anchors are manual.** Each object carries a ``.. _model-<lowercase>:``
label so ``:ref:`` links to it work from other pages. A new object needs a new
anchor.

**Vocabulary shifts by audience.** The home page and Quickstart avoid the word
"payload" — a newcomer meets ``input``, ``result``, "the JSON", or "document"
instead. The implementation guide uses "payload" freely, since it is the precise
term for data arriving over an interface and its readers are programmers. Keep
that split when editing; it is deliberate, not an inconsistency to tidy up.

**An API reference is coming.** Once a v2 implementation lives in this
repository, an API reference section will be generated from it with autodoc, and
the field tables here will be able to be generated too. Until then, the tables
are the specification and are maintained by hand.

To check for broken links and references:

.. code-block:: console

   $ make html SPHINXOPTS="-W --keep-going -n"
   $ make linkcheck


Testing schema changes
======================

This repository carries JSON Schema files and a small validator:

.. code-block:: console

   $ pytest -v

Bear in mind that those files still describe the older layout, so a v2 change has
no test to fail here yet. Until the in-repo v2 implementation exists, the
practical check on a proposed change is whether it can be expressed in the JSON
Schema files and whether an existing implementation can round-trip a payload
through it.


Code of conduct and licensing
=============================

QCSchema is a `MolSSI <https://molssi.org>`_ project, released under the
BSD-3-Clause license. Contributions are accepted under the same terms.
