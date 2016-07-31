"""Test whole message flows."""
from AYABInterface.communication import Communication
from AYABInterface.machines import KH910
from io import BytesIO
from pytest import fixture


class Connection(object):

    """A mocked connection."""

    def __init__(self, input):
        self._reader = BytesIO(input)
        self._writer = BytesIO()
        self.read = self._reader.read
        self.write = self._writer.write


class MessageTest(object):

    """Run a set of messages."""
    
    input = b''  #: the input
    output = b''   #: the output
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake"]
    lines = ["B" * 200]  #: the lines to get
    machine = KH910  #: the machine type
    
    def get_line(self, line_numer):
        if 0 <= line_number < len(self.lines):
            return self.lines[line_number]
        return None
        
    @fixture
    def connection(self):
        return Connection(self.input)
        
    @fixture
    def communication(self, connection):
        return Communication(connection, self.get_line, self.machine(),
                             [lambda m: print("message:", m)])
    
    def test_run(self, communication):
        print("state:", communication.state)
        assert communication.state.is_waiting_for_start()
        communication.start()
        for test in self.states:
            print("state:", communication.state)
            if isinstance(test, str):
                test_method = getattr(communication.state, test)
                assert test_method()
            else:
                assert isinstance(test, int)
                assert communication.state.is_knitting_line()
                assert communication.state.line_number == test
            communication.receive_message()
        print("state:", communication.state)
        assert communication.state.is_connection_closed()


class TestEmptyConnection(MessageTest):

    """Test what happens if no bytes are received."""


class TestEmptyConnectionWithDebugMessages(MessageTest):
    
    """Insert debug messages."""
    
    input = b'#debug!\r\n#debug\r\n'  #: the input
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake"] * 3


