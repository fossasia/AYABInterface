from AYABInterface.communication.states import ConnectionClosed, \
    WaitingForStart, InitialHandshake, UnsupportedApiVersion, \
    InitializingMachine, StartingToKnit, StartingFailed, KnittingStarted, \
    KnittingLine
from pytest import fixture
from unittest.mock import Mock
from test_assertions import assert_identify
import pytest
from AYABInterface.communication.host_messages import LineConfirmation, \
    StartRequest, InformationRequest


class StateTest(object):

    """Base class for testing states."""

    state_class = None  #: the class to test
    tests = None  #: the true tests

    @fixture
    def message(self):
        return Mock()

    @fixture
    def communication(self):
        communication = Mock()
        communication.state = None
        return communication

    @fixture
    def state(self, communication):
        assert self.state_class is not None, "Set state_class!"
        return self.state_class(communication)

    def test_receive_message(self, state):
        """The receive_message method double dispatches to the message."""
        message = Mock()
        state.receive_message(message)
        message.received_by.assert_called_once_with(state)

    def test_connection_closed(self, state, communication, message):
        state.receive_connection_closed(message)
        assert communication.state.is_connection_closed()

    def test_true_tests(self, state):
        assert self.tests is not None
        assert_identify(state, self.tests)


class TestConnectionClosed(StateTest):

    """Test ConnectionClosed.

    Test for
    :class:`AYABInterface.communication.states.ConnectionClosed`.
    """

    state_class = ConnectionClosed  #: the class to test
    tests = ["is_final", "is_connection_closed"]  #: the true tests


class TestWaitingForStart(StateTest):

    """Test ConnectionClosed.

    Test for
    :class:`AYABInterface.communication.states.ConnectionClosed`.
    """

    state_class = WaitingForStart  #: the class to test
    tests = ["is_before_knitting", "is_waiting_for_start"]  #: the true tests

    def test_on_started(self, state, communication):
        state.communication_started()
        assert communication.state.is_initial_handshake()


class TestInitialHandshake(StateTest):

    state_class = InitialHandshake  #: the class to test
    tests = ["is_before_knitting", "is_initial_handshake"]  #: the true tests

    def test_enter_and_send_information_request(self, state, communication):
        state.enter()
        communication.send.assert_called_once_with(InformationRequest)

    def test_positive_response(self, state, message, communication):
        message.api_version_is_supported.return_value = True
        state.receive_information_confirmation(message)
        assert communication.state.is_initializing_machine()

    def test_negative_response(self, state, message, communication):
        message.api_version_is_supported.return_value = False
        state.receive_information_confirmation(message)
        assert communication.state.is_unsupported_api_version()


class TestUnsupportedApiVersion(StateTest):

    state_class = UnsupportedApiVersion  #: the class to test
    tests = ["is_final", "is_unsupported_api_version"]  #: the true tests


class TestInitializingMachine(StateTest):

    state_class = InitializingMachine  #: the class to test

    #: the true tests
    tests = ["is_before_knitting", "is_initializing_machine",
             "is_waiting_for_carriage_to_pass_the_left_turn_mark"]

    def test_ready_indicated(self, state, message, communication):
        message.is_ready_to_knit.return_value = True
        state.receive_state_indication(message)
        assert communication.state.is_starting_to_knit()

    def test_ready_not_indicated(self, state, message, communication):
        message.is_ready_to_knit.return_value = False
        state.receive_state_indication(message)
        assert communication.state is None


class TestStartingToKnit(StateTest):

    state_class = StartingToKnit  #: the class to test
    tests = ["is_before_knitting", "is_starting_to_knit"]  #: the true tests

    def test_success(self, state, message, communication):
        message.is_success.return_value = True
        state.receive_start_confirmation(message)
        assert communication.state.is_knitting_started()

    def test_failure(self, state, message, communication):
        message.is_success.return_value = False
        state.receive_start_confirmation(message)
        assert communication.state.is_starting_failed()

    def test_enter_sends_start_confirmation(self, state, communication):
        state.enter()
        communication.send.assert_called_once_with(
            StartRequest, communication.left_end_needle,
            communication.right_end_needle)


class TestStartingFailed(StateTest):

    state_class = StartingFailed  #: the class to test
    tests = ["is_final", "is_starting_failed"]  #: the true tests


class TestKnittingStarted(StateTest):

    state_class = KnittingStarted  #: the class to test
    tests = ["is_knitting", "is_knitting_started"]  #: the true tests

    @pytest.mark.parametrize("number", [1, 4, 66])
    def test_receive_line_request(self, message, state, communication, number):
        print(state, self)
        message.line_number = number
        state.receive_line_request(message)
        assert communication.state.is_knitting_line()
        assert communication.state.line_number == number
        assert communication.state != state


class TestKnittingLine(TestKnittingStarted):

    state_class = KnittingLine  #: the class to test
    tests = ["is_knitting", "is_knitting_line"]  #: the true tests
    line_number = object()

    @fixture
    def state(self, communication):
        return self.state_class(communication, self.line_number)

    def test_line_number(self, state):
        assert state.line_number == self.line_number

    @pytest.mark.parametrize("result", [True, False])
    def test_last_line(self, state, communication, result):
        communication.is_last_line.return_value = result
        assert state.is_knitting_last_line() == result
        communication.is_last_line.assert_called_once_with(self.line_number)

    def test_enter_sends_line_configuration(self, state, communication):
        state.enter()
        communication.send.assert_called_once_with(LineConfirmation,
                                                   self.line_number)

    def test_enter_sets_last_line_requested(self, state, communication):
        state.enter()
        assert communication.last_requested_line_number == self.line_number
