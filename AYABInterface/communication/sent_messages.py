"""This module contains the messages that are sent to the controller."""
from abc import ABCMeta, abstractmethod


class Request(object):
    
    """This is the interface for sent messages."""
    
    @abstractmethod
    def send(self):
        """Send this message to the controller."""

class Request
