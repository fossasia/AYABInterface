"""This module provides the interface to the AYAB shield."""
from itertools import chain


class NeeldePositions(object):

    """An interface that just focusses on the needle positions."""
    
    def __init__(self, needle_positions, start_index, machine):
        """Create a needle interface.
        
        :needle_positions: a"""
        self._needle_positions = needle_positions
        self._machine = machine
        self.check()
    
    @property
    def machine(self):
        """The machine these positions are on."""
        return self._machine
        
    
    def check(self):
        """Check for validity.
        
        :raises TypeError: if the contents of the lists in the list are not
          all :class:`integers <int>`
        :raises ValueError: if the lines are empty or not of same size or the
          contents are not within the range of
          :attr:`number_of_needle_positions`
        """
    
    @property
    def all_needle_positions(self):
        """The posistions of the needles.
        
        :rtype: list
        """
        return self._needle_positions

    def current_needle_positions()
        




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
        
    def primitive_interface(self):
        """Return the primitive interface.
        
        :rtype: PrimitiveInterface
        """

__all__ = ["Interface"]
