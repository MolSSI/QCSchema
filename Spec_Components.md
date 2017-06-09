# Specification Components

The JSON format is a general container, and the current works focuses primarily
aimed at developing a standard on top of the [JSON](http://www.json.org/) (and
[BSON](http://bsonspec.org/)) format for chemical data.

## Purpose

The purppose here is to document the format, provide an [open
specification](https://en.wikipedia.org/wiki/Open_specifications), establish
what is required or optional, and to provide a living spefication as we extend
the format. This could reuse some of the previous work done in the [CML
format](http://www.xml-cml.org/) for XML.

## Input Components

### Topology

The closest representation to the real physical nature of the system. In
practical terms, for molecular sciences, this is the coordinates (in some form)
and the elements/Z-number at that coordinate. For both QM and MM, this is your
molecule. This may include bonding information and unit cell, lattice
parameters, etc, as well.
 
This is the foundation upon which you build the model basis of your
calculation.

### Driver

What are you looking to calculate? Energy, trajectory, some property

### Model

The overall mathematical model we are using for our calculation.
 
In QM, this is the Hamiltonian (HF, DFT, …) combined with the overall basis of
the calculation. An example in QM would be HF/STO-3G or B3LYP/6-311G**. Custom
basis sets can be handled with custom keywords.

DGAS Note: Some pushback in combining the model and basis together.

### Parameters:

Various tunable parameters for the calculation. These vary widely, depending on
the basis and model chemistry.



## Output Components
 - Repeat of input components
 - Driver return - Return of the requested driver (energy/gradient/etc)
 - Ancillary return - Other properties/values constructed as by products of the computation)
 - Provenance - Code, computer, user information
 - Raw Output - If requested, the canonical domain specific ASCII output
 - Skipped Input Fields - If the input allows pass through of other fields print the skipped ones
 - Errors - If the computation failed the raised error should go here.

