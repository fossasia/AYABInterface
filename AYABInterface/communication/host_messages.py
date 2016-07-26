"""This module contains the messages that are sent to the controller."""


class Message(object):

    """This is the interface for sent messages."""

    def __init__(self, file, communication, *args, **kw):
        """Create a new Request object"""
        self._file = file
        self._communication = communication
        assert self.MESSAGE_ID is not None
        self.init(*args, **kw)

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


def _start_needle_error_message(needle):
    return "Start needle is {0} but 0 <= {0} <= 198 was expected.".format(
        repr(needle))


def _stop_needle_error_message(needle):
    return "Stop needle is {0} but 1 <= {0} <= 199 was expected.".format(
        repr(needle))


class RequestStart(Message):

    """This is the start of the conversation.

    .. seealso:: :ref:`reqstart`
    """

    MESSAGE_ID = 0x01  #: the first byte to identify this message

    def init(self, start_needle, stop_needle):
        """Initialize the RequestStart with start and stop needle.
        
        :raises TypeError: if the arguments are not integers
        :raises ValueError: if the values do not match the
          :ref:`specification <m4-01>`
        """
        if not isinstance(start_needle, int):

            raise TypeError(_start_needle_error_message(start_needle))
        if start_needle < 0 or start_needle > 198:
            raise ValueError(_start_needle_error_message(start_needle))
        if not isinstance(stop_needle, int):
            raise TypeError(_stop_needle_error_message(stop_needle))
        if stop_needle < 1 or stop_needle > 199:
            raise ValueError(_stop_needle_error_message(stop_needle))
        self._start_needle = start_needle
        self._stop_needle = stop_needle
        
    @property
    def start_needle(self):
        """The needle to start knitting with.
        
        :rtype: int
        :return: value where ``0 <= value <= 198``
        """
        return self._start_needle

    @property
    def stop_needle(self):
        """The needle to start knitting with.
        
        :rtype: int
        :return: value where ``1 <= value <= 199``
        """
        return self._stop_needle

    def content_bytes(self):
        """Return the start and stop needle.
        
        :rtype: bytes
        """
        return bytes([self._start_needle, self._stop_needle])


class LineConfiguration(Message):

    """This message send the data to configure a line.

    .. seealso:: :ref:`cnfline`
    """

    MESSAGE_ID = 0x42  #: the first byte to identify this message

    def init(self, line_number):
        """Initialize the RequestStart with the line number."""
        self._line_number = line_number

    def content_bytes(self):
        """Return the start and stop needle."""
        return self._communication.get_line_configuration_message(
            self._line_number)


class InformationRequest(Message):

    """Start the initial handshake.

    .. seealso:: :ref:`reqinfo`,
      :class:`ConfigurationInformation
      <AYABInterface.communication.hardware_messages.ConfigurationInformation>`
    """

    MESSAGE_ID = 0x03  #: the first byte to identify this message


__all__ = ["Message", "RequestStart", "LineConfiguration",
           "InformationRequest"]
