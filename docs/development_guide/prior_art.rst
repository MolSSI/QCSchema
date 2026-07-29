=========
Prior art
=========

JSON- or XML-based input and output is a common abstraction in quantum chemistry,
and QCSchema was not the first attempt. The idea from the outset was to pull from
the wide range of existing efforts and coalesce into a single specification, to
prevent further duplication of effort.

Anyone proposing a change should look here first. It is likely that someone has
already made the choice you are considering, one way or the other.


Program-specific JSON and XML efforts
=====================================

- `Autodesk JSON
  <https://github.com/Autodesk/molecular-design-toolkit/wiki/Molecular-JSON-Draft-Spec#molecule>`_
- `BAGEL JSON
  <https://github.com/nubakery/bagel/blob/master/test/benzene_sto3g_pml.json>`_
- `Chemical JSON <https://github.com/OpenChemistry/chemicaljson>`_
- `MPQC JSON <https://gist.github.com/dgasmith/28ce209867afd272d361a00322960160>`_
- `NWChem JSON <https://github.com/wadejong/NWChemOutputToJson>`_
- `Psi4 JSON
  <https://github.com/psi4/psi4/blob/master/psi4/driver/json_wrapper.py>`_
- `PyQC Schema <https://github.com/PyQC/json_schema>`_
- `Molpro database XML
  <https://www.molpro.net/manual/doku.php?id=the_xml_output_file>`_
- `Chemical Markup Language <http://www.xml-cml.org>`_

Two of these are worth singling out. **Chemical JSON** remains actively used by
the OpenChemistry stack and is the closest thing to a peer format for molecular
data. **Chemical Markup Language** is the most thoroughly worked-out attempt at
the problem and is the origin of the value-plus-unit pattern discussed in
:doc:`open_questions`.


Property and variable vocabularies
==================================

QCSchema's property names did not come from nowhere. When proposing a new property
key, check these first — matching an existing name is nearly always better than
coining one.

- `PsiVariables
  <https://psicode.org/psi4manual/master/glossary_psivariables.html>`_ — Psi4's
  variable glossary, which QCSchema's naming tracks most closely
- `cclib data notes <https://cclib.github.io/data_notes.html>`_ — quantities
  cclib parses across many programs, and therefore a good survey of what programs
  actually report
- `CODESSA quantum descriptors
  <http://www.codessa-pro.com/descriptors/quantum/eee.htm>`_


Standards bodies and terminology
================================

- `IUPAC Goldbook <https://goldbook.iupac.org>`_ — authoritative terminology;
  see in particular
  `units and constants <https://goldbook.iupac.org/lists/list_math.html>`_ and
  `electron density <https://goldbook.iupac.org/terms/view/E01986>`_
- `IUPAC recommendations for computational chemistry
  <https://doi.org/10.1515/pac-2012-1204>`_ and the
  `earlier 1997 recommendations <https://doi.org/10.1351/pac199769051137>`_
- `IUPAC recommendations, recently published
  <https://iupac.org/recommendations/recently-published/>`_
- `IUPAC InChI activities beyond organics
  <https://iupac.org/who-we-are/divisions/division-details/?body_code=802>`_ —
  relevant to the ``identifiers`` field on :doc:`../user_guide/molecule`

Basis set data has its own well-established source, which QCSchema's
:doc:`../user_guide/basis_set` object is designed to interoperate with:

- `Basis Set Exchange <https://www.basissetexchange.org>`_ — emits QCSchema
  directly, and is the reason exponents and coefficients may be strings as well as
  numbers

And for AO ordering, the convention QCSchema adopts:

- `libint's solid harmonic Gaussian ordering
  <https://github.com/evaleev/libint/wiki/using-modern-CPlusPlus-API#solid-harmonic-gaussians-ordering-and-normalization>`_
  — the CCA standard as implemented there
