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
