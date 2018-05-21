# Compliance Levels

The specificiation has various levels of compliance so that partner codes can
implement various levels of specification based on their requirements and
desired support.  

## Tier 1
- A) Verifies the JSON input
- B) Can perform energy, optimization, and frequency computations and record output 

## Tier 2 
- C) Can obtain energy/gradient/Hessian quantities
- D) Records all miscellaneous quantities into the Variables field without
    requiring specific nomenclature for intra-program consistency (one-electron
    energy, two-electron energy, KS energy, ...) 
- E) Exports Wavefunction quantities (orbitals, eigenvalues, densities, ...)

## Tier 3
- F) Converts AO quantities to a common ordered and normalized representation
- G) Uses a standard dictionary of Variables as output
