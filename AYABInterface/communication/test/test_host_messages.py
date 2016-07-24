"""Test the messages that are sent by the host.

They are all in the module :mod:`AYABInterface.communication.host_messages`.
"""
import pytest
from AYABInterface.communication.host_messages import RequestStart
from pytest import raises, fixture
from io import BytesIO
from unittest.mock import MagicMock


@fixture
def file():
    return BytesIO()


@fixture
def communication():
    return MagicMock()


class TestReqStart(object):

    """Test the reqStart message.
    
    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.RequestStart`,
      :ref:`reqstart`
    """
    
    VALID_START_NEEDLES = [0, 4, 29, 198, 120]
    VALID_STOP_NEEDLES = [1, 4, 29, 199, 120]
    
    @pytest.mark.parametrize("start_needle", VALID_START_NEEDLES)
    @pytest.mark.parametrize("stop_needle", VALID_STOP_NEEDLES)
    def test_initialize_with_correct_arguments(
            self, start_needle, stop_needle, file, communication):
        content_bytes = bytes([start_needle, stop_needle])
        first_byte = 0x01
        all_bytes = bytes([first_byte]) + content_bytes
        message = RequestStart(file, communication, start_needle, stop_needle)
        assert message.FIRST_BYTE == first_byte
        assert message.start_needle == start_needle
        assert message.stop_needle == stop_needle
        assert message.content_bytes() == content_bytes
        assert message.as_bytes() == all_bytes
        message.send()
        assert file.getvalue() == all_bytes

    TYPE_ERRORS = [None, "asd", object()]
    INVALID_START_NEEDLES = [-1, -4, 199, 200, 123123123] + TYPE_ERRORS
    INVALID_STOP_NEEDLES = [0, -1234, -29, 200, 821737382193, -1] + TYPE_ERRORS
    
    @pytest.mark.parametrize("start_needle", INVALID_START_NEEDLES)
    @pytest.mark.parametrize("stop_needle", VALID_STOP_NEEDLES)
    def test_invalid_start_needle(
            self, start_needle, stop_needle, file, communication):
        error_type = (ValueError if type(start_needle) == int else TypeError)
        with raises(error_type) as error:
            RequestStart(file, communication, start_needle, stop_needle)
        message = "Start needle is {0} but 0 <= {0} <= 198 was expected."\
            "".format(repr(start_needle))
        assert error.value.args[0] == message
    
    @pytest.mark.parametrize("start_needle", VALID_START_NEEDLES)
    @pytest.mark.parametrize("stop_needle", INVALID_STOP_NEEDLES)
    def test_invalid_stop_needle(
            self, start_needle, stop_needle, file, communication):
        error_type = (ValueError if type(stop_needle) == int else TypeError)
        with raises(error_type) as error:
            RequestStart(file, communication, start_needle, stop_needle)
        message = "Stop needle is {0} but 1 <= {0} <= 199 was expected."\
            "".format(repr(stop_needle))
        assert error.value.args[0] == message
    
    
