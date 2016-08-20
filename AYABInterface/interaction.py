"""This module can be used to interact with the AYAB Interface."""
from .actions import SwitchOnMachine, \
    MoveCarriageOverLeftHallSensor, MoveCarriageToTheLeft, \
    MoveCarriageToTheRight, PutColorInNutA, PutColorInNutB, \
    MoveNeedlesIntoPosition, SwitchCarriageToModeNl, SwitchCarriageToModeKc, \
    SwitchOffMachine
from AYABInterface.carriages import KnitCarriage
from AYABInterface.communication import Communication
from itertools import chain


cached_property = property


class Interaction(object):

    """Interaction with the knitting pattern."""

    def __init__(self, knitting_pattern, machine):
        """Create a new interaction object.

        :param knitting_pattern: a
          :class:`~knittingpattern.KnittingPattern.KnittingPattern`
        :param AYABInterface.machines.Machine machine: the machine to knit on
        """
        self._machine = machine
        self._communication = None
        self._rows = knitting_pattern.rows_in_knit_order()
        self._knitting_pattern = knitting_pattern

    @cached_property
    def left_end_needle(self):
        return min(chain(*map(self._get_row_needles, range(len(self._rows)))))

    @cached_property
    def right_end_needle(self):
        return max(chain(*map(self._get_row_needles, range(len(self._rows)))))

    @property
    def communication(self):
        """The communication with the controller.

        :rtype:AYABInterface.communication.Communication
        """
        return self._communication

    def communicate_through(self, file):
        """Setup communication through a file.

        :rtype: AYABInterface.communication.Communication
        """
        if self._communication is not None:
            raise ValueError("Already communicating.")
        self._communication = communication = Communication(
            file, self._get_needle_positions,
            self._machine, [self._on_message_received],
            right_end_needle=self.right_end_needle,
            left_end_needle=self.left_end_needle)
        return communication

    @cached_property
    def colors(self):
        return list(reversed(self._knitting_pattern.instruction_colors))

    def _get_row_needles(self, row_index):
        number_of_needles = self._rows[row_index].number_of_consumed_meshes
        start = int(self._machine.number_of_needles / 2 -
                    number_of_needles / 2)
        return list(range(start, start + number_of_needles))

    def _get_needle_positions(self, row_index):
        if row_index not in range(len(self._rows)):
            return None
        needle_positions = self._machine.needle_positions
        needles = self._get_row_needles(row_index)
        result = [needle_positions[0]] * self._machine.number_of_needles
        colors = self.colors
        row = self._rows[row_index]
        consumed_meshes = row.consumed_meshes
        for i, needle in enumerate(needles):
            color = consumed_meshes[i].consuming_instruction.color
            color_index = colors.index(color)
            needle_position = needle_positions[color_index]
            result[needle] = needle_position
            print("row {} at {}\t{}\t{}".format(
                row.id, row_index, needle, needle_position))
        return result

    def _on_message_received(self, message):
        """Call when a potential state change has occurred."""

    @cached_property
    def actions(self):
        """A list of actions to perform.

        :return: a list of :class:`AYABInterface.actions.Action`
        """
        actions = []
        do = actions.append

        # determine the number of colors
        colors = self.colors

        # rows and colors
        movements = (
            MoveCarriageToTheRight(KnitCarriage()),
            MoveCarriageToTheLeft(KnitCarriage()))
        rows = self._rows
        first_needles = self._get_row_needles(0)

        # handle switches
        if len(colors) == 1:
            actions.extend([
                SwitchOffMachine(),
                SwitchCarriageToModeNl()])
        else:
            actions.extend([
                SwitchCarriageToModeKc(),
                SwitchOnMachine()])

        # move needles
        do(MoveNeedlesIntoPosition("B", first_needles))
        do(MoveCarriageOverLeftHallSensor())

        # use colors
        if len(colors) == 1:
            do(PutColorInNutA(colors[0]))
        if len(colors) == 2:
            do(PutColorInNutA(colors[0]))
            do(PutColorInNutB(colors[1]))

        # knit
        for index, row in enumerate(rows):
            do(movements[index & 1])
        return actions
