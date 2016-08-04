"""This module contains the information about the different types of machines.

Every machine specific knowledge should be put in this file. Machine specific
knowledge is, for example:

- the number of needles a machine supports
- whether it is single or double bed
- how many colors are supported
- the name of the machine

"""
from abc import ABCMeta, abstractproperty


class Machine(object, metaclass=ABCMeta):

    """The type of the machine.

    This is an abstract base class and some methods need to be overwritten.
    """

    NAME = None  #: the name of the machine

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

    @property
    def left_end_needle(self):
        """The index of the leftmost needle.

        :rtype: int
        :return: ``0``
        """
        return 0

    @property
    def right_end_needle(self):
        """The index of the rightmost needle.

        :rtype: int
        :return: :attr:`left_end_needle` + :attr:`number_of_needles` - ``1``
        """
        return self.left_end_needle + self.number_of_needles - 1

    def needle_positions_to_bytes(self, needle_positions):
        """Convert the needle positions to the wire format.

        This conversion is used for :ref:`cnfline`.

        :param needle_positions: an iterable over :attr:`needle_positions` of
          length :attr:`number_of_needles`
        :rtype: bytes
        """
        bit = self.needle_positions
        assert len(bit) == 2
        max_length = len(needle_positions)
        assert max_length == self.number_of_needles
        result = []
        for byte_index in range(0, max_length, 8):
            byte = 0
            for bit_index in range(8):
                index = byte_index + bit_index
                if index >= max_length:
                    break
                needle_position = needle_positions[index]
                if bit.index(needle_position) == 1:
                    byte |= 1 << bit_index
            result.append(byte)
            if byte_index >= max_length:
                break
        result.extend(b"\x00" * (25 - len(result)))
        return bytes(result)

    @property
    def name(self):
        """The identifier of the machine."""
        name = self.__class__.__name__
        for i, character in enumerate(name):
            if character.isdigit():
                return name[:i] + "-" + name[i:]
        return name

    @property
    def _id(self):
        """What this object is equal to."""
        return (self.__class__, self.number_of_needles, self.needle_positions,
                self.left_end_needle)

    def __eq__(self, other):
        """Equavalent of ``self == other``.

        :rtype: bool
        :return: whether this object is equal to the other object
        """
        return other == self._id

    def __hash__(self):
        """Return the hash of this object.

        .. seealso:: :func:`hash`
        """
        return hash(self._id)

    def __repr__(self):
        """Return this object as a string."""
        return "<Machine {}>".format(self.name)


class KH9XXSeries(Machine):

    """The base class for the KH9XX series."""

    @property
    def number_of_needles(self):
        """The number of needles on this machine.

        :rtype: int
        :return: ``200``. The KH9XX series has 200 needles.
        """
        return 200

    @property
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

    @property
    def number_of_needles(self):
        """The number of needles on this machine.

        :rtype: int
        :return: ``200``. The KH9XX series has 200 needles.
        """
        return 200

    @property
    def needle_positions(self):
        """The different needle positions.

        :rtype: tuple
        :return: the needle positions are "B" and "D"
        """
        return ("B", "D")


class KH270(Machine):

    """The machine type for the Brother KH-270."""

    @property
    def number_of_needles(self):
        """The number of needles on this machine.

        :rtype: int
        :return: ``200``. The KH9XX series has 200 needles.
        """
        return 114

    @property
    def needle_positions(self):
        """The different needle positions.

        :rtype: tuple
        :return: the needle positions are "B" and "D"
        """
        return ("B", "D")


def get_machines():
    """Return a list of all machines.

    :rtype: list
    :return: a list of :class:`Machines <Machines>`
    """
    return [CK35(), KH900(), KH910(), KH930(), KH950(), KH965(), KH270()]

__all__ = ["Machine", "KH9XXSeries", "CK35", "KH900", "KH910", "KH930",
           "KH950", "KH965", "KH270", "get_machines"]
