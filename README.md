# QC_JSON_Schema
A JSON Schema for Quantum Chemistry

The purpose of this schema is to provide API like access to pre-existing quantum
chemistry packages to enable more complex workflows.  The core of this is to
avoid parsing ASCII-based output files and place output variables, vectors,
matrices in a consistent format that can be easily parsed.

## High Level Aspirations
In order to help define the overall scope and direction of the specification several high level goals will be pursued: 

- Ability to connect to visualizers and GUI's
- Connect to existing Workflows tools
- Transfer data between QM programs (Orbitals, Densities, etc)
- Provide a rigorous record of computation for large scale QM databases
- Provide a framework for QM API access

A concrete list of requirements for this schema can be found [here](Requirements.md).

## Example
The following is an example input to the program. Note that the specification
is likely to change heavily, especially with regard to units. However, this is
an example of the common input and output structures:

```
>>> json_molecule = {}
>>> json_molecule["geometry"] = [[0, 0, 0], [0, 0, 1]]
>>> json_molecule["atoms"] = ["He", "He"]

>>> json_input = {}
>>> json_input["molecule"] = json_molecule
>>> json_input["driver"] = "energy"
>>> json_input["method"] = {"expression": "SCF",
                            "basis":     "sto-3g"}
```

This would output the following JSON dictionary

```
>>> program.run_json(json_input)
{
    'raw_output': 'Output storing was not requested.',
    'molecule': {
        'geometry': {
            'val': [[0, 0, 0], [0, 0, 1]],
            'units': 'angstrom'
        },
        'atoms': ['He', 'He']
    },
    'driver': 'energy',
    'method': {
        'expression': 'SCF',
        'basis': 'sto-3g'
    },
    'variables': {
        'SCF N ITERS': 2.0,
        'SCF DIPOLE Y': {
            'val': 0.0,
            'units': 'hartree'
        },
        'SCF TOTAL ENERGY': {
            'val': -5.433191881443323,
            'units': 'hartree'
        },
        'SCF TWO-ELECTRON ENERGY': {
            'val': 4.124089347186247,
            'units': 'hartree'
        },
        'SCF DIPOLE Z': {
            'val': 0.0,
            'units': 'hartree'
        },
        'NUCLEAR REPULSION ENERGY': {
            'val': 2.11670883436,
            'units': 'hartree'
        },
        'SCF DIPOLE X': {
            'val': 0.0,
            'units': 'hartree'
        },
        'ONE-ELECTRON ENERGY': {
            'val': -11.67399006298957,
            'units': 'hartree'
        }
    },
    'return_value': {
        'val': -5.433191881443323,
        'units': 'hartree'
    },
    'error': '',
    'success': True,
    'provenance': {
        'creator': 'QM Program',
        'routine': 'program.run_json',
        'version': '1.1rc1'
    }
}
```

A discussion of each top level component can be found [here](Spec_Components.md).
Details can also be found on [variable names](Variables.md) and the [technical specifications](Technical_Specifications.md).

## Partners
The following is a list of programs that have agreed to implement this JSON
specification once a stable version has been released. If do not see your code
here and would like to be part of the project, get in touch!
 
  
### Organizations
 - [The Molecular Sciences Software Institute](http://www.molssi.org)
 
### Visualizers
 - [Avogadro](https://avogadro.cc)
 - [Molecular Design Toolkit](https://github.com/Autodesk/molecular-design-toolkit)
 
### Quantum Chemistry Engines
 - [NWChem](http://www.nwchem-sw.org/index.php/Main_Page)
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
 
