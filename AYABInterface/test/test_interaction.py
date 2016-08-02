"""Test the interation module."""
from knittingpattern import load_from_relative_file
from AYABInterface.interaction import Interaction
from AYABInterface.actions import SwitchOnMachine, \
    MoveCarriageOverLeftHallSensor, MoveCarriageToTheLeft, \
    MoveCarriageToTheRight, PutColorInNutA, PutColorInNutB, \
    MoveNeedlesIntoPosition, SwitchCarriageToModeNl, SwitchCarriageToModeKc, \
    SwitchOffMachine
from AYABInterface.carriages import KnitCarriage
from unittest.mock import Mock
from AYABInterface.machines import KH910
from pytest import fixture


class InteractionTest(object):

    """Test the interaction."""
    
    pattern = None  #: the pattern to test with
    actions = None  #: the actions to perdorm
    machine = None  #: the machine type to use
    

    @fixture
    def interaction(self):
        return Interaction(self.patterns.patterns.at(0), self.machine())
        
    
    def test_pattern_interactions(self, interaction):
        assert interaction.actions == self.actions
    

class TestOneColorBlockPattern(InteractionTest):

    """Test the interaction."""
    
    patterns = load_from_relative_file(__name__, "test_patterns/block4x4.json")
    actions = [
        SwitchOffMachine(),  # no need to switch on the machine for one color
        SwitchCarriageToModeNl(),
        MoveNeedlesIntoPosition("B", [98, 99, 100, 101]),
        MoveCarriageOverLeftHallSensor(),
        PutColorInNutA(None),
        MoveCarriageToTheRight(KnitCarriage()),
        MoveCarriageToTheLeft(KnitCarriage()),
        MoveCarriageToTheRight(KnitCarriage()),
        MoveCarriageToTheLeft(KnitCarriage())]
    machine = KH910
    

class TestColoredBlockPattern(InteractionTest):
    
    patterns = load_from_relative_file(
        __name__, "test_patterns/block4x4-colored.json")
    actions = [
        SwitchCarriageToModeKc(),
        SwitchOnMachine(),
        MoveNeedlesIntoPosition("B", [98, 99, 100, 101]),
        MoveCarriageOverLeftHallSensor(),
        PutColorInNutA(None),
        PutColorInNutB("green"),
        MoveCarriageToTheRight(KnitCarriage()),
        MoveCarriageToTheLeft(KnitCarriage()),
        MoveCarriageToTheRight(KnitCarriage()),
        MoveCarriageToTheLeft(KnitCarriage())]
    machine = KH910

    
class Test6x3Pattern(InteractionTest):
    
    patterns = load_from_relative_file(
        __name__, "test_patterns/block6x3.json")
    actions = [
        SwitchCarriageToModeKc(),
        SwitchOnMachine(),
        MoveNeedlesIntoPosition("B", [97, 98, 99, 100, 101, 102]),
        MoveCarriageOverLeftHallSensor(),
        PutColorInNutA("blue"),
        PutColorInNutB("orange"),
        MoveCarriageToTheRight(KnitCarriage()),
        MoveCarriageToTheLeft(KnitCarriage()),
        MoveCarriageToTheRight(KnitCarriage())]
    machine = KH910




