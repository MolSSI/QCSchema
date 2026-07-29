==================
Producing QCSchema
==================

The outbound half of an interface: turning a finished computation into a payload
someone else can read.


Build the result around the input
=================================

A v2 result **embeds** the input that produced it. Keep the input object around
for the duration of the computation and hand it back:

.. code-block:: python

   result = AtomicResult(
       input_data=atomic_input,          # exactly what you were given
       molecule=result_frame_molecule,   # the frame your numbers belong to
       properties=properties,
       return_result=value,
       success=True,
       provenance={
           "creator": "MyProgram",
           "version": my_program.__version__,
           "routine": "myprogram.qcschema.run",
       },
   )

Do not modify ``input_data`` on the way through. If you translated or reoriented,
that belongs in the top-level ``molecule``, and the input keeps the frame the
caller submitted.


Fill in properties generously
=============================

This is the part with the most value per line of code, and the part most often
skimped. Every intermediate you already have in memory should be reported:

.. code-block:: python

   properties = {
       # Always: these fix the shape of everything else
       "calcinfo_natom": nat,
       "calcinfo_nbasis": nbf,
       "calcinfo_nmo": nmo,
       "calcinfo_nalpha": nalpha,
       "calcinfo_nbeta": nbeta,

       # Always: geometry-only
       "nuclear_repulsion_energy": e_nuc,

       # The requested answer
       "return_energy": e_total,

       # Everything you computed along the way
       "scf_one_electron_energy": e_one,
       "scf_two_electron_energy": e_two,
       "scf_total_energy": e_scf,
       "scf_iterations": niter,
       "mp2_correlation_energy": e_corr,
       "mp2_total_energy": e_mp2,
   }

.. important::

   ``calcinfo_natom`` is effectively mandatory. Every derivative's shape is
   expressed in terms of it, so a gradient or Hessian without it cannot be
   validated at all and should be refused.

Rules of thumb:

- Omit what you did not compute. Do not emit ``0.0`` as a placeholder — absence
  and zero mean different things to a consumer.
- ``return_energy`` is the energy of the *requested method*. For an MP2 job that
  is ``mp2_total_energy``, not ``scf_total_energy``.
- Report spin components **unscaled**, so consumers can build SCS-MP2 and friends
  themselves.
- Use the documented key or no key at all. A near-miss name like
  ``scf_1e_energy`` is worse than silence, because it will be rejected by strict
  validation and ignored by everyone else.


Honour the protocols
====================

Protocols are a contract about output size. Check them before you serialize
anything large:

.. code-block:: python

   protocols = atomic_input.specification.protocols

   wavefunction = None
   if protocols.wavefunction != "none":
       wavefunction = collect_wavefunction(protocols.wavefunction)

   stdout = log_text if protocols.stdout else None

   native_files = {}
   if protocols.native_files == "all":
       native_files = collect_all_files()
   elif protocols.native_files == "input":
       native_files = {"input": generated_input_text}

Protocols are a guarantee to the consumer, not a suggestion: data the protocol
excludes must not appear in the result. Filtering before you assemble it also
saves you the cost of building something that is about to be thrown away.

See :doc:`protocols` for the full semantics of each value.


Get ``return_result`` right
===========================

Its type is determined by the driver:

.. code-block:: python

   if driver == "energy":
       return_result = float(energy)
   elif driver == "gradient":
       return_result = gradient.reshape(-1)         # 3*nat, flat
   elif driver == "hessian":
       return_result = hessian.reshape(-1)          # (3*nat)^2, flat
   elif driver == "properties":
       return_result = {"dipole": [...], "mulliken_charges": [...]}

Also duplicate it into the matching property — ``return_energy``,
``return_gradient``, or ``return_hessian`` — so a consumer reading only
``properties`` still finds the answer.


Stamp provenance honestly
=========================

.. code-block:: json

   {
     "provenance": {
       "creator": "MyProgram",
       "version": "3.2.1",
       "routine": "myprogram.qcschema.run_single_point",
       "wall_time": 41.2,
       "nthreads": 8
     }
   }

``creator`` is your program's name, ``version`` must be `PEP 440
<https://www.python.org/dev/peps/pep-0440/>`_-sortable, and ``routine`` is the
specific entry point. ``Provenance`` permits extra keys, so timing and resource
detail belong here rather than in ``extras``.

Do not overwrite the provenance already on ``input_data`` or on ``molecule``. The
accumulation of provenance across a pipeline is the point.


Fail with a ``FailedOperation``
===============================

Never return a half-populated result. If the computation did not produce the
requested answer, return a :ref:`FailedOperation <model-failedoperation>`:

.. code-block:: python

   return FailedOperation(
       input_data=atomic_input,
       error=ComputeError(
           error_type="convergence_error",
           error_message=f"SCF did not converge in {maxiter} iterations.\n{tail_of_log}",
       ),
   )

Classify carefully — ``random_error`` invites a retry and ``input_error`` does
not, so schedulers act on the distinction. See
:doc:`../user_guide/errors`.


Serialize fully
===============

Emit every field the object has. In particular, do not strip unset or
default-valued fields on the way out: that removes ``schema_name`` and
``schema_version``, and the payload will fail validation at the other end.

Two rules govern what the JSON looks like:

- **Arrays serialize flat**, as lists of numbers — a gradient is
  :math:`3 N_{\text{atom}}` values, not a nested list of triples. See
  :doc:`conventions`.
- **Null-stripping applies to exactly five objects**: ``Molecule``,
  ``AtomicProperties``, ``WavefunctionProperties``, ``OptimizationProperties``,
  and ``ManyBodyProperties`` omit fields whose value is null. Everywhere else,
  emit the key.


A checklist
===========

.. list-table::
   :widths: 6 94
   :header-rows: 0

   * - ☐
     - ``schema_name`` and ``schema_version`` on every object
   * - ☐
     - ``input_data`` is the unmodified input you received
   * - ☐
     - top-level ``molecule`` is the frame your results belong to
   * - ☐
     - ``calcinfo_natom`` set, alongside the other ``calcinfo_*`` values
   * - ☐
     - ``return_result`` type matches the driver, and is duplicated into
       ``properties``
   * - ☐
     - every computed intermediate reported under its documented key
   * - ☐
     - arrays flat, coordinates in Bohr, energies in Hartree
   * - ☐
     - wavefunction matrices column-major, CCA basis-function order
   * - ☐
     - protocols honoured for wavefunction, stdout, and native files
   * - ☐
     - ``provenance`` names your program and version
   * - ☐
     - failures returned as ``FailedOperation`` with a classified ``error_type``
