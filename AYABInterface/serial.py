"""The serial interface.

Execute this module to print all serial ports currently available.
"""

import sys
import glob
try:
    import serial
    from serial import Serial
except:
    print("Install the serial module width '{} -m pip install PySerial'."
          "".format(sys.executable))


def list_serial_port_strings():
    """Lists serial port names.

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system

    .. seealso:: `The Stack Overflow answer
      <http://stackoverflow.com/a/14224477/1320237>`__
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def list_serial_ports():
    """Return a list of all available serial ports.

    :rtype: list
    :return: a list of :class:`serial ports <SerialPort>`
    """
    return list(map(SerialPort, list_serial_port_strings()))


class SerialPort(object):

    """A class abstracting the port behavior."""

    def __init__(self, port):
        """Create a new serial port instance.

        :param str port: the port to connect to

        .. note:: The baud rate is specified in
          :ref:`serial-communication-specification`
        """
        self._port = port

    @property
    def name(self):
        """The name of the port for displaying.

        :rtype: str
        """
        return self._port

    def connect(self):
        """Return a connection to this port.

        :rtype: serial.Serial
        """
        return Serial(self._port, 115200)

    def __repr__(self):
        """Return this object as string.

        :rtype: str
        """
        return "<{} \"{}\">".format(self.__class__.__name__,
                                    repr(self._port)[1:-1])

__all__ = ["list_serial_port_strings", "list_serial_ports", "SerialPort"]

if __name__ == '__main__':
    print(list_serial_port_strings())
