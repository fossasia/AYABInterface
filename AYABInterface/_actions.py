"""These are the actions that can be executed."""


class Action(object):

    """The base class for actions."""

    def is_movement(self):
        """Whether this is a move action.

        :rtype: bool
        """
        return isinstance(self, Movement)

    def is_color_change(self):
        """Whether this action requires colors to be changed.

        :rtype: bool
        """
        return isinstance(self, ColorChange)

    def has_carriage(self):
        """Whether this action is performed using a carriage."""
        return isinstance(self, ActionOnCarriage)


class ActionOnCarriage(Action):

    """This is an action that requires a carriage."""

    @property
    def carriage(self):
        """The carriage to move.

        :rtype: AYABInterface.carriages.Carriage
        """


class Movement(ActionOnCarriage):

    """The base class for movement actions with carriages."""

    def is_initialization(self):
        """Whether the carriage should be moved over the left turn mark.

        :rtype: bool
        """

    def is_move_left(self):
        """Whether the carriage should be moved to the left.

        :rtype: bool
        """

    def is_move_right(self):
        """Whether the carriage should be moved to the right.

        :rtype: bool
        """

    def should_pass_turn_mark(self):
        """Whether the carriage should be moved over the turn mark.

        This can be required from time to time to prevent knitting mistakes
        in counting.

        :rtype: bool
        """


class ColorChange(ActionOnCarriage):

    """The base action for changing colors."""

    # TODO: Nut A and Nut B is very specific to the carriage.
    # This should be in the carriage.

    def changes_color_in_nut_a(self):
        """Whether the color in nut A should be changed.

        :rtype: bool
        """

    @property
    def color_in_nut_a(self):
        """The new color in nut A.

        :rtype: int
        """

    def changes_color_in_nut_b(self):
        """Whether the color in nut B should be changed.

        :rtype: bool
        """

    @property
    def color_in_nut_b(self):
        """The new color in nut B.

        :rtype: int
        """

__all__ = ["Action", "ActionOnCarriage", "Movement", "ColorChange"]
