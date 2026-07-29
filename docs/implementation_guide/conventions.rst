.. _conventions:

===========
Conventions
===========

The rules that hold everywhere in QCSchema. Most interoperability bugs are a
violation of one of these rather than a misunderstanding of a particular field.

.. contents:: On this page
   :local:
   :depth: 1


Units
=====

QCSchema values carry **no unit tags**. Each field has exactly one documented
unit, and it is atomic units throughout.

.. list-table::
   :widths: 34 18 48
   :header-rows: 1

   * - Quantity
     - Unit
     - Appears as
   * - Length / coordinates
     - :math:`a_0` (Bohr)
     - ``Molecule.geometry``
   * - Energy
     - :math:`E_h` (Hartree)
     - ``*_energy``, ``return_energy``
   * - Gradient
     - :math:`E_h/a_0`
     - ``return_gradient``, ``scf_total_gradient``
   * - Hessian
     - :math:`E_h/a_0^2`
     - ``return_hessian``, ``scf_total_hessian``
   * - Dipole moment
     - :math:`e\,a_0`
     - ``*_dipole_moment``
   * - Quadrupole moment
     - :math:`e\,a_0^2`
     - ``scf_quadrupole_moment``
   * - Mass
     - u
     - ``Molecule.masses``

.. danger::

   **Ångström is not a QCSchema unit.** Reading Ångström coordinates as Bohr is
   the most common error made against this specification, and it does not fail
   loudly — it produces a plausible-looking energy for the wrong molecule.

If your program works in Ångström internally, convert at the boundary and only
there — and take the conversion factor from a CODATA-derived constants library
rather than a literal in your source.

Do not invent your own conversion constants; different programs historically used
slightly different values for the Bohr radius, and reproducing a number to eight
decimal places requires agreeing on it.


Indexing and naming
===================

- Arrays are **zero-indexed**. Atom 0 is the first atom. ``connectivity``
  entries and ``fragments`` members are 0-indexed atom references.
- Keys are ``snake_case``.
- Property keys read ``<method>_<quantity>``; see
  :doc:`../user_guide/properties`.


Array layout
============

Multidimensional data is stored **flat** and reshaped by the consumer using a
documented shape. Shapes are expressed with these abbreviations:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Symbol
     - Meaning
   * - ``nat``
     - Number of atoms, :math:`=` ``calcinfo_natom``
   * - ``nfr``
     - Number of fragments
   * - ``nao``
     - Number of atomic orbitals, :math:`=` ``calcinfo_nbasis``
   * - ``nmo``
     - Number of molecular orbitals, :math:`=` ``calcinfo_nmo``

So:

.. list-table::
   :widths: 40 25 35
   :header-rows: 1

   * - Field
     - Flat length
     - Reshape to
   * - ``Molecule.geometry``
     - :math:`3 \cdot nat`
     - ``(nat, 3)``
   * - ``return_gradient``
     - :math:`3 \cdot nat`
     - ``(nat, 3)``
   * - ``return_hessian``
     - :math:`9 \cdot nat^2`
     - ``(3*nat, 3*nat)``
   * - ``scf_dipole_moment``
     - 3
     - ``(3,)``
   * - ``scf_quadrupole_moment``
     - 9
     - ``(3, 3)`` (redundant, 6 unique)
   * - ``scf_orbitals_a``
     - :math:`nao \cdot nmo`
     - ``(nao, nmo)``
   * - ``scf_density_a``
     - :math:`nao^2`
     - ``(nao, nao)``

.. important::

   Matrix quantities in the :doc:`wavefunction <../user_guide/wavefunction>`
   block are **column-major**. The per-atom arrays (``geometry``, gradients) are
   row-major in the sense that consecutive triples are one atom's :math:`x,y,z`.

Because ``calcinfo_natom`` fixes the shape of every derivative, the reference
implementation refuses to validate a gradient or Hessian without it. Always set
it.


Basis function ordering
=======================

AO basis functions follow the CCA standard as implemented in
`libint <https://github.com/evaleev/libint/wiki/using-modern-CPlusPlus-API#solid-harmonic-gaussians-ordering-and-normalization>`_.

This is a real obligation, not a formality. Two programs can agree on every
number in an orbital coefficient matrix and still be describing different
wavefunctions if they disagree about which basis function each row indexes. If
your program uses a different internal ordering — and many do — permute on the
way out.

Whether a shell contributes :math:`2L+1` or :math:`(L+1)(L+2)/2` functions is
determined by ``ElectronShell.harmonic_type``, so ``nbf`` is computable from the
basis data alone. Use that as a checksum.


The reordering rule
===================

Several fields carry a "guidance" clause in their description. Collected, they say
one thing:

.. admonition:: Do not reattach a stale molecule
   :class: danger

   - A consumer that **shuffles atoms** must not reattach the input
     (pre-shuffling) molecule to any output (post-shuffling) per-atom result
     (e.g. a gradient).
   - A consumer that **shuffles fragments** must not reattach the input molecule
     to any per-fragment result (e.g. an n-body energy array).
   - A consumer that **translates** the geometry must not reattach the
     pre-translation molecule to origin-sensitive results.
   - A consumer that **rotates** the geometry must not reattach the pre-rotation
     molecule to frame-sensitive results (e.g. vibrational modes).

This is why :ref:`AtomicResult <model-atomicresult>` has a top-level ``molecule``
distinct from ``input_data.molecule``. Populate the top-level one with the frame
your results actually belong to, and leave the input untouched.

Programs reorder atoms all the time — for symmetry detection, for fragment
grouping, for load balancing. That is fine. What is not fine is returning
reordered gradients alongside the original atom list.


Frames: ``fix_com`` and ``fix_orientation``
===========================================

"Fix" means *specify*, not *freeze*:

- ``fix_com=false`` (default) — the origin in ``geometry`` is happenstance; you
  may translate the center of mass to :math:`(0,0,0)`.
- ``fix_com=true`` — the origin is a deliberate part of the specification; leave
  it alone.

The same reading applies to ``fix_orientation`` and reorientation along the
inertial tensor.

.. warning::

   With the defaults, the geometry a consumer receives back is generally **not**
   the geometry it submitted. If your caller needs the original frame — because it
   is placing an external field, or comparing against an experimental structure —
   it must set the fix flags, and you must honour them.


Sparsity on serialization
=========================

Serialize **all** fields. Five objects are exceptions and omit ``null`` values:
``Molecule``, ``AtomicProperties``, ``WavefunctionProperties``,
``OptimizationProperties``, and ``ManyBodyProperties``. Everywhere else, emit the
key even when its value is a default.

For those five, note that setting a field to ``null`` and omitting it are the same
thing. A pipeline that serializes, mutates, and reconstructs — a common way to
build an ionized molecule from a neutral one — cannot use ``null`` to mean
"explicitly nothing".

Whatever your library calls it, there will be a "skip unset/default fields" mode.
Do not use it for anything crossing a process boundary: it drops ``schema_name``
and ``schema_version`` along with everything else at its default, and the payload
then fails validation at the far end.

.. code-block:: text

   full dump    ->  { "schema_name": ..., "schema_version": 2, "molecule": {...}, ... }
   sparse dump  ->  { "molecule": {...} }                          <- unusable


Extension points
================

.. list-table::
   :widths: 22 78
   :header-rows: 1

   * - Mechanism
     - Use for
   * - ``keywords``
     - Program-specific input settings. Never validated by QCSchema.
   * - ``extras``
     - Anything the specification does not describe; scratch space and driver
       annotations.
   * - ``provenance``
     - Execution detail — wall time, thread count, host. Permits extra keys.
   * - ``model``
     - Model-defining information not yet standardized. Permits extra keys.
   * - ``native_files``
     - Program-native files, protocol-controlled.

Everything else forbids unknown keys. Do not invent top-level fields; a payload
carrying them will be rejected by a strict consumer rather than passed through.
If you find yourself wanting a new field, that is a
:doc:`specification change <../development_guide/index>`.
