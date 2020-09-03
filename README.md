# QCSchema

[![Build Status](https://img.shields.io/travis/MolSSI/QCSchema/master.svg?logo=linux&logoColor=white)](https://travis-ci.org/MolSSI/QCSchema)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MolSSI/QCSchema.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MolSSI/QCSchema/context:python)
[![Documentation Status](https://readthedocs.org/projects/molssi-qc-schema/badge/?version=latest)](https://molssi-qc-schema.readthedocs.io/en/latest/?badge=latest)

A Key-Value/Array Schema for Quantum Chemistry

The purpose of this schema is to provide API like access to pre-existing quantum
chemistry packages to enable more complex workflows.  The core of this is to
avoid parsing ASCII-based output files and place output variables, vectors,
matrices in a consistent format that can be easily parsed.

Please see the [website](http://molssi-qc-schema.readthedocs.io/en/latest/index.html#) for the current specification. 

## Modifying the Schema

JSON Schema can specify only data layout, descriptions, and basic
defaults and type information for the models that compose QCSchema. To
supplement data layout validation, physics validation, defaulting,
serialization, and helper functions, a reference implementation in
Python for the latest development version of QCSchema is available
at the [QCElemental](https://github.com/MolSSI/QCElemental/)
project. QCElemental uses
[Pydantic](https://github.com/samuelcolvin/pydantic) to encode the
models into Python classes which undergo considerable testing. Since
the classes can auto-generate JSON Schema, it makes sense to use them
as the definition of QCSchema, rather than hand-writing schema here
and synching versions.

The gist of the above is that schema in this repository are read-only. To
propose a change, open an issue here at QCSchema or open a pull request
at QCElemental. Any discussion of changes to QCSchema will take place
here or will be cross-linked to here in accordance with The Guidance.

* [`qcschema/dev/QCSchema.schema`](qcschema/dev/QCSchema.schema) — single-file, human-readable development schema exported from QCElemental.
* [`qcschema/data/vdev/`](qcschema/data/vdev) — multi-file, compressed development schema exported from QCElemental. contents redundant to above.
* [`qcschema/data/v2/`](qcschema/data/v2) — multi-file, compressed version 2 schema hand-written here. contents were `qcschema/dev/` until September 2020.
* [`qcschema/data/v1/`](qcschema/data/v1) — multi-file, compressed version 1 schema hand-written here.

