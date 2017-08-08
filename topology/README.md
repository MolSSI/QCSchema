### Topology

The topology is the physical representation of the system. For now this should
be a molecule, or molecular cluster. However, this can be extended out to
periodic systems as well if there is enough of a desire to do so. This folder
contains a host of example JSON topology specifcications found throught the CMS community.

High level sets of computations such as many-body, thermochemical reactions, etc computations
should likely be handled by a higher level driver and not make the spec more difficult.

The following molecule specification is used. The required fields are:

  - `symbols` (list) - A list of strings 
  - `geometry` (list) - A `(N, 3)` XYZ coordinate list of list in bohr, will likely change to encompase decided unit specifications

The following are optional fields and default values (option, more a list of possibilities QM programs would want):

  - `masses` (list of floats) - The mass of the molecule, canonical weights assumed if not given.
  - `name` (str, `""`) - The name of the molecule
  - `charge` (float, `0.0`) - The overall charge of the molecule
  - `multiplicity` (int, `1`)- The overall mulitiplicity of the molecule.
  - `real` (list of bool, `[True, ...]`) - A list describing if the atoms are real or ghost.
  - `comment` (str) - Any additional comment one would attach to the molecule.
  - `fragments` (list of tuples, `[]`) - A list of indices (0-indexed) for molecular fragments within the topology.
  - `fragment_charges` (list of floats, `[]`) - A list of charges associated with the fragments tuple.
  - `fragment_multiplicities` (list of ints, `[]`) - A list of multiplicites associated with each fragment. 
  - `provenance` (dict, `{}`) - The provencance of the molecule.
    - `doi` - A doi reference for the molecule.

Other possible quantities:
  - Bonds - Holding data for MM computations
  - Basis Sets per atom 
  - `fix_com` (bool) - whether to adjust to the molecule to the COM or not
  - `fix_orientation` (bool) - whether to rotate the molecule to a standard orientation or not
  - label (list of str) - Per-atom labels which may be seperate from fragments
  - Extend the `real` quantitity to cover real, ghost, absent, qm/mm region, etc.
  - EFP quantities `fragment_types`, `coordinate_hints`. This is an example and likely not part of the spec. How would we handle this? 
