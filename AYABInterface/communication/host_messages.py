"""This module contains the messages that are sent to the controller."""


class Message(object):

    """This is the interface for sent messages."""

    def __init__(self, file, communication, *args, **kw):
        """Create a new Request object"""
        self._file = file
        self._communication = communication
        assert self.FIRST_BYTE is not None
        self.init(*args, **kw)

    def init(self):
        """Override this method."""

    FIRST_BYTE = None  #: the first byte to identify this message

    def content_bytes(self):
        """The message content as bytes."""
        return b''

    def as_bytes(self):
        """The message represented as bytes."""
        return self.FIRST_BYTE + self.get_content_bytes()

    def send(self):
        """Send this message to the controller."""
        self._file.write(self.as_bytes())


class RequestStart(Message):

    """This is the start of the conversation.

    .. seealso:: :ref:`message-reqstart`
    """

    FIRST_BYTE = 0x01  #: the first byte to identify this message

    def init(self, start_needle, stop_needle):
        """Initialize the RequestStart with start and stop needle."""

    def content_bytes(self):
        """Return the start and stop needle."""


class LineConfiguration(Message):

    """This message send the data to configure a line.

    .. seealso:: :ref:`message-cnfline`
    """

    FIRST_BYTE = 0x42  #: the first byte to identify this message

    def init(self, line_number):
        """Initialize the RequestStart with the line number."""

    def content_bytes(self):
        """Return the start and stop needle."""


class InformationRequest(Message):

    """Start the initial handshake.

    .. seealso:: :ref:`message-reqinfo`,
      :class:`ConfigurationInformation
      <AYABInterface.communication.hardware_messages.ConfigurationInformation>`
    """

    FIRST_BYTE = 0x03  #: the first byte to identify this message



__all__ = ["Message", "RequestStart", "LineConfiguration",
           "InformationRequest"]
