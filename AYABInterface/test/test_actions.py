"""test the different actions a user can perform."""
from AYABInterface.actions import SwitchOnMachine, \
    MoveCarriageOverLeftHallSensor, MoveCarriageToTheLeft, \
    MoveCarriageToTheRight, PutColorInNutA, PutColorInNutB, \
    MoveNeedlesIntoPosition, SwitchCarriageToModeNl, SwitchCarriageToModeKc, \
    SwitchOffMachine, Action
import pytest


class SimpleAction(Action):
    pass


class OtherAction(Action):
    pass


class TestCompareActions(object):

    @pytest.mark.parametrize("arguments", [(1, 2), ("asd", 12312)])
    @pytest.mark.parametrize("action_class", [SimpleAction, OtherAction])
    def test_equal(self, arguments, action_class):
        a = action_class(*arguments)
        b = action_class(*arguments)
        assert a == b
        assert hash(a) == hash(b)

    @pytest.mark.parametrize("a,b", [
        (SimpleAction(3, 5), SimpleAction(3, 6)),
        (SimpleAction(3), SimpleAction(3, 5)),
        (OtherAction(3, 5), SimpleAction(3, 5))])
    def test_unequal(self, a, b):
        assert a != b

    def test_tests(self):
        assert SimpleAction().is_simple_action()
        assert not OtherAction().is_simple_action()
        assert not SimpleAction().is_other_action()
        assert OtherAction().is_other_action()
