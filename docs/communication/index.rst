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
   name      source    id  length        parameters
========== ========== ==== ====== =============================================
reqStart   .. _m-01:  0x01 3      ``0xaa 0xbb``

                                  - ``aa`` = startNeedle (Range: 0..198)
           host                   - ``bb`` = stopNeedle  (Range: 1..199)
                                  
                                  .. seealso:: :class:`~AYABInterface.communication.host_messages.RequestStart`

cnfStart   .. _m-C1:  0xC1 2      ``0x0a``
           
           hardware               - ``a`` = success (0 = false, 1 = true)
           
                                  .. seealso:: :class:`~AYABInterface.communication.hardware_messages.ConfigurationStart`

reqLine    .. _m-82:  0x82 2      ``0xaa``

           hardware               - ``aa`` = lineNumber (Range: 0..255)
           
                                  .. seealso:: :class:`~AYABInterface.communication.hardware_messages.LineRequest`

cnfLine    .. _m-42:  0x42 29     ``0xaa 0xbb[24, 23, 22, ... 1, 0] 0xcc 0xdd``

           host                   - ``aa`` = lineNumber (Range: 0..255)
                                  - ``bb[24 to 0]`` = binary pixel data
                                  - ``cc`` = flags (bit 0: lastLine)
                                  - ``dd`` = CRC8 Checksum
                                  
                                  .. seealso:: :class:`~AYABInterface.communication.host_messages.LineConfiguration`

reqInfo    .. _m-03:  0x03 1      

           host

cnfInfo    .. _m-C3:  0xC3 4      ``0xaa 0xbb 0xcc``

           hardware               - ``aa`` = Version identifier
                                  - ``bb`` = Major Version
                                  - ``cc`` = Minor Version

indInit    .. _m-84:  0x84 2      ``0x0a``

           hardware               - a = initialized (0 = false, 1 = true)

debug      .. _m-FF:  0xFF var    a debug string ending with ``\r\n``

           hardware
========== ========== ==== ====== =============================================

.. seealso:: 
  - `the original specification
    <https://bitbucket.org/chris007de/ayab-apparat/wiki/english/Software/SerialCommunication>`__
  - the :mod:`hardware messages module
    <AYABInterface.communication.hardware_messages>`
    for messages sent by the hardware
  - the :mod:`host messages module
    <AYABInterface.communication.host_messages>`
    for messages sent by the host
