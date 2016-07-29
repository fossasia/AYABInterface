"""Test the received messages."""
from AYABInterface.communication.host_messages import LineConfirmation
from AYABInterface.communication.hardware_messages import read_message_type, \
    UnknownMessage, SuccessConfirmation, StartConfirmation, LineRequest, \
    InformationConfirmation, TestConfirmation, StateIndication, Debug
import pytest
from io import BytesIO
from pytest import fixture
from unittest.mock import MagicMock
from AYABInterface.utils import next_line
import AYABInterface.communication.hardware_messages as hardware_messages
from test_assertions import assert_identify


@fixture
def configuration():
    return MagicMock()


def one_byte_file(byte):
    """Create a BytesIO with one byte."""
    return BytesIO(bytes([byte]))


class Message(BytesIO):

    """A message in a file."""

    def assert_is_read(self):
        """Make sure this message is read 100%."""
        current_index = self.tell()
        bytes = self.getvalue()
        maximum_index = len(bytes)
        everything_is_read = current_index == maximum_index
        message = "Expected the message {} to be read to the end, " \
            "but the last {} bytes are not read: {}." \
            "".format(repr(bytes), maximum_index - current_index,
                      repr(bytes[current_index:]))
        assert everything_is_read, message

    def assert_bytes_read(self, bytes_read):
        """Make sure a portion of the message is read."""
        message = "The message should be read until {}, but it is read to" \
            " {} .".format(bytes_read, self.tell())
        assert self.tell() == bytes_read, message


class TestReadMessageFromFile(object):

    """Test read_message_type.

    .. seealso::
      :func:`AYABInterface.communication.hardware_messages.read_message_type`
    """

    @pytest.mark.parametrize("byte,message_type", [
        (0xc1, StartConfirmation), (0xc3, InformationConfirmation),
        (0xc4, TestConfirmation), (0x82, LineRequest),
        (0x84, StateIndication), (0x23, Debug)])
    def test_read_message_from_file(self, byte, message_type):
        assert message_type.MESSAGE_ID == byte
        assert read_message_type(one_byte_file(byte)) == message_type

    @pytest.mark.parametrize("byte", [0x00, 0xfe, 0x0d1])
    def test_read_unknown_message(self, byte):
        assert read_message_type(one_byte_file(byte)) == UnknownMessage


@fixture
def file():
    """The file to read the messages from."""
    return BytesIO()


@fixture
def communication():
    """The communication object."""
    return MagicMock()


class TestUnknownMessage(object):

    """Test UnknownMessage.

    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.UnknownMessage`
    """

    @pytest.mark.parametrize("bytes,index", [
        (b"\r\n", 2), (b"asdladlsjk\r\nasd\r\n", 12)])
    def test_tests_and_bytes_read(self, bytes, index):
        """Test the is_* methods."""
        file = Message(bytes)
        message = UnknownMessage(file, communication)
        assert_identify(message, ["is_unknown"])
        file.assert_bytes_read(index)


class TestSuccessMessage(object):

    """Test success messages.

    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.SuccessMessage`
    """

    message_type = SuccessConfirmation
    identifiers = []
    success = b'\x01\r\n'
    failure = b'\x00\r\n'

    def test_success(self, communication):
        file = Message(self.success)
        message = self.message_type(file, communication)
        assert_identify(message, self.identifiers + ["is_success", "is_valid"])
        file.assert_is_read()

    def test_failure(self, communication):
        file = Message(self.failure)
        message = self.message_type(file, communication)
        assert_identify(message, self.identifiers + ["is_valid"])
        file.assert_is_read()

    @pytest.mark.parametrize("byte", [2, 20, 220, 255])
    def test_invalid(self, communication, byte):
        file = Message(bytes([byte]) + b"\r\n")
        message = self.message_type(file, communication)
        assert_identify(message, self.identifiers)
        file.assert_is_read()


class TestStartConfirmation(TestSuccessMessage):

    """Test the StartConfirmation.

    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.StartConfirmation`
    """

    message_type = StartConfirmation
    identifiers = ["is_start_confirmation"]


class TestLineRequest(object):

    """Test the LineRequest.

    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.LineRequest`
    """

    @pytest.mark.parametrize("last_line", [-123, 1, 3000])
    @pytest.mark.parametrize("next_line", [-4, 444, 60000])
    @pytest.mark.parametrize("byte", [b'\x00', b'f'])
    def test_line_number(self, last_line, next_line, byte, monkeypatch, file,
                         communication):
        def mock_next_line(last_line_, next_line_):
            assert last_line_ == last_line
            assert next_line_ == byte[0]
            return next_line
        monkeypatch.setattr(hardware_messages, 'next_line', mock_next_line)
        communication.last_line = last_line
        file = Message(byte + b'\r\n')
        message = LineRequest(file, communication)
        assert_identify(message, ["is_line_request", "is_valid"])
        assert message.line_number == next_line
        file.assert_is_read()

    def test_next_line_is_from_utils(self):
        assert hardware_messages.next_line == next_line

    def test_answer(self, communication, monkeypatch):
        file = Message(b'\x00\r\n')
        next_line = MagicMock()
        line_conf = MagicMock()
        monkeypatch.setattr(hardware_messages, 'next_line', next_line)
        monkeypatch.setattr(hardware_messages, 'LineConfirmation', line_conf)
        message = LineRequest(file, communication)
        file.assert_is_read()
        assert message.has_answer()
        answer = message.answer
        assert answer == line_conf.return_value, "LineConfirmation expected"
        line_conf.assert_called_once_with(file, communication,
                                          next_line.return_value)
        answer.send.assert_not_called()
        message.send_answer()
        answer.send.assert_called_once_with()

    def test_line_configuration_is_from_host_messages(self):
        assert hardware_messages.LineConfirmation == LineConfirmation


class TestInformationConfirmation(object):

    """Test the InformationConfirmation.

    .. seealso:: :class:`InformationConfirmation
      <AYABInterface.communication.hardware_messages.InformationConfirmation>`
    """

    @pytest.mark.parametrize("bytes", [b"\x01\x02\x03\r\n", b"abc\r\n"])
    @pytest.mark.parametrize("api_version", [True, False])
    def test_versions(self, bytes, configuration, api_version):
        file = Message(bytes)
        configuration.api_version_is_supported.return_value = api_version
        message = InformationConfirmation(file, configuration)
        file.assert_is_read()
        assert message.api_version == bytes[0]
        assert message.firmware_version == (bytes[1], bytes[2])
        assert message.firmware_version.major == bytes[1]
        assert message.firmware_version.minor == bytes[2]
        assert_identify(message, ["is_information_confirmation", "is_valid"])
        assert message.api_version_is_supported() == api_version
        configuration.api_version_is_supported.assert_called_once_with(
            bytes[0])


class TestStateIndication(object):

    """Test the StateIndication.

    .. seealso:: :class:`StateIndication
      <AYABInterface.communication.hardware_messages.StateIndication>`
    """

    @pytest.mark.parametrize("ready,valid", [(0, True), (1, True), (2, False),
                                             (77, False)])
    @pytest.mark.parametrize("left_hall,left_bytes", [
        (0xaa, b'\x00\xaa'), (0x1234, b'\x12\x34')])
    @pytest.mark.parametrize("right_hall,right_bytes", [
        (0x4a5, b'\x04\xa5'), (0x01, b'\x00\x01')])
    @pytest.mark.parametrize("carriage,carriage_tests", [
        (0, []), (1, ["is_knit_carriage"]), (2, ["is_hole_carriage"]),
        (77, ["is_unknown_carriage"])])
    @pytest.mark.parametrize("needle", [0, 45, 99])
    def test_versions(self, ready, valid, left_hall, left_bytes, right_hall,
                      right_bytes, carriage, carriage_tests, needle,
                      configuration):
        file = Message(bytes([ready]) + left_bytes + right_bytes +
                       bytes([carriage, needle]) + b'\r\n')
        message = StateIndication(file, configuration)
        file.assert_is_read()
        assert_identify(message, ["is_state_indication"] +
                        ["is_valid"] * valid +
                        ["is_ready_to_knit"] * (ready == 1))
        assert message.left_hall_sensor_value == left_hall
        assert message.right_hall_sensor_value == right_hall
        assert_identify(message.carriage, carriage_tests)
        assert message.current_needle == needle
        assert message.carriage.needle_position == needle


class TestDebugMessage(object):

    """Test the Debug.

    .. seealso:: :class:`StateIndication
      <AYABInterface.communication.hardware_messages.StateIndication>`
    """

    @pytest.mark.parametrize("bytes,length", [
        (b"\r\n", 0), (b"asd\r\n", 3), (b"asdasd\r\nasd\r\n", 6)])
    def test_debug_message(self, bytes, length, configuration):
        file = Message(bytes)
        message = Debug(file, configuration)
        file.assert_bytes_read(length + 2)
        assert_identify(message, ["is_valid", "is_debug"])
        assert message.bytes == bytes[:length]


class TestTestConfirmation(TestSuccessMessage):

    """Test the TestConfirmation.

    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.TestConfirmation`
    """

    message_type = TestConfirmation
    identifiers = ["is_test_confirmation"]


class TestIncompleteRead(object):

    def test_todo(self):
        pytest.skip()
