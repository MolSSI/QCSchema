# Technical Specifications
This document contains various technical considerations and commentary. This is very much a work in progress.

## How do we uniquely specify physical units?

Publicly-available JSON file with supported units and conversions
Standardize to some externally-chosen database or web service
How to specify compound units?

For instance, velocity might be "angstrom/fs" Alternatives:

 1) Require units in the form {`unit_name:exponent`}, e.g. `atom.velocity.units={'angstrom':1, 'fs':-1}`
 2) Allow strings of the form `atom.velocity.units="angstrom/fs"`, but require that units be chosen from a specific list of specifications
 3) Allow strings of the form `atom.velocity.units="angstrom/fs"`, and require file parsers to parse the units according to a specified syntax

How do we store large lists of objects (such as lists of atoms or bonds?)

 1) As a table of values (these values do very well in HDF5 as well)
 2) As a set of arrays
 3) As a list of objects

Examples:

```python
// 1) Storing fields as tables: creates an mmCIF/PDB-like layout
{atoms={type:'table[atom]',
        fields=['name', 'atomic_number', 'mass/Dalton', 'residue_index', 'position/angstrom', 'momentum/angstrom*amu*fs^-1']
        entries=[
          ['CA', 6, 12.0, 0, [0.214,12.124,1.12], [0,0,0]],
          ['N', 7, 14.20, 0, [0.214,12.124,1.12], [0,0,0]],
          ...}

// 2) Storing fields as arrays: much more compact, but harder to read and edit
{num_atoms=1234,
 atoms={names:['CA','CB','OP' ...],
        atomic_numbers:[6,6,8, ...],
        masses:{val:[12.0, 12.0, 16.12, ...], units:amu},
        residue_indices:[0,0,0,1,1, ...],
        positions:{val:[[0.214,12.124,1.12], [0.214,12.124,1.12], ...], units:angstrom},
        momenta:{val:[[0,0,0], [1,2,3], ...], units:angstrom*amu*fs^-1}
        }

// 3) Storing the fieldnames for each atom: readable, but makes the file huge
{atoms=[
  {name:'CA', atnum:6, residue_index:0,
   mass:{value:12.00, units:'Daltons'},
   position:{value:[0.214,12.124,1.12], units:'angstroms'},
   momentum:{value:[0.0, 0.0, 0.0], units:'angstrom*dalton*fs^-1'},
  },
  {name:'N', atnum:7, residue_index:0,
   mass:{value:14.20, units:'Daltons'},
   position:{value:[0.214,12.124,1.12], units:'angstroms'},
   momentum:{value:[0.0, 0.0, 0.0], units:'angstrom*dalton*fs^-1'},
  },
  ...
  }]
}
```

## JSON and HDF5

The object specifications in this document are tailored to JSON, but can be
easily stored in an HDF5 file as well. HDF5 is, like JSON, hierarchical and
self-describing. These similarities make it easy to perform 1-to-1
transformations between well-formed JSON and a corresponding HDF5
representation.

Unlike JSON, HDF5 is binary and requires custom libraries to read, but has far
better performance and storage characteristics for numerical data. We will
provide tools to easily interconvert files between JSON and HDF5. Applications
that support this format should always provide JSON support; ones that require
high performance should also support the HDF5 variant.

## How do we reference other objects?

JSON does not directly support object references. This makes it non-trivial to,
say, maintain a list of bonds between atoms. Some solutions are:

 1) by array index (e.g., `residue.atom_indices=[3,4,5,6]`)
 2) by JSON path reference (see, e.g., https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03)
 3) by a unique key. (e.g., `residue.id='a83nd83'`, `residue.atoms=['a9n3d9', '31di3']`)

Array index is probably the best option - although they are a little fragile,
they're no more fragile than path references, and require far less overhead
than unique keys.

See also: http://stackoverflow.com/q/4001474/1958900
