.. _software_status:

===============
Software status
===============

Which packages speak QCSchema v1, v2, or both. Useful when planning a migration:
the constraint is usually the least-migrated package in your pipeline.

.. note::

   This page is a snapshot, not part of the specification. It reflects the state
   as of QCElemental 0.50; check each project's own changelog for anything newer,
   and if you know of an entry that is out of date,
   :doc:`a correction is welcome <../development_guide/contributing>`.


MolSSI packages
===============

.. list-table::
   :widths: 20 14 66
   :header-rows: 1

   * - Package
     - Since
     - QCSchema support
   * - QCElemental
     - 0.50.0
     - Python (Pydantic) models for both v1 and v2. The most complete
       implementation today, and what most of the ecosystem is built on.
   * - QCEngine
     - 0.50.0
     - v2 internally; accepts and returns either. ``return_version=1|2``,
       otherwise version-in-is-version-out.
   * - QCManyBody
     - 0.6.0
     - ManyBody schema in v1 and v2. The core interface is version-indifferent;
       the high-level interface is version-in-is-version-out via
       ``qcmanybody.v1.ManyBodyComputer`` or ``qcmanybody.v2.ManyBodyComputer``.
   * - QCFractal / QCPortal
     - —
     - See the `QCArchive documentation <https://molssi.github.io/QCFractal>`_.


Quantum chemistry programs
==========================

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Program
     - Since
     - QCSchema support
   * - Psi4
     - 1.11.0
     - v2 internally; accepts and returns either. ``return_version=1|2``,
       otherwise version-in-is-version-out. *(Not yet released as of the
       QCElemental 0.50 notes.)*
   * - xtb
     - 26.1?
     - Either version, version-in-is-version-out, through
       ``xtb.qcschema.harness.run_qcschema()``. *(Not yet released.)*
   * - tblite
     - 0.6.0?
     - Either version, version-in-is-version-out, through
       ``tblite.qcschema.run_schema()``. *(Not yet released.)*

Programs not listed here are typically reached through a QCEngine harness rather
than a native QCSchema interface, which is the recommended route — see
:doc:`index`.


Procedures and corrections
==========================

.. list-table::
   :widths: 20 14 66
   :header-rows: 1

   * - Package
     - Since
     - QCSchema support
   * - optking
     - 0.5.0
     - Either version, version-in-is-version-out.
   * - simple-dftd3 / s-dftd3
     - 1.3.0
     - Either version, version-in-is-version-out, through
       ``dftd3.qcschema.run_qcschema()``.
   * - dftd4
     - 4.1.0
     - Either version, version-in-is-version-out, through
       ``dftd4.qcschema.run_qcschema()``.
   * - geomeTRIC
     - —
     - Not yet implemented; still v1 internally.


Version-in-is-version-out
=========================

Most of the ecosystem converged on the same convention, and it is worth stating
plainly because it makes mixed pipelines workable: **if you hand a package a v1
payload you get a v1 payload back, and likewise for v2**, regardless of which
version the package uses internally.

An explicit ``return_version`` argument overrides it where a package supports one.

The consequence is that you can migrate a pipeline incrementally at its *edges*
even though no single package can mix versions internally. A v1 driver can call a
v2-internal program and never notice.



Implementation notes
====================

Details belonging to particular packages rather than to the specification. These
are the ones that most often bite during a migration; each package's own docs are
authoritative.

**Import the version you mean.** Libraries that carry both schema families
usually expose them under separate namespaces, and the unqualified path may well
resolve to v1 for backwards compatibility. Be explicit.

**Check Python version support before committing to v1.** QCSchema v1 models
built on Pydantic's v1 compatibility layer do not work on Python 3.14; v2 models
do. If you need 3.14, you need v2. This applies to QCElemental 0.50 and later,
where importing is fine but instantiating a v1 model raises.

**Serialize everything.** Whatever your library calls it, avoid the
"skip unset fields" mode for payloads crossing a process boundary — it strips
``schema_name`` and ``schema_version``. See :doc:`producing`.

**Watch where a driver puts its extras.** When one package wraps another, added
input extras land in the v2 layout at
``AtomicResult.input_data.specification.extras`` rather than
``AtomicResult.extras``, which is where the v1 layout had them. Code reading
driver-supplied extras needs updating even if nothing else does.
