"""This module contains the information about the different types of machines.

Every machine specific knowledge should be put in this file. Machine specific
knowledge is, for example:

- the number of needles a machine supports
- whether it is single or double bed
- how many colors are supported
- the name of the machine

"""
from abc import ABCMeta, abstractmethod,abstractproperty


class Machine(object, metaclass=ABCMeta):

    """The type of the machine.

    This is an abstract base class and some methods need to be overwritten.
    """

    @abstractproperty
    def number_of_needles(self):
        """The number of needles of this machine.
        
        :rtype: int
        """

    @abstractproperty
    def needle_positions(self):
        """The different needle positions.
        
        :rtype: tuple
        """

    def is_ck35(self):
        """Whether this machine is a Brother CK-35.
        
        :rtype: bool
        """
        return isinstance(self, CK35)

    def is_kh900(self):
        """Whether this machine is a Brother KH-910.
        
        :rtype: bool
        """
        return isinstance(self, KH900)

    def is_kh910(self):
        """Whether this machine is a Brother KH-900.
        
        :rtype: bool
        """
        return isinstance(self, KH910)

    def is_kh930(self):
        """Whether this machine is a Brother KH-930.
        
        :rtype: bool
        """
        return isinstance(self, KH930)

    def is_kh950(self):
        """Whether this machine is a Brother KH-950.
        
        :rtype: bool
        """
        return isinstance(self, KH950)

    def is_kh965(self):
        """Whether this machine is a Brother KH-965.
        
        :rtype: bool
        """
        return isinstance(self, KH965)


    def is_kh270(self):
        """Whether this machine is a Brother KH-270.
        
        :rtype: bool
        """
        return isinstance(self, KH270)


class KH9XXSeries(Machine):
    
    """The base class for the KH9XX series."""

    def number_of_needles(self):
        """The number of needles on this machine.
        
        :rtype: int
        :return: ``200``. The KH9XX series has 200 needles.
        """
        return 200

    def needle_positions(self):
        """The different needle positions.
        
        :rtype: tuple
        :return: the needle positions are "B" and "D"
        """
        return ("B", "D")


class KH900(KH9XXSeries):
    
    """The machine type for the Brother KH-900."""


class KH910(KH9XXSeries):
    
    """The machine type for the Brother KH-910."""


class KH930(KH9XXSeries):
    
    """The machine type for the Brother KH-930."""


class KH950(KH9XXSeries):
    
    """The machine type for the Brother KH-950."""


class KH965(KH9XXSeries):
    
    """The machine type for the Brother KH-965."""


class CK35(Machine):
    
    """The machine type for the Brother CK-35."""
    
    def number_of_needles(self):
        """The number of needles on this machine.
        
        :rtype: int
        :return: ``200``. The KH9XX series has 200 needles.
        """
        return 200



class KH270(Machine):
    
    """The machine type for the Brother KH-270."""
    
    def number_of_needles(self):
        """The number of needles on this machine.
        
        :rtype: int
        :return: ``200``. The KH9XX series has 200 needles.
        """
        return 114




__all__ = ["Machine", "KH9XXSeries", "CK35", "KH900", "KH910", "KH930",
           "KH950", "KH965", "KH270"]
