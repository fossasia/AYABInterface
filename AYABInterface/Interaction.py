"""This module can be used to interact with the AYAB Interface."""
from .actions import SwitchOnMachine, \
    MoveCarriageOverLeftHallSensor, MoveCarriageToTheLeft, \
    MoveCarriageToTheRight, PutColorInNutA, PutColorInNutB, \
    MoveNeedlesIntoPosition, SwitchCarriageToModeNl, SwitchCarriageToModeKc, \
    SwitchOffMachine
from AYABInterface.carriages import KnitCarriage
    

class Interaction(object):

    """Interaction with the knitting pattern."""
    
    def __init__(self, knitting_pattern, machine):
        self._machine = machine
        self._actions = []
        
        # determine the number of colors
        colors = list()
        for instruction in knitting_pattern.rows.at(0).instructions:
            color = instruction.color
            if color not in colors:
                colors.append(color)
        assert len(colors) <= 2
        
        # rows and colors
        movements = (
            MoveCarriageToTheRight(KnitCarriage()),
            MoveCarriageToTheLeft(KnitCarriage()))
        rows = knitting_pattern.rows_in_knit_order()
        number_of_needles = rows[0].number_of_consumed_meshes
        start = int(self._machine.number_of_needles / 2 -
                    number_of_needles / 2)
        first_needles = list(range(start, start + number_of_needles))
        
        # handle switches
        if len(colors) == 1:
            self._actions.extend([
                SwitchOffMachine(),
                SwitchCarriageToModeNl()])
        else:
            self._actions.extend([
                SwitchCarriageToModeKc(),
                SwitchOnMachine()])
        
        # move needles
        self._actions.append(MoveNeedlesIntoPosition("B", first_needles))
        self._actions.append(MoveCarriageOverLeftHallSensor())
        
        # use colors
        if len(colors) == 1:
            self._actions.append(PutColorInNutA(colors[0]))
        if len(colors) == 2:
            self._actions.append(PutColorInNutA(colors[1]))
            self._actions.append(PutColorInNutB(colors[0]))
        
        # knit
        for index, row in enumerate(rows):
            self._actions.append(movements[index & 1])

    @property
    def actions(self):
        """A list of actions to perform.
        
        :return: a list of :class:`AYABInterface.actions.Action`
        """
        return self._actions


