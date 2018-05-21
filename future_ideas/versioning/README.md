How to start and manage a JSON extension
----------------------------------------

Soon, we'll get a separate GitHub Organization. Pretend all this text refers to that organization.

Vote on the name by incrementing the tally!
- [ ] MolSciSchema
- [ ] MolecularScienceSchema

There will be a main repo `MolSciSchema-core` into which the core, approved, common, consensus schema goes.

To create an extension, create a new repo in this org, essentially registering your domain, eg.g. `MolSciSchema-nwchem`. Please be lowercase in your domain.

Within your repo, you have freedom of contents. Any keys you add should be prefixed and include a colon e.g., `nwchem:modes`. You have freedom of commit management. "Owners" of the repo will probably be you (and those with power to commit to the core schema repo). With respect to versioning, you are strongly encouraged to follow SchemaVer (remember viz and the like are depending on reading these).

As extension find common fields and utility and converge on a semi-proved structure for that utility, make a PR to the core schema repo. The PR is the time for community review. Some governance will merge PRs into core. Periodically, timed releases will be made aiming to follow SchemaVer.

Instance documents will contain a field for core version and an array with the version numbers for any used extensions. For instance a Psi4 output json doc will have 0.4.4 core ver and ['psi4': 2.2.2, 'avogadro': 1.1.1] where core contains basic molecule, psi4 extension contains molecule fragmentation, and vibrational modes are written out according to the avogadro extension. There will be a regularization of that version into a string (e.g., v0.4.4-psi4v2.2.2-avogadrov1.1.1).

Optional keys in JSON will be always allowed, but overlaps will be _effectively_ forbidden by requiring the namespace-colon for anything not in core.

Not strictly on the versioning topic but brought up
---------------------------------------------------

- Versioning of data absorbed by codes/schema (not strictly program) like basisset, element masses. Changes in basisset exchange lead to different results. Versioning will provide key information about changes. Use of CODATA fundamental constants, IUPAC Gold Book for naming conventions (including atom names for superheavies) and semantic meaning of terms (see their Gold Book).

- Adherence of codes, visualizers, etc. to schema: bronze, molden, silver, gold, platinum compliance levels that will change with core version
