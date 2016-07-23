"""This module contains the messages that are sent to the controller."""


class Request(object):
    
    """This is the interface for sent messages."""
    
    def __init__(self, file, communication, *args, **kw):
        """Create a new Request object"""
        self._file = file
        self._communication = communication
        assert self.FIRST_BYTE is not None
        self.init(*args, **kw)
    
    def init(self):
        """Override this method."""
    
    FIRST_BYTE = None  #: the first byte to identify this message
    
    def content_bytes(self):
        """The message content as bytes."""
        return b''
        
    def as_bytes(self):
        """The message represented as bytes."""
        return self.FIRST_BYTE + self.get_content_bytes()
        
    def send(self):
        """Send this message to the controller."""
        self._file.write(self.as_bytes())

        
class Information(Request):

    """An information request message."""
    
    FIRST_BYTE = None  #: the first byte to identify this message

    
class Test(Request):

    """Set the controller into test mode."""
    
    FIRST_BYTE = None  #: the first byte to identify this message


class LineConfiguration(Request):

    """Senf information about a specific line."""
    
    FIRST_BYTE = None  #: the first byte to identify this message

    def init(self, line_number):
        """Create a new LineConfiguration message."""
        