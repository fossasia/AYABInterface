"""These are the actions that can be executed."""
from .utils import camel_case_to_under_score


_doc_base = """Test whether this is a {}.

:rtype: bool
:return: :obj:`{}`
"""

def _new_test(name, container, result, clsname):
    def test(self):
        return result
    test.__name__ = name
    test.__qualname__ = container.__qualname__ + "." + name
    test.__doc__ = _doc_base.format(clsname, result)
    setattr(container, name, test)

Action = None

class ActionMetaClass(type):

    def __init__(cls, name, bases, attributes):
        super().__init__(name, bases, attributes)
        test_name = "is_" + camel_case_to_under_score(name)
        if Action is not None:
            _new_test(test_name, Action, False, cls.__name__)
        _new_test(test_name, cls, True, cls.__name__)

class Action(object, metaclass=ActionMetaClass):
    
    """A base class for actions."""
    
    def __init__(self, *arguments):
        self._arguments = arguments
    
    def __hash__(self):
        return hash(self.__class__) ^ hash(self._arguments)
    
    def __eq__(self, other):
        return other == (self.__class__, self._arguments)


class SwithOnMachine(Action):
    
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
