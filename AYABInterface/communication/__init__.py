"""This module is used to communicate with the shield.

Requirement: Make objects from binary stuff.
"""
from abc import ABCMeta, abstractmethod, abstractproperty
from .hardware_messages import read_message_type, ConnectionClosed


class Content(object, metaclass=ABCMeta):

    """The interface used by the Communication.

    This class is the interface that the :class:`Communication` requires.

    This class does no validity checks, it assumes the :class:`Configuration`
    is valid and there are only valid parameters given to the methods.

    In the message specification, the term 'line' equivalent to 'row'.

    .. seealso:: :class:`AYABInterface.interface.NeedlePositions`

    .. _communication-rows:

    When we talk about a row, we talk about a list

    - containing :attr:`needle positions
      <AYABInterface.machines.Machine.needle_positions>`
    - with a length of :attr:`the number of needles
      <AYABInterface.machines.Machine.number_of_needles>`.

    """

    @abstractproperty
    def machine(self):
        """The machine for the Communication.

        :rtype: AYABInterface.machines.Machine
        """

    @abstractproperty
    def api_version(self):
        """
        :rtype: int
        :returns: The API version of this interface
        """

    @abstractmethod
    def row_completed(self, index):
        """Mark the row at index as completed.

        :param int index: the index in the rows

        Invalid indices are ignored, no Exception is raised.
        """

    @abstractmethod
    def get_row(self, index, default=None):
        """Return the row at an index.

        :param int index:
        :return:

          - If there is a :ref:`row <communication-rows>` at this index,
            this returns the row.
          - If there is no row at this index, this returns :paramref:`default`.
        """

    @abstractmethod
    def handle_msg(self, input):
        """Handle incoming bytearray, return message.

        Valid message types are (APIv4):

        - cnfStart (0xc1)

          - success (bool)

        - cnfInfo (0xc3)

          - api_version (uint8)

        - cnfTest (0xc4)

          - success (bool)

        - reqLine (0x82)

          - line_number (uint8)

        - indState (0x84)

          - hall_left (uint16)
          - hall_right (uint16)
          - carriage_type (enum)
          - carriage_position (uint8)

        :param bytes input: Sequence of chars, coming from the communication
          layer.

        :return:

          - If the data contains a valid message, the message type and
            its parameters are returned.
          - If the data does not contain a valid message, message type none is
            returned.
        """

    @abstractmethod
    def req_start(self, left_end_needle, right_end_needle):
        """Start request message.

        This acts as a setup message, to tell the controller the basic
        parameters of operation.

        :param int left_end_needle: Left end needle of knitting piece
          formerly known as 'startNeedle')
        :param int right_end_needle: Right end needle of knitting piece
          formerly known as 'stopNeedle')
        """

    @abstractmethod
    def req_info(self):
        """Information request message.
        """

    @abstractmethod
    def req_test(self):
        """Put controller into 'test' mode.
        """

    @abstractmethod
    def cnf_line(self, line_number, line_data, last_line):
        """Line confirm message.

        The data sent here is parsed by the Arduino controller to set the
        knitting needles accordingly in the next carriage run.

        :param int line_number: Same line number as given in the req_line
          message
        :param row line_data: The bytearray to be sent to needles.
        :param bytes last_line: Indicates whether this is the last line to
          knit.

        Flags are given as parameters to this method explicitly,
        conversion to byte represenation is done here, as this is protocol
        knowledge.

        - Bit 0: Last line (indicate that this is the last line of the pattern.

        CRC8 is currently not checked in the controller.

        .. todo:: Calculate CRC8 in this method, as it is part of the protocol
        """


class _Communication(object):

    """This class comunicates with the AYAB shield."""

    def __init__(self, file):
        """Create a new Communication object.

        :param file: a file-like object with read and write methods for the
          communication with the Arduino. This could be a
          :class:`serial.Serial` or a :meth:`socket.socket.makefile`.
        """
        self._file = file

    def start(self, content):
        """Start the communication about a content.

        :param Content content: the content of the communication.
        """

    def stop(self):
        """Stop the communication with the shield."""


class Communication(object):

    """This class comunicates with the AYAB shield."""

    def __init__(self, file, get_needle_positions, machine,
                 on_message_received=[]):
        """Create a new Communication object.

        :param file: a file-like object with read and write methods for the
          communication with the Arduino. This could be a
          :class:`serial.Serial` or a :meth:`socket.socket.makefile`.
        """
        self._file = file
        self._get_needle_positions = get_needle_positions
        self._on_message_received = on_message_received
        self._machine = machine
        self._started = False
        self._stopped = False
        self._last_requested_line = (None, None)
        
    @property
    def machine(self):
        """The machine type to communicate with.
        
        :rtype: AYABInterface.machines.Machine
        """
        
    def get_needle_positions(self, line_number):
        """The needle positions for a line with a number.
        
        :param int line_number: the number of the line
        :rtype: list
        :return: the needle positions for a specific line specified by 
          :paramref:`line_number`
        """

    def get_needle_position_bytes(self, line_number):
        """Get the bytes representing needle positions or None.
        
        :param int line_number: the line number to take the bytes from
        :rtype: bytes
        :return: the bytes that represent the message or :obj:`None` if no
          data is there for the line.
        
        Depending on the :attr:`machine`, the length and result may vary.
        """
        if self._last_requested_line[0] == line_number:
            return self._last_requested_line[1]
        needle_positions = self._get_needle_positions(line_number)
        if needle_positions is None:
            return None
        bytes_ = self._machine.needle_positions_to_bytes(needle_positions)
        self._last_requested_line = (line_number, bytes_)
        return bytes_
        
    def get_line_configuration_message(self, line_number):
        """Return the cnfLine content without id for the line.
        
        :param int line_number: the number of the line
        :rtype: bytes
        :return: a cnfLine message as defined in :ref:`cnfLine` 
        """

    def start(self):
        """Start the communication about a content.

        :param Content content: the content of the communication.
        """
        self._started = True

    _read_message_type = staticmethod(read_message_type)

    def _message_received(self, message):
        """Notify the observers about the received message."""
        for callable in self._on_message_received:
            callable(message)

    def receive_message(self):
        """Receive a message from the file."""
        assert self._started and not self._stopped
        message_type = self._read_message_type(self._file)
        message = message_type(self._file, self)
        if message.wants_to_answer():
            message.send_answer()
        self._message_received(message)

    def stop(self):
        """Stop the communication with the shield."""
        self._stopped = True
        self._message_received(ConnectionClosed(self._file, self))


__all__ = ["Communication", "Content"]
