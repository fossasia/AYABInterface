"""This module provides the interface to the AYAB shield."""

_NEEDLE_POSITION_ERROR_MESSAGE = \
    "Needle position in row {} at index {} is {} but one of {} was expected."
_ROW_LENGTH_ERROR_MESSAGE = "The length of row {} is {} but {} is expected."


class NeedlePositions(object):

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
        self._on_row_completed = []
        self.check()

    def check(self):
        """Check for validity.

        :raises ValueError:

          - if not all lines are as long as the :attr:`number of needles
            <AYABInterface.machines.Machine.number_of_needles>`
          - if the contents of the rows are not :attr:`needle positions
            <AYABInterface.machines.Machine.needle_positions>`
        """
        # TODO: This violates the law of demeter.
        #       The architecture should be changed that this check is either
        #       performed by the machine or by the unity of machine and
        #       carriage.
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

    # the Content interface

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

        This method notifies the obsevrers from :meth:`on_row_completed`.
        """
        self._completed_rows.append(index)
        for row_completed in self._on_row_completed:
            row_completed(index)

    # end of the Content interface

    @property
    def completed_row_indices(self):
        """The indices of the completed rows.

        :rtype: list

        When a :meth:`row was completed <row_completed>`, the index of the row
        turns up here. The order is preserved, entries may occur duplicated.
        """
        return self._completed_rows.copy()

    def on_row_completed(self, callable):
        """Add an observer for completed rows.

        :param callable: a callable that is called with the row index as first
          argument

        When :meth:`row_completed` was called, this :paramref:`callable` is
        called with the row index as first argument. Call this method several
        times to register more observers.
        """
        self._on_row_completed.append(callable)

__all__ = ["NeedlePositions"]
