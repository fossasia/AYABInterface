"""Test the machines."""
import pytest
from AYABInterface.machines import Machine, KH910, KH270, get_machines
import AYABInterface


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


class MachineN(Machine):

    number_of_needles = None
    needle_positions = None


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


class TestName(object):

    """Test the name attribute."""

    @pytest.mark.parametrize("machine,name", [
        (MachineN, "MachineN"), (KH910, "KH-910"),
        (KH270, "KH-270")])
    def test_id(self, machine, name):
        assert machine().name == name


class TestGetMachines(object):

    """Test get_machines."""

    @pytest.mark.parametrize("get_machines", [
        get_machines, AYABInterface.get_machines])
    @pytest.mark.parametrize("machine", [KH910, KH270])
    def test_is_inside(self, machine, get_machines):
        assert machine() in get_machines()


class TestEquality(object):

    """Test equality and hashing."""

    @pytest.mark.parametrize("a,b", [
        (KH910(), KH270()), (MachineN(), KH910()),
        (XMachine(1, 3), XMachine(1, 2)), (XMachine(2, 2), XMachine(1, 2)),
        (XMachine(2, 2), XMachine(1, 3))])
    def test_unequality(self, a, b):
        assert a != b

    @pytest.mark.parametrize("a,b", [
        (KH910(), KH910()), (MachineN(), MachineN()),
        (XMachine(1, 2), XMachine(1, 2))])
    def test_equality(self, a, b):
        assert a == b
        assert hash(a) == hash(b)
