"""Test the machines."""
import pytest
from AYABInterface.machines import Machine, KH910

class XMachine(Machine):

    def __init__(self, left_end_needle, number_of_needles):
        self._number_of_needles = number_of_needles
        self._left_end_needle = left_end_needle
    
    @property
    def number_of_needles(self):
        return self._number_of_needles
    
    @property
    def needle_positions(self):
        return ("A", "C")
    
    @property
    def left_end_needle(self):
        return self._left_end_needle
     
    
class TestNeedleEnds(object):

    @pytest.mark.parametrize("number_of_needles", [1, -22, 222])
    @pytest.mark.parametrize("left_end_needle", [0, 6, -3])
    def test_right_end_needle(self, left_end_needle, number_of_needles):
        machine = XMachine(left_end_needle, number_of_needles)
        right_end_needle = left_end_needle + number_of_needles - 1
        assert machine.right_end_needle == right_end_needle
    
    def test_left_end_needle(self):
        assert KH910().left_end_needle == 0
        

