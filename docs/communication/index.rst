Communication
=============

This document specifies the communication between the host computer and the
Controller.

Serial Communication
--------------------

115200 baud

Line Ending: ``\n\r`` (10 13)

Sequence Chart
--------------

.. image:: ../_static/sequence-chart.png
   :alt: sequence diagram for the communication between host and controller

Message Identifier Format
-------------------------

Message identifier format

0b"**AB**rr **CCCC**"

======= ===================== =====================
  Bit        Description             Values
======= ===================== =====================
A       message source
                              - 0 = host
                              - 1 = hardware
B	    message type
                              - 0 = request
                              - 1 = confirm
r	    reserved

CCCC	message identifier
======= ===================== =====================

Message definitions (API v4)
----------------------------

The length is the total length with id and parameters.

========== ========== ==== ====== =============================================
  source      name     id  length        parameters
========== ========== ==== ====== =============================================
host       .. _m4-01: 0x01 3      ``0xaa 0xbb``

           reqStart               - ``aa`` = startNeedle (Range: 0..198)
                                  - ``bb`` = stopNeedle  (Range: 1..199)
hardware   .. _m4-C1: 0xC1 2      ``0x0a``

           cnfStart               - ``a`` = success (0 = false, 1 = true)
hardware   .. _m4-82: 0x82 2      ``0xaa``

           reqLine                - ``aa`` = lineNumber (Range: 0..255)
host       .. _m4-42: 0x42 29     ``0xaa 0xbb[24, 23, 22, ... 1, 0] 0xcc 0xdd``

           cnfLine                - ``aa`` = lineNumber (Range: 0..255)
                                  - ``bb[24 to 0]`` = binary pixel data
                                  - ``cc`` = flags (bit 0: lastLine)
                                  - ``dd`` = CRC8 Checksum
host       .. _m4-03: 0x03 1

           reqInfo
hardware   .. _m4-C3: 0xC3 4      ``0xaa 0xbb 0xcc``

           cnfInfo                - ``aa`` = Version identifier
                                  - ``bb`` = Major Version
                                  - ``cc`` = Minor Version
hardware   .. _m4-84: 0x84 2      ``0x0a``

           indInit                - a = initialized (0 = false, 1 = true)
hardware   .. _m4-FF: 0xFF var    a debug string ending with ``\r\n``

           debug
========== ========== ==== ====== =============================================



.. _message-reqstart:

The ``reqStart`` Message
~~~~~~~~~~~~~~~~~~~~~~~~

The host starts the knitting process.

- implementation: :class:`RequestStart <AYABInterface.communication.host_messages.RequestStart>`
- table: :ref:`reqStart <m4-01>`
- requests answer: :ref:`message-cnfstart`
- direction: host → controller



.. _message-cnfstart:

The ``cnfStart`` Message
~~~~~~~~~~~~~~~~~~~~~~~~

The controller indicates the success of :ref:`message-reqstart`.

- implementation: :class:`~AYABInterface.communication.hardware_messages.ConfigurationStart`
- table: :ref:`reqStart <m4-C1>`
- answers: `The reqStart Message`_
- direction: controller → host


.. _message-reqline:

The ``reqLine`` Message
~~~~~~~~~~~~~~~~~~~~~~~

The controller requests a new line from the host.

- implementation: :class:`~AYABInterface.communication.hardware_messages.LineRequest`
- table: :ref:`reqLine <m4-82>`
- requests answer: `The cnfLine Message`_
- direction: controller → host


.. _message-cnfline:

The ``cnfLine`` Message
~~~~~~~~~~~~~~~~~~~~~~~

The host answers `The reqLine Message`_ with a line configuration.

- implementation: :class:`~AYABInterface.communication.host_messages.LineConfiguration`
- table: :ref:`cnfLine <m4-42>`
- answers: `The reqLine Message`_
- direction: host → controller


.. _message-reqinfo:

The ``reqInfo`` Message
~~~~~~~~~~~~~~~~~~~~~~~

The host initializes the handshake.

- implementation: :class:`~AYABInterface.communication.host_messages.InformationRequest`
- table: :ref:`reqInfo <m4-03>`
- requests answer: `The cnfInfo Message`_
- direction: host → controller


.. _message-cnfinfo:

The ``cnfInfo`` Message
~~~~~~~~~~~~~~~~~~~~~~~

The controller answers `The reqInfo Message`_ with the API version.

- implementation: :class:`~AYABInterface.communication.hardware_messages.ConfigurationInformation`
- table: :ref:`cnfInfo <m4-C3>`
- answers: `The reqInfo Message`_
- direction: controller → host


.. _message-indinit:

The ``indInit`` Message
~~~~~~~~~~~~~~~~~~~~~~~~

TODO: What is this? Is this indState?

- implementation: :class:`~AYABInterface.communication.hardware_messages.InitializationIndication`
- table: :ref:`indInit <m4-84>`
- direction: controller → host


.. _message-debug:

The ``debug`` Message
~~~~~~~~~~~~~~~~~~~~~

TODO: How to parse this message?

- implementation: :class:`~AYABInterface.communication.hardware_messages.Debug`
- table: :ref:`debug <m4-FF>`
- direction: controller → host


References
~~~~~~~~~~

.. seealso::
  - `the original specification
    <https://bitbucket.org/chris007de/ayab-apparat/wiki/english/Software/SerialCommunication>`__
  - the :mod:`hardware messages module
    <AYABInterface.communication.hardware_messages>`
    for messages sent by the hardware
  - the :mod:`host messages module
    <AYABInterface.communication.host_messages>`
    for messages sent by the host
