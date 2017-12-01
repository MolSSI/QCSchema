# Extensions & Program-Specific Input and Properties

## Description:
We anticipate adapting concepts from Cascading Style Sheets and OpenGL, where program-specific options and properties are gradually adapted into core/systematic properties in future versions of the schema.

## Global View:
Multiple quantum chemical programs exist because they each have unique capabilities. This implies that while some shared options overlap (e.g., every program can perform geometry optimizations with HF/6-31G(d), etc.) the schema should enable programs to save all current “output formats” in an extensible standardized container.

## Input Keywords
Naturally, many keywords are program-specific. Since the intent is for files to serve as both input and output. This means all program options should be echo’ed in the JSON in a way that enables re-running a job (e.g., a checkpoint or restart).

* Phase 0: An escaped-string of input options must be provided in the output file
* Phase 1: All input options are provided as vendor-keyed dictionaries, separated as individual elements.
* Phase 2: “Core” options, such as job types, basis sets, dft method names, etc. are provided, allowing shared options across multiple programs.
* Beyond this, periodic updates of the schema will be expected to adapt vendor options into “core” options with agreed schemantics.

### Phase 0 Example:

```
'input_keywords': {
	'input_file': '$rem\njobtype energy\nmethod hf\nbasis 6-31g(d)\nscf_algorithm rca\nthresh_rca_switch 6\n$end\n\n$molecule\n 0 1\nC   	-2.8202909762  	0.2981766257  	0.0010924612\nH   	-3.2111619258 	-0.7206086156 	-0.2109382547\nH   	-3.2111634695  	1.0332876486 	-0.7354473924\nH   	-3.1690187454  	0.5999311173  	1.0101248656\nO   	-1.4221041763  	0.2942007922 	-0.0122064685\nH   	-1.1586268938  	0.0200859203 	-0.9288117087\n$end\n'
}
```

### Phase 1 Example:

```
'input_keywords': {
  'jobtype': 'energy',
  'method': 'hf',
  'basis': '6-31G(d)',
  'extensions' : {
    '_qchem': {
      // Q-Chem Specific Options
      'thresh_rca_switch' : 6,
      'scf_algorithm': 'rca'
     }
    '_avogadro': {
      // Avogadro-specific options
      'render_style': 'balls-and-sticks, axes',
    }
  }
}
```

## Output Properties
Not all programs compute the same properties. For example, some higher-order multipole moments are evaluated (e.g., hexadecapole moments) for all geometries. 

Phase 1 will concentrate on core properties (energies, dipole moments, orbital eigenvalues) to be provided as key/value/unit pairs.

### Phase 1 Example:

```
'properties': {
'energy': { 'value': '-34.519', //.. }
  'extensions' : {
    '_qchem' {
     '_sos_mp2_energy' : { 'val' : xxxx },
     '_hexadecapole' : [ .. ]
    }
  }
}
```

## Tasks:

* Identify incentives for vendor-specific keys to become standardized keys in later schema versions
** Incentives for computational chemistry package developers
** Incentives for organizing body/other schema users
* Merging/integrating matrices between input & output (e.g., initial guess)
* What levels in the hierarchy should vendor keys go?
* How much provenance should be associated with the vendor?
** Yes: version, compiler, math library, MPI information, hostname, command line arguments
** No: memory available/used
* Provenance is not necessarily associated with input keywords
