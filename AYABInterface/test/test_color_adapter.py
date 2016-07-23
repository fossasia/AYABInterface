"""Test the color adapter.

.. seealso:: :class`AYABInterface.interface.ColorAdapter`
"""
from AYABInterface.interface import ColorAdapter
from unittest.mock import MagicMock

@fixture
def machine():
    """The machine to knit on."""
    return Machine(5, (1, 2))


class TestNeedlePositionInitialization(object):

    """Test """

