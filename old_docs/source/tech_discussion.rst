Technical Discussion
====================
This document contains various technical considerations that are both open and those which have been discussed and closed.

Open Questions
--------------

How do we reference other objects?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JSON does not directly support object references. This makes it non-trivial to,
say, maintain a list of bonds between atoms. Some solutions are:

 1) by array index (e.g., :code:`residue.atom_indices=[3,4,5,6]`)
 2) by JSON path reference (see, e.g., https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03)
 3) JSON-LD allows some flexibility of referencing. Also gives flexibility to break one document 
    or one JSON object into pieces that can be referenced against.
 4) by a unique key. (e.g., :code:`residue.id='a83nd83'`, :code:`residue.atoms=['a9n3d9', '31di3']`)

Array index is probably the best option - although they are a little fragile,
they're no more fragile than path references, and require far less overhead
than unique keys.

We need to look at this beyond atoms and bonds. Especially in workflows we can reuse pieces of data 
from previous tasks in the workflow. Instead of repeating we can use referencing.

See also: http://stackoverflow.com/q/4001474/1958900

How do we uniquely specify physical units?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For instance, velocity might be "angstrom/fs" Alternatives:

 1) Require units in the form {:code:`unit_name:exponent`}, e.g. :code:`atom.velocity.units={'angstrom':1, 'fs':-1}`
 2) Allow strings of the form :code:`atom.velocity.units="angstrom/fs"`, but require that units be chosen from a specific list of specifications
 3) Allow strings of the form :code:`atom.velocity.units="angstrom/fs"`, and require file parsers to parse the units according to a specified syntax
 
 Note: There are multiple standards specifications for units, and conversions. If done right in a schema, you can use JSON-LD to
 link to the actual standards definition. Some examples in CML:
 
.. code:: python

    "orbitalEnergy": {"units": "Hartree", "value": 0.935524}
    "shieldingAnisotropy": {"units": "ppm","value": 17.5292}


JSON and HDF5
~~~~~~~~~~~~~

The object specifications in this document are tailored to JSON, but can be
easily stored in an HDF5 file as well. HDF5 is, like JSON, hierarchical and
self-describing. These similarities make it easy to perform 1-to-1
transformations between well-formed JSON and a corresponding HDF5
representation.

Unlike JSON, HDF5 is binary and requires custom libraries to read, but has far
better performance and storage characteristics for numerical data. We will
provide tools to easily interconvert files between JSON and HDF5. Applications
that support this format should always provide JSON support; ones that require
high performance should also support the HDF5 variant.

Closed Questions
----------------

Store large collections of objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
There exists multiple ways to arrange data which represents objects. These expressions come down to two primary categories:

The "big" approach where each field is a flat (1D) array for each category:

.. code:: python

    {
        "symbols": ["C", "C", ...],
        "geometry": [0.000, 1.396, 0.000, 1.209, 0.698, 0.000, ...],
        "masses": [12.017, 12.017, ...]
    }

The "small" approach which has a closer object-base mapping:
 
.. code:: python

    {
        "fields": ["symbols", "geometry", "masses"],
        "table": [
            ["C", [0.000, 1.396, 0.000], 12.017],
            ["C", [1.209, 0.698, 0.000], 12.017],
            ...
        ]
    }

For the QC Schema it was decided to follow the big approach as it has the following benefits:
 -  Serialization/deserialization is much faster due to the smaller number of objects generated.
 -  The "small" approach can lead to a complex hierarchy of fields.
 -  It is generally thought the "big" approach is more straightforward to program due to its flatter structure.

