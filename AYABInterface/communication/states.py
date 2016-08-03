"""This module contains the state machine for the communication class.

Click on this image to go to the states from the diagram:

.. image:: ../../../_static/CommunicationStateDiagram.svg
   :target: ../../../_static/CommunicationStateDiagram.html
   :alt: State Disgram for the Communication class.

"""
from .host_messages import InformationRequest, LineConfirmation, StartRequest


class State(object):

    """The base class for states."""

    def __init__(self, communication):
        """Create a new state.

        Please use the subclasses of this.

        :param AYABInterface.communication.Communication communication:
          the communication object which is in this state
        """
        self._communication = communication

    def enter(self):
        """Called when the state is entered.

        The :attr:`AYABInterface.communication.Communication.state` is set
        to this state.
        """

    def exit(self):
        """Called when this state is left.

        The :attr:`AYABInterface.communication.Communication.state` is set
        to this state.
        """

    def receive_message(self, message):
        """Receive a message from the controller.

        :param AYABInterface.communication.hardware_messages.Message message:
          the message to receive

        This method calls :meth:`message.received_by
        <AYABInterface.communication.hardware_messages.Message.received_by>`
        which dispatches the call to the ``receive_*`` methods.
        """
        message.received_by(self)

    def receive_state_indication(self, message):
        """Receive a StateIndication message.

        :param message: a :class:`StateIndication
          <AYABInterface.communication.hardware_messages.StateIndication>`
          message
        """

    def receive_line_request(self, message):
        """Receive a LineRequest message.

        :param message: a :class:`LineRequest
          <AYABInterface.communication.hardware_messages.LineRequest>`
          message
        """

    def receive_test_confirmation(self, message):
        """Receive a TestConfirmation message.

        :param message: a :class:`TestConfirmation
          <AYABInterface.communication.hardware_messages.TestConfirmation>`
          message
        """

    def receive_information_confirmation(self, message):
        """Receive a InformationConfirmation message.

        :param message: a :class:`InformationConfirmation
          <AYABInterface.communication.hardware_messages.InformationConfirmation>`
          message
        """

    def receive_debug(self, message):
        """Receive a Debug message.

        :param message: a :class:`Debug
          <AYABInterface.communication.hardware_messages.Debug>`
          message

        This logs the debug message.
        """

    def receive_start_confirmation(self, message):
        """Receive a StartConfirmation message.

        :param message: a :class:`StartConfirmation
          <AYABInterface.communication.hardware_messages.StartConfirmation>`
          message
        """

    def receive_unknown(self, message):
        """Receive a UnknownMessage message.

        :param message: a :class:`UnknownMessage
          <AYABInterface.communication.hardware_messages.UnknownMessage>`
          message
        """

    def receive_connection_closed(self, message):
        """Receive a ConnectionClosed message.

        :param message: a :class:`ConnectionClosed
          <AYABInterface.communication.hardware_messages.ConnectionClosed>`
          message

        If the is called, the communication object transits into the
        :class:`ConnectionClosed`.
        """
        self._next(ConnectionClosed)

    def is_waiting_for_the_communication_to_start(self):
        """Whether the communication can be started.

        When this is :obj:`True`, you call call
        :meth:`AYABInterface.communication.Communication.start` to leave the
        state.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_before_knitting(self):
        """Whether the knitting should start soon.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_knitting(self):
        """Whether the machine ready to knit or knitting.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_final(self):
        """Whether the communication is over.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_connection_closed(self):
        """Whether the connection is closed.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def communication_started(self):
        """Call when the communication starts."""

    def is_waiting_for_start(self):
        """Whether this state is waiting for the start.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_initial_handshake(self):
        """Whether the communication object is in the intial handshake.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def _next(self, state_class, *args):
        """Transition into the next state.

        :param type state_class: a subclass of :class:`State`. It is intialized
          with the communication object and :paramref:`args`
        :param args: additional arguments
        """
        self._communication.state = state_class(self._communication, *args)

    def is_unsupported_api_version(self):
        """Whether the API version of communcation and controller do not match.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_initializing_machine(self):
        """Whether the machine is currently being initialized.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_starting_to_knit(self):
        """Whether the machine initialized and knitting starts.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_knitting_started(self):
        """Whether the machine ready to knit the first line.

        :rtype: bool
        :return: :obj:`false`
        """
        return False

    def is_knitting_line(self):
        """Whether the machine knits a line.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def __repr__(self):
        """This object as string.

        :rtype: str
        """
        return "<{}>".format(self.__class__.__name__)


class FinalState(State):

    """Base class for states that can not reach knitting."""

    def is_final(self):
        """From the current state, the knitting can not be reached.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class ConnectionClosed(FinalState):

    """The connection is closed."""

    def is_connection_closed(self):
        """The connection is closed.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class WaitingForStart(State):

    """Waiting for the start() method to be called.

    This is the initial state of a
    :class:`AYABInterface.communication.Communication`.
    """

    def is_before_knitting(self):
        """Whether the knitting should start soon.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def communication_started(self):
        """Call when the communication starts.

        The communication object transits into :class:`InitialHandshake`.
        """
        self._next(InitialHandshake)

    def is_waiting_for_start(self):
        """Whether this state is waiting for the start.

        Call :meth:`AYABInterface.communication.Comunication.start` to leave
        this state.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class InitialHandshake(State):

    """The communication  has started."""

    def enter(self):
        """This starts the handshake.

        A :class:`AYABInterface.communication.host_messages.InformationRequest`
        is sent to the controller.
        """
        self._communication.send(InformationRequest)

    def receive_information_confirmation(self, message):
        """A InformationConfirmation is received.

        If :meth:`the api version is supported
        <AYABInterface.communication.Communication.api_version_is_supported>`,
        the communication object transitions into a
        :class:`InitializingMachine`, if unsupported, into a
        :class:`UnsupportedApiVersion`
        """
        if message.api_version_is_supported():
            self._next(InitializingMachine)
        else:
            self._next(UnsupportedApiVersion)

        self._communication.controller = message

    def is_before_knitting(self):
        """Whether the knitting should start soon.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_initial_handshake(self):
        """Whether the communication object is in the intial handshake.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class UnsupportedApiVersion(FinalState):

    """The api version of the controller is not supported."""

    def is_unsupported_api_version(self):
        """Whether the API version of communcation and controller do not match.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class InitializingMachine(State):

    """The machine is currently being intialized."""

    def is_before_knitting(self):
        """Whether the knitting should start soon.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_waiting_for_carriage_to_pass_the_left_turn_mark(self):
        """The carriage should be moved over the left turn mark.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def receive_state_indication(self, message):
        """Receive a StateIndication message.

        :param message: a :class:`StateIndication
          <AYABInterface.communication.hardware_messages.StateIndication>`
          message

        If the message says that the controller is :meth:`is ready to knit
        <AYABInterface.communication.hardware_messages.StateIndication.is_ready_to_knit>`,
        there is a transition to :class:`StartingToKnit` or else the messages
        are ignored because they come from :ref:`reqtest`.
        """
        if message.is_ready_to_knit():
            self._next(StartingToKnit)

    def is_initializing_machine(self):
        """Whether the machine is currently being initialized.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class StartingToKnit(State):

    """:ref:`cnfstart` is sent and we wait for an answer."""

    def is_before_knitting(self):
        """The knitting should start soon.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def receive_start_confirmation(self, message):
        """Receive a StartConfirmation message.

        :param message: a :class:`StartConfirmation
          <AYABInterface.communication.hardware_messages.StartConfirmation>`
          message

        If the message indicates success, the communication object transitions
        into :class:`KnittingStarted` or else, into :class:`StartingFailed`.
        """
        if message.is_success():
            self._next(KnittingStarted)
        else:
            self._next(StartingFailed)

    def is_starting_to_knit(self):
        """The machine initialized and knitting starts.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def enter(self):
        """Send a StartRequest."""
        self._communication.send(StartRequest,
                                 self._communication.left_end_needle,
                                 self._communication.right_end_needle)


class StartingFailed(FinalState):

    """The starting process has failed."""

    def is_starting_failed(self):
        """The machine machine could not be configured to start.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class KnittingStarted(State):

    """The knitting started and we are ready to receive :ref:`reqline`."""

    def receive_line_request(self, message):
        """Receive a LineRequest message.

        :param message: a :class:`LineRequest
          <AYABInterface.communication.hardware_messages.LineRequest>`
          message

        The communicaion transisitions into a :class:`KnittingLine`.
        """
        self._next(KnittingLine, message.line_number)

    def is_knitting(self):
        """The machine ready to knit or knitting.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_knitting_started(self):
        """The machine ready to knit the first line.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class KnittingLine(State):

    """The machine is currently knitting a line."""

    def __init__(self, communication, line_number):
        """The machine is knitting a line."""
        super().__init__(communication)
        self._line_number = line_number

    def enter(self):
        """Send a LineConfirmation to the controller.

        When this state is entered, a
        :class:`AYABInterface.communication.host_messages.LineConfirmation`
        is sent to the controller.
        Also, the :attr:`last line requested
        <AYABInterface.communication.Communication.last_requested_line_number>`
        is set.
        """
        self._communication.last_requested_line_number = self._line_number
        self._communication.send(LineConfirmation, self._line_number)

    def is_knitting(self):
        """The machine ready to knit or knitting.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_knitting_line(self):
        """The machine knits a line.

        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_knitting_last_line(self):
        """Whether the line currently knit is the last line.

        :rtype: bool
        """
        return self._communication.is_last_line(self._line_number) is True

    @property
    def line_number(self):
        """The number if the line which is currently knit.

        :rtype: int
        """
        return self._line_number

    def receive_line_request(self, message):
        """Receive a LineRequest message.

        :param message: a :class:`LineRequest
          <AYABInterface.communication.hardware_messages.LineRequest>`
          message

        The communicaion transisitions into a :class:`KnittingLine`.
        """
        self._next(KnittingLine, message.line_number)

# TODO: is it possible to know when the knitting process is over?
__all__ = ["State", "ConnectionClosed", "WaitingForStart",
           "InitialHandshake", "UnsupportedApiVersion",
           "InitializingMachine", "StartingToKnit", "StartingFailed",
           "KnittingStarted", "KnittingLine", "FinalState"]
