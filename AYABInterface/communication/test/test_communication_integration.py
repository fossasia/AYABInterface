"""Test whole message flows."""
from AYABInterface.communication import Communication
from AYABInterface.machines import KH910
from io import BytesIO
from pytest import fixture


class Connection(object):

    """A mocked connection."""

    def __init__(self, input):
        self.reader = BytesIO(input)
        self.writer = BytesIO()
        self.read = self.reader.read
        self.write = self.writer.write


class MessageTest(object):

    """Run a set of messages."""
    
    input = b''  #: the input
    output = b''  #: the output
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
    
    def test_run(self, communication, connection):
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
        assert connection.writer.getvalue() == self.output, "Output matches."
        assert connection.reader.tell() == len(self.input), "All is read."
        self.after_test_run(communication)
    
    def after_test_run(self, communication):
        pass


class TestEmptyConnection(MessageTest):

    """Test what happens if no bytes are received."""

    output = b'\x03\r\n'  #: the output


class TestEmptyConnectionWithDebugMessages(MessageTest):
    
    """Insert debug messages."""
    
    input = b'#debug!\r\n#debug\r\n'  #: the input
    output = b'\x03\r\n'  #: the output
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake"] * 3


class TestUnsupportedAPIVersion(MessageTest):
    
    """Insert debug messages."""
    
    #: the input
    input = b'\xc3\x05\x00\x01\r\n'  # cnfInfo
    output = b'\x03\r\n'  #: the output
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake", "is_unsupported_api_version"]
    
    def after_test_run(self, communication):
        assert communication.controller.api_version == 5
        assert communication.controller.firmware_version == (0, 1)


class TestStartingFailed(MessageTest):

    """Go into the StartingFailed state."""

    #: the input
    input = (b'\xc3\x04\x03\xcc\r\n' +  # cnfInfo
             b'\x84\x00BbCcde\r\n' +    # indState(false)
             b'\x84\x01BbCcde\r\n' +    # indState(true)
             b'\xc1\x00\r\n'            # cnfStart(false) 
             )
    #: the output
    output = (b'\x03\r\n' +        # reqInfo
              b'\x01\x00\xc7\r\n'  # reqStart
              )
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake", "is_initializing_machine",
              "is_initializing_machine", "is_starting_to_knit",
              "is_starting_failed"]
    
    def after_test_run(self, communication):
        assert communication.right_end_needle == 199
        assert communication.left_end_needle == 0

