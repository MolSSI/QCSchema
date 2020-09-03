Frequently Asked Questions
==========================

Will the json be validated before it reaches my software?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is a question for the producer and consumers of the QC Schema. It is certainly recommended
to validate the schema and validation can be accomplished in a variety of langauges
found at the `JSON-Schema website <http://json-schema.org/implementations.html>`_.

Does the schema accept arbitrary extra fields if my software piece needs internal extensions?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes, we are currently discussing which fields are reserved and where the best
place for arbitrary fields would be. Most high-level schema do *not* accept
additional arbitrary fields, but they do have an ``extras`` dictionary-like field
that can be used for schema development and scratch space.

Are there libraries for writing the schema in [programming-language]?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
JSON is agnostic to the underlying programming language and is well supported
in a variety of languages (C++/Python/JS/etc). We will provide examples on how
to write JSON in other languages where JSON is not as well supported (Fortran).

Why not use XML?
~~~~~~~~~~~~~~~~
The ability to hand write and tweak a given input has been a sought after
property. In addition, the overall structure of JSON is viewed as simpler and
more intuitive than XML. As the schema is fully specified it should be possible
for the validator to take in a JSON input and return an XML output.

What style will be used for indexing and case?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We will support zero-indexing for arrays and snake_case for keys.
Discussion is underway if we will follow the `Google JSON Style
Guide <https://google.github.io/styleguide/jsoncstyleguide.xml>`_.

Will the schema be versioned?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes, the schema will have version flags so that the Schema can evolve over time.
