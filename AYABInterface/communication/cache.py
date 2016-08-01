"""Convert and cache needle positions."""
from crc8 import crc8


class NeedlePositionCache(object):

    """Convert and cache needle positions."""

    def __init__(self, get_needle_positions, machine):
        """Create a new NeedlePositions object."""
        self._get = get_needle_positions
        self._machine = machine
        self._get_cache = {}
        self._needle_position_bytes_cache = {}
        self._line_configuration_message_cache = {}

    def get(self, line_number):
        """Return the needle positions or None.

        :param int line_number: the number of the line
        :rtype: list
        :return: the needle positions for a specific line specified by
          :paramref:`line_number` or :obj:`None` if no were given
        """
        if line_number not in self._get_cache:
            self._get_cache[line_number] = self._get(line_number)
        return self._get_cache[line_number]

    def is_last(self, line_number):
        """Whether the line number is has no further lines.

        :rtype: bool
        :return: is the next line above the line number are not specified
        """
        return self.get(line_number + 1) is None

    def get_bytes(self, line_number):
        """Get the bytes representing needle positions or None.

        :param int line_number: the line number to take the bytes from
        :rtype: bytes
        :return: the bytes that represent the message or :obj:`None` if no
          data is there for the line.

        Depending on the :attr:`machine`, the length and result may vary.
        """
        if line_number not in self._needle_position_bytes_cache:
            line = self._get(line_number)
            if line is None:
                line_bytes = None
            else:
                line_bytes = self._machine.needle_positions_to_bytes(line)
            self._needle_position_bytes_cache[line_number] = line_bytes
        return self._needle_position_bytes_cache[line_number]

    def get_line_configuration_message(self, line_number):
        """Return the cnfLine content without id for the line.

        :param int line_number: the number of the line
        :rtype: bytes
        :return: a cnfLine message without id as defined in :ref:`cnfLine`
        """
        if line_number not in self._line_configuration_message_cache:
            line_bytes = self.get_bytes(line_number)
            if line_bytes is not None:
                line_bytes = bytes([line_number & 255]) + line_bytes
                line_bytes += bytes([self.is_last(line_number)])
                line_bytes += crc8(line_bytes).digest()
            self._line_configuration_message_cache[line_number] = line_bytes
            del line_bytes
        line = self._line_configuration_message_cache[line_number]
        if line is None:
            # no need to cache a lot of empty lines
            line = (bytes([line_number & 255]) +
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' +
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01')
            line += crc8(line).digest()
        return line

__all__ = ["NeedlePositionCache"]
