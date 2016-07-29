"""This module contains the carriages which are communicated by the firmware.
"""


class Carriage(object):

    """A base class for carriages."""

    def __init__(self, needle_position):
        """Create a new carriage.

        :param int needle_position: the position of the carriage
        """
        self._needle_position = needle_position

    @property
    def needle_position(self):
        """The needle position of the carriages.

        :return: the needle position of the carriage counted from the left,
          starting with ``0``
        :rtype: int
        """
        return self._needle_position

    def is_knit_carriage(self):
        """Whether this is a knit carriage.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_hole_carriage(self):
        """Whether this is a hole carriage.

        :rtype: bool
        :return: :obj:`False`
        """
        return False

    def is_unknown_carriage(self):
        """Whether the type of this carriage is unkown.

        :rtype: bool
        :return: :obj:`False`
        """
        return False


class NullCarriage(Carriage):

    """This is an empty carriage."""


class KnitCarriage(Carriage):

    """The carriage for knitting."""

    def is_knit_carriage(self):
        """This is a knit carriage.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class HoleCarriage(Carriage):

    """The carriage for creating holes."""

    def is_hole_carriage(self):
        """This is a knit carriage.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


class UnknownCarriage(Carriage):

    """The carriage type if the type is not known."""

    def is_unknown_carriage(self):
        """The type of this carriage is unknown.

        :rtype: bool
        :return: :obj:`True`
        """
        return True


def id_to_carriage_type(carriage_id):
    """Return the carriage type for an id.

    :rtype: type
    :return: a subclass of :class:`Carriage`
    """
    return _id_to_carriage.get(carriage_id, UnknownCarriage)

_id_to_carriage = {0: NullCarriage, 1: KnitCarriage, 2: HoleCarriage}

__all__ = ["NullCarriage", "KnitCarriage", "HoleCarriage", "UnknownCarriage",
           "id_to_carriage_type", "Carriage"]
