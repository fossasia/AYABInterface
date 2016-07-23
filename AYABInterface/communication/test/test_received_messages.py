"""Test the received messages."""
from AYABInterface.communication.received_messages import read_message_type, \
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
      :func:`AYABInterface.communication.received_messages.read_message_type`.
    """

    @pytest.mark.parametrize("byte,message_type", [
        (0xc1, ConfigurationStart), (0xc3, ConfigurationInformation), 
        (0xc4, ConfigurationTest), (0x82, LineRequest),
        (0x84, StateIndication)])
    def test_read_message_from_file(self, byte, message_type):
        assert message_type.MESSAGE_ID == byte
        assert read_message_type(one_byte_file(byte)) == message_type

    @pytest.mark.parametrize("byte", [0x00, 0xff, 0x0d1])
    def test_read_unknown_message(self, byte):
        assert read_message_type(one_byte_file(byte)) == UnknownMessage


def assert_identify(message, true=[]):
    """Make sure the messages "is_*" are True or False."""
    for method_name in dir(message):
        if method_name.startswith("is_"):
            test_method = getattr(message, method_name)
            value = method_name in true
            assert test_method() == value


class TestUnknownMessage(object):

    """Test UnknownMessage.
    
    .. seealso::
      :func:`AYABInterface.communication.received_messages.UnknownMessage`.
    """
    
    @fixture
    def message(self):
        return UnknownMessage(BytesIO(), MagicMock())
    
    def test_tests(self, message):
        assert_identify(message, ["is_unknown"])
