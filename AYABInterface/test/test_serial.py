"""Test the serial specification."""
from AYABInterface.serial import list_serial_ports, list_serial_port_strings, \
    SerialPort
import AYABInterface
import AYABInterface.serial as serial
import pytest
from unittest.mock import Mock, call


class TestListPorts(object):

    """Test the port listing."""

    def test_list_connections_includes_serial_connections(self, monkeypatch):
        """test that all serial connections are int the listed ocnnections."""
        mocked_list = Mock()
        monkeypatch.setattr(serial, "list_serial_ports", mocked_list)
        assert AYABInterface.get_connections() == mocked_list.return_value
        mocked_list.assert_called_once_with()

    @pytest.mark.parametrize("ports", [["asd", "asdsd", "COM1"], [1, 2, 3, 4]])
    def test_serial_ports_use_the_result_from_strings(
            self, monkeypatch, ports):
        serial_port = Mock()
        serial_ports = Mock()
        serial_ports.return_value = ports
        monkeypatch.setattr(serial, "SerialPort", serial_port)
        monkeypatch.setattr(serial, "list_serial_port_strings", serial_ports)
        listed_ports = list_serial_ports()
        assert listed_ports == [serial_port.return_value] * len(ports)
        serial_port.assert_has_calls(list(map(call, ports)))
        serial_ports.assert_called_once_with()

    def test_list_serial_ports_strings_works(self):
        assert isinstance(list_serial_port_strings(), list)


class TestSerialPort(object):

    """Test the SerialPort."""

    @pytest.mark.parametrize("port", ["COM1", "COM2", "COM24"])
    def test_get_name(self, port):
        serial_port = SerialPort(port)
        assert serial_port.name == port

    def test_connect(self, monkeypatch):
        """test creating new serial.Serial instances.

        For the baud rate see :ref:`serial-communication-specification`.
        """
        Serial = Mock()
        port = Mock()
        monkeypatch.setattr(serial, "Serial", Serial)
        serial_port = SerialPort(port)
        serial_connection = serial_port.connect()
        assert serial_connection == Serial.return_value
        Serial.assert_called_once_with(port, 115200)

    def test_can_mock_serial_Serial(self):
        from serial import Serial
        assert serial.Serial == Serial

    @pytest.mark.parametrize("port", ["COM1", "COM2", "COM24"])
    def test_string(self, port):
        serial_port = SerialPort(port)
        string = repr(serial_port)
        assert string == "<SerialPort \"{}\">".format(port)
