==================
Consuming QCSchema
==================

The inbound half of an interface: taking a payload you have been handed and
turning it into a computation.


Identify before you parse
=========================

``schema_name`` tells you what you are holding, and it should be the first thing
you look at. Do not infer the type from which fields happen to be present.

.. code-block:: python

   handlers = {
       "qcschema_atomic_input": run_single_point,
       "qcschema_optimization_input": run_optimization,
   }

   handler = handlers.get(payload["schema_name"])
   if handler is None:
       raise ValueError(f"unsupported schema_name: {payload['schema_name']!r}")

Then check ``schema_version``, which for v2 top-level containers is ``2`` — except
``Molecule``, which is ``3``. See :doc:`versioning`.


Validate at the boundary
========================

Validate once, on entry, and then trust the object internally. If you have a
library that models the schema, construction *is* the validation:

.. code-block:: python

   try:
       atomic_input = AtomicInput(**payload)
   except ValidationError as exc:
       return FailedOperation(
           input_data=payload,
           error=ComputeError(error_type="input_error", error_message=str(exc)),
       )

Note what the failure returns: a :ref:`FailedOperation <model-failedoperation>`
with ``input_data`` set to the *raw* payload. The payload did not validate, so it
cannot be stored as an ``AtomicInput`` — which is exactly why ``input_data`` on
``FailedOperation`` is untyped.

For non-Python implementations, see :doc:`validation`.


Read the specification, not the input
=====================================

The fields you need moved in v2. They are on the specification:

.. code-block:: python

   spec = atomic_input.specification

   spec.driver          # energy | gradient | hessian | properties
   spec.model.method    # e.g. "B3LYP"
   spec.model.basis     # str, BasisSet, or None
   spec.keywords        # your program's own settings
   spec.protocols       # how much output to keep

   atomic_input.molecule    # the system


Handle the driver you were given
================================

``driver`` is not advisory. If you cannot compute what was asked for, that is an
``input_error``, not a silently substituted answer.

.. code-block:: python

   if spec.driver == "energy":
       value = run_energy(...)
   elif spec.driver == "gradient":
       value = run_gradient(...)          # (nat, 3), flattened on output
   elif spec.driver == "hessian":
       value = run_hessian(...)           # (3*nat, 3*nat)
   elif spec.driver == "properties":
       value = run_properties(...)        # dict of named values
   else:
       raise ValueError(f"unsupported driver {spec.driver}")

Computing a gradient when an energy was requested is acceptable (you may report
both), but ``return_result`` must match the driver's type.


Handle ``basis`` being three things
===================================

``model.basis`` may be a name, a full :ref:`BasisSet <model-basisset>`, or
``null``:

.. code-block:: python

   basis = spec.model.basis
   if basis is None:
       pass                          # semiempirical, MM, or otherwise basis-free
   elif isinstance(basis, str):
       load_basis_by_name(basis)
   else:                             # a qcschema_basis_set object
       build_basis_from_schema(basis)

If you only support named bases, reject the object form with an ``input_error``
rather than ignoring it and quietly running the wrong basis.


Respect the frame flags
=======================

Before you recenter or reorient, look at the molecule:

.. code-block:: python

   mol = atomic_input.molecule
   if not mol.fix_com:
       geometry = translate_to_com(geometry)
   if not mol.fix_orientation:
       geometry = orient_to_inertial_frame(geometry)

Whatever you end up with is what belongs in the result's top-level ``molecule``.
See :doc:`conventions`.


Keywords are yours; unknown keys are your call
==============================================

QCSchema does not validate ``keywords``, so you decide what an unrecognized key
means. Two defensible policies:

**Strict** — reject unknown keywords with an ``input_error``. Preferable, because
a typo'd convergence threshold that is silently ignored produces a wrong answer
that looks right.

**Permissive** — ignore unknown keywords. Reasonable if your program is
frequently driven by generic tooling that may pass keywords meant for a different
code.

Whichever you pick, document it. Do not pick per-keyword.


Consuming results
=================

If you are on the reading side — a database, an analysis script, a visualizer —
the things worth knowing:

.. code-block:: python

   # Branch on success before anything else
   if not payload.success:
       handle_failure(payload.error)
       return

   # Per-atom results belong to the top-level molecule, not input_data.molecule
   gradient = payload.return_result.reshape(-1, 3)
   atoms = payload.molecule.symbols

   # Properties are sparse: absent means "not computed", not "zero"
   scf = payload.properties.scf_total_energy
   if scf is None:
       ...

.. warning::

   A missing property key means the program did not report that quantity. It does
   not mean the value is zero. ``mp2_singles_energy`` genuinely *is* ``0.0`` for a
   closed-shell reference, and that is different from its absence.

Do not assume optional blocks are present. ``wavefunction`` is ``null`` unless a
protocol asked for it, ``stdout`` is ``null`` if the ``stdout`` protocol was
``false``, and ``trajectory_results`` is empty by default for optimizations.
