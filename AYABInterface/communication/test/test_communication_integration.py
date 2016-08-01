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


class CommunicationTest(object):

    """Run a set of messages."""

    input = b''  #: the input
    output = b''  #: the output
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake"]
    lines = ["B" * 200]  #: the lines to get
    machine = KH910  #: the machine type
    lines_requested = None

    def get_line(self, line_number):
        if self.lines_requested is None:
            self.lines_requested = []
        self.lines_requested.append(line_number)
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
        output = connection.writer.getvalue().split(b'\r\n')
        expected_output = self.output.split(b'\r\n')
        assert output == expected_output, (len(output), len(expected_output))
        assert connection.reader.tell() == len(self.input), "All is read."
        self.after_test_run(communication)

    def after_test_run(self, communication):
        pass


class TestEmptyConnection(CommunicationTest):

    """Test what happens if no bytes are received."""

    output = b'\x03\r\n'  #: the output


class TestEmptyConnectionWithDebugMessages(CommunicationTest):

    """Insert debug messages."""

    input = b'#debug!\r\n#debug\r\n'  #: the input
    output = b'\x03\r\n'  #: the output
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake"] * 3


class TestUnsupportedAPIVersion(CommunicationTest):

    """Insert debug messages."""

    #: the input
    input = b'\xc3\x05\x00\x01\r\n'  # cnfInfo
    output = b'\x03\r\n'  #: the output
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake", "is_unsupported_api_version"]

    def after_test_run(self, communication):
        assert communication.controller.api_version == 5
        assert communication.controller.firmware_version == (0, 1)


class TestStartingFailed(CommunicationTest):

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


class TestKnitSomeLines(CommunicationTest):

    """Test that we knit some lines."""

    #: the lines to get
    lines = ["B" * 200] * 301
    lines[100] = "BBBBBBBDDBBBBBBBDDDDBBBBDBDBDBDB" + "B" * 168
    line_100 = b'\x80\x01\x0fU' + b'\00' * 21 + b'\x00' + b'\xd0'

    #: the input
    input = (b'\xc3\x04\x03\xcc\r\n' +  # cnfInfo
             b'\x84\x00BbCcde\r\n' +    # indState(false)
             b'\x84\x01BbCcde\r\n' +    # indState(true)
             b'\xc1\x01\r\n' +          # cnfStart(true)
             b'\x82\x64\r\n' +          # reqLine(100)
             b'\x82\xc8\r\n' +          # reqLine(200)
             b'\x82\x2c\r\n' +          # reqLine(300)
             b'\x82\x90\r\n' +          # reqLine(400)
             b'')
    #: the output
    output = (b'\x03\r\n' +                                   # reqInfo
              b'\x01\x00\xc7\r\n' +                           # reqStart
              b'\x42\x64' + line_100 + b'\r\n'                # cnfLine(100)
              b'\x42\xc8' + b'\x00' * 26 + b'\x07\r\n'        # cnfLine(200)
              b'\x42\x2c' + b'\x00' * 25 + b'\x01\xdd\r\n' +  # cnfLine(300)
              b'\x42\x90' + b'\x00' * 25 + b'\x01\xb3\r\n' +  # cnfLine(400)
              b'')
    #: the tests to perform between receiving messages
    states = ["is_initial_handshake", "is_initializing_machine",
              "is_initializing_machine", "is_starting_to_knit",
              "is_knitting_started", 100, 200, 300, 400]
