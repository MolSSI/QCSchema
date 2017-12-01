### Topology

The topology is the physical representation of the system. For now this should
be a molecule, or molecular cluster. However, this can be extended out to
periodic systems as well if there is enough of a desire to do so. This folder
contains a host of example JSON topology specifcications found throught the CMS community.

High level sets of computations such as many-body, thermochemical reactions, etc computations
should likely be handled by a higher level driver and not make the spec more difficult.

The following molecule specification is used. The required fields are:

  - `symbols` (list) - A list of strings
  - `unit_cell` (list of lists) - (optional) 3x3 matrix defining lattice vectors for periodic systems
  - `geometry` (list) - A `(N, 3)` XYZ coordinate list of list in bohr, will likely change to encompase decided unit specifications

The following are optional fields and default values (option, more a list of possibilities QM programs would want):

  - `name` (str, `""`) - The name of the molecule
  - `charge` (float, `0.0`) - The overall charge of the molecule
  - `multiplicity` (int, `1`)- The overall mulitiplicity of the molecule.
  - `masses` (list of floats) - The mass of the atoms, canonical weights assumed if not given.
  - `num_protons` (list of floats) - The number of protons in each atom, atomic number assumed if not given.
  - `num_electrons` (list of floats) - The number of electrons in each atom, atomic number assumed if not given.
  - `basis` (list of str) - The list of basis set id's (defined in basisSet section) for each atom. Default is ?
  - `comment` (str) - Any additional comment one would attach to the molecule.
  - `fragments` (list of tuples, `[]`) - A list of indices (0-indexed) for molecular fragments within the topology.
  - `fragment_charges` (list of floats, `[]`) - A list of charges associated with the fragments tuple.
  - `fragment_multiplicities` (list of ints, `[]`) - A list of multiplicites associated with each fragment. 
  - `provenance` (dict, `{}`) - The provencance of the molecule.
    - `doi` - A doi reference for the molecule.

Other possible quantities:
  - `fix_com` (bool) - whether to adjust to the molecule to the COM or not
  - `fix_orientation` (bool) - whether to rotate the molecule to a standard orientation or not
  - label (list of str) - Per-atom labels which may be seperate from fragments
  - Extend the `real` quantitity to cover real, ghost, absent, qm/mm region, etc.
  - EFP quantities `fragment_types`, `coordinate_hints`. This is an example and likely not part of the spec. How would we handle this? 

# Connectivity

Connectivity describes relationships between lists of atoms and associated metadata: typically, this is between a pair of atoms (a bond). Connectivity is supported across periodic boundaries.

Each connection between `M` atoms is defined as:

* `M`, number of atomic sites involved, `M` is 2 for connections between pairs of atoms (e.g. bonds)
* `indices`, an ordered list of length `N` of atomic indexes defining the connection, length is multiple of `M`
* `images`, (optional, only relevant if a unit cell lattice is defined) an ordered list of length `3N` describing the periodic image of the connected atom -- by default, this is assumed to be (0,0,0), meaning that the connected atom is in the origin image, and first index is set to (0,0,0) by convention
* a dictionary of metadata, where each value is a list of length `N` (for example, a key could be "bond_type" and values could be "single", "double", etc.)

As an example:

`indices`: [0, 1, 5, 6]
`images`: [0,0,0, 0,0,0, 0,0,0, 1,0,0]

defines two bonds, one between atoms 0 and 1 and one between atoms 5 and 6. In this case, the atom 6 is in periodic image (1,0,0).

For metadata, there are a few pre-defined keys with strict meanings:

* `bond_type` can take values `single`, `double`, `triple` [to replace -- this is just an example], only suitable for connections involving pairs of atoms, this is useful for GUI/visualization tools
* `length` is pre-computed bond lengths in the global unit system, only suitable for connections involving pairs of atoms
* `angle` is pre-computed bond angles, only suitable for connections involving triplets of atoms
* `label`, a string used by visualization tools

But the user can choose to store any arbitrary key as is suitable for their application.

For a buffer representation for big systems, where information is stored in one large array for all atoms, we propose the following format on the same level as `atoms`:

```
"connectivity": {
	2: {  # key is M, e.g. 2 is typically for bonds
		"indices": [...] # multiple of 2, indices of atoms
		"images": [...] # length 3*indices
		"metadata": {
			"...": [...] # length of indices/2
		}
	},
	3: {  # 3 is typically for bond angles
		"indices": [...] # multiple of 3
		etc.
	},
	4: { ... }
	
}
```

The `connectivity` dict is optional, the keys have to be integers greater than or equal to 2, but no keys are mandatory.

With this scheme, not just bonds can be defined, but clusters of atoms too. This makes it versatile for e.g. QM/MM schemes, cluster expansions, etc.
