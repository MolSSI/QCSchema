# Compliance Levels

The specificiation has various levels of compliance so that partner codes can
implement various levels of specification based on their requirements and
desired support.  

## Tier 1
- A) Verifies the JSON input
- B) Can obtain energy/gradient/Hessian quantities
- C) Can perform optization, response, frequency, and spectra computations and
     record output 

## Tier 2 
- D) Records all miscellaneous quantities into the Variables field
     (one-electron energy, two-electron energy, KS energy, ...) 
- E) Exports Wavefunction quantities (orbitals, eigenvalues, densities, orbitals)

## Tier 3
- F) Converts AO quantities to a common ordered and normalized representation
- G) Uses a standard dictionary of Variables as output
