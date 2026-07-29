.. _errors:

=======================
Errors and provenance
=======================

Two small objects show up everywhere: one describing how a computation failed,
and one describing who produced it.


Failures are a separate type
============================

A result object always describes a success. ``AtomicResult.success``,
``OptimizationResult.success``, and ``TorsionDriveResult.success`` are all fixed to
``true``, and none of them has an ``error`` field.

A failure is a :ref:`FailedOperation <model-failedoperation>` instead.

.. code-block:: text

   success ──┬── AtomicResult / OptimizationResult / ...    success: true
             └── FailedOperation                            success: false

Because both carry ``success``, a consumer can branch before knowing what it
holds:

So a consumer reads ``success`` first: if ``true`` the payload is a result and
``return_result`` is present; if ``false`` it is a ``FailedOperation`` and
``error`` is present. Neither object can be in the other state, so no third case
needs handling.

What you gain is that a result can no longer lie about itself. There is no such
thing as a v2 ``AtomicResult`` with a missing ``return_result`` and an
apologetic error attached; if it validates, the numbers are there.


.. _model-failedoperation:

FailedOperation
===============

:``schema_name``: ``qcschema_failed_operation``
:``schema_version``: 2

A record that a given operation — program, procedure, whatever — failed, carrying
both the reason and the input that provoked it.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``schema_name``
     - ``"qcschema_failed_operation"``
     - \-
     - The QCSchema object this conforms to. Fixed value.
   * - ``schema_version``
     - ``2``
     - \-
     - The version of ``schema_name`` this conforms to. Fixed value.
   * - ``id``
     - string
     - \-
     - A unique identifier for this record, often the identifier the operation would have carried had it succeeded. Usually set programmatically by a database.
   * - ``input_data``
     - object
     - \-
     - The complete input which, when run, caused the operation to fail. Untyped, because a payload that failed *because* it was malformed cannot be validated as any input object.
   * - ``success``
     - ``false``
     - \-
     - A boolean indicator that the operation failed consistent with the model of successful operations. Should always be False. Allows programmatic assessment of all operations regardless of if they failed or succeeded
   * - ``error``
     - :ref:`ComputeError <model-computeerror>`
     - **required**
     - Details of the error that failed this operation.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the failed operation. Details pertaining specifically to a thrown error belong in the ``error`` field. See ``ComputeError`` for details.

.. code-block:: json

   {
     "schema_name": "qcschema_failed_operation",
     "schema_version": 2,
     "success": false,
     "input_data": {"schema_name": "qcschema_atomic_input", "...": "..."},
     "error": {
       "error_type": "convergence_error",
       "error_message": "SCF failed to converge after 100 iterations."
     },
     "extras": {}
   }

``input_data`` is intentionally untyped: a ``FailedOperation`` may wrap an atomic
input, an optimization input, or — importantly — a payload that failed *because it
was malformed* and therefore cannot be validated as any of them. It should be the
complete input that, when run, caused the failure.

``id`` often carries the identifier the successful operation would have had, so a
database can slot the failure into the same place the result would have gone.


.. _model-computeerror:

ComputeError
============

A complete description of the error from an unsuccessful program execution.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``error_type``
     - string
     - **required**
     - The type of error thrown, as a short classifier such as ``input_error``.
   * - ``error_message``
     - string
     - **required**
     - Text associated with the thrown error. This is often the backtrace, but it can contain additional information as well.
   * - ``extras``
     - object
     - \-
     - Additional information to bundle with the error.

``error_type`` should be a short classifier, not a sentence. The enumeration is
not yet strict — the schema accepts any string — but the widely used classifiers
come from `QCEngine's exceptions
<https://github.com/MolSSI/QCEngine/blob/master/qcengine/exceptions.py>`_:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - ``error_type``
     - Meaning
   * - ``input_error``
     - The input was malformed or asked for something impossible.
   * - ``convergence_error``
     - An iterative procedure failed to converge.
   * - ``memory_error``
     - The computation needed more memory than was available.
   * - ``random_error``
     - A transient failure; retrying may succeed.
   * - ``resource_error``
     - Disk, time limit, or other resource exhaustion.
   * - ``unknown_error``
     - Everything else.

The distinction that matters operationally is ``random_error`` versus the rest: a
scheduler can retry a random error and should not retry an input error.

``error_message`` is the human-readable detail. It is often a backtrace, and it
may contain program output. Put structured detail in ``extras`` rather than
encoding it into the message.

.. tip::

   Resist the urge to put the whole output file in ``error_message``. If you want
   the log, that is what the ``stdout`` protocol and ``native_files`` are for.


.. _model-provenance:

Provenance
==========

A short description of what created an object. Present on molecules, inputs, and
results.

.. list-table::
   :widths: 18 18 18 46
   :header-rows: 1

   * - Field
     - Type
     - Notes
     - Description
   * - ``creator``
     - string
     - **required**
     - The name of the program, library, or person that created the object.
   * - ``version``
     - string
     - default ``""``
     - The version of the creator, blank otherwise. This should be sortable by the very broad `PEP 440 <https://www.python.org/dev/peps/pep-0440/>`_.
   * - ``routine``
     - string
     - default ``""``
     - The name of the routine or function within the creator, blank otherwise.

.. code-block:: json

   {
     "provenance": {
       "creator": "Psi4",
       "version": "1.9",
       "routine": "psi4.schema_runner"
     }
   }

``version`` should be sortable by `PEP 440
<https://www.python.org/dev/peps/pep-0440/>`_ — this is a broad requirement, but
it rules out formats that cannot be ordered.

``Provenance`` is one of the two objects that permit **extra keys**, and this is
by design: it is the right place for richer execution detail such as wall time,
core count, host name, or compiler information.

.. code-block:: json

   {
     "provenance": {
       "creator": "Psi4",
       "version": "1.9",
       "routine": "psi4.schema_runner",
       "wall_time": 41.2,
       "nthreads": 8,
       "hostname": "node014",
       "memory": 4.0
     }
   }

Provenance accumulates rather than being overwritten. An
:ref:`AtomicResult <model-atomicresult>` produced from an
:ref:`AtomicInput <model-atomicinput>` has its own provenance naming the program
that ran it, while ``input_data.provenance`` still names whatever built the
input, and ``molecule.provenance`` names whatever built the molecule. A payload
that has passed through a driver, an optimizer, and a QC program carries all
three.

.. note::

   Provenance is the mechanism behind one of the project's founding goals:
   providing a rigorous record of computation for large-scale QC databases. A
   result whose provenance is complete can be traced, audited, and reproduced.
