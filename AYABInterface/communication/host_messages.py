"""This module contains the messages that are sent to the controller."""


class Message(object):

    """This is the interface for sent messages."""

    def __init__(self, file, communication, *args, **kw):
        """Create a new Request object"""
        self._file = file
        self._communication = communication
        assert self.MESSAGE_ID is not None
        self.init(*args, **kw)

    def is_from_host(self):
        """Whether this message is sent by the host.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_from_controller(self):
        """Whether this message is sent by the controller.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def init(self):
        """Override this method."""

    MESSAGE_ID = None  #: the first byte to identify this message

    def content_bytes(self):
        """The message content as bytes.

        :rtype: bytes
        """
        return b''

    def as_bytes(self):
        """The message represented as bytes.

        :rtype: bytes
        """
        return bytes([self.MESSAGE_ID]) + self.content_bytes()

    def send(self):
        """Send this message to the controller."""
        self._file.write(self.as_bytes())
        self._file.write(b'\r\n')

    def __repr__(self):
        """This message as string inclding the bytes.

        :rtype: str
        """
        return "<{} {}>".format(self.__class__.__name__,
                                self.as_bytes() + b"\r\n")


def _left_end_needle_error_message(needle):
    return "Start needle is {0} but 0 <= {0} <= 198 was expected.".format(
        repr(needle))


def _right_end_needle_error_message(needle):
    return "Stop needle is {0} but 1 <= {0} <= 199 was expected.".format(
        repr(needle))


class StartRequest(Message):

    """This is the start of the conversation.

    .. seealso:: :ref:`reqstart`
    """

    MESSAGE_ID = 0x01  #: the first byte to identify this message

    def init(self, left_end_needle, right_end_needle):
        """Initialize the StartRequest with start and stop needle.

        :raises TypeError: if the arguments are not integers
        :raises ValueError: if the values do not match the
          :ref:`specification <m4-01>`
        """
        if not isinstance(left_end_needle, int):

            raise TypeError(_left_end_needle_error_message(left_end_needle))
        if left_end_needle < 0 or left_end_needle > 198:
            raise ValueError(_left_end_needle_error_message(left_end_needle))
        if not isinstance(right_end_needle, int):
            raise TypeError(_right_end_needle_error_message(right_end_needle))
        if right_end_needle < 1 or right_end_needle > 199:
            raise ValueError(_right_end_needle_error_message(right_end_needle))
        self._left_end_needle = left_end_needle
        self._right_end_needle = right_end_needle

    @property
    def left_end_needle(self):
        """The needle to start knitting with.

        :rtype: int
        :return: value where ``0 <= value <= 198``
        """
        return self._left_end_needle

    @property
    def right_end_needle(self):
        """The needle to start knitting with.

        :rtype: int
        :return: value where ``1 <= value <= 199``
        """
        return self._right_end_needle

    def content_bytes(self):
        """Return the start and stop needle.

        :rtype: bytes
        """
        return bytes([self._left_end_needle, self._right_end_needle])


class LineConfirmation(Message):

    """This message send the data to configure a line.

    .. seealso:: :ref:`cnfline`
    """

    MESSAGE_ID = 0x42  #: the first byte to identify this message

    def init(self, line_number):
        """Initialize the StartRequest with the line number."""
        self._line_number = line_number

    def content_bytes(self):
        """Return the start and stop needle."""
        get_message = \
            self._communication.needle_positions.get_line_configuration_message
        return get_message(self._line_number)


class InformationRequest(Message):

    """Start the initial handshake.

    .. seealso:: :ref:`reqinfo`,
      :class:`InformationConfirmation
      <AYABInterface.communication.hardware_messages.InformationConfirmation>`
    """

    MESSAGE_ID = 0x03  #: the first byte to identify this message


class TestRequest(Message):

    """Start the test mode of the controller.

    .. seealso:: :ref:`reqtest`,
      :class:`InformationConfirmation
      <AYABInterface.communication.hardware_messages.TestConfirmation>`
    """

    MESSAGE_ID = 0x04  #: the first byte to identify this message

__all__ = ["Message", "StartRequest", "LineConfirmation",
           "InformationRequest", "TestRequest"]
