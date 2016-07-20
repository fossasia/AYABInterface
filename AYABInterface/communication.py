"""This module is used to communicate with the shield.

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
    
    def close(self):
        """Close the connection."""
    
__all__ = ["Communication"]