"""AYABInterface - a module to control the AYAB shield.

.. seealso:: http://ayab-knitting.com/
"""
# there should be no imports

__version__ = "0.0.9"


def NeedlePositions(*args, **kw):
    """Create a new NeedlePositions object.

    :return: an :class:`AYABInterface.needle_positions.NeedlePositions`

    .. seealso:: :class:`AYABInterface.needle_positions.NeedlePositions`
    """
    from .needle_positions import NeedlePositions
    return NeedlePositions(*args, **kw)


def get_machines():
    """Return a list of all machines that can be used.

    :rtype: list
    :return: a list of :class:`Machines <Machines>`
    """
    from .machines import get_machines
    return get_machines()


def get_connections():
    """Return a list of all available serial connections.

    :rtype: list
    :return: a list of :class:`AYABInterface.SerialPort`. All of the
      returned objects have a ``connect()`` method and a ``name`` attribute.
    """
    from .serial import list_serial_ports
    return list_serial_ports()

__all__ = ["NeedlePositions", "get_machines", "get_connections"]
