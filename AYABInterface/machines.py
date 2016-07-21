"""This module contains the information about the different types of machines.

Every machine specific knowledge should be put in this file. Machine specific
knowledge is, for example:

- the number of needles a machine supports
- whether it is single or double bed
- how many colors are supported
- the name of the machine

"""


class Machine(object):

    """The type of the machine."""
    
    def __init__(self, number_of_needles):
        """Create a new machine type.
        
        :param int number_of_needles: the number of needles that his machine
          has
        """
        self._number_of_needles = number_of_needles

    @property
    def number_of_needles(self):
        """The number of needles of this machine.
        
        :rtype: int
        """
        return self._number_of_needles

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
    
    def __init__(self):
        """Create a new machine type for the KH9Xx series.
        
        .. warning:: Use the subclasses to create instances of this.
        """
        super().__init__(200)


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
    
    def __init__(self):
        """Create a new machine type for the Brother CK-35."""
        super().__init__(200)


class KH270(Machine):
    
    """The machine type for the Brother KH-270."""
    
    def __init__(self):
        """Create a new machine type for the Brother KH-270."""
        super().__init__(114)


__all__ = ["Machine", "KH9XXSeries", "CK35", "KH900", "KH910", "KH930",
           "KH950", "KH965"]
