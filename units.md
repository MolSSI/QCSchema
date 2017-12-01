## Units will be an array

  units:["Hartree",1.0] # 1st entry: label of the unit for human reading. 2nd entry: Conversion constant to the default unit.
  
  units:["eV", 0.036749]
  
  units:["Bohr",1.0]
  
  units:["Angstrom",1.8897]
  
  units:["kcal/mol", 0.0015936]
  
  units:["Angstrom/(atomic time)", 1.8897]
  
  units:["cm-1",  2.1948e+05]
  
  units:["THz", 6579.8]
  
  units:["amu", 1822.89]
  
  units:["seconds": 2.418884326509e-17]
  
 
  
 
  
## Defult units use unless specified

  Default units use atomic units for everything expect for coordinates (Angstrom)
  
  coordinates: atomic units
  
  distance: atomic units (bohrs)
  
  velocity:bohrs/(au seconds)
  
  forces: bohrs/(au seconds^2)
  
## Put the units close to quantities:

    eg.
    coords:{ units:["Bohr",2.2],
             xyz:[...] }
             
    total_enery:{value: 23,
                 units:[...]}
                 
## If the "_" pointers are implemented then the units can be specified one level above follows

    eg. 
          coords:{ xyz:[...]}
          coords_units:[...]
