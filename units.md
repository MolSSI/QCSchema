## Units will be an array

  units:["Hartree",1.0] # 1st entry: label of the unit for human reading. 2nd entry: Conversion constant to the default unit.
  
  units:["Hartree",1.0,1] # the third entry specify the power, allowing for reciprocals etc.
  
## Defult units use unless specified

  Default units use atomic units for everything expect for coordinates (Angstrom)
  
  coordinates: Angstrom
  
  distance: Angstrom
  
  velocity: Angstrom/(au seconds)
  
  forces: Angstrom/(au seconds^2)
  
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
