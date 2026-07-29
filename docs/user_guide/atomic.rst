.. _atomic:

==============================
Single points (Atomic)
==============================

A *single point* — one energy, gradient, Hessian, or property evaluation at one
fixed geometry — is the atom of QCSchema, and the family of objects describing it
is named accordingly. Everything else in the specification is built on top of
it.

.. code-block:: text

   AtomicInput          qcschema_atomic_input          molecule + specification
   └── AtomicSpecification   qcschema_atomic_specification   driver, model, keywords
       ├── Model                                       method + basis
       └── AtomicProtocols  qcschema_atomic_protocols   what output to keep

   AtomicResult         qcschema_atomic_result         input_data + results


.. _model-model:

Model
=====

The overall mathematical model used for the calculation. Another way to think
about this is *the largest superset that still gives roughly the same result*.
In QM this is the Hamiltonian (HF, DFT, …) combined with the basis; in MM it is
the force field and the atom-typer.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``method``
     - string
     - **required**
     - The quantum chemistry method to evaluate (e.g., B3LYP, PBE, ...). For MM, name of the force field.
   * - ``basis``
     - string or :ref:`BasisSet <model-basisset>`
     - \-
     - The quantum chemistry basis set to evaluate (e.g., 6-31g, cc-pVDZ, ...). Can be ``None`` for methods without basis sets. For molecular mechanics, name of the atom-typer.

.. code-block:: json

   {"model": {"method": "B3LYP", "basis": "cc-pVDZ"}}

``basis`` may be a plain name, a full :ref:`BasisSet <model-basisset>` object for
custom or program-generated bases, or ``null`` for methods that have no basis
set (semiempirical, most force fields):

.. code-block:: json

   {"model": {"method": "GFN2-xTB", "basis": null}}

``Model`` is one of the two objects that permit extra keys, so a program may
attach model-defining information the specification has not standardized yet.

.. note::

   ``method`` is not a controlled vocabulary. ``"B3LYP"``, ``"b3lyp"``, and
   ``"B3LYP-D3BJ"`` are all things programs accept, and normalizing them is the
   job of the adaptor layer (QCEngine), not the schema.


Driver
======

What you want computed. The ``driver`` determines the type of
``AtomicResult.return_result``.

.. list-table::
   :widths: 20 25 55
   :header-rows: 1

   * - ``driver``
     - ``return_result``
     - Notes
   * - ``energy``
     - number
     - Total energy of the requested method, in :math:`E_h`.
   * - ``gradient``
     - array, ``(nat, 3)``
     - First derivatives, :math:`E_h/a_0`. Stored flat.
   * - ``hessian``
     - array, ``(3*nat, 3*nat)``
     - Second derivatives, :math:`E_h/a_0^2`. Stored flat.
   * - ``properties``
     - object
     - A dictionary of named property values.

The first three drivers form a derivative ladder — ``energy`` is order 0,
``gradient`` order 1, ``hessian`` order 2 — which is why a program asked for a
gradient may also report the energy it computed along the way. ``properties`` sits
outside that ladder at order 0.


.. _model-atomicspecification:

AtomicSpecification
===================

:``schema_name``: ``qcschema_atomic_specification``

How to run a single point, with no reference to *what* it runs on. Keeping these
fields in their own object is what makes them reusable — one specification can be
applied to many molecules, and nested inside a procedure that needs a single point
computed.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_atomic_specification"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``keywords``
     - object
     - \-
     - The program specific keywords to be used.
   * - ``program``
     - string
     - default ``""``
     - The program for which the Specification is intended.
   * - ``driver``
     - ``energy``, ``gradient``, ``hessian``, ``properties``
     - **required**
     - What the computation should return.
   * - ``model``
     - :ref:`Model <model-model>`
     - **required**
     - The computational model to run: method plus basis.
   * - ``protocols``
     - :ref:`AtomicProtocols <model-atomicprotocols>`
     - \-
     - Directives for how much of the output to retain.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the computation. Use for schema development and scratch space.

``keywords`` is the deliberate escape hatch for everything program-specific.
QCSchema neither standardizes nor validates its contents:

.. code-block:: json

   {
     "keywords": {
       "scf_type": "df",
       "e_convergence": 1e-8,
       "freeze_core": true
     }
   }

``program`` names the code the specification targets. It is informational — it
exists so a specification can be stored and passed around on its own — and a
runner is not obliged to act on it. Do not rely on it to route a computation.

.. tip::

   Build the specification once and reuse it — that is the whole point of the
   object existing. One specification object, many inputs:

   .. code-block:: text

      specification  ──┬──▶  AtomicInput(molecule=A, specification=spec)
                       ├──▶  AtomicInput(molecule=B, specification=spec)
                       └──▶  AtomicInput(molecule=C, specification=spec)

   The same object also drops straight into an
   :ref:`OptimizationSpecification <model-optimizationspecification>` as the
   gradient producer, unchanged.


.. _model-atomicprotocols:

AtomicProtocols
===============

:``schema_name``: ``qcschema_atomic_protocols``

How much output to keep. Wavefunctions and program scratch files can dwarf the
rest of a record, so the defaults throw them away.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_atomic_protocols"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``wavefunction``
     - ``all``, ``orbitals_and_eigenvalues``, ``occupations_and_eigenvalues``, ``return_results``, ``none``
     - default ``"none"``
     - Wavefunction to keep from a computation.
   * - ``stdout``
     - boolean
     - default ``true``
     - Primary output file to keep from the computation
   * - ``error_correction``
     - :ref:`ErrorCorrectionProtocol <model-errorcorrectionprotocol>`
     - \-
     - Policies for error correction
   * - ``native_files``
     - ``all``, ``input``, ``none``
     - default ``"none"``
     - Policies for keeping processed files from the computation

Protocols are enforced by the *result* constructor, not merely advisory: if the
protocol says ``wavefunction: none``, a wavefunction handed to ``AtomicResult``
is dropped rather than stored. Full detail, including each enum's values, is in
:doc:`../implementation_guide/protocols`.


.. _model-atomicinput:

AtomicInput
===========

:``schema_name``: ``qcschema_atomic_input``
:``schema_version``: 2

A molecule plus a specification: a complete, runnable request.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``id``
     - string
     - \-
     - The optional ID for the computation.
   * - ``schema_name``
     - ``"qcschema_atomic_input"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``schema_version``
     - ``2``
     - \-
     - The version of ``schema_name`` this conforms to. Fixed value.
   * - ``molecule``
     - :ref:`Molecule <model-molecule>`
     - **required**
     - The molecule to use in the computation.
   * - ``specification``
     - :ref:`AtomicSpecification <model-atomicspecification>`
     - **required**
     - Additional fields specifying how to run the single-point computation.
   * - ``provenance``
     - :ref:`Provenance <model-provenance>`
     - \-
     - Information about what created this input.

.. code-block:: json

   {
     "schema_name": "qcschema_atomic_input",
     "schema_version": 2,
     "molecule": {"schema_name": "qcschema_molecule", "schema_version": 3,
                  "symbols": ["He"], "geometry": [0.0, 0.0, 0.0]},
     "specification": {
       "schema_name": "qcschema_atomic_specification",
       "driver": "energy",
       "model": {"method": "HF", "basis": "cc-pVDZ"},
       "keywords": {}
     }
   }


.. _model-atomicresult:

AtomicResult
============

:``schema_name``: ``qcschema_atomic_result``
:``schema_version``: 2

Everything that came out, plus the input that produced it.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_atomic_result"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``schema_version``
     - ``2``
     - \-
     - The version of ``schema_name`` this conforms to. Fixed value.
   * - ``id``
     - string
     - \-
     - The optional ID for the computation.
   * - ``input_data``
     - :ref:`AtomicInput <model-atomicinput>`
     - **required**
     - The complete input that produced this result.
   * - ``molecule``
     - :ref:`Molecule <model-molecule>`
     - **required**
     - The molecule with the frame and orientation of the results.
   * - ``properties``
     - :ref:`AtomicProperties <model-atomicproperties>`
     - **required**
     - Named properties computed along the way.
   * - ``wavefunction``
     - :ref:`WavefunctionProperties <model-wavefunctionproperties>`
     - \-
     - Wavefunction quantities — orbitals, densities, Fock matrices. Presence and contents controlled by the ``wavefunction`` protocol.
   * - ``return_result``
     - number or array[number] or object
     - **required**
     - The primary return specified by the ``driver`` field. Scalar if energy; array if gradient or hessian; dictionary with property keys if properties.
   * - ``stdout``
     - string
     - \-
     - The primary logging output of the program, whether natively standard output or a file. Presence vs. absence (or null-ness?) configurable by protocol.
   * - ``stderr``
     - string
     - \-
     - The standard error of the program execution.
   * - ``native_files``
     - object
     - \-
     - Program-native files retained from the computation. Contents controlled by the ``native_files`` protocol.
   * - ``success``
     - ``true``
     - \-
     - The success of program execution. If False, other fields may be blank.
   * - ``provenance``
     - :ref:`Provenance <model-provenance>`
     - **required**
     - Information about the program that produced this result.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the computation. Use for schema development and scratch space.

Reading a result
----------------

Where to look for what, as field paths from the top of the result object:

.. code-block:: text

   return_result                            the primary answer
   properties.scf_total_energy              named intermediates
   molecule                                 frame the results are in
   input_data.molecule                      frame that was submitted
   input_data.specification.model.method    what was asked for
   provenance.creator                       which program answered

Three fields deserve attention.

``input_data``
   The complete :ref:`AtomicInput <model-atomicinput>` that produced this result.
   A result is therefore a self-contained record: store one object and you have the
   full trace from request to answer.

``molecule`` (top level)
   The frame and orientation the results are expressed in. With the default
   ``fix_com=false`` and ``fix_orientation=false``, a program is free to
   translate and rotate, so this often differs from
   ``input_data.molecule``. Per-atom results — gradients, Hessians — belong to
   *this* molecule.

``success``
   Fixed to ``true``. An ``AtomicResult`` cannot describe a failure, and there is
   no ``error`` field. Failures are :ref:`FailedOperation <model-failedoperation>`
   objects instead; see :doc:`errors`.

``extras`` on the result is independent of ``input_data.specification.extras``, so
a driver's input annotations survive a program writing its own.


.. seealso::

   :doc:`../implementation_guide/migrating_from_v1` for the field-by-field
   mapping from QCSchema v1, if you have existing v1 payloads or code.
