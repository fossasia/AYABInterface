"""This module contains the configuration of the shield.

The configuration is seperate from the interface. They are composed instead of
inherited.
"""
from .utils import number_of_colors

_NUMBER_OF_NEEDLES_ERROR_MESSAGE = \
    "The number of needles in row {index} is {got} but {expected} was" \
    " expected."
_INDEX_NOT_IN_ROWS = \
    "The start index is {got}. Expected 0 <= {got}."
_COLOR_SHOULD_BE_INT = \
    "The color {got} at {index} in row {row_index} is a {type_name} but an" \
    "int was expected."
_COLOR_OUT_OF_BOUNDS = \
    "The color {got} at {index} in row {row_index} is a out of bounds." \
    " Expected 0 <= {got} <= {maximum}."
_END_NEEDLE_INVALID = \
    "The {which} end needle has to be between {min} and {max}, but is " \
    "set to {got}."


class InvalidConfigurationException(ValueError):

    """This occurs when the configuration is invalid."""


class Configuration(object):

    """The configuration of the interface."""

    def __init__(self, rows, machine_type, left_end_needle, right_end_needle,
                 start_index_in_rows=0):
        """Create a new configuration.

        :param list rows: a :class:`list` of :class:`lists <list>` of
          :class:`colors <int>`. Each color is a positive :class:`integer
          <int>`. All colors start from 0 and go up to the
          :attr:`number of colors <number_of_colors>` - 1.
        :param AYABInterface.machines.Machine machine_type: the type of the
          used machine
        :param int left_end_needle: Leftmost needle of the pattern to knit.
        :param int right_end_needle: Rightmost needle of the pattern to knit.
        :param int start_index_in_rows: the index of the first row to use.
          The rows with an index lower than this are ignored.
        :raises AYABInterface.configuration.InvalidConfigurationException:
          if the configuration is invalid
        """
        self._rows = rows
        self._machine_type = machine_type
        self._left_end_needle = left_end_needle
        self._right_end_needle = right_end_needle
        self._index_of_first_row = start_index_in_rows
        self._number_of_colors = number_of_colors(rows)
        self.check()

    def check(self):
        """Check whether this configuration is valid.

        :raises AYABInterface.configuration.InvalidConfigurationException:
          if this configuration is invalid
        """
        expected_needles = self._machine_type.number_of_needles
        max_color = self._number_of_colors - 1
        for index, row in enumerate(self._rows):
            if len(row) != expected_needles:
                message = _NUMBER_OF_NEEDLES_ERROR_MESSAGE.format(
                    index=index, got=len(row), expected=expected_needles)
                raise InvalidConfigurationException(message, row)
            for color_index, color in enumerate(row):
                if not isinstance(color, int):
                    message = _COLOR_SHOULD_BE_INT.format(
                        got=color, index=color_index, row_index=index,
                        type_name=type(color).__name__)
                    raise InvalidConfigurationException(message)
                if color < 0 or color >= max_color:
                    message = _COLOR_OUT_OF_BOUNDS.format(
                        got=color, index=color_index, row_index=index,
                        maximum=max_color)
                    raise InvalidConfigurationException(message)

        index = self._index_of_first_row
        if index < 0:
            message = _INDEX_NOT_IN_ROWS.format(got=index)
            raise InvalidConfigurationException(message)

        left_end_needle = self._left_end_needle
        if left_end_needle < 0 or left_end_needle >= expected_needles:
            message = _END_NEEDLE_INVALID.format(
                which="left", min=0, max=expected_needles - 1,
                got=left_end_needle)
            raise InvalidConfigurationException(message)

        right_end_needle = self._right_end_needle
        if right_end_needle <= left_end_needle or \
                right_end_needle > expected_needles:
            message = _END_NEEDLE_INVALID.format(
                which="right", min=left_end_needle + 1, max=expected_needles,
                got=right_end_needle)
            raise InvalidConfigurationException(message)

    @property
    def machine(self):
        """The machine type.

        :rtype: AYABInterface.machines.Machine
        """
        return self._machine_type

    @property
    def rows(self):
        """The rows that should be knit

        :rtype: list
        :return: the rows
        """
        return self._rows

    @property
    def index_of_first_row(self):
        """The index of the current row in progress.

        :rtype: int
        """
        return self._index_of_first_row

    @property
    def number_of_colors(self):
        """The number of colors used in the rows.

        :rtype: int
        """
        return self._number_of_colors

__all__ = ["Configuration", "InvalidConfigurationException"]
