"""Test the interation module."""
from knittingpattern import load_from_relative_file
from AYABInterface.interaction import Interaction
from AYABInterface.actions import SwithOnMachine, \
    MoveCarriageOverLeftHallSensor, MoveCarriageToTheLeft, \
    MoveCarriageToTheRight, PutColorInNutA, PutColorInNutB, \
    MoveNeedlesIntoPosition, SwitchCarriageToModeNl, SwitchCarriageToModeKc, \
    SwitchOffMachine
from AYABInterface.carriages import KnitCarriage
from unittest import Mock
from AYABInterface.machines import KH910


class InteractionTest(object):

    """Test the interaction."""
    
    pattern = load_from_relative_file(__name__, "test_patterns/block4x4.json")
    actions = [
        MoveCarriageOverLeftHallSensor(),
        PutColorInNutA(None),
        MoveNeedlesIntoPosition("B", [198, 199, 200, 201]),
        SwitchCarriageToModeNl(),
        SwitchOffMachine(),  # no need to switch on the machine for one color
        MoveCarriageToTheRight(KnitCarriage()),
        MoveCarriageToTheLeft(KnitCarriage()),
        MoveCarriageToTheRight(KnitCarriage()),
        MoveCarriageToTheLeft(KnitCarriage())]
    machine = KH910
    

    @fixture
    def interaction(self):
        return Interaction(self.pattern, self.machine())
        
    
    def test_pattern_interactions(self, interaction):
        assert interaction.actions == self.actions
    







