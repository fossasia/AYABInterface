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
from pytest import fixture, raises
import AYABInterface.interaction as interaction


class InteractionTest(object):

    """Test the interaction."""

    pattern = None              #: the pattern to test with
    actions = None              #: the actions to perdorm
    machine = None              #: the machine type to use
    needle_positions = None     #: the needle positions for the pattern

    @fixture
    def interaction(self):
        return Interaction(self.patterns.patterns.at(0), self.machine())

    def test_pattern_interactions(self, interaction):
        assert interaction.actions == self.actions

    def test_needle_positions(self, interaction):
        assert interaction._get_needle_positions(-1) is None
        max_i = len(self.needle_positions)
        assert interaction._get_needle_positions(max_i) is None
        positions = ["".join(interaction._get_needle_positions(i))
                     for i in range(max_i)]
        expected_positions = self.needle_positions
        assert positions == expected_positions

    def test_left_end_needle(self, interaction):
        assert interaction.left_end_needle == self.left_end_needle

    def test_right_end_needle(self, interaction):
        assert interaction.right_end_needle == self.right_end_needle


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
    needle_positions = ["B" * 200] * 4
    left_end_needle = 98
    right_end_needle = 101


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
    needle_positions = ["B" * (98 + i) + "D" + "B" * (101 - i)
                        for i in range(4)]
    left_end_needle = 98
    right_end_needle = 101


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
    needle_positions = ["B" * 97 + "DDBBDD" + "B" * 97,
                        "B" * 97 + "BBBBBB" + "B" * 97,
                        "B" * 97 + "DDBBDD" + "B" * 97]
    left_end_needle = 97
    right_end_needle = 102


class TestCreateCommunication(object):

    @fixture
    def Communication(self, monkeypatch):
        Communication = Mock()
        monkeypatch.setattr(interaction, "Communication", Communication)
        return Communication

    @fixture
    def machine(self):
        return KH910()

    @fixture
    def pattern(self):
        return Mock()

    @fixture
    def file(self):
        return Mock()

    @fixture
    def interaction(self, pattern, machine):
        return Interaction(pattern, machine)

    @fixture
    def communication(self, interaction, Communication, file, monkeypatch):
        monkeypatch.setattr(interaction.__class__, "right_end_needle", Mock())
        monkeypatch.setattr(interaction.__class__, "left_end_needle", Mock())
        return interaction.communicate_through(file)

    def test_communication_creation(self, interaction, communication, machine,
                                    Communication, file):
        assert communication == Communication.return_value
        Communication.assert_called_once_with(
            file, interaction._get_needle_positions, machine,
            [interaction._on_message_received],
            right_end_needle=interaction.right_end_needle,
            left_end_needle=interaction.left_end_needle)

    def test_interaction_communication_attribute(self, interaction,
                                                 communication):
        assert interaction.communication == communication

    def test_can_not_communicate_while_communicating(self, interaction,
                                                     communication):
        with raises(ValueError) as error:
            interaction.communicate_through(Mock())
        message = "Already communicating."
        assert error.value.args[0] == message

    def test_initial_comunication_is_None(self, interaction):
        assert interaction.communication is None
