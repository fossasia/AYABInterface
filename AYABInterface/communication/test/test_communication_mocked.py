"""Test the Communication class.

.. seealso:: :class:`AYABInterface.communication.Communication`
"""
from AYABInterface.communication import Communication
import AYABInterface.communication as communication_module
from pytest import fixture, raises
import pytest
from unittest.mock import MagicMock, call, Mock
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

    def test_stop_notifies_with_close_message(self, started_communication,
                                              messages):
        started_communication.stop()
        assert messages[0].is_connection_closed()


class TestSend(object):

    """Test the send method."""

    @pytest.mark.parametrize("args", [(), (3,), ("asd", "as", "a"), (2, 2)])
    def test_initialized_with_arguments(self, communication, file, args):
        req_class = Mock()
        communication.send(req_class, *args)
        req_class.assert_called_once_with(file, communication, *args)

    def test_sent(self, communication):
        req_class = Mock()
        communication.send(req_class, 1)
        req_class.return_value.send.assert_called_once_with()


class TestLastRequestedLine(object):

    """Test the last_requested_line_number."""

    def test_last_line_requested_default(self, communication):
        assert communication.last_requested_line_number == 0

    def test_set_the_last_line(self, communication):
        communication.last_requested_line_number = 9
        assert communication.last_requested_line_number == 9


class TestState(object):

    def test_set_state_and_enter_is_called(self, communication):
        state = Mock()
        communication.state = state
        state.enter.assert_called_once_with()
        state.exit.assert_not_called()

    def test_when_leaving_exit_is_called(self, communication):
        state = Mock()
        communication.state = state
        communication.state = Mock()
        state.exit.assert_called_once_with()

    def test_first_state(self, communication):
        assert communication.state.is_waiting_for_start()

    def test_received_message_goes_to_state(self, communication):
        message = Mock()
        communication.state = state = Mock()
        communication._message_received(message)
        state.receive_message.assert_called_once_with(message)

    def test_start(self, communication):
        communication.state = state = Mock()
        communication.start()
        state.communication_started.assert_called_once_with()


class TestController(object):

    """Test the controller attribute."""

    def test_initial_value_is_None(self, communication):
        assert communication.controller is None

    def test_set_controller(self, communication):
        communication.controller = controller = Mock()
        assert communication.controller == controller

    @pytest.mark.parametrize("api_version,truth", [(4, True), (3, False),
                                                   (-2, False)])
    def test_support_api_version(self, communication, api_version, truth):
        assert communication.api_version_is_supported(api_version) == truth


class TestNeedles(object):

    """tets the right and left end needles."""

    def test_default_needles_default_to_machine(self, communication, machine):
        assert communication.left_end_needle == machine.left_end_needle
        assert communication.right_end_needle == machine.right_end_needle

    @pytest.mark.parametrize("needle", [12, 23])
    def test_change_left_end_needle(self, file, get_needle_positions, machine,
                                    needle):
        communication = Communication(file, get_needle_positions, machine,
                                      left_end_needle=needle)
        assert communication.left_end_needle == needle

    @pytest.mark.parametrize("needle", [12, 23])
    def test_change_right_end_needle(self, file, get_needle_positions, machine,
                                     needle):
        communication = Communication(file, get_needle_positions, machine,
                                      right_end_needle=needle)
        assert communication.right_end_needle == needle


class TestParallelization(object):

    @fixture
    def receive_message(self):
        return Mock()

    @fixture
    def communication(self, receive_message):
        communication = Communication(Mock(), Mock(), Mock())
        communication.receive_message = receive_message
        return communication

    @pytest.mark.timeout(1)
    def test_parallelize_calls_receive_message(self, communication):
        try:
            communication.start()
            communication.parallelize(0)
            assert communication._thread.is_alive()
            while communication.receive_message.call_count < 10:
                pass
        finally:
            communication.stop()

    @pytest.mark.timeout(1)
    def test_parallelize_can_be_stopped(self, communication):
        try:
            communication.start()
            communication.parallelize(0)
            communication.stop()
            while communication._thread.is_alive():
                pass
        finally:
            communication.stop()

    @pytest.mark.timeout(1)
    def test_parallelize_before_start_calls_start(self, communication):
        try:
            communication.start = start = Mock()
            communication.parallelize(0)
            while not start.called:
                pass
        finally:
            communication.stop()

    @pytest.mark.timeout(1)
    def test_parallelize_after_stop_is_ok(
            self, communication):
        try:
            communication.start()
            communication.stop()
            communication.parallelize(0)
            communication._thread.join()
        finally:
            communication.stop()

    def test_runs_in_parallel_is_false_on_start(self, communication):
        assert not communication.runs_in_parallel()

    @pytest.mark.timeout(1)
    def _test_still_running(self, communication):
        try:
            communication.start()
            communication.parallelize(0)
            assert communication.runs_in_parallel()
            communication.stop()
            communication._thread.join()
            assert not communication.runs_in_parallel()
        finally:
            communication.stop()
