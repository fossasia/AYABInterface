"""This module provides the interface to the AYAB shield."""
from itertools import chain
from .Communication import Content

class NeeldePositions(Content):

    """An interface that just focusses on the needle positions."""
    
    def __init__(self, rows, machine):
        """Create a needle interface.
        
        :param list rows: a list of lists of :attr:`needle positions
            <AYABInterface.machines.Machine.needle_positions>`
        :param AYABInterface.machines.Machine: the machine type to use
        :raises ValueError: if the arguments are not valid, see :meth:`check`
        """
        self._needle_positions = needle_positions
        self._machine = machine
        self.check()

    def check(self):
        """Check for validity.
        
        :raises ValueError: 
          
          - if not all lines are as long as the :attr:`number of needles
            <AYABInterface.machines.Machine.number_of_needles>`
          - if the contents of the rows are not :attr:`needle positions
            <AYABInterface.machines.Machine.needle_positions>`
        """

    # The Content interface
        
    @property
    def machine(self):
        """The machine these positions are on."""
        return self._machine
    
    def get_row(self, index, default=None):
        """Return the row at the given index or the default value."""

    def row_completed(self, index):
        """Mark the row at index as completed.
        
        .. seealso:: :meth:`completed_row_indices`"""
    
    @property
    def completed_row_indices(self):
        """The indices of the completed rows.
        
        :rtype: list
        
        When a :meth:`row was completed <row_completed>`, the index of the row
        turns up here. The order is preserved, entries may occur duplicated.
        """


class ColorInterface(object):

    """This class provides the interface for communication with the shield."""
    
    def __init__(self, configuration, communication):
        """Create a new interface to the AYAB shield.
        
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
        
        :rtype: NeeldePositions
        """

__all__ = ["ColorInterface", "NeeldePositions"]
