"""Test the machines."""
import pytest
from AYABInterface.machines import Machine, KH910, KH270


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


class TestNeedlePositions(object):

    @pytest.mark.parametrize("machine_class", [KH910, KH270])
    @pytest.mark.parametrize("input,result", [
        ("BBDDBBBDBDDBDDDD" * 13, b'\x8c\xf6' * 13),
        ("B" * 200, b'\x00' * 25)])
    def test_byte_conversion(self, machine_class, input, result):
        machine = machine_class()
        assert machine.needle_positions == ("B", "D")
        input = input[:machine.number_of_needles]
        output = machine.needle_positions_to_bytes(input)
        expected_output = result[:machine.number_of_needles // 8] + \
            b'\x00' * (25 - machine.number_of_needles // 8)
        assert output == expected_output
