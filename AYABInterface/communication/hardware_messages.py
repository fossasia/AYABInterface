"""This modue contains all the messages taht are received."""
from ..utils import next_line
from collections import namedtuple
from .carriages import id_to_carriage_type
import struct


class Message(object):

    """This is the base class for messages that are received."""

    def __init__(self, file, communication):
        """Create a new Message."""
        self._file = file
        self._communication = communication
        self._init()

    def _init(self):
        """Initialize the message.

        Override this method to configure your message.
        This pattern is called template method.
        Reading from the file should be done here and nowhere else.
        """

    def is_from_host(self):
        """Whether this message is sent by the host.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_from_controller(self):
        """Whether this message is sent by the controller.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_valid(self):
        """Whether the message is valid.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_start_confirmation(self):
        """Whether this is a StartConfirmation message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def is_information_confirmation(self):
        """Whether this is a InformationConfirmation message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def is_test_confirmation(self):
        """Whether this is a TestConfirmation message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def is_state_indication(self):
        """Whether this is a StateIndication message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def is_line_request(self):
        """Whether this is a LineRequest message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def is_connection_closed(self):
        """Whether this is a ConnectionClosed message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def is_unknown(self):
        """Whether this is a StateIndication message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def is_debug(self):
        """Whether this is a Debug message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def wants_to_answer(self):
        """Whether this message produces and answer message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def __repr__(self):
        """This object as string.

        :rtype: str
        """
        return "<{}>".format(self.__class__.__name__)


class FixedSizeMessage(Message):

    """This is a message of fixed size."""

    def __init__(self, file, communication):
        """Create a new Message."""
        super().__init__(file, communication)
        self.read_end_of_message()

    def read_end_of_message(self):
        """Read the b"\\r\\n" at the end of the message."""
        read = self._file.read
        last = read(1)
        current = read(1)
        while last != b'' and current != b'' and not \
                (last == b'\r' and current == b'\n'):
            last = current
            current = read(1)


class SuccessConfirmation(FixedSizeMessage):

    """Base class for massages of success and failure."""

    def _init(self):
        """Read the success byte."""
        self._success = self._file.read(1)

    def is_valid(self):
        """Whether this message is valid."""
        return self._success <= b"\x01"

    def is_success(self):
        """Whether the configuration was successful.

        :rtype: bool
        """
        return self._success == b"\x01"


class StartConfirmation(SuccessConfirmation):

    """This marks the success or failure of a reqStart message.

    .. seealso:: :ref:`cnfstart`
    """

    MESSAGE_ID = 0xc1  #: The first byte that indicates this message

    def is_start_confirmation(self):
        """Whether this is a StartConfirmation message.

        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def received_by(self, visitor):
        """Call visitor.receive_state_confirmation."""
        visitor.receive_start_confirmation(self)


class ConnectionClosed(Message):

    """This message is notified about when the connection is closed."""

    def is_connection_closed(self):
        """Whether this is a ConnectionClosed message.

        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def received_by(self, visitor):
        """Call visitor.receive_connection_closed."""
        visitor.receive_connection_closed(self)


class UnknownMessage(FixedSizeMessage):

    """This is a special message for unknown message types."""

    def is_unknown(self):
        """Whether this is a StateIndication message.

        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def is_valid(self):
        """Whether the message is valid.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def received_by(self, visitor):
        """Call visitor.receive_unkown."""
        visitor.receive_unknown(self)


FirmwareVersion = namedtuple("FirmwareVersion", ["major", "minor"])


class InformationConfirmation(FixedSizeMessage):

    """This message is the answer in the initial handshake.

    A :class:`~AYABInterface.communication.host_messages.InformationRequest`
    requests this message from the controller to start the initial handshake.

    .. seealso:: :ref:`cnfinfo`
      :class:`~AYABInterface.communication.host_messages.InformationRequest`
    """

    MESSAGE_ID = 0xc3  #: The first byte that indicates this message

    def is_information_confirmation(self):
        """Whether this is a InformationConfirmation message.

        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def _init(self):
        """Read the success byte."""
        self._api_version = self._file.read(1)[0]
        self._firmware_version = FirmwareVersion(*self._file.read(2))

    @property
    def api_version(self):
        """The API version of the controller.

        :rtype: int
        """
        return self._api_version

    def api_version_is_supported(self):
        """Whether the communication object supports this API version.

        :rtype: bool

        .. seealso::
          :meth:`Communication.api_version_is_supported
          <AYABInterface.communication.Communication.api_version_is_supported>`
        """
        return self._communication.api_version_is_supported(self._api_version)

    @property
    def firmware_version(self):
        """The firmware version of the controller.

        :rtype: FirmwareVersion

        .. code:: python

            minor_version = int()
            mayor_version = int()

            assert message.firmware_version == (mayor_version, minor_version)
            assert message.firmware_version.major == mayor_version
            assert message.firmware_version.minor == minor_version

        """
        return self._firmware_version

    def received_by(self, visitor):
        """Call visitor.receive_information_confirmation."""
        visitor.receive_information_confirmation(self)


class TestConfirmation(SuccessConfirmation):

    """This message is sent at/when"""  # TODO

    MESSAGE_ID = 0xc4  #: The first byte that indicates this message

    def is_test_confirmation(self):
        """Whether this is a TestConfirmation message.

        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def received_by(self, visitor):
        """Call visitor.test_information_confirmation."""
        visitor.receive_test_confirmation(self)


class LineRequest(FixedSizeMessage):

    """The controller requests a line.

    .. seealso:: :ref:`reqline`

    """

    MESSAGE_ID = 0x82  #: The first byte that indicates this message

    def is_line_request(self):
        """Whether this is a LineRequest message.

        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def _init(self):
        """Read the line number."""
        self._line_number = next_line(
            self._communication.last_requested_line_number,
            self._file.read(1)[0])

    @property
    def line_number(self):
        """The line number that was requested."""
        return self._line_number

    def received_by(self, visitor):
        """Call visitor.receive_line_request."""
        visitor.receive_line_request(self)


class StateIndication(FixedSizeMessage):

    """This message shows the state of the controller.

    .. seealso:: :ref:`indstate`
    """

    MESSAGE_ID = 0x84  #: The first byte that indicates this message

    def is_state_indication(self):
        """Whether this is a InformationConfirmation message.

        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def _init(self):
        """Read the success byte."""
        self._ready = self._file.read(1)
        self._hall_left = self._file.read(2)
        self._hall_right = self._file.read(2)
        self._carriage_type = self._file.read(1)[0]
        self._carriage_position = self._file.read(1)[0]

    def is_valid(self):
        """Whether this messages matches the specification."""
        return self._ready == b'\x00' or self._ready == b'\x01'

    def is_ready_to_knit(self):
        """Whether this message indicates that the controller can knit now."""
        return self._ready == b'\x01'

    @property
    def left_hall_sensor_value(self):
        """The value of the left hall sensor.

        :rtype: int
        """
        return struct.unpack(">H", self._hall_left)[0]

    @property
    def right_hall_sensor_value(self):
        """The value of the left hall sensor.

        :rtype: int
        """
        return struct.unpack(">H", self._hall_right)[0]

    @property
    def carriage(self):
        """The carriage which is reported.

        :rtype: AYABInterface.communication.carriages.Carriage
        :return: the carriage with information about its position
        """
        carriage_type = id_to_carriage_type(self._carriage_type)
        return carriage_type(self._carriage_position)

    @property
    def current_needle(self):
        """The current needle position.

        :rtype: int
        """
        return self._carriage_position

    def received_by(self, visitor):
        """Call visitor.receive_state_indication."""
        visitor.receive_state_indication(self)


class Debug(Message):

    """This message contains debug output from the controller.

    .. seealso:: :ref:`debug`
    """

    MESSAGE_ID = 0x23

    def is_debug(self):
        """Whether this is a Debug message.

        :rtype: bool
        :returns: :obj:`False`
        """
        return True

    def _init(self):
        """Read the b"\\r\\n" at the end of the message."""
        read_values = []
        read = self._file.read
        last = read(1)
        current = read(1)
        while last != b'' and current != b'' and not \
                (last == b'\r' and current == b'\n'):
            read_values.append(last)
            last = current
            current = read(1)
        if current == b'' and last != b'\r':
            read_values.append(last)
        self._bytes = b''.join(read_values)

    @property
    def bytes(self):
        """The debug message as bytes.

        :rtype: bytes
        :return: the debug message as bytes without the ``b'\\r\\n'`` at
          the end
        """
        return self._bytes

    def received_by(self, visitor):
        """Call visitor.receive_debug."""
        visitor.receive_debug(self)


_message_types = {}
for message_type in list(globals().values()):
    message_id = getattr(message_type, "MESSAGE_ID", None)
    if message_id is not None:
        _message_types[message_id] = message_type
del message_type, message_id


def read_message_type(file):
    """Read the message type from a file."""
    message_byte = file.read(1)
    if message_byte == b'':
        return ConnectionClosed
    message_number = message_byte[0]
    return _message_types.get(message_number, UnknownMessage)

__all__ = ["read_message_type", "StateIndication", "LineRequest",
           "TestConfirmation", "InformationConfirmation", "Debug",
           "StartConfirmation", "SuccessConfirmation",
           "UnknownMessage", "Message", "ConnectionClosed", "FirmwareVersion",
           "FixedSizeMessage"]
