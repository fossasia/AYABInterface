"""This module is used to communicate with the shield.

Requirement: Make objects from binary stuff.
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class Content(object, metaclass=ABCMeta):

    """The interface used by the Communication.

    This class is the interface that the :class:`Communication` requires.

    This class does no validity checks, it assumes the :class:`Configuration` is
    valid and there are only valid parameters given to the methods.

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

        :param int line_number: Same line number as given in the req_line message
        :param row line_data: The bytearray to be sent to needles.
        :param bytes last_line: Indicates whether this is the last line to knit.

        Flags are given as parameters to this method explicitly,
        conversion to byte represenation is done here, as this is protocol
        knowledge.

        - Bit 0: Last line (indicate that this is the last line of the pattern.

        CRC8 is currently not checked in the controller.

        .. todo:: Calculate CRC8 in this method, as it is part of the protocol
        """



class Communication(object):

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

__all__ = ["Communication", "Content"]
