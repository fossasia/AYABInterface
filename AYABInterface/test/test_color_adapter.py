"""Test the color adapter.

.. seealso:: :class`AYABInterface.interface.ColorAdapter`
"""
from AYABInterface.interface import ColorAdapter
from unittest.mock import MagicMock
from collections import namedtuple
from pytest import fixture
Machine = namedtuple("Machine", ("number_of_needles", "needle_positions"))

@fixture
def machine():
    """The machine to knit on."""
    return Machine(5, (1, 2))


class TestNeedlePositionInitialization(object):

    """Test """

