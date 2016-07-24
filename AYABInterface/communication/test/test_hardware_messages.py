"""Test the received messages."""
from AYABInterface.communication.hardware_messages import read_message_type, \
    StateIndication, LineRequest, ConfigurationTest, MessageWithAnswer, \
    ConfigurationStart, ConfigurationSuccess, ConfigurationInformation, \
    UnknownMessage
import pytest
from io import BytesIO
from pytest import fixture
from unittest.mock import MagicMock


def one_byte_file(byte):
    """Create a BytesIO with one byte."""
    return BytesIO(bytes([byte]))


class TestReadMessageFromFile(object):

    """Test read_message_type.

    .. seealso::
      :func:`AYABInterface.communication.hardware_messages.read_message_type`
    """

    @pytest.mark.parametrize("byte,message_type", [
        (0xc1, ConfigurationStart), (0xc3, ConfigurationInformation),
        (0xc4, ConfigurationTest), (0x82, LineRequest),
        (0x84, StateIndication)])
    def test_read_message_from_file(self, byte, message_type):
        assert message_type.MESSAGE_ID == byte
        assert read_message_type(one_byte_file(byte)) == message_type

    @pytest.mark.parametrize("byte", [0x00, 0xfe, 0x0d1])
    def test_read_unknown_message(self, byte):
        assert read_message_type(one_byte_file(byte)) == UnknownMessage


def assert_identify(message, true=[]):
    """Make sure the messages "is_*" are True or False."""
    for method_name in dir(message):
        if method_name.startswith("is_"):
            test_method = getattr(message, method_name)
            value = method_name in true
            assert test_method() == value


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

    @fixture
    def message(self, file, communication):
        """The message to test."""
        return UnknownMessage(file, communication)

    def test_tests(self, message):
        """Test the is_* methods."""
        assert_identify(message, ["is_unknown"])


class TestSuccessMessage(object):

    """Test success messages.
    
    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.SuccessMessage`
    """
    
    message_type = ConfigurationSuccess
    identifiers = []
    success = b'\x01'
    failure = b'\x00'
    
    def test_success(self, communication):
        message = self.message_type(BytesIO(self.success), communication)
        assert_identify(message, self.identifiers + ["is_success", "is_valid"])
        
    def test_failure(self, communication):
        message = self.message_type(BytesIO(self.failure), communication)
        assert_identify(message, self.identifiers + ["is_valid"])
        
    @pytest.mark.parametrize("byte", [2, 20, 220, 255])
    def test_invalid(self, communication, byte):
        message = self.message_type(BytesIO(bytes([byte])), communication)
        assert_identify(message, self.identifiers)
        

class TestConfigurationStart(TestSuccessMessage):

    """Test the ConfigurationStart.
    
    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.ConfigurationStart`
    """

    message_type = ConfigurationStart
    identifiers = ["is_configutation_start"]


class TestLineRequest(object):

    """Test the LineRequest.
    
    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.LineRequest`
    """
