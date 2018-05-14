.. QC_JSON_Schema documentation master file, created by
   sphinx-quickstart on Thu Mar 15 13:55:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Quantum Chemistry Schema
========================
A JSON Schema for Quantum Chemistry


The purpose of this schema is to provide API-like access to existing workhorse quantum
chemistry packages to enable more complex and unified workflows.  Primary to this is
avoiding parsing ASCII-based output files, instead placing output variables, vectors,
matrices in a consistent format that can be easily read/loaded by humans or tools.

High-Level Aspirations
----------------------
In order to help define the overall scope and direction of the specification, several high-level goals will be pursued:

 * Connecting QC to visualizers and GUIs
 * Connecting QC to existing Workflows tools
 * Transfer data between QC programs (Orbitals, Densities, etc.)
 * Provide a rigorous record of computation for large-scale QC databases
 * Provide a framework for QC API access

A concrete list of requirements for this schema can be found [here](Requirements.md).

**Organizations:**
 * `The Molecular Sciences Software Institute <http://www.molssi.org>`_

**Visualizers:**
 - `Avogadro <https://avogadro.cc>`_
 - `Molecular Design Toolkit <https://github.com/Autodesk/molecular-design-toolkit>`_
 - `VTK <http://www.vtk.org>`_
 - `Jmol / JSmol <http://jmol.org/>`_

**Quantum Chemistry Engines:**
 - `GAMESS <http://www.msg.ameslab.gov/gamess/>`_
 - `MPQC <https://github.com/ValeevGroup/mpqc>`_
 - `NWChem <http://www.nwchem-sw.org/index.php/Main_Page>`_
 - `Psi4 <https://github.com/psi4/psi4>`_
 - `PySCF <http://sunqm.github.io/pyscf/>`_

**Translators:**
 - `cclib <http://cclib.github.io>`_
 - `openbabel <http://openbabel.org/>`_
 
**Utilities:**
 - `geomeTRIC <https://github.com/leeping/geomeTRIC>`_


Existing JSON Efforts
----------------------
JSON or XML based input or output is a common abstraction with quantum chemistry.
The idea is to pull from the wide and coalesce into a
single specification to prevent duplication of effort.

 * `Autodesk JSON <https://github.com/Autodesk/molecular-design-toolkit/wiki/Molecular-JSON-Draft-Spec#molecule>`_
 * `BAGEL JSON <https://github.com/nubakery/bagel/blob/master/test/benzene_sto3g_pml.json>`_
 * `Chemical JSON <https://github.com/OpenChemistry/chemicaljson>`_
 * `MPQC JSON <https://gist.github.com/dgasmith/28ce209867afd272d361a00322960160>`_
 * `NWChem JSON <https://github.com/wadejong/NWChemOutputToJson>`_
 * `Psi4 JSON <https://github.com/psi4/psi4/blob/master/psi4/driver/json_wrapper.py#L55>`_
 * `PyQC Schema <https://github.com/PyQC/json_schema>`_
 * `Molpro Database XML <https://www.molpro.net/info/2015.1/doc/manual/node814.html>`_
 * `Chemical Markup Language <http://www.xml-cml.org>`_


Contents
--------

.. toctree::
   :maxdepth: 1
   :caption: Contents
   
   spec_components
   faq
   tech_specs
   examples

.. toctree::
   :maxdepth: 1
   :caption: Schema Keywords
   
   auto_topology
   auto_props
