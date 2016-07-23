"""This module provides the interface to the AYAB shield."""
from .communication import Content

_NEEDLE_POSITION_ERROR_MESSAGE = \
    "Needle position in row {} at index {} is {} but one of {} was expected."
_ROW_LENGTH_ERROR_MESSAGE = "The length of row {} is {} but {} is expected."


class NeedlePositions(Content):

    """An interface that just focusses on the needle positions."""

    def __init__(self, rows, machine):
        """Create a needle interface.

        :param list rows: a list of lists of :attr:`needle positions
            <AYABInterface.machines.Machine.needle_positions>`
        :param AYABInterface.machines.Machine: the machine type to use
        :raises ValueError: if the arguments are not valid, see :meth:`check`
        """
        self._rows = rows
        self._machine = machine
        self._completed_rows = []
        self.check()

    def check(self):
        """Check for validity.

        :raises ValueError:

          - if not all lines are as long as the :attr:`number of needles
            <AYABInterface.machines.Machine.number_of_needles>`
          - if the contents of the rows are not :attr:`needle positions
            <AYABInterface.machines.Machine.needle_positions>`
        """
        expected_positions = self._machine.needle_positions
        expected_row_length = self._machine.number_of_needles
        for row_index, row in enumerate(self._rows):
            if len(row) != expected_row_length:
                message = _ROW_LENGTH_ERROR_MESSAGE.format(
                    row_index, len(row), expected_row_length)
                raise ValueError(message)
            for needle_index, needle_position in enumerate(row):
                if needle_position not in expected_positions:
                    message = _NEEDLE_POSITION_ERROR_MESSAGE.format(
                        row_index, needle_index, repr(needle_position),
                        ", ".join(map(repr, expected_positions)))
                    raise ValueError(message)

    # The Content interface

    @property
    def machine(self):
        """The machine these positions are on."""
        return self._machine

    def get_row(self, index, default=None):
        """Return the row at the given index or the default value."""
        if not isinstance(index, int) or index < 0 or index >= len(self._rows):
            return default
        return self._rows[index]

    def row_completed(self, index):
        """Mark the row at index as completed.

        .. seealso:: :meth:`completed_row_indices`
        """
        self._completed_rows.append(index)

    @property
    def completed_row_indices(self):
        """The indices of the completed rows.

        :rtype: list

        When a :meth:`row was completed <row_completed>`, the index of the row
        turns up here. The order is preserved, entries may occur duplicated.
        """
        return self._completed_rows.copy()


class ColorInterface(object):

    """This class provides the interface for communication with the shield."""

    def __init__(self, configuration, communication):
        """Create a new interface to the AYAB shield.

        .. todo:: Provide an interface to stop knitting manually.

        :param AYABInterface.configuration.Configuration configuration:
          the configuration of the interface
        :param AYABInterface.communication.Communication communication:
          the communication interface to the shield
        """
        self._configuration = configuration
        self._communication = communication

    @property
    def communication(self):
        """The communication in use.

        :rtype: AYABInterface.communication.Communication
        """
        return self._communication

    @property
    def initial_configuration(self):
        """The initial configuration of the interface.

        :rtype: AYABInterface.configuration.Configuration
        """
        return self._configuration

    @property
    def machine(self):
        """The machine this interface is connected to.

        :rtype: AYABInterface.machines.Machine
        """
        return self._configuration.machine

    @property
    def current_row(self):
        """The row currently in progress.

        :rtype: list
        :return: a list of :class:`colors <int>`. If a color was knit, it is
          positive. Colors that were not knit are negative.
        """

    @property
    def index_of_current_row(self):
        """The index of the current row.

        :rtype: int
        """

    @property
    def carriages(self):
        """The carriages used.

        :return: a :class:`list` of :class:`carriages
          <AYABInterface.carriages.Carriage>`
        :rtype: list
        """
        return [self.color_carriage]

    @property
    def color_carriage(self):
        """The carriage to knit with color.

        :rtype: AYABInterface.carriages.Carriage
        """

    @property
    def actions(self):
        """A list of actions that are to to.

        :return: an iterable over :class:`actions
          <AYABInterface.actions.Action>` to perform.
        """
        # TODO: does this match the expectations?

    def needle_positions(self):
        """Return the needle positions.

        :rtype: AYABInterface.interface.NeedlePositions
        """

__all__ = ["ColorInterface", "NeedlePositions"]
