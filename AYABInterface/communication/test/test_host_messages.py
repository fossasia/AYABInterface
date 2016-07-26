"""Test the messages that are sent by the host.

They are all in the module :mod:`AYABInterface.communication.host_messages`.
"""
import pytest
from AYABInterface.communication.host_messages import RequestStart, \
    LineConfiguration
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

    @pytest.mark.parametrize("left_end_needle", VALID_START_NEEDLES)
    @pytest.mark.parametrize("right_end_needle", VALID_STOP_NEEDLES)
    def test_initialize_with_correct_arguments(
            self, left_end_needle, right_end_needle, file, communication):
        content_bytes = bytes([left_end_needle, right_end_needle])
        first_byte = 0x01
        all_bytes = bytes([first_byte]) + content_bytes
        message = RequestStart(file, communication, left_end_needle, right_end_needle)
        assert message.MESSAGE_ID == first_byte
        assert message.left_end_needle == left_end_needle
        assert message.right_end_needle == right_end_needle
        assert message.content_bytes() == content_bytes
        assert message.as_bytes() == all_bytes
        message.send()
        assert file.getvalue() == all_bytes

    TYPE_ERRORS = [None, "asd", object()]
    INVALID_START_NEEDLES = [-1, -4, 199, 200, 123123123] + TYPE_ERRORS
    INVALID_STOP_NEEDLES = [0, -1234, -29, 200, 821737382193, -1] + TYPE_ERRORS

    @pytest.mark.parametrize("left_end_needle", INVALID_START_NEEDLES)
    @pytest.mark.parametrize("right_end_needle", VALID_STOP_NEEDLES)
    def test_invalid_left_end_needle(
            self, left_end_needle, right_end_needle, file, communication):
        error_type = (ValueError if type(left_end_needle) == int else TypeError)
        with raises(error_type) as error:
            RequestStart(file, communication, left_end_needle, right_end_needle)
        message = "Start needle is {0} but 0 <= {0} <= 198 was expected."\
            "".format(repr(left_end_needle))
        assert error.value.args[0] == message

    @pytest.mark.parametrize("left_end_needle", VALID_START_NEEDLES)
    @pytest.mark.parametrize("right_end_needle", INVALID_STOP_NEEDLES)
    def test_invalid_right_end_needle(
            self, left_end_needle, right_end_needle, file, communication):
        error_type = (ValueError if type(right_end_needle) == int else TypeError)
        with raises(error_type) as error:
            RequestStart(file, communication, left_end_needle, right_end_needle)
        message = "Stop needle is {0} but 1 <= {0} <= 199 was expected."\
            "".format(repr(right_end_needle))
        assert error.value.args[0] == message


class TestLineConfiguration(object):

    """Test the LineConfiguration.

    .. seealso::
      :class:`AYABInterface.communication.hardware_messages.LineConfiguration`,
      :ref:`cnfline`
    """

    MESSAGE_ID = 0x42

    @pytest.mark.parametrize("line_number", [-12, -1, 0, 1, 5])
    @pytest.mark.parametrize("line_bytes", [b'123123', b'0' * 24])
    @pytest.mark.parametrize("last_line", [True, False])
    def test_bytes(self, line_number, communication, file, line_bytes,
                   last_line):
        communication.get_line_configuration_message.return_value = line_bytes
        cnfLine = LineConfiguration(file, communication, line_number)
        bytes_ = cnfLine.content_bytes()
        assert bytes_ == line_bytes
        communication.get_line_configuration_message.assert_called_with(
            line_number)
        cnfLine.send()
        assert file.getvalue() == bytes([self.MESSAGE_ID]) + line_bytes

    def test_first_byte(self):
        assert LineConfiguration.MESSAGE_ID == self.MESSAGE_ID

