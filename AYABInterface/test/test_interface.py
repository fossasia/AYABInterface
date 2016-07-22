import pytest
from pytest import fixture
from AYABInterface import Interface
from unittest.mock import MagicMock


@fixture
def rows():
    return [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 0, 1, 0],
            [0, 2, 1, 2, 0]]


@fixture
def configuration(rows):
    configuration = MagicMock()
    configuration.rows = rows
    configuration.number_of_needles = len(rows[0])
    configuration.index_of_first_row = 1
    return configuration


@fixture
def communication():
    return MagicMock()


@fixture
def interface(configuration, communication):
    return Interface(configuration, communication)


def test_get_communication(interface, communication):
    assert interface.communication == communication


def test_get_initial_confguration(interface, configuration):
    assert interface.initial_configuration == configuration


def test_machine(interface, configuration):
    assert interface.machine == configuration.machine


def test_current_row_is_not_knit(interface, configuration):
    row = interface.current_row
    assert len(row) == configuration.number_of_needles
    assert row == [-1] * configuration.number_of_needles


def test_configured_rows(interface, communication, rows):
    """Rows with two colors can be knit easily."""
    communication.initialize.assert_called_once(rows, interface.observer)


def test_index_in_rows(interface):
    assert interface.index_of_current_row == 1


def test_knit_one_row(interface):
    interface.observer.row_completed(1)
    assert interface.