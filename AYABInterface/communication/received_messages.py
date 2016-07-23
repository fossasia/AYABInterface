"""This modue contains all the messages taht are received."""
from abc import ABCMeta, abstractproperty


class Message(object):

    """This is the base class for messages that are received."""
    
    def __init__(self, file, communication):
        """Create a new Message."""
        self._file = file
        self.communication = communication
        self._init()
    
    def _init(self):
        """Initialize the message.
        
        Override this method to configure your message.
        This pattern is called template method.
        """
        
    def is_valid(self):
        """Whether the message is valid.
        
        :rtype: bool
        :return: :obj:`True`
        """
        return True

    def is_configutation_start(self):
        """Whether this is a ConfigurationStart message.
        
        :rtype: bool
        :returns: :obj:`False`
        """
        return False
    
    def is_configuration_information(self):
        """Whether this is a ConfigurationInformation message.
        
        :rtype: bool
        :returns: :obj:`False`
        """
        return False    
        
    def is_configuration_test(self):
        """Whether this is a ConfigurationTest message.
        
        :rtype: bool
        :returns: :obj:`False`
        """
        return False
        
    def is_line_request(self):
        """Whether this is a LineRequest message.
        
        :rtype: bool
        :returns: :obj:`False`
        """
        return False
        
    def is_state_indication(self):
        """Whether this is a StateIndication message.
        
        :rtype: bool
        :returns: :obj:`False`
        """
        return False     
        
    def is_unknown(self):
        """Whether this is a StateIndication message.
        
        :rtype: bool
        :returns: :obj:`False`
        """
        return False

    def wants_to_answer(self):
        """Whether this message produces and answer message.
        
        :rtype: bool
        :returns: :obj:`False`
        """
        return False


class UnknownMessage(Message):
    
    """This is a special message for unknown message types."""
    
    def is_unknown(self):
        """Whether this is a StateIndication message.
        
        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def is_valid(self):
        """Whether the message is valid.
        
        :rtype: bool
        :return: :obj:`False`
        """
        return False


class MessageWithAnswer(Message, metaclass=ABCMeta):

    def wants_to_answer(self):
        """Whether this message produces and answer message.
        
        :rtype: bool
        :returns: :obj:`True`
        """
        return True
    
    @abstractproperty
    def answer(self):
        """The message to answer.
        
        :rtype: AYABInterface.conmmunication.sent_messages.SentMessage
        """


class ConfigurationSuccess(Message):
    
    def _init(self):
        """Read the success byte."""
        self._success = self._file.read(1)
    
    def is_success(self):
        """Whether the configuration was successful.

        :rtype: bool
        """
        return self._success


class ConfigurationStart(ConfigurationSuccess):

    """This message is sent at/when""" # TODO

    MESSAGE_ID = 0xc1  #: The first byte that indicates this message

    def is_configutation_start(self):
        """Whether this is a ConfigurationStart message.
        
        :rtype: bool
        :returns: :obj:`True`
        """
        return True


class ConfigurationInformation(Message):

    """This message is sent at/when""" # TODO

    MESSAGE_ID = 0xc3  #: The first byte that indicates this message
    
    def is_configuration_information(self):
        """Whether this is a ConfigurationInformation message.
        
        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def _init(self):
        """Read the success byte."""
        self._api_version = self._file.read(1)
    
    @property
    def api_version(self):
        """The API version of the controller.
        
        :rtype: int
        """
        return self._api_version

    def is_correct_api_version(self):
        """Whether this is the same API version as of the communication.
        
        :rtype: bool
        """
        return self.api_version == self.communication.api_version


class ConfigurationTest(ConfigurationSuccess):

    """This message is sent at/when""" # TODO
    
    MESSAGE_ID = 0xc4  #: The first byte that indicates this message
    
    def is_configuration_test(self):
        """Whether this is a ConfigurationTest message.
        
        :rtype: bool
        :returns: :obj:`True`
        """
        return True


class LineRequest(MessageWithAnswer):

    """This message is sent at/when""" # TODO
    
    MESSAGE_ID = 0x82  #: The first byte that indicates this message
    
    def is_line_request(self):
        """Whether this is a LineRequest message.
        
        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def _init(self):
        """Read the line number."""
        self._line_number = self._file.read(1)
        # TODO: compute real line number with overflow
    
    @property
    def line_number(self):
        """The line number that was requested."""
        return self._line_number
    
    @property
    def answer(self):
        """Message to inform about the upcoming line."""


class StateIndication(Message):

    """This message is sent at/when""" # TODO

    MESSAGE_ID = 0x84  #: The first byte that indicates this message
    
    def is_configuration_information(self):
        """Whether this is a ConfigurationInformation message.
        
        :rtype: bool
        :returns: :obj:`True`
        """
        return True

    def _init(self):
        """Read the success byte."""
        self._hall_left = self._file.read(2)
        self._hall_right = self._file.read(2)
        self._carriage_type = self._file.read(1)
        self._carriage_position = self._file.read(1)


_message_types = {}     
for message_type in list(globals().values()):
    message_id = getattr(message_type, "MESSAGE_ID", None)
    if message_id is not None:
        _message_types[message_id] = message_type
del message_type, message_id


def read_message_type(file):
    """Read the message type from a file."""
    message_number = file.read(1)[0]
    return _message_types.get(message_number, UnknownMessage)

__all__ = ["read_message_type", "StateIndication", "LineRequest",
           "ConfigurationTest", "ConfigurationInformation",
           "ConfigurationStart", "ConfigurationSuccess", "MessageWithAnswer",
           "UnknownMessage", "Message"]
