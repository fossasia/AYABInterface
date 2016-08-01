Communication Specification
===========================

This document specifies the communication between the host and a controller
with the
`AYAB firmware <https://github.com/AllYarnsAreBeautiful/ayab-firmware>`_.

Serial Communication
--------------------

115200 baud

Line Ending: ``\n\r`` (10 13)
Each message ends with a Line Ending.

Sequence Chart
--------------

.. image:: ../_static/sequence-chart.png
   :alt: sequence diagram for the communication between host and controller

The host waits for a **indState(true)** message before requesting to start the knitting.
On startup, the Arduino continuously checks for the initialization of the machine (carriage passed left hall sensor).
When this happens, it sends an **indState(true)** to tell the host that the machine is ready to knit.
After receiving this message, the host sends a **reqStart** message, which is immediately confirmed with a **cnfStart** message.
When **reqStart** was successful, the Arduino begins to poll the host for line data with **reqLine**, the host answers with **cnfLine**.
This reqLine/cnfLine happens each time the carriage moves passed the borders given by the Start/StopNeedle parameters in **reqStart**.
When the host does not have any more lines to send, it marks the last line with the *lastLine* flag in its last **cnfLine** message.

To see an example implementation, see the :mod:`states of the communication
module <AYABInterface.communication.states>`.

.. _message-identifier-format:

Message Identifier Format
-------------------------

Messages start with a byte that identifies their type. This byte is called
"id" or "message id" in the following document. This table lists all the bits
of this byte and assigns their purpose:

+-----+-------+--------------------+------------------------------------------+
| Bit | Value |        Name        |         Description and Values           |
+=====+=======+====================+==========================================+
|     |       |                    | - 0 = the message is from the host       |
|  7  |  128  | message source     | - 1 = the message is from the controller |
|     |       |                    |                                          |
+-----+-------+--------------------+------------------------------------------+
|     |       |                    | - 0 = the message is a request           |
|  6  |   64  | message type       | - 1 = the message is a confirmation      |
|     |       |                    |   of a request                           |
+-----+-------+--------------------+------------------------------------------+
|  5  |   32  |                    |                                          |
+-----+-------+ reserved           | must be zero                             |
|  4  |   16  |                    |                                          |
+-----+-------+--------------------+------------------------------------------+
|  3  |    8  |                    |                                          |
+-----+-------+                    | These are the values that identify the   |
|  2  |    4  |                    | message.                                 |
+-----+-------+ message identifier |                                          |
|  1  |    2  |                    | .. seealso::                             |
+-----+-------+                    |    :ref:`message-definitions-v4`         |
|  0  |    1  |                    |                                          |
+-----+-------+--------------------+------------------------------------------+

.. _message-definitions-v4:

Message definitions (API v4)
----------------------------

The length is the total length with :ref:`id <message-identifier-format>`
and parameters. Note that the two characters ``\r\n`` following the message are
not included in the length.

========== ========== ==== ====== =============================================
  source      name     id  length        parameters
========== ========== ==== ====== =============================================
host       .. _m4-01: 0x01 3      ``0xaa 0xbb``

           reqStart_              - ``aa`` = left end needle (Range: 0..198)
                                  - ``bb`` = right end needle (Range: 1..199)

                                  Start and
hardware   .. _m4-C1: 0xC1 2      ``0x0a``

           cnfStart_              - ``a`` = success (0 = false, 1 = true)
hardware   .. _m4-82: 0x82 2      ``0xaa``

           reqLine_               - ``aa`` = line number (Range: 0..255)
host       .. _m4-42: 0x42 29     ``0xaa 0xbb[24, 23, 22, ... 1, 0] 0xcc 0xdd``

           cnfLine_               - ``aa`` = line number (Range: 0..255)
                                  - ``bb[24 to 0]`` = binary pixel data
                                  - ``cc`` = flags (bit 0: lastLine)
                                  - ``dd`` = CRC8 Checksum
host       .. _m4-03: 0x03 1

           reqInfo_
hardware   .. _m4-C3: 0xC3 4      ``0xaa 0xbb 0xcc``

           cnfInfo_               - ``aa`` = API Version Identifier
                                  - ``bb`` = Firmware Major Version
                                  - ``cc`` = Firmware Minor Version
hardware   .. _m4-84: 0x84 8      ``0x0a 0xBB 0xbb 0xCC 0xcc 0xdd 0xee``

           indState_              - ``a`` = ready (0 = false, 1 = true)
                                  - ``BBbb`` = :class:`int` left hall sensor value
                                  - ``CCcc`` = :class:`int` right hall sensor value
                                  - ``dd`` = the carriage

                                    - ``0`` = no carriage detected
                                    - ``1`` = knit carriage "Strickschlitten"
                                    - ``2`` = hole carriage "Lochmusterschlitten"
                                  - ``ee`` = the needle number currently in progress
hardware   .. _m4-23: 0x23 var    A debug string. The id is the character ``#``.
                                  The length is variable and can be determined
           debug_                 by the end ``\r\n'``.
host       .. _m4-04: 0x04 1      put the controller into test mode

           reqTest_
host       .. _m4-C4: 0xC4 2      ``0x0a``

           cnfTest_               - ``a`` = success (0 = false, 1 = true)
========== ========== ==== ====== =============================================



.. _reqstart:

The ``reqStart`` Message
~~~~~~~~~~~~~~~~~~~~~~~~

The host starts the knitting process.

- Python: :class:`StartRequest <AYABInterface.communication.host_messages.StartRequest>`
- Arduino: `h_reqStart <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/ayab.ino#L57>`__
- table: :ref:`reqStart <m4-01>`
- requests answer: :ref:`cnfstart`
- direction: host → controller


.. _cnfstart:

The ``cnfStart`` Message
~~~~~~~~~~~~~~~~~~~~~~~~

The controller indicates the success of :ref:`reqstart`.

- Python: :class:`~AYABInterface.communication.hardware_messages.StartConfirmation`
- Arduino: `h_reqStart <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/ayab.ino#L74>`__
- table: :ref:`reqStart <m4-C1>`
- answers: :ref:`reqStart`
- direction: controller → host


.. _reqline:

The ``reqLine`` Message
~~~~~~~~~~~~~~~~~~~~~~~

The controller requests a new line from the host.

More than 256 lines are supported.
There are three possibilities for the next line based on the last line:

1. the new line is greater than the last line
2. the new line is lower than the last line
3. the new line is the last line

We choose the line closest to the last line. This is trivial for (3).
In case two lines are equally distant from the last line, we choose the
smaller line.

This is computed by the function :func:`AYABInterface.utils.next_line` which
is tested and can be seen as a reference implementation for other languages.

- Python: :class:`~AYABInterface.communication.hardware_messages.LineRequest`
- Arduino: `Knitter::reqLine <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/knitter.cpp#L366>`__
- table: :ref:`reqLine <m4-82>`
- requests answer: :ref:`cnfLine`
- direction: controller → host


.. _cnfline:

The ``cnfLine`` Message
~~~~~~~~~~~~~~~~~~~~~~~

The host answers :ref:`reqLine` with a line configuration.

.. _byte-cnfline-v4:

This table shows the message content without the first byte that identifies the
message:

+------+---------------+------------------------------------------------------+
| Byte |     Name      |                     Description                      |
+======+===============+======================================================+
|      |               | These are the lowest 8 bit of the line. They must    |
|  0   | line number   | match the line number in :ref:`reqLine`.             |
|      |               |                                                      |
+------+---------------+------------------------------------------------------+
|  1   |               | Each bit of the bytes represents a needle position.  |
+------+               |                                                      |
|  2   |               | - 0 = "B"                                            |
+------+               | - 1 = "D"                                            |
| ...  | needle        |                                                      |
+------+ positions     | For the exact mapping of bits to needles see the     |
|  24  |               | :ref:`table below <bit-needle-position-mapping-v4>`. |
+------+               |                                                      |
|  25  |               |                                                      |
+------+---------------+------------------------------------------------------+
|      |               | Bits: ``0000000L``                                   |
|  26  | flags         |                                                      |
|      |               | - ``L`` - "LastLine" (0 = false, 1 = true)           |
+------+---------------+------------------------------------------------------+
|      |               | This checksum is computed from bytes 0 to 26, \      |
|  27  | crc8 checksum | including byte 26. The controller may use this       |
|      |               | checksum to check the result and if the checksum     |
|      |               | does not match, it can send :ref:`reqLine` anew.     |
+------+---------------+------------------------------------------------------+

.. _bit-needle-position-mapping-v4:

In the following table, you can see the mapping of bytes to needles.

.. note::
  - The **Needles** are counted from the leftmost needle on the machine.
  - The **Needle** count starts with ``0``.
  - The **Byte** numbering is taken from :ref:`the table above <byte-cnfline-v4>`.
  - The **Bit** numbering is consistent with :ref:`message-identifier-format`.
    The highest bit has the number 7 and the lowest bit has number 0.

+--------+-------------------------------+-------------------------------+-----+-------------------------------+-------------------------------+
| Byte   |               1               |               2               |     |              24               |               25              |
+--------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+-----+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| Bit    | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | ... | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
+--------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+-----+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| Needle | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |                         ...                                                         |198|199|
+--------+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+-----+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

- Python: :class:`~AYABInterface.communication.host_messages.LineConfirmation`
- Arduino: `h_cnfLine <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/ayab.ino#L80>`__
- table: :ref:`cnfLine <m4-42>`
- answers: :ref:`reqLine`
- direction: host → controller


.. _reqinfo:

The ``reqInfo`` Message
~~~~~~~~~~~~~~~~~~~~~~~

The host initializes the handshake.

- Python: :class:`~AYABInterface.communication.host_messages.InformationRequest`
- Arduino: `h_reqInfo <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/ayab.ino#L110>`__
- table: :ref:`reqInfo <m4-03>`
- requests answer: :ref:`reqInfo`
- direction: host → controller


.. _cnfinfo:

The ``cnfInfo`` Message
~~~~~~~~~~~~~~~~~~~~~~~

The controller answers :ref:`reqinfo` with the API version.

- Python: :class:`~AYABInterface.communication.hardware_messages.InformationConfirmation`
- Arduino: `h_reqInfo <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/ayab.ino#L112>`__
- table: :ref:`cnfInfo <m4-C3>`
- answers: :ref:`reqinfo`
- direction: controller → host


.. _indstate:

The ``indState`` Message
~~~~~~~~~~~~~~~~~~~~~~~~

This is sent when the controller indicates its state.
When ``ready`` it is

- ``1``, then this is the first state indication. The machine is now
  ready to knit
- ``0``, the controller is in test mode. This message is sent periodically.
  :ref:`reqTest` switches this on.

- Python: :class:`~AYABInterface.communication.hardware_messages.StateIndication`
- Arduino: `Knitter::indState <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/knitter.cpp#L375>`__
- table: :ref:`indState <m4-84>`
- direction: controller → host


.. _debug:

The ``debug`` Message
~~~~~~~~~~~~~~~~~~~~~

This message ends with a ``\r\n`` like evey message.
It contains debug information from the controller.

- Python: :class:`~AYABInterface.communication.hardware_messages.Debug`
- Arduino: `DEBUG_PRINT <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/debug.h#L32>`__
- table: :ref:`debug <m4-23>`
- direction: controller → host


.. _reqtest:

The ``reqTest`` Message
~~~~~~~~~~~~~~~~~~~~~~~

This message puts the controller in a test mode instead of a knitting mode.


- Python: :class:`~AYABInterface.communication.host_messages.TestRequest`
- Arduino: `h_reqTest <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/ayab.ino#L119>`__
- table: :ref:`reqTest <m4-04>`
- requests answer: :ref:`cnfTest`
- direction: host → controller


.. _cnftest:

The ``cnfTest`` Message
~~~~~~~~~~~~~~~~~~~~~~~

This messsage confirms whether the controller is in the test mode.
If success is indicated, the controller sends :ref:`indstate` messages
periodically, containing the sensor and position values.

- Python: :class:`~AYABInterface.communication.hardware_messages.TestConfirmation`
- Arduino: `h_reqTest <https://github.com/AllYarnsAreBeautiful/ayab-firmware/blob/c236597c6fdc6d320f9f2db2ebeb17d64c438b64/ayab.ino#L119>`__
- table: :ref:`cnfTest <m4-C4>`
- answers: :ref:`reqTest`
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
  - `a discussion about the specification
    <https://github.com/AllYarnsAreBeautiful/ayab-desktop/issues/17>`__
