.. _model-molecule:

========
Molecule
========

:``schema_name``: ``qcschema_molecule``
:``schema_version``: 3

The physical Cartesian representation of the molecular system — the closest
representation to the real physical nature of what you are computing on. In
practical terms this is the coordinates and the elements at those coordinates,
optionally extended with bonding, fragmentation, charges, masses, and isotopes.

For both QM and MM, this is your molecule. It is the foundation upon which the
model of the calculation is built.

The smallest legal molecule is two fields:

.. code-block:: json

   {
     "schema_name": "qcschema_molecule",
     "schema_version": 3,
     "symbols": ["O", "H", "H"],
     "geometry": [0.0, 0.0, -0.1294, 0.0, -1.4941, 1.0274, 0.0, 1.4941, 1.0274]
   }

.. warning::

   ``geometry`` is in Bohr (:math:`a_0`) and stored **flat**: :math:`3N` numbers
   in :math:`x_1, y_1, z_1, x_2, y_2, z_2, \ldots` order, reshapable to
   ``(nat, 3)``. Reading Ångström coordinates as Bohr is the single most common
   QCSchema mistake.


Atom ordering is a contract
===========================

The index of ``symbols`` sets atomic order for the whole object *and* for every
per-atom result derived from it. Several fields carry an explicit obligation in
their description, and it is worth stating plainly:

.. admonition:: The reordering rule
   :class: important

   A consumer that shuffles atoms **must not** reattach the input
   (pre-shuffling) molecule to any output (post-shuffling) per-atom result such
   as a gradient. Likewise a consumer that translates the geometry must not
   reattach the pre-translation molecule to origin-sensitive results, and one
   that rotates it must not reattach the pre-rotation molecule to
   frame-sensitive results such as vibrational modes.

This is why :ref:`AtomicResult <model-atomicresult>` has its own top-level
``molecule`` field distinct from ``input_data.molecule``: it is the frame the
results actually belong to.


Fields
======

Required
--------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``symbols``
     - array[string]
     - **required**; shape ``(nat)``
     - The ordered array of atomic elemental symbols in title case. This field's index sets atomic order for all other per-atom fields like ``real`` and the first dimension of ``geometry``. Ghost/virtual atoms must have an entry here in ``symbols``; ghostedness is indicated through the ``real`` field.
   * - ``geometry``
     - array[number]
     - **required**; units ``a0``; shape ``(nat, 3)``
     - The ordered array of Cartesian XYZ atomic coordinates. Serialized storage is always flat, ``(3*nat,)``, and is reshaped to ``(nat, 3)`` by the consumer. The index of the first dimension matches the 0-indexed indices of all other per-atom fields such as ``symbols`` and ``real``. Atom ordering is fixed: a consumer that shuffles atoms must not reattach the input (pre-shuffling) molecule to any output (post-shuffling) per-atom result such as a gradient.

Identification
--------------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_molecule"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``schema_version``
     - ``3``
     - \-
     - The version of ``schema_name`` this conforms to. Fixed value.
   * - ``name``
     - string
     - \-
     - Common or human-readable name to assign to this molecule. This field can be arbitrary; see ``identifiers`` for well-defined labels.
   * - ``comment``
     - string
     - \-
     - Additional comments for this molecule. Intended for pure human/user consumption and clarity.
   * - ``identifiers``
     - :ref:`Identifiers <model-identifiers>`
     - \-
     - An optional dictionary of additional identifiers by which this molecule can be referenced, such as INCHI, canonical SMILES, etc. See the ``Identifiers`` model for more details.
   * - ``id``
     - object
     - \-
     - A unique identifier for this molecule. Exists primarily so that databases can track and look up this specific object, and should virtually never need to be set by hand.
   * - ``validated``
     - boolean
     - default ``false``
     - A boolean indicator, for speed purposes, that this molecule data has already been checked for schema compliance (data layout and type) and physics compliance (e.g. non-overlapping atoms, feasible multiplicity). Should be ``false`` in most cases; only a trusted producer — a constructor, a database, or a previously serialized molecule — should ever set it ``true``.

``validated`` deserves emphasis: it asserts that the physics has *already* been
checked, and a consumer that believes it will skip those checks. Set it only for
data you produced yourself or received from a source you control. See
:doc:`../implementation_guide/validation`.

Charge and spin
---------------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``molecular_charge``
     - number
     - default ``0.0``
     - The net electrostatic charge of the molecule.
   * - ``molecular_multiplicity``
     - number
     - default ``1``
     - The total multiplicity of the molecule.

Per-atom data
-------------

All of these are optional and all are indexed identically to ``symbols``.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``masses``
     - array[number]
     - units ``u``; shape ``(nat)``
     - The ordered array of atomic masses. Index order matches the 0-indexed indices of all other per-atom fields like ``symbols`` and ``real``. If this is not provided, the mass of each atom is inferred from its most common isotope. If this is provided, it must be the same length as ``symbols`` but can accept ``None`` entries for standard masses to infer from the same index in the ``symbols`` field.
   * - ``real``
     - array[boolean]
     - shape ``(nat)``
     - The ordered array indicating if each atom is real (``True``) or ghost/virtual (``False``). Index matches the 0-indexed indices of all other per-atom settings like ``symbols`` and the first dimension of ``geometry``. If this is not provided, all atoms are assumed to be real (``True``). If this is provided, the reality or ghostedness of every atom must be specified.
   * - ``atomic_numbers``
     - array[integer]
     - shape ``(nat)``
     - An optional ordered 1-D array-like object of atomic numbers of shape (nat,). Index matches the 0-indexed indices of all other per-atom settings like ``symbols`` and ``real``. Values are inferred from the ``symbols`` list if not explicitly set. Ghostedness should be indicated through ``real`` field, not zeros here.
   * - ``mass_numbers``
     - array[integer]
     - shape ``(nat)``
     - An optional ordered 1-D array-like object of atomic *mass* numbers of shape (nat). Index matches the 0-indexed indices of all other per-atom settings like ``symbols`` and ``real``. Values are inferred from the most common isotopes of the ``symbols`` list if not explicitly set. If single isotope not (yet) known for an atom, -1 is placeholder.
   * - ``atom_labels``
     - array[string]
     - shape ``(nat)``
     - Additional per-atom labels as an array of strings. Typical use is in model conversions, such as Elemental <-> Molpro and not typically something which should be user assigned. See the ``comment`` field for general human-consumable text to affix to the molecule.

Note that ghost (virtual) atoms get a normal entry in ``symbols`` and are marked
through ``real``, not by a zero in ``atomic_numbers``.

Connectivity and fragments
--------------------------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``connectivity``
     - array[array[integer, integer, number]]
     - \-
     - A list of bonds within the molecule. Each entry is a tuple of ``(atom_index_A, atom_index_B, bond_order)`` where the ``atom_index`` matches the 0-indexed indices of all other per-atom settings like ``symbols`` and ``real``. Bonds may be freely reordered and inverted.
   * - ``fragments``
     - array[array[integer]]
     - shape ``(nfr, <varies>)``
     - List of indices grouping atoms (0-indexed) into molecular fragments within the molecule. Each entry in the outer list is a new fragment; index matches the ordering in ``fragment_charges`` and ``fragment_multiplicities``. Inner lists are 0-indexed atoms which compose the fragment; every atom must be in exactly one inner list. Noncontiguous fragments are allowed, though no QM program is known to support them. Fragment ordering is fixed; that is, a consumer who shuffles fragments must not reattach the input (pre-shuffling) molecule schema instance to any output (post-shuffling) per-fragment results (e.g., n-body energy arrays).
   * - ``fragment_charges``
     - array[number]
     - shape ``(nfr)``
     - The total charge of each fragment in the ``fragments`` list. The index of this list matches the 0-index indices of ``fragments`` list. Will be filled in based on a set of rules if not provided (and ``fragments`` are specified).
   * - ``fragment_multiplicities``
     - array[number]
     - shape ``(nfr)``
     - The multiplicity of each fragment in the ``fragments`` list. The index of this list matches the 0-index indices of ``fragments`` list. Will be filled in based on a set of rules if not provided (and ``fragments`` are specified).

``connectivity`` is a list of ``(atom_index_a, atom_index_b, bond_order)``
triples using 0-indexed atom indices. Bonds may be freely reordered and
inverted, so ``(0, 1, 1.0)`` and ``(1, 0, 1.0)`` are the same bond.

``fragments`` groups atoms into subsystems; every atom must appear in exactly one
inner list. Fragment order is fixed in the same way atom order is — a consumer
that shuffles fragments must not reattach the original molecule to per-fragment
results such as n-body energy arrays.

Frame and symmetry
------------------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``fix_com``
     - boolean
     - default ``false``
     - Whether translation of the geometry is disallowed (fix ``true``) or allowed (fix ``false``). 'Fix' is used in the sense of 'specify': ``true`` signals that the origin in ``geometry`` is a deliberate part of the molecule specification, while ``false`` allows that the origin is happenstance and a consumer may translate the center of mass to ``(0, 0, 0)``. A consumer that translates the geometry must not reattach the pre-translation molecule to origin-sensitive results.
   * - ``fix_orientation``
     - boolean
     - default ``false``
     - Whether rotation of the geometry is disallowed (fix ``true``) or allowed (fix ``false``). 'Fix' is used in the sense of 'specify': ``true`` signals that the frame orientation in ``geometry`` is a deliberate part of the molecule specification, while ``false`` allows that the frame is happenstance and a consumer may reorient along the inertial tensor. A consumer that rotates the geometry must not reattach the pre-rotation molecule to frame-sensitive results such as vibrational modes.
   * - ``fix_symmetry``
     - string
     - \-
     - Maximal point group symmetry which ``geometry`` should be treated. Lowercase.

"Fix" here means *specify*, not *freeze*. ``fix_com=true`` declares that the
origin in ``geometry`` is a deliberate part of the specification;
``fix_com=false`` (the default) says the origin is happenstance and a consumer
may translate the center of mass to :math:`(0,0,0)`. The same reading applies to
``fix_orientation`` and reorientation along the inertial tensor.

This matters more than it looks. With the defaults, the geometry you submit is
generally **not** the geometry that comes back.

Metadata
--------

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``provenance``
     - :ref:`Provenance <model-provenance>`
     - \-
     - The provenance information about how this Molecule (and its attributes) were generated, provided, and manipulated.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the molecule. Use for schema development and scratch space.


Identifiers
===========

.. _model-identifiers:

``identifiers`` holds canonical chemical identifiers, as opposed to the
free-form human label in ``name``:

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``molecule_hash``
     - string
     - \-
     - Hash of the molecule's geometry, masses, and charges; used for duplicate detection.
   * - ``molecular_formula``
     - string
     - \-
     - The molecular formula, e.g. ``H2O``.
   * - ``smiles``
     - string
     - \-
     - SMILES string.
   * - ``inchi``
     - string
     - \-
     - IUPAC InChI string.
   * - ``inchikey``
     - string
     - \-
     - IUPAC InChIKey, the fixed-length hash of the InChI.
   * - ``canonical_explicit_hydrogen_smiles``
     - string
     - \-
     - Canonical SMILES with hydrogens written explicitly.
   * - ``canonical_isomeric_explicit_hydrogen_mapped_smiles``
     - string
     - \-
     - Canonical isomeric SMILES with explicit hydrogens and atom mapping.
   * - ``canonical_isomeric_explicit_hydrogen_smiles``
     - string
     - \-
     - Canonical isomeric SMILES with hydrogens written explicitly.
   * - ``canonical_isomeric_smiles``
     - string
     - \-
     - Canonical SMILES including stereochemistry.
   * - ``canonical_smiles``
     - string
     - \-
     - Canonical SMILES, without stereochemistry.
   * - ``pubchem_cid``
     - string
     - \-
     - PubChem Compound ID
   * - ``pubchem_sid``
     - string
     - \-
     - PubChem Substance ID
   * - ``pubchem_conformerid``
     - string
     - \-
     - PubChem Conformer ID

.. code-block:: json

   {
     "identifiers": {
       "molecular_formula": "H2O",
       "smiles": "O",
       "inchikey": "XLYOFNOQVPJJNP-UHFFFAOYSA-N",
       "pubchem_cid": "962"
     }
   }


Hashing and duplicate detection
===============================

Geometries, masses, and charges are rounded to 8, 6, and 4 decimal places
respectively before hashing, so that two molecules differing only in
floating-point noise hash to the same value and are recognized as the same
system. The result is carried in ``identifiers.molecule_hash``.

The rounding is part of the specification rather than an implementation detail: a
producer that hashes the raw floats will disagree with one that does not, and
duplicate detection across a database depends on everyone agreeing. Positive and
negative zero are normalized to positive zero for the same reason.


Sparsity on serialization
=========================

``Molecule`` is one of the few v2 objects that **omits null fields** when
serialized, rather than emitting every key. A minimal helium atom therefore
serializes to just the fields that have values:

.. code-block:: json

   {
     "schema_name": "qcschema_molecule",
     "schema_version": 3,
     "validated": true,
     "symbols": ["He"],
     "geometry": [0.0, 0.0, 0.0],
     "name": "He",
     "molecular_charge": 0.0,
     "molecular_multiplicity": 1.0,
     "fix_com": false,
     "fix_orientation": false,
     "provenance": {"creator": "MyDriver", "version": "1.0",
                    "routine": "mydriver.build_molecule"},
     "extras": {}
   }

Note that ``masses``, ``real``, ``connectivity``, ``fragments`` and the rest are
simply absent rather than present-and-null.

If you build pipelines that serialize, edit, and reconstruct — for example making
an ionized molecule from a neutral one — remember that a field you never set will
not be present to edit, and that setting a field to ``null`` is the same as
omitting it.
