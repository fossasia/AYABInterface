"""This module contains all the supported carriages."""

class Carriage(object):

    """The base class for the carriages."""

    def is_color(self):
        """Whether this carriage is for colored yarn.
        
        :rtype: bool
        """
        return False
    
    def is_kg881(self):
        """Whether this is a KG881.
        
        :rtype: bool
        """
        return False

    def is_kg882(self):
        """Whether this is a KG882.
        
        :rtype: bool
        """
        return False

    def is_kg88(self):
        """Whether this is a KG88X.
        
        :rtype: bool
        """
        return self.is_kg882() or self.is_kg881()

    def is_on_the_left(self):
        """Whether this carriage is currently on the left side.
        
        :rtype: bool
        """
    
    def is_on_the_right(self):
        """Whether this carriage is currently on the right side.
        
        :rtype: bool
        """
        
    def transits(self):
        """Whether this carriage is currently in transition.
        
        :rtype: bool
        """
        return self.transits_from_left_to_right() or \
            self.transits_from_right_to_left()
    
    def transits_from_left_to_right(self):
        """Whether this carriage is currently in transition to the right.
        
        :rtype: bool
        """
    
    def transits_from_right_to_left(self):
        """Whether this carriage is currently in transition to the left.
        
        :rtype: bool
        """

    @property
    def transition_progess(self):
        """Where the carriage is.
        
        :rtype: float
        :return: a float between or equal to 0 and 1. 0 means at the start and
          1 means completed.
        
        This can be estimated.
        """
        return (0.5 if self.transits() else 1)

__all__ = ["Carriage"]
