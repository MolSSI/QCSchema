# QC_JSON_Schema
A JSON Schema for Quantum Chemistry

## High Level Aspirations
In order to help define the overall scope and direction of the specification several high level goals will be pursued: 

- Ability to connect to visualizers and GUI's
- Connect to existing Workflows such as [ASE](https://wiki.fysik.dtu.dk/ase/)
- Transfer data between QM programs (Orbitals, Densities, etc)
- Provide a framework for QM API access

## Partners
The following is a list of programs that have agreed to implement this JSON
specification once a stable version has been released. If do not see your code
here and would like to be part of the project, get in touch!
 
### Visualizers
 - [Avogadro](https://avogadro.cc)
 - [Molecular Design Toolkit](https://github.com/Autodesk/molecular-design-toolkit)
 
### Quantum Chemistry Engines
 - [Psi4](https://github.com/psi4/psi4)
 
## Governance
This project is currently managed by the following members:

 - Marcus D. Hanwell - [Kitware](http://www.openchemistry.org)
 - Bert de Jong - [LBNL](https://crd.lbl.gov/departments/computational-science/ccmc/staff/staff-members/bert-de-jong/)
 - Daniel G. A. Smith - [MolSSI](molssi.org)
 - Aaron Virshup  - [Autodesk](https://bionano.autodesk.com)

This management group will serve as a nexus for writing the schema and facilitate communication with the community. 


## Existing JSON Efforts
The following is a list of efforts that are very similar to the current
proposed spec. The idea is to pull from this diverse group and coalesce into a
single specification to prevent duplication of effort.

 - [Autodesk JSON](https://github.com/Autodesk/molecular-design-toolkit/wiki/Molecular-JSON-Draft-Spec#molecule)
 - [BAGEL JSON](https://github.com/nubakery/bagel/blob/master/test/benzene_sto3g_pml.json)
 - [Chemical JSON](https://github.com/OpenChemistry/chemicaljson)
 - [NWChem JSON](https://github.com/wadejong/NWChemOutputToJson)
 - [Psi4 JSON](https://github.com/psi4/psi4/blob/master/psi4/driver/json_wrapper.py#L55)
 - [PyQC Schema](https://github.com/PyQC/json_schema)
 
