Specification Components
========================

A brief overview of the fields present in the QC Schema is contained below.
It should be noted that a signifigant amount of customization can be added to each
field, please see the Schema or Examples document section for further information.

Input Components
----------------

Topology
~~~~~~~~

The closest representation to the real physical nature of the system. In
practical terms, for molecular sciences, this is the coordinates (in some form)
and the elements/Z-number at that coordinate. For both QM and MM, this is your
molecule. This may include bonding information and unit cell, lattice
parameters, etc, as well.

This is the foundation upon which you build the model basis of your
calculation.

A water molecule example:

.. code:: python

  {
    "molecule": { 
      "geometry": [
        0.0,  0.0000, -0.1294,
        0.0, -1.4941,  1.0274,
        0.0,  1.4941,  1.0274
      ],
      "symbols": ["O", "H", "H"]
    }
  }


Driver
~~~~~~

What are you looking to calculate: energy, gradient, Hessian, or property.

A energy call:

.. code:: python

  {
    "driver": "energy"
  }

Model
~~~~~

The overall mathematical model we are using for our calculation. Another way to
think about this is the largest superset that still obtains roughly the same
result. In QM, this is the Hamiltonian (HF, DFT, ...) combined with the overall basis of
the calculation. An example in QM would be HF/STO-3G or B3LYP/6-311G**. Custom
basis sets can be handled with custom keywords.

A example B3LYP call in the cc-pVDZ basis.

.. code:: python

  {
    "model": {
      "method": "B3LYP",
      "basis": "cc-pVDZ"
    }
  }

Keywords
~~~~~~~~

Various tunable parameters for the calculation. These vary widely, depending on
the basis and model chemistry. These represent the keywords of individual programs currently.

Program specific keywords requesting a density-fitting SCF call and a specific energy convergence tolerance:

.. code:: python

  {
    "keywords": {
      "scf_type": "df",
      "e_congerence": 1.e-7
    }
  }

Output Components
-----------------

Input Components
~~~~~~~~~~~~~~~~
The input components are duplicated in the output so that the result is a complete trace of the requested computation from input specification to results.

Success
~~~~~~~
A description if the computation was successful or not. For unsuccessful computations standard errors will be placed in the output such as covergence errors, IO errors, etc.

A successful example:

.. code:: python

  {
    "success": true,
  {

An unsuccessful example:

.. code:: python

  {
    "success": false,
    "error": {
      "error_type": "convergence_error",
      "errorm_message": "SCF failed to converge after 50 iterations"
  {


Returned Result
~~~~~~~~~~~~~~~
The "primary" return of a given computation. For energy, gradient, and Hessian quantities these are either single numbers or a array representing the derivative quantity.

A simple "energy" driver example:

.. code:: python

  {
     "return_result": -76.4187620271478
  {

Provenance
~~~~~~~~~~
A brief description of the program, version, and routine used to generate the output. Can
include more detailed information such as computation time, processor information, and host location.

.. code:: python

  {
    "provenance": {
      "creator": "QM Program",
      "version": "1.1",
      "routine": "module.json.run_json"
    },
  }

Properties
~~~~~~~~~~
A set of intermediate values produced by the QM program such as the one-elecron and two-electron erngies in SCF.
In addition, this will include such values such as the number of atomic orbitals and the number of alpha and beta electrons.

An example properties from a water HF/cc-pVDZ computation:

.. code:: python

  {
    "properties": {
      "calcinfo_nbasis": 24,
      "calcinfo_nmo": 24,
      "calcinfo_nalpha": 5,
      "calcinfo_nbeta": 5,
      "scf_one_electron_energy": -122.44534536383044,
      "scf_two_electron_energy": 37.622464940400654,
      "nuclear_repulsion_energy": 8.80146205625184,
      "scf_total_energy": -76.02141836717794
    }
  }

Know variable lists include:

 * `IUPAC Goldbook <https://goldbook.iupac.org>`_
 
  * `Units/Constants <https://goldbook.iupac.org/lists/list_math.html, https://goldbook.iupac.org/lists/list_goldbook_unit_defs.html>`_
  * `Electron Density <https://goldbook.iupac.org/html/E/E01986.html>`_

 * `IUPAC recommendations for computational chemistry <https://doi.org/10.1351/pac199769051137, https://doi.org/10.1515/pac-2012-1204>`_
 * `IUPAC recommendations are product of IUPAC Projects <https://iupac.org/recommendations/recently-published/>`_
 * `IUPAC InChI related activities beyond organics <https://iupac.org/who-we-are/divisions/division-details/?body_code=802>`_
 * `CCLibVars <http://cclib.github.io/data_notes.html>`_
 * `PsiVars <http://psicode.org/psi4manual/master/glossary_psivariables.html>`_
 * `Codessa <http://www.codessa-pro.com/descriptors/quantum/eee.htm>`_


Basis Quantities
~~~~~~~~~~~~~~~~

The schema supports the export of basis quantities such as the overlap matrix or the orbitals. TBD



