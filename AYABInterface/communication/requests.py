"""This module contains the messages that are sent to the controller."""
from abc import ABCMeta, abstractmethod


class Request(object):
    
    """This is the interface for sent messages."""
    
    @abstractmethod
    def send(self):
        """Send this message to the controller."""


class Information(Request):

    """An information request message."""


class Test(Request):

    """Set the controller into test mode."""


class LineConfiguration(Request):

    """Set the controller into test mode."""

    def __init__(self, communication, line_number):
        """Create a new LineConfiguration message."""
        