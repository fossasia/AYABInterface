"""Test the Communication class.

.. seealso:: :class:`AYABInterface.communication.Communication`
"""
from AYABInterface.communication import Communication
from pytest import fixture, raises
import pytest
from unittest.mock import MagicMock, call
from io import BytesIO


@fixture
def messages():
    return []


@fixture
def on_message_received(messages):
    """The observer that is notified if a message was received."""
    return messages.append


@fixture
def file():
    """The file object to read from."""
    return BytesIO()


@fixture
def create_message():
    return MagicMock()


@fixture
def get_needle_positions():
    return MagicMock()


@fixture
def machine():
    return MagicMock()


@fixture
def communication(file, on_message_received, monkeypatch, create_message,
                  get_needle_positions, machine):
    monkeypatch.setattr(Communication, '_read_message_type', create_message)
    return Communication(file, get_needle_positions, machine,
                         on_message_received=[on_message_received])


class TestReceiveMessages(object):

    """Test the receive_message, start and stop methods.

    .. seealso::
        :meth:`AYABInterface.communication.Commmunication.receive_message`,
        :meth:`AYABInterface.communication.Commmunication.start`,
        :meth:`AYABInterface.communication.Commmunication.stop`

    """

    def test_before_start_no_message_was_received(
            self, communication, create_message):
        create_message.assert_not_called()

    @fixture
    def started_communication(self, communication):
        communication.start()
        return communication

    def test_after_start_no_message_was_received(
            self, started_communication, create_message):
        create_message.assert_not_called()

    def test_receiving_message_before_start_is_forbidden(self, communication):
        with raises(AssertionError):
            communication.receive_message()

    def test_receiving_message_after_stop_is_forbidden(
            self, started_communication):
        started_communication.stop()
        with raises(AssertionError):
            started_communication.receive_message()

    @fixture
    def message(self, create_message):
        message_type = create_message.return_value
        return message_type.return_value

    def test_can_receive_message(
            self, started_communication, create_message, file, messages):
        started_communication.receive_message()
        message_type = create_message.return_value
        create_message.assert_called_once_with(file)
        message_type.assert_called_once_with(file, started_communication)
        assert messages == [message_type.return_value]

    def test_message_answers(self, started_communication, message):
        started_communication.receive_message()
        assert message.wants_to_answer.return_value
        message.send_answer.assert_called_once_with()

    def test_message_does_not_answer(
            self, started_communication, create_message, message):
        message.wants_to_answer.return_value = False
        started_communication.receive_message()
        message.send_answer.assert_not_called()

    def test_stop_notifies_with_close_message(self, started_communication,
                                              messages):
        started_communication.stop()
        assert messages[0].is_connection_closed()


class TestGetLineBytes(object):

    """Test the get_needle_position_bytes method.

    .. seealso::
        :meth:`AYABInterface.communication.Commmunication.get_line_bytes`
    """

    @pytest.mark.parametrize("line", [1, -123, 10000])
    def test_get_line(self, communication, get_needle_positions, line,
                      machine):
        line_bytes = communication.get_needle_position_bytes(line)
        get_needle_positions.assert_called_with(line)
        machine.needle_positions_to_bytes.assert_called_with(
            get_needle_positions.return_value)
        assert line_bytes == machine.needle_positions_to_bytes.return_value

    @pytest.mark.parametrize("line", [4, -89])
    def test_line_is_cached(self, communication, get_needle_positions,
                            line, machine):
        communication.get_needle_position_bytes(line)
        cached_value = machine.needle_positions_to_bytes.return_value
        machine.needle_positions_to_bytes.return_value = None
        line_bytes = communication.get_needle_position_bytes(line)
        assert line_bytes == cached_value

    @pytest.mark.parametrize("line", [55, 4])
    @pytest.mark.parametrize("added", [-1, 1, 12, -2])
    def test_cache_works_only_for_specific_line(
            self, communication, get_needle_positions, line, machine, added):
        communication.get_needle_position_bytes(line)
        machine.needle_positions_to_bytes.return_value = None
        line_bytes = communication.get_needle_position_bytes(line + added)
        assert line_bytes is None

    @pytest.mark.parametrize("line", [55, 4])
    def test_line_is_not_known(self, communication,
                               get_needle_positions, machine, line):
        get_needle_positions.return_value = None
        assert communication.get_needle_position_bytes(line) is None
        machine.needle_positions_to_bytes.assert_not_called()

    @pytest.mark.parametrize("api_version,truth", [(4, True), (3, False),
                                                   (-2, False)])
    def test_sopport_api_version(self, communication, api_version, truth):
        assert communication.api_version_is_supported(api_version) == truth
