### Note: QCSchema as defined by this repository is very out of date. We are reviving it, but please see the QCElemental repository, particularly https://github.com/MolSSI/QCElemental/tree/master/qcelemental/models/v2 for the current specification.

# QCSchema

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MolSSI/QCSchema.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MolSSI/QCSchema/context:python)
[![Documentation Status](https://readthedocs.org/projects/molssi-qc-schema/badge/?version=latest)](https://molssi-qc-schema.readthedocs.io/en/latest/?badge=latest)

A Key-Value/Array Schema for Quantum Chemistry

The purpose of this schema is to provide API like access to pre-existing quantum
chemistry packages to enable more complex workflows.  The core of this is to
avoid parsing ASCII-based output files and place output variables, vectors,
matrices in a consistent format that can be easily parsed.

Please see the [website](http://molssi-qc-schema.readthedocs.io/en/latest/index.html#) for the current specification.

## Development

Install the package with development dependencies and set up pre-commit hooks:

```bash
pip install -e .
pip install pre-commit
pre-commit install
```

Pre-commit will automatically lint and format code on each commit using [ruff](https://github.com/astral-sh/ruff).

