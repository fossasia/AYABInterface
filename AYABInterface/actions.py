"""These are the actions that can be executed by the users."""
from .utils import camel_case_to_under_score


_doc_base = """Test whether this is a {}.

:rtype: bool
:return: :obj:`{}`
"""


def _new_test(name, container, result, clsname):
    """Create the "is_*" functions for the Actions."""
    def test(self):
        return result
    test.__name__ = name
    test.__qualname__ = container.__qualname__ + "." + name
    test.__doc__ = _doc_base.format(clsname, result)
    setattr(container, name, test)

Action = None


class ActionMetaClass(type):

    """Metaclass for the actions.

    This class makes sure each :class:`Action` has tests.

    If a class is named ``MyAction``, each :class:`Action` gets the method
    ``is_my_action()`` which returns :obj:`False` for all :class:`Actions
    <Action>` expcept for ``MyAction`` it returns :obj:`True`.
    """

    def __init__(cls, name, bases, attributes):
        """Create a new :class:`Action` subclass."""
        super().__init__(name, bases, attributes)
        test_name = "is_" + camel_case_to_under_score(name)
        if Action is not None:
            _new_test(test_name, Action, False, cls.__name__)
        _new_test(test_name, cls, True, cls.__name__)


class Action(object, metaclass=ActionMetaClass):

    """A base class for actions."""

    def __init__(self, *arguments):
        """Create a new :class:`Action`.

        :param tuple arguments: The arguments passed to the action. These are
          also used to determine :meth:`equality <__eq__>` and the :meth:`hash
          <__hash__>`.
        """
        self._arguments = arguments

    def __hash__(self):
        """The hash of the object.

        :rtype: int
        :return: the :func:`hash` of the object
        """
        return hash(self.__class__) ^ hash(self._arguments)

    def __eq__(self, other):
        """Whether this object is equal to the other.

        :rtype: bool
        """
        return other == (self.__class__, self._arguments)

    def __repr__(self):
        """Return this object as string.

        :rtype: str
        """
        return self.__class__.__name__ + repr(self._arguments)


class SwitchOnMachine(Action):

    """The user switches on the machine."""


class SwitchOffMachine(Action):

    """The user switches off the machine."""


class MoveNeedlesIntoPosition(Action):

    """The user moves needles into position."""


class PutColorInNutB(Action):

    """The user puts a color into nut B."""


class PutColorInNutA(Action):

    """The user puts a color into nut A."""


class MoveCarriageToTheRight(Action):

    """The user moves the carriage to the right."""


class MoveCarriageToTheLeft(Action):

    """The user moves the carriage to the left."""


class MoveCarriageOverLeftHallSensor(Action):

    """The user moves the carriage over the left hall sensor."""


class SwitchCarriageToModeNl(Action):

    """The user switches the mode of the carriage to NL."""


class SwitchCarriageToModeKc(Action):

    """The user switches the mode of the carriage to KC."""

__all__ = ["ActionMetaClass", "Action", "SwitchCarriageToModeKc",
           "SwitchCarriageToModeNl", "MoveCarriageOverLeftHallSensor",
           "MoveCarriageToTheLeft", "MoveCarriageToTheRight",
           "PutColorInNutA", "PutColorInNutB", "MoveNeedlesIntoPosition",
           "SwitchOffMachine", "SwitchOnMachine"]
