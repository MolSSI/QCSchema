==============
Open questions
==============

Technical considerations that have been raised and not settled. Contributions on
any of these are welcome — see :doc:`contributing`.


How should physical units be specified?
=======================================

QCSchema currently fixes one unit per field and carries no unit information in the
payload. That is cheap and unambiguous, but it makes an entire class of error
silent: reading Ångström coordinates as Bohr yields a plausible energy for the
wrong molecule.

For a quantity like a velocity in "angstrom/fs", the alternatives are:

1. **Structured units** — require the form ``{unit_name: exponent}``, e.g.
   ``atom.velocity.units = {"angstrom": 1, "fs": -1}``.
2. **Strings from a controlled list** — allow ``atom.velocity.units =
   "angstrom/fs"`` but require the value to come from a specified list.
3. **Strings with a parsing grammar** — allow ``"angstrom/fs"`` and require
   parsers to interpret it according to a specified syntax.

There are multiple existing standards specifications for units and conversions. If
this were done well in the schema, JSON-LD could link to the actual standards
definition rather than restating it. Chemical Markup Language takes the
value-plus-unit approach:

.. code-block:: json

   {
     "orbitalEnergy": {"units": "Hartree", "value": 0.935524},
     "shieldingAnisotropy": {"units": "ppm", "value": 17.5292}
   }

The trade-off is verbosity and payload size — wrapping every number in an object
with a unit is a large cost across an array of a million values — against
catching a class of error that currently passes silently.


How should objects be referenced across documents?
==================================================

Within one document, references are by array index; that question is
:doc:`closed <design_decisions>`. What remains open is referencing *between*
documents.

The motivating case is workflows. A workflow reusing pieces of data from previous
tasks currently has to repeat them: an optimization trajectory of 40 steps
repeats the same specification 40 times, and a torsion drive repeats the molecule
at every grid point. Referencing rather than repeating would shrink records
substantially.

This also needs consideration beyond atoms and bonds. JSON-LD in particular gives
the flexibility to break one document into pieces that can be referenced against
each other, which would make partial retrieval possible — fetch the properties of a
result without fetching its wavefunction.

The obvious counterweight is that a reference-based record is no longer
self-contained, which cuts against the "rigorous record of computation" goal in
:doc:`goals`.

.. seealso::

   `Stack Overflow: how to reference objects in JSON
   <https://stackoverflow.com/q/4001474/1958900>`_


JSON and HDF5
=============

The object specifications in QCSchema are tailored to JSON but map cleanly onto
HDF5, which is — like JSON — hierarchical and self-describing. Those similarities
make 1-to-1 transformations between well-formed JSON and a corresponding HDF5
representation straightforward.

Unlike JSON, HDF5 is binary and requires custom libraries to read, but it has far
better performance and storage characteristics for numerical data. That matters
most for exactly the payloads that are already painful: wavefunctions, densities,
and long trajectories.

The intended arrangement is that tools be provided to interconvert. Applications
supporting this format should **always** support JSON; ones that require high
performance should *also* support the HDF5 variant.

Tooling for this has not materialized. In the meantime MessagePack serves a
similar purpose in practice: implementations commonly support a ``msgpack-ext``
encoding, which gets most of the size benefit for numerical arrays without needing
a second schema representation at all.


Which fields are reserved?
==========================

The schema accepts arbitrary extra fields in specific places — ``extras``,
``keywords``, ``provenance``, ``model`` — and forbids them elsewhere. Which field
names are reserved, and where the best place for arbitrary fields is, has been
discussed but not fully settled.

v2 sharpened this considerably by setting ``extra="forbid"`` on most models, which
at least makes the boundary enforceable rather than conventional. What is still
missing is guidance on namespacing *within* ``extras`` — two tools writing the same
key into ``extras`` will silently collide, and there is no convention preventing
it.

A plausible convention would be to key ``extras`` by producer
(``extras["qcengine"]``, ``extras["my_tool"]``), and QCEngine informally does
something like this, but nothing is specified.


Should ``error_type`` be an enumeration?
========================================

``ComputeError.error_type`` is documented as a short classifier and the
`QCEngine exception names
<https://github.com/MolSSI/QCEngine/blob/master/qcengine/exceptions.py>`_ are the
de facto vocabulary — but the field accepts any string, and the reference
implementation notes it is "not yet strict".

Making it a closed enumeration would let consumers branch reliably, most usefully
on the retryable/not-retryable distinction. Keeping it open lets programs report
failures the enumeration did not anticipate. A middle path — a standard enumeration
plus a documented escape value — has not been proposed formally.


Where do properties beyond the current set belong?
==================================================

:ref:`AtomicProperties <model-atomicproperties>` covers SCF, MP2, and coupled
cluster through CCSDTQ. It does not cover multireference methods, excited states,
response properties, or most of what a modern program computes.

There is no established process for adding a property name, and no clear answer
to whether the model should keep growing a flat namespace of
``<method>_<quantity>`` keys, or whether some categories deserve their own
sub-objects. The flat namespace is simple and has served well, but "one field per
method per quantity" does not obviously scale to excited states, where the natural
shape is a list.

See :doc:`../user_guide/properties` for the current set and the prior art that
informed it.
