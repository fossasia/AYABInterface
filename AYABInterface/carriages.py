"""This module contains all the supported carriages."""


class Carriage(object):

    """A base class for carriages."""

    def __eq__(self, other):
        """Equivalent to ``self == other``."""
        return other == (self.__class__,)

    def __hash__(self):
        """Make this object hashable."""
        return hash((self.__class__,))

    def __repr__(self):
        """This object as string."""
        return self.__class__.__name__


class KnitCarriage(Carriage):

    """The carriage used for knitting."""

__all__ = ["Carriage", "KnitCarriage"]
