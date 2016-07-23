"""This module is used to communicate with the shield.

Requirement: Make objects from binary stuff.
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class Content(object, metaclass=ABCMeta):

    """The interface used by the Communication.

    This class is the interface that the :class:`Communication` requires.

    .. seealso:: :class:`AYABInterface.interface.NeedlePositions`

    .. _communication_rows:
    Rows
    ----

    When we talk about a row, we talk about a list

    - containing :attr:`needle positions
      <AYABInterface.machines.Machine.needle_positions>`
    - with a length of :attr:`the number of needles
      <AYABInterface.machines.Machine.number_of_needles>`.
    """

    @abstractproperty
    def machine(self):
        """The machine for the Communication.

        :rtype: AYABInterface.machines.Machine
        """

    @abstractmethod
    def row_completed(self, index):
        """Mark the row at index as completed.

        :param int index: the index in the rows

        Invalid indices are ignored, no Exception is raised.
        """

    @abstractmethod
    def get_row(self, index, default=None):
        """Return the row at an index.

        :param int index:
        :return:

          - If there is a :ref:`row <_communication_rows>` at this index,
            this returns the row.
          - If there is no row at this index, this returns :paramref:`default`.
        """


class Communication(object):

    """This class comunicates with the AYAB shield."""

    def __init__(self, file):
        """Create a new Communication object.

        :param file: a file-like object with read and write methods for the
          communication with the Arduino. This could be a
          :class:`serial.Serial` or a :meth:`socket.socket.makefile`.
        """
        self._file = file

    def start(self, content):
        """Start the communication about a content.

        :param Content content: the content of the communication.
        """

    def stop(self):
        """Stop the communication with the shield."""

__all__ = ["Communication"]
