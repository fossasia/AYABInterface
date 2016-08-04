"""This module is used to communicate with the shield.

Requirement: Make objects from binary stuff.
"""
from .hardware_messages import read_message_type, ConnectionClosed
from .states import WaitingForStart
from .cache import NeedlePositionCache
from threading import RLock, Thread
from itertools import chain
from time import sleep


class Communication(object):

    """This class comunicates with the AYAB shield."""

    def __init__(self, file, get_needle_positions, machine,
                 on_message_received=(), left_end_needle=None,
                 right_end_needle=None):
        """Create a new Communication object.

        :param file: a file-like object with read and write methods for the
          communication with the Arduino. This could be a
          :class:`serial.Serial` or a :meth:`socket.socket.makefile`.
        :param get_needle_positions: a callable that takes an :class:`index
          <int>` and returns :obj:`None` or an iterable over needle positions.
        :param AYABInterface.machines.Machine machine: the machine to use for
          knitting
        :param list on_message_received: an iterable over callables that takes
          a received :class:`message
          <AYABInterface.communication.hardware_messages.Message>` whenever
          it comes in. Since :attr:`state` changes only take place when a
          message is received, this can be used as an state observer.
        :param left_end_needle: A needle number on the machine.
          Other needles that are on the left side of this needle are not used
          for knitting. Their needle positions are not be set.
        :param right_end_needle: A needle number on the machine.
          Other needles that are on the right side of this needle are not used
          for knitting. Their needle positions are not be set.

        """
        self._file = file
        self._on_message_received = on_message_received
        self._machine = machine
        self._state = WaitingForStart(self)
        self._controller = None
        self._last_requested_line_number = 0
        self._needle_positions_cache = NeedlePositionCache(
            get_needle_positions, self._machine)
        self._left_end_needle = (
            machine.left_end_needle
            if left_end_needle is None else left_end_needle)
        self._right_end_needle = (
            machine.right_end_needle
            if right_end_needle is None else right_end_needle)
        self._lock = RLock()
        self._thread = None
        self._number_of_threads_receiving_messages = 0
        self._on_message = []

    @property
    def needle_positions(self):
        """A cache for the needle positions.

        :rtype: AYABInterface.communication.cache.NeedlePositionCache
        """
        return self._needle_positions_cache

    def start(self):
        """Start the communication about a content.

        :param Content content: the content of the communication.
        """
        with self.lock:
            self._state.communication_started()

    _read_message_type = staticmethod(read_message_type)

    def _message_received(self, message):
        """Notify the observers about the received message."""
        with self.lock:
            self._state.receive_message(message)
            for callable in chain(self._on_message_received, self._on_message):
                callable(message)

    def on_message(self, callable):
        """Add an observer to received messages.

        :param callable: a callable that is called every time a
          :class:`AYABInterface.communication.host_messages.Message` is sent or
          a :class:`AYABInterface.communication.controller_messages.Message` is
          received
        """
        self._on_message.append(callable)

    def receive_message(self):
        """Receive a message from the file."""
        with self.lock:
            assert self.can_receive_messages()
            message_type = self._read_message_type(self._file)
            message = message_type(self._file, self)
            self._message_received(message)

    def can_receive_messages(self):
        """Whether tihs communication is ready to receive messages.]

        :rtype: bool

        .. code:: python

            assert not communication.can_receive_messages()
            communication.start()
            assert communication.can_receive_messages()
            communication.stop()
            assert not communication.can_receive_messages()

        """
        with self.lock:
            return not self._state.is_waiting_for_start() and \
                not self._state.is_connection_closed()

    def stop(self):
        """Stop the communication with the shield."""
        with self.lock:
            self._message_received(ConnectionClosed(self._file, self))

    def api_version_is_supported(self, api_version):
        """Return whether an api version is supported by this class.

        :rtype: bool
        :return: if the :paramref:`api version <api_version>` is supported
        :param int api_version: the api version

        Currently supported api versions: ``4``
        """
        return api_version == 4

    def send(self, host_message_class, *args):
        """Send a host message.

        :param type host_message_class: a subclass of
          :class:`AYABImterface.communication.host_messages.Message`
        :param args: additional arguments that shall be passed to the
          :paramref:`host_message_class` as arguments
        """
        message = host_message_class(self._file, self, *args)
        with self.lock:
            message.send()
            for callable in self._on_message:
                callable(message)

    @property
    def state(self):
        """The state this object is in.

        :return: the state this communication object is in.
        :rtype: AYABInterface.communication.states.State

        .. note:: When calling :meth:`parallelize` the state can change while
          you check it.
        """
        return self._state

    @property
    def lock(self):
        """The lock of the communication.

        In case you :meth:`parallelize` the communication, you may want to use
        this :class:`lock <threading.RLock>` to make shure the parallelization
        does not break your code.
        """
        return self._lock

    @state.setter
    def state(self, new_state):
        """Set the state."""
        with self.lock:
            self._state.exit()
            self._state = new_state
            self._state.enter()

    @property
    def left_end_needle(self):
        """The left end needle of the needle positions.

        :rtype: int
        :return: the :attr:`left end needle of the machine
          <AYABInterface.machine.Machine.left_end_needle>`
        """
        return self._left_end_needle

    @property
    def right_end_needle(self):
        """The left end needle of the needle positions.

        :rtype: int
        :return: the :attr:`right end needle of the machine
          <AYABInterface.machine.Machine.right_end_needle>`
        """
        return self._right_end_needle

    @property
    def controller(self):
        """Information about the controller.

        If no information about the controller is received, the return value
        is :obj:`None`.

        If information about the controller is known after :ref:`cnfinfo` was
        received, you can access these values:

        .. code:: python

            >>> communication.controller.firmware_version
            (5, 2)
            >>> communication.controller.firmware_version.major
            5
            >>> communication.controller.firmware_version.minor
            2
            >>> communication.controller.api_version
            4

        """
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value

    @property
    def last_requested_line_number(self):
        """The number of the last line that was requested.

        :rtype: int
        :return: the last requested line number or ``0``
        """
        return self._last_requested_line_number

    @last_requested_line_number.setter
    def last_requested_line_number(self, line_number):
        """Set the last requested line number."""
        self._last_requested_line_number = line_number

    def parallelize(self, seconds_to_wait=2):
        """Start a parallel thread for receiving messages.

        If :meth:`start` was no called before, start will be called in the
        thread.
        The thread calls :meth:`receive_message` until the :attr:`state`
        :meth:`~AYABInterface.communication.states.State.is_connection_closed`.

        :param float seconds_to_wait: A time in seconds to wait with the
          parallel execution. This is useful to allow the controller time to
          initialize.

        .. seealso:: :attr:`lock`, :meth:`runs_in_parallel`
        """
        with self.lock:
            thread = Thread(target=self._parallel_receive_loop,
                            args=(seconds_to_wait,))
            thread.deamon = True
            thread.start()
            self._thread = thread

    def _parallel_receive_loop(self, seconds_to_wait):
        """Run the receiving in parallel."""
        sleep(seconds_to_wait)
        with self._lock:
            self._number_of_threads_receiving_messages += 1
        try:
            with self._lock:
                if self.state.is_waiting_for_start():
                    self.start()
            while True:
                with self.lock:
                    if self.state.is_connection_closed():
                        return
                    self.receive_message()
        finally:
            with self._lock:
                self._number_of_threads_receiving_messages -= 1

    def runs_in_parallel(self):
        """Whether the communication runs in parallel.

        :rtype: bool
        :return: whether :meth:`parallelize` was called and the communication
          still receives messages and is not stopped
        """
        return self._number_of_threads_receiving_messages != 0

__all__ = ["Communication"]
