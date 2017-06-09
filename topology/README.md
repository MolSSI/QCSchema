### Topology

The topology is the physical representation of the system. For now this should
be a molecule, or molecular cluster. However, this can be extended out to
periodic systems as well.

The following molecule specification is used. The required fields are:

  - `symbols` (list) - A list of strings 
  - `geometry` (list) - A (N, 3) XYZ coordinate list of list in bohr

The following are optional fields and default values (option, more a list of possibilities QM programs would want):

  - `name` (str, `""`) - The name of the molecule
  - `charge` (float, `0.0`) - The overall charge of the molecule
  - `multiplicity` (int, `1`)- The overall mulitiplicity of the molecule.
  - `real` (list of bool, `[True, ...]`) - A list describing if the atoms are real or ghost.
  - `comment` (str) - Any additional comment one would attach to the molecule.
  - `fragments` (list of list, `[]`) - A list of indices (0-indexed) for molecular fragments within the topology.
  - `fragment_charges` (list, `[]`) - A list of charges associated with the fragments tuple.
  - `fragment_multiplicities` (list, `[]`) - A list of multiplicites associated with each fragment. 
  - `provenance` (dict, `{}`) - The provencance of the molecule.
    - `doi` - ??

Other possible quantities:
  - Bonds
  - Basis Sets per atom 
