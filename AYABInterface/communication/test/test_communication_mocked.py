"""Test the Communication class.

.. seealso:: :class:`AYABInterface.communication.Communication`
"""
from AYABInterface.communication import Communication
from pytest import fixture, raises
import pytest
from unittest.mock import MagicMock
from io import BytesIO


@fixture
def messages():
    return []


@fixture
def on_message_received(messages):
    """The observer that is notified if a message was received."""
    return messages.append


@fixture
def file():
    """The file object to read from."""
    return BytesIO()


@fixture
def send_message(file):
    """Write message bytes to the file."""
    def send_message_(bytes_):
        position = file.tell()
        file.write(bytes_)
        file.seek(position)
    return send_message_


@fixture
def create_message():
    return MagicMock()


@fixture
def communication(file, on_message_received, monkeypatch, create_message):
    monkeypatch.setattr(Communication, '_read_message_type', create_message)
    return Communication(file, MagicMock(), 
                         on_message_received=[on_message_received])


def test_before_start_no_message_was_received(communication, create_message):
    assert create_message.assert_not_called()


@fixture
def started_communication(communication):
    communication.start()
    return communication


def test_after_start_no_message_was_received(
        started_communication, create_message):
    assert create_message.assert_not_called()


def test_receiving_message_before_start_is_forbidden(communication):
    with raises(AssertionError):
        communication.receive_message()


def test_receiving_message_after_stop_is_forbidden(started_communication):
    started_communication.stop()
    with raises(AssertionError):
        started_communication.receive_message()

    
@fixture
def message(create_message):    
    message_type = create_message.return_value
    return message_type.return_value


def test_can_receive_message(
        started_communication, create_message, file, messages):
    started_communication.receive_message()
    message_type = create_message.return_value
    create_message.assert_called_once_with(file)
    message_type.assert_called_once_with(file, started_communication)
    assert messages == [message_type.return_value]


def test_message_answers(started_communication, message):
    started_communication.receive_message()
    assert message.wants_to_answer.return_value
    message.send_answer.assert_called_once_with()


def test_message_does_not_answer(
        started_communication, create_message, message):
    message.wants_to_answer.return_value = False
    started_communication.receive_message()
    assert message.send_answer.assert_not_called()


def test_stop_notifies_with_close_message(started_communication, messages):
    started_communication.stop()
    assert messages[0].is_connection_closed()
    