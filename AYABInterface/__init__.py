"""AYABInterface - a module to control the AYAB shield.

.. seealso:: http://ayab-knitting.com/
"""
# there should be no imports

__version__ = "0.0.1"


def Interface(*args, **kw):
    """Create a new Interface object.
    
    :return: an :class:`AYABInterface.interface.Interface`
    
    .. seealso:: :class:`AYABInterface.interface.Interface`
    """
    from .interface import Interface
    return Interface(*args, **kw)


def NeedlePositions(*args, **kw):
    """Create a new NeedlePositions object.
    
    :return: an :class:`AYABInterface.interface.NeedlePositions`
    
    .. seealso:: :class:`AYABInterface.interface.NeedlePositions`
    """
    from .interface import NeedlePositions
    return NeedlePositions(*args, **kw)


__all__ = ["Interface", "NeedlePositions"]
