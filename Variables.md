# Variables

A key component of any schema is a comprehensive dictionary of component names and descriptions. 

## Methodologies

Some sort of discussion of consistent QM nomenclature. (MP2, Moller-Plesset2, B3LYLP, B3LYP5, etc).

## Methodology returns

QM Methodologies produce a wide array of variables that need to be named and tagged for downstream use. For example if we think
about a simple SCF computation we can produce the following variables:

 - Nuclear Repulsion Energy
 - SCF Total Energy
 - One-Electron Energy
 - Two-Electron Energy
 - Number of SCF Iterations
 - SCF Energy Convergence
 - SCF Density Convergence
 - Dipole X, Y, Z
 - Additional One-Electron Properties
 
From this list it is likely the SCF Total Energy is the most important quantity; however, other quantities may be more
important depending on the circumstances. Some sort of decision of which variables are imporant and how we want to describe
them is in order.
 
If we take the first variable `Nuclear Repulsion Energy` this has a very basic form
`nuc_rep = \frac{1}{2}\frac{q_i * q_j}{r_{ij}}`. For most SCF quantities the closed form is easy to write down; however,
this quickly breaks down for more advanced theories. Im not saying that we need to do this, but bringing up the point that
some decision on how explicit we are needs to be made.

### Known Variable Lists:
 - [CCLibVars](http://cclib.github.io/data_notes.html)
 - [PsiVars](http://psicode.org/psi4manual/master/glossary_psivariables.html)
