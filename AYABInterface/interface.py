"""This module provides the interface to the AYAB shield."""


class Interface(object):

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

__all__ = ["Interface"]
