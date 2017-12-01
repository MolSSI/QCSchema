###Units will be an array

  units:["Hartree",1.0]
  
  units:["Hartree",1.0,1]
  
###Defult units use unless specified

  Default units use atomic units for everything expect for coordinates (Angstrom)
  
  coordinates: Angstrom
  
  distance: Angstrom
  
  velocity: Angstrom/(au seconds)
  
  forces: Angstrom/(au seconds^2)
  
###Put the units close to quantities:

    eg.
    coords:{ units:["Bohr",2.2],
             xyz:[] }
             
    total_enery:{value: 23,
                 units:[]}
                 
###Possiblely we can also do

    eg. coords:[]
    
        coords_units:[]
     
