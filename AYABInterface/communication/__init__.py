"""This module is used to communicate with the shield.

Requirement: Make objects from binary stuff.
"""
from abc import ABCMeta, abstractmethod, abstractproperty
from .hardware_messages import read_message_type, ConnectionClosed
from .states import WaitingForStart
from .cache import NeedlePositionCache


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
                 on_message_received=(), left_end_needle=None, 
                 right_end_needle=None):
        """Create a new Communication object.

        :param file: a file-like object with read and write methods for the
          communication with the Arduino. This could be a
          :class:`serial.Serial` or a :meth:`socket.socket.makefile`.
        :param get_needle_positions: a callable that takes an :class:`index
          <int>` and returns :obj:`None` or an iterable over needle positions.
        :param AYABInterface.machines.Machine machine: the machine to use for
          knitting
        :param list on_message_received: an iterable over callables that takes
          a received :class:`message
          <AYABInterface.communication.hardware_messages.Message>` whenever
          it comes in. Since :attr:`state` changes only take place when a
          message is received, this can be used as an state observer.
        :param left_end_needle: A needle number on the machine.
          Other needles that are on the left side of this needle are not used
          for knitting. Their needle positions are not be set.
        :param right_end_needle: A needle number on the machine.
          Other needles that are on the right side of this needle are not used
          for knitting. Their needle positions are not be set.
          
        """
        self._file = file
        self._on_message_received = on_message_received
        self._machine = machine
        self._state = WaitingForStart(self)
        self._controller = None
        self._last_requested_line_number = 0
        self._needle_positions_cache = NeedlePositionCache(
            get_needle_positions, self._machine)
        self._left_end_needle = (
            machine.left_end_needle
            if left_end_needle is None else left_end_needle)
        self._right_end_needle = (
            machine.right_end_needle
            if right_end_needle is None else right_end_needle)

    @property
    def needle_positions(self):
        """A cache for the needle positions.

        :rtype: AYABInterface.communication.cache.NeedlePositionCache
        """
        return self._needle_positions_cache

    def start(self):
        """Start the communication about a content.

        :param Content content: the content of the communication.
        """
        self._state.communication_started()

    _read_message_type = staticmethod(read_message_type)

    def _message_received(self, message):
        """Notify the observers about the received message."""
        self._state.receive_message(message)
        for callable in self._on_message_received:
            callable(message)

    def receive_message(self):
        """Receive a message from the file."""
        assert not self._state.is_waiting_for_start() and \
            not self._state.is_connection_closed()
        message_type = self._read_message_type(self._file)
        message = message_type(self._file, self)
        self._message_received(message)

    def stop(self):
        """Stop the communication with the shield."""
        self._message_received(ConnectionClosed(self._file, self))

    def api_version_is_supported(self, api_version):
        """Return whether an api version is supported by this class.

        :rtype: bool
        :return: if the :paramref:`api version <api_version>` is supported
        :param int api_version: the api version

        Currently supported api versions: ``4``
        """
        return api_version == 4

    def send(self, host_message_class, *args):
        """Send a host message.

        :param type host_message_class: a subclass of
          :class:`AYABImterface.communication.host_messages.Message`
        :param args: additional arguments that shall be passed to the
          :paramref:`host_message_class` as arguments
        """
        message = host_message_class(self._file, self, *args)
        message.send()

    @property
    def state(self):
        """The state this object is in.

        :return: the state this communication object is in.
        :rtype: AYABInterface.communication.states.State
        """
        return self._state

    @state.setter
    def state(self, new_state):
        """Set the state."""
        self._state.exit()
        self._state = new_state
        self._state.enter()

    @property
    def left_end_needle(self):
        """The left end needle of the needle positions.

        :rtype: int
        :return: the :attr:`left end needle of the machine
          <AYABInterface.machine.Machine.left_end_needle>`
        """
        return self._left_end_needle

    @property
    def right_end_needle(self):
        """The left end needle of the needle positions.

        :rtype: int
        :return: the :attr:`right end needle of the machine
          <AYABInterface.machine.Machine.right_end_needle>`
        """
        return self._right_end_needle

    @property
    def controller(self):
        """Information about the controller.

        If no information about the controller is received, the return value
        is :obj:`None`.

        If information about the controller is known after :ref:`cnfinfo` was
        received, you can access these values:

        .. code:: python

            >>> communication.controller.firmware_version
            (5, 2)
            >>> communication.controller.firmware_version.major
            5
            >>> communication.controller.firmware_version.minor
            2
            >>> communication.controller.api_version
            4

        """
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value

    @property
    def last_requested_line_number(self):
        """The number of the last line that was requested.

        :rtype: int
        :return: the last requested line number or ``0``
        """
        return self._last_requested_line_number

    @last_requested_line_number.setter
    def last_requested_line_number(self, line_number):
        """Set the last requested line number."""
        print("set last_requested_line_number:", line_number)
        self._last_requested_line_number = line_number

__all__ = ["Communication", "Content"]
